#!/usr/bin/env python3
"""本機 ComfyUI MiniMax H3 影片介面；不讀取供應商 API 金鑰。"""
from __future__ import annotations
import copy
import json
import math
import mimetypes
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from comfyui_image_adapter import (
    AdapterFailure, auth_token, base_url, read_job, request_json,
    save_handle, get_history,
)

PROVIDER = "comfyui-local-video"


def fail(detail, code="invalid_video_parameters"):
    raise AdapterFailure(detail, category="invalid_request", code=code)


def integer(value, name, low, high, multiple=1):
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high or value % multiple:
        fail(f"{name} 超出範圍或不符合倍數要求")
    return value


def preflight(job):
    if job.get("modality") != "video":
        fail("此介面只接受 video 任務")
    if not isinstance(job.get("prompt"), str) or not job["prompt"].strip():
        fail("影片提示詞不可空白")
    outputs = job.get("outputs")
    if not isinstance(outputs, list) or len(outputs) != 1 or not isinstance(outputs[0], str) or Path(outputs[0]).suffix.lower() != ".mp4":
        fail("每次任務須指定一個 MP4 輸出")
    p = job.get("parameters", {})
    if not isinstance(p, dict):
        fail("parameters 必須是物件")
    allowed = {"prompt_language", "workflow", "width", "height", "duration", "frames",
               "fps", "seed", "steps", "audio", "frame_policy", "allow_long_video"}
    if set(p) - allowed:
        fail("含有不支援的影片引數")
    mode = p.get("workflow", "fl2va")
    if mode not in {"fl2va", "ref2va"}:
        fail("workflow 須為 fl2va 或 ref2va")
    width = integer(p.get("width", 768), "width", 64, 2048, 32)
    height = integer(p.get("height", 768), "height", 64, 2048, 32)
    fps = p.get("fps", 24)
    if isinstance(fps, bool) or fps != 24:
        fail("目前 H3 工作流固定使用 24 fps")
    policy = p.get("frame_policy", "exact")
    if policy not in {"exact", "ceil"}:
        fail("frame_policy 須為 exact 或 ceil")
    duration = p.get("duration")
    if duration is not None and (isinstance(duration, bool) or not isinstance(duration, (int, float)) or not math.isfinite(duration) or duration <= 0):
        fail("duration 必須是有限正數")
    frames = p.get("frames")
    if frames is None:
        if duration is None:
            fail("須指定 duration 或 frames")
        requested = duration * fps
        frames = max(5, math.ceil((requested - 5) / 17 - 1e-9) * 17 + 5)
        if policy == "exact" and abs(frames - requested) > 1e-6:
            fail("時長不符合 17k+5 幀格；請明確使用 frame_policy=ceil 或指定合法 frames")
    frames = integer(frames, "frames", 5, 3600)
    if (frames - 5) % 17:
        fail("frames 必須符合 17k+5")
    if duration is not None:
        delta = frames - duration * fps
        if policy == "exact" and abs(delta) > 1e-6 or policy == "ceil" and not -1e-6 <= delta < 17 + 1e-6:
            fail("frames 與 duration 不一致")
    for name in ("audio", "allow_long_video"):
        if name in p and not isinstance(p[name], bool):
            fail(name + " 必須是布林值")
    if frames > 362 and not p.get("allow_long_video", False):
        fail("超過約 15 秒的模型已訓練範圍；請先拆鏡，或明確允許未驗證長片段")
    seed = integer(p.get("seed", 42), "seed", 0, 2**64 - 1)
    steps = integer(p.get("steps", 8), "steps", 1, 100)
    bindings = job.get("reference_bindings", [])
    if not isinstance(bindings, list) or any(not isinstance(b, dict) for b in bindings):
        fail("reference_bindings 必須是物件陣列")
    roles = [b.get("role") for b in bindings]
    if mode == "fl2va":
        if roles.count("first_frame") != 1 or roles.count("last_frame") > 1 or any(r not in {"first_frame", "last_frame"} for r in roles):
            fail("fl2va 須有一張首幀，可選一張尾幀，不可混入外貌參考圖")
    elif not 1 <= len(roles) <= 9 or any(r != "reference_image" for r in roles):
        fail("ref2va 須有 1 至 9 張 reference_image，不可混用首尾幀角色")
    if [b.get("order") for b in bindings] != list(range(1, len(bindings) + 1)):
        fail("參考圖 order 須由 1 連續編號")
    root = Path(job.get("project_root", "")).resolve()
    files = []
    for binding in bindings:
        rel = binding.get("path")
        if not isinstance(rel, str) or Path(rel).is_absolute():
            fail("參考圖須使用專案相對路徑")
        path = (root / rel).resolve()
        if not path.is_relative_to(root) or not path.is_file() or path.stat().st_size > 30 * 1024 * 1024:
            fail("參考圖遺失、過大或超出專案")
        data = path.read_bytes()
        valid = (data.startswith(b"\x89PNG\r\n\x1a\n") or data.startswith(b"\xff\xd8\xff")
                 or data[:4] == b"RIFF" and data[8:12] == b"WEBP")
        if not valid:
            fail("參考圖須為 PNG、JPEG 或 WebP")
        files.append((binding["role"], path))
    if not isinstance(job.get("output_root"), str) or not job["output_root"]:
        fail("缺少 output_root")
    timeout = float(os.environ.get("COMFYUI_VIDEO_TIMEOUT_SECONDS", "3300"))
    interval = float(os.environ.get("COMFYUI_POLL_INTERVAL_SECONDS", "2"))
    if not math.isfinite(timeout) or not 1 <= timeout <= 3500 or not math.isfinite(interval) or not .2 <= interval <= 60:
        fail("輪詢時間設定不合法")
    return dict(mode=mode, width=width, height=height, frames=frames, fps=24,
                seed=seed, steps=steps, audio=p.get("audio", False),
                files=files, timeout=timeout, interval=interval)


