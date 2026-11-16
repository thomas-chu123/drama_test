#!/usr/bin/env python3
"""short-drama-produce adapter for a local ComfyUI Z-Image-Turbo workflow.

Reads one confirmed image job from stdin, submits to ComfyUI's local HTTP API,
polls its history, downloads PNG outputs into output_root, and emits the
short-drama-produce adapter response on stdout.
"""
from __future__ import annotations

import json
import math
import os
import re
import shutil
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any

PROVIDER = "comfyui-local"
MAX_STDIN_BYTES = 256 * 1024
MAX_RESPONSE_BYTES = 32 * 1024 * 1024
MAX_BATCH = 16
WORKFLOW_FILE = Path(__file__).with_name("gen_image_api.json")


class AdapterFailure(Exception):
    def __init__(
        self,
        message: str,
        *,
        category: str = "configuration",
        code: str = "invalid_configuration",
        retryable: bool = False,
        submitted: bool = False,
        request_id: str | None = None,
        http_status: int | None = None,
    ) -> None:
        super().__init__(message)
        self.category = category
        self.code = code
        self.retryable = retryable
        self.submitted = submitted
        self.request_id = request_id
        self.http_status = http_status


def emit_error(exc: AdapterFailure) -> None:
    error: dict[str, Any] = {
        "provider": PROVIDER,
        "category": exc.category,
        "code": exc.code,
        "retryable": exc.retryable,
        "submitted": exc.submitted,
        "detail": str(exc)[:160],
    }
    if exc.request_id:
        error["request_id"] = exc.request_id
    if exc.http_status is not None:
        error["http_status"] = exc.http_status
    sys.stdout.write(json.dumps({"error": error}, ensure_ascii=False) + "\n")


def read_job() -> dict[str, Any]:
    raw = sys.stdin.buffer.read(MAX_STDIN_BYTES + 1)
    if len(raw) > MAX_STDIN_BYTES:
        raise AdapterFailure("job input exceeds the size limit", category="contract", code="job_too_large")
    try:
        job = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AdapterFailure("job input is not valid UTF-8 JSON", category="contract", code="invalid_job_json") from exc
    if not isinstance(job, dict):
        raise AdapterFailure("job must be a JSON object", category="contract", code="invalid_job")
    return job