def template(params):
    name = "gen_video_" + params["mode"] + "_api.json"
    try:
        graph = json.loads(Path(__file__).with_name(name).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        fail("影片 API 工作流模板不可讀", "workflow_missing")
    return graph


def check_nodes(graph, info):
    if not isinstance(info, dict):
        fail("無法取得節點規格")
    for node in graph.values():
        schema = info.get(node["class_type"])
        if not isinstance(schema, dict):
            fail("ComfyUI 缺少工作流所需節點", "node_missing")
        specs = schema.get("input", {})
        for key, val in node["inputs"].items():
            if node["class_type"] == "LoadImage" and key == "image":
                continue
            spec = specs.get("required", {}).get(key, specs.get("optional", {}).get(key))
            if spec and isinstance(spec[0], list) and not isinstance(val, list) and val not in spec[0]:
                fail("工作流使用的模型或選項未安裝", "model_or_option_missing")


def upload(base, token, path):
    boundary = "drama" + uuid.uuid4().hex
    filename = "drama-" + uuid.uuid4().hex + path.suffix.lower()
    data = path.read_bytes()
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{filename}\"\r\n"
            f"Content-Type: {mimetypes.guess_type(filename)[0] or 'application/octet-stream'}\r\n\r\n").encode() + data
    body += (f"\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"type\"\r\n\r\ninput"
             f"\r\n--{boundary}--\r\n").encode()
    headers = {"Content-Type": "multipart/form-data; boundary=" + boundary}
    if token:
        headers["Authorization"] = "Bearer " + token
    try:
        with urllib.request.urlopen(urllib.request.Request(base + "/upload/image", data=body, headers=headers), timeout=60) as response:
            value = json.loads(response.read(1024 * 1024))
    except Exception as exc:
        raise AdapterFailure("參考圖上傳失敗，尚未提交生成", category="network", code="upload_failed", retryable=True) from exc
    name, folder = value.get("name"), value.get("subfolder", "")
    if not isinstance(name, str) or Path(name).name != name or not isinstance(folder, str) or ".." in Path(folder).parts or Path(folder).is_absolute():
        fail("上傳回傳檔名不合法")
    return (folder.rstrip("/") + "/" if folder else "") + name


def build(job, params, graph, uploaded):
    graph = copy.deepcopy(graph)
    graph["8"]["inputs"].update(prompt=job["prompt"], width=params["width"],
                                height=params["height"], length=params["frames"])
    graph["9"]["inputs"]["noise_seed"] = params["seed"]
    graph["12"]["inputs"]["steps"] = params["steps"]
    graph["16"]["inputs"]["fps"] = params["fps"]
    if not params["audio"]:
        graph["16"]["inputs"].pop("audio", None)
        graph.pop("15", None)
        if params["mode"] == "fl2va":
            graph.pop("5", None)
    for i, (role, filename) in enumerate(uploaded):
        node_id = str(100 + i)
        graph[node_id] = {"class_type": "LoadImage", "inputs": {"image": filename}}
        key = role if role in {"first_frame", "last_frame"} else "ref_images.ref_image_" + str(i)
        graph["8"]["inputs"][key] = [node_id, 0]
    save_id = "28" if params["mode"] == "fl2va" else "17"
    graph[save_id]["inputs"].update(filename_prefix="drama-video-" + uuid.uuid4().hex, format="mp4", codec="h264")
    return graph, save_id


def download(base, token, item, target):
    name = item.get("filename")
    folder = item.get("subfolder", "")
    if not isinstance(name, str) or Path(name).name != name or not name.lower().endswith(".mp4"):
        fail("ComfyUI 影片檔名不合法")
    if not isinstance(folder, str) or ".." in Path(folder).parts or Path(folder).is_absolute() or item.get("type", "output") != "output":
        fail("ComfyUI 影片路徑不合法")
    query = urllib.parse.urlencode({"filename": name, "subfolder": folder, "type": "output"})
    headers = {"Authorization": "Bearer " + token} if token else {}
    temp = target.with_suffix(".part")
    try:
        with urllib.request.urlopen(urllib.request.Request(base + "/view?" + query, headers=headers), timeout=120) as response, temp.open("wb") as stream:
            size = 0
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                size += len(chunk)
                if size > 2 * 1024**3:
                    fail("影片超過 2GB 上限")
                stream.write(chunk)
        with temp.open("rb") as stream:
            header = stream.read(12)
        if header[4:8] != b"ftyp":
            fail("輸出不是有效 MP4 容器")
        temp.replace(target)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise AdapterFailure("影片下載失敗；請 collect 原任務重試下載", category="network", code="download_failed", retryable=True) from exc
    finally:
        temp.unlink(missing_ok=True)


def run(job):
    params = preflight(job)
    base, token = base_url(), auth_token()
    prompt_id = job.get("collect_provider_job_id")
    save_id = "28" if params["mode"] == "fl2va" else "17"
    if prompt_id is not None and (not isinstance(prompt_id, str) or not prompt_id):
        fail("collect_provider_job_id 不合法")
    if prompt_id is None:
        graph = template(params)
        info = request_json(base + "/object_info", token=token)
        check_nodes(graph, info)
        uploaded = [(role, upload(base, token, path)) for role, path in params["files"]]
        graph, save_id = build(job, params, graph, uploaded)
        response = request_json(base + "/prompt", payload={"prompt": graph, "client_id": str(uuid.uuid4())}, token=token)
        if not isinstance(response, dict) or not isinstance(response.get("prompt_id"), str):
            raise AdapterFailure("ComfyUI 未回傳任務編號", category="provider_response", code="missing_prompt_id", submitted=True)
        prompt_id = response["prompt_id"]
        save_handle(job.get("handle_path"), prompt_id)
    try:
        deadline = time.monotonic() + params["timeout"]
        while time.monotonic() < deadline:
            history = get_history(base, prompt_id, token)
            status = history.get("status", {})
            if status.get("status_str") == "error":
                raise AdapterFailure("ComfyUI 影片工作流執行失敗", category="provider_response", code="workflow_failed")
            node = history.get("outputs", {}).get(save_id, {})
            candidates = []
            for key in ("videos", "images", "gifs"):
                values = node.get(key, [])
                if isinstance(values, list):
                    candidates.extend(x for x in values if isinstance(x, dict) and str(x.get("filename", "")).lower().endswith(".mp4"))
            if candidates:
                out = Path(job["output_root"])
                out.mkdir(parents=True, exist_ok=True)
                target = out / "comfyui-video.mp4"
                download(base, token, candidates[0], target)
                return {"outputs": [{"target": job["outputs"][0], "source": str(target)}],
                        "provider_job_id": prompt_id}
            if status.get("completed"):
                raise AdapterFailure("工作流完成但沒有 MP4", category="provider_response", code="missing_video")
            time.sleep(params["interval"])
        raise AdapterFailure("輪詢逾時；請 collect 原任務，不要重送", category="timeout", code="comfyui_timeout", retryable=True)
    except AdapterFailure as exc:
        exc.submitted = True
        exc.request_id = prompt_id
        raise
    except Exception as exc:
        raise AdapterFailure("影片回收失敗；請 collect 原任務", category="provider_response", code="collection_failed", submitted=True, request_id=prompt_id, retryable=True) from exc


def main():
    try:
        print(json.dumps(run(read_job()), ensure_ascii=False))
        return 0
    except AdapterFailure as exc:
        error = {"provider": PROVIDER, "category": exc.category, "code": exc.code,
                 "retryable": exc.retryable, "submitted": exc.submitted, "detail": str(exc)[:160]}
        if exc.request_id:
            error["request_id"] = exc.request_id
        if exc.http_status:
            error["http_status"] = exc.http_status
        print(json.dumps({"error": error}, ensure_ascii=False))
        return 1
    except Exception:
        print(json.dumps({"error": {"provider": PROVIDER, "category": "provider_response",
                                   "code": "adapter_error", "retryable": False, "submitted": False,
                                   "detail": "影片介面發生未預期錯誤；請先核對任務紀錄"}}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