def clean_parameters(job: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    if job.get("modality") != "image":
        raise AdapterFailure("ComfyUI image adapter requires modality=image", category="contract", code="wrong_modality")
    prompt = job.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise AdapterFailure("image prompt is empty", category="contract", code="empty_prompt")
    outputs = job.get("outputs")
    if not isinstance(outputs, list) or not 1 <= len(outputs) <= MAX_BATCH or not all(isinstance(x, str) for x in outputs):
        raise AdapterFailure("outputs must contain 1 to 16 image paths", category="contract", code="invalid_outputs")
    if any(Path(x).suffix.lower() != ".png" for x in outputs):
        raise AdapterFailure("ComfyUI gen_image workflow currently writes PNG only", category="invalid_request", code="png_only")
    references = job.get("references", [])
    bindings = job.get("reference_bindings", [])
    if references or bindings:
        raise AdapterFailure("gen_image workflow supports text-to-image only; references are not configured", category="invalid_request", code="references_unsupported")
    params = job.get("parameters", {})
    if not isinstance(params, dict):
        raise AdapterFailure("parameters must be an object", category="contract", code="invalid_parameters")
    allowed = {"prompt_language", "width", "height", "size", "seed", "steps"}
    unsupported = sorted(set(params) - allowed)
    if unsupported:
        raise AdapterFailure("unsupported image parameters: " + ", ".join(unsupported[:5]), category="invalid_request", code="unsupported_parameters")
    size = params.get("size")
    width = params.get("width", 1024)
    height = params.get("height", 1024)
    if size is not None:
        if not isinstance(size, str) or re.fullmatch(r"\d{2,5}x\d{2,5}", size) is None:
            raise AdapterFailure("size must use WIDTHxHEIGHT, for example 1024x1024", category="invalid_request", code="invalid_size")
        width, height = (int(v) for v in size.lower().split("x"))
    for name, value in (("width", width), ("height", height)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 64 or value > 4096 or value % 8:
            raise AdapterFailure(f"{name} must be a multiple of 8 from 64 to 4096", category="invalid_request", code="invalid_size")
    seed = params.get("seed", 967096310351888)
    steps = params.get("steps", 8)
    if not isinstance(seed, int) or isinstance(seed, bool) or not 0 <= seed <= 0xFFFFFFFFFFFFFFFF:
        raise AdapterFailure("seed must be an unsigned 64-bit integer", category="invalid_request", code="invalid_seed")
    if not isinstance(steps, int) or isinstance(steps, bool) or not 1 <= steps <= 100:
        raise AdapterFailure("steps must be an integer from 1 to 100", category="invalid_request", code="invalid_steps")
    return outputs, {"prompt": prompt, "width": width, "height": height, "seed": seed, "steps": steps}


def base_url() -> str:
    value = os.environ.get("COMFYUI_BASE_URL", "http://127.0.0.1:8188").strip().rstrip("/")
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise AdapterFailure("COMFYUI_BASE_URL must be an http(s) URL", code="invalid_base_url")
    return value


def auth_token() -> str | None:
    token = os.environ.get("COMFYUI_TOKEN", "").strip()
    if token:
        return token
    env_path = Path(os.environ.get("COMFYUI_ENV_FILE", "/mnt/data/ComfyUI/.env"))
    try:
        lines = env_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    for raw in lines:
        line = raw.strip()
        if line.startswith("export "):
            line = line[7:].lstrip()
        key, sep, value = line.partition("=")
        if sep and key.strip() == "COMFYUI_TOKEN":
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]
            else:
                value = value.split(" #", 1)[0].strip()
            return value or None
    return None


def request_json(
    url: str,
    *,
    payload: dict[str, Any] | None = None,
    timeout: float = 30,
    token: str | None = None,
) -> Any:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"} if data is not None else {}
    if token:
        headers["Authorization"] = "Bearer " + token
    request = urllib.request.Request(url, data=data, headers=headers, method="POST" if data is not None else "GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
    except urllib.error.HTTPError as exc:
        category = "authentication" if exc.code == 401 else "permission" if exc.code == 403 else "provider_response"
        raise AdapterFailure("ComfyUI HTTP request failed", category=category, code=f"http_{exc.code}", retryable=exc.code == 429 or exc.code >= 500, submitted=payload is not None, http_status=exc.code) from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise AdapterFailure("ComfyUI is unreachable", category="network", code="comfyui_unreachable", retryable=True, submitted=payload is not None) from exc
    if len(raw) > MAX_RESPONSE_BYTES:
        raise AdapterFailure("ComfyUI response exceeds the size limit", category="provider_response", code="response_too_large", submitted=payload is not None)
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AdapterFailure("ComfyUI returned invalid JSON", category="provider_response", code="invalid_response", submitted=payload is not None) from exc


def save_handle(path_value: object, prompt_id: str) -> None:
    if not isinstance(path_value, str) or not path_value:
        return
    try:
        path = Path(path_value)
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(prefix=".comfy-handle-", dir=str(path.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                json.dump({"provider_job_id": prompt_id}, stream)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp_name, path)
        finally:
            try:
                os.unlink(temp_name)
            except FileNotFoundError:
                pass
    except Exception as exc:
        raise AdapterFailure("任務已提交但回收紀錄保存失敗；請以任務編號 collect", category="configuration", code="handle_save_failed", submitted=True, request_id=prompt_id, retryable=True) from exc


def build_workflow(prompt: str, width: int, height: int, seed: int, steps: int, batch: int, filename_prefix: str) -> dict[str, Any]:
    try:
        workflow = json.loads(WORKFLOW_FILE.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AdapterFailure("ComfyUI API workflow template is unavailable", code="workflow_missing") from exc
    workflow["27"]["inputs"]["text"] = prompt
    workflow["13"]["inputs"].update({"width": width, "height": height, "batch_size": batch})
    workflow["3"]["inputs"].update({"seed": seed, "steps": steps})
    workflow["9"]["inputs"]["filename_prefix"] = filename_prefix
    return workflow


def get_history(base: str, prompt_id: str, token: str | None) -> dict[str, Any]:
    result = request_json(base + "/history/" + urllib.parse.quote(prompt_id, safe=""), token=token)
    if not isinstance(result, dict):
        raise AdapterFailure("ComfyUI history response is invalid", category="provider_response", code="invalid_history", submitted=True, request_id=prompt_id)
    item = result.get(prompt_id)
    if item is None:
        return {}
    if not isinstance(item, dict):
        raise AdapterFailure("ComfyUI history item is invalid", category="provider_response", code="invalid_history", submitted=True, request_id=prompt_id)
    return item


def download_image(base: str, item: dict[str, Any], target: Path, token: str | None) -> None:
    filename = item.get("filename")
    subfolder = item.get("subfolder", "")
    image_type = item.get("type", "output")
    if not isinstance(filename, str) or not filename or Path(filename).name != filename:
        raise AdapterFailure("ComfyUI returned an unsafe image filename", category="provider_response", code="invalid_output", submitted=True)
    if not isinstance(subfolder, str) or not isinstance(image_type, str):
        raise AdapterFailure("ComfyUI returned invalid image metadata", category="provider_response", code="invalid_output", submitted=True)
    query = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": image_type})
    url = base + "/view?" + query
    headers = {"Authorization": "Bearer " + token} if token else {}
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=60) as response, target.open("wb") as out:
            shutil.copyfileobj(response, out, length=1024 * 1024)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise AdapterFailure("ComfyUI image download failed", category="network", code="download_failed", retryable=True, submitted=True) from exc
    if not target.is_file() or target.stat().st_size == 0:
        raise AdapterFailure("ComfyUI returned an empty image", category="provider_response", code="empty_output", submitted=True)


def main() -> int:
    prompt_id = None
    try:
        job = read_job()
        targets, params = clean_parameters(job)
        base = base_url()
        token = auth_token()
        output_root = job.get("output_root")
        if not isinstance(output_root, str) or not output_root:
            raise AdapterFailure("output_root is missing", category="contract", code="missing_output_root")
        out_dir = Path(output_root)
        out_dir.mkdir(parents=True, exist_ok=True)
        try:
            timeout = int(os.environ.get("COMFYUI_TIMEOUT_SECONDS", "900"))
            interval = float(os.environ.get("COMFYUI_POLL_INTERVAL_SECONDS", "2"))
        except ValueError as exc:
            raise AdapterFailure("輪詢時間設定不合法", code="invalid_poll_settings") from exc
        if not 1 <= timeout <= 3600 or not math.isfinite(interval) or not 0.2 <= interval <= 60:
            raise AdapterFailure("invalid ComfyUI polling configuration", code="invalid_poll_settings", submitted=False)
        prompt_id = job.get("collect_provider_job_id")
        if prompt_id is not None:
            if not isinstance(prompt_id, str) or not prompt_id:
                raise AdapterFailure("collect_provider_job_id is invalid", category="contract", code="invalid_handle")
        else:
            suffix = re.sub(r"[^A-Za-z0-9_-]+", "-", str(job.get("job_id", "image")))[:32].strip("-") or "image"
            prefix = "drama-" + suffix + "-" + uuid.uuid4().hex[:10]
            workflow = build_workflow(params["prompt"], params["width"], params["height"], params["seed"], params["steps"], len(targets), prefix)
            response = request_json(base + "/prompt", payload={"prompt": workflow, "client_id": str(uuid.uuid4())}, token=token)
            if not isinstance(response, dict) or not isinstance(response.get("prompt_id"), str):
                raise AdapterFailure("ComfyUI did not return a prompt ID", category="provider_response", code="missing_prompt_id", submitted=True)
            prompt_id = response["prompt_id"]
            save_handle(job.get("handle_path"), prompt_id)

        deadline = time.monotonic() + timeout
        history: dict[str, Any] = {}
        while time.monotonic() < deadline:
            history = get_history(base, prompt_id, token)
            status = history.get("status", {})
            status_text = status.get("status_str") if isinstance(status, dict) else None
            if status_text == "error":
                raise AdapterFailure("ComfyUI workflow execution failed", category="provider_response", code="workflow_failed", submitted=True, request_id=prompt_id)
            outputs = history.get("outputs", {})
            save_node = outputs.get("9", {}) if isinstance(outputs, dict) else {}
            images = save_node.get("images", []) if isinstance(save_node, dict) else []
            if isinstance(images, list) and len(images) >= len(targets):
                break
            time.sleep(interval)
        else:
            raise AdapterFailure("ComfyUI generation timed out; the task may still be running", category="timeout", code="comfyui_timeout", retryable=True, submitted=True, request_id=prompt_id)

        sources: list[dict[str, str]] = []
        for index, (image, target) in enumerate(zip(images, targets), 1):
            source = out_dir / f"comfyui-{index:02d}.png"
            download_image(base, image, source, token)
            sources.append({"target": target, "source": str(source)})
        sys.stdout.write(json.dumps({"outputs": sources, "provider_job_id": prompt_id}, ensure_ascii=False) + "\n")
        return 0
    except AdapterFailure as exc:
        if prompt_id:
            exc.submitted, exc.request_id = True, prompt_id
        emit_error(exc)
        return 1
    except Exception:
        emit_error(AdapterFailure("ComfyUI adapter failed unexpectedly", category="provider_response", code="adapter_error", submitted=bool(prompt_id), request_id=prompt_id))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
