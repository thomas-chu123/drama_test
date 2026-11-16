#!/usr/bin/env python3
"""以本機 Qwen 參考圖編輯流程生成首幀。"""
from pathlib import Path
import json
import time
import uuid
from comfyui_image_adapter import (
    AdapterFailure, auth_token, base_url, request_json, read_job,
    save_handle, get_history, download_image,
)
from comfyui_video_adapter import check_nodes, upload, fail


def preflight(job):
    if job.get("modality") != "image" or not isinstance(job.get("prompt"), str) or not job["prompt"].strip():
        fail("須提供圖片任務與非空提示詞")
    targets = job.get("outputs", [])
    if len(targets) != 1 or not isinstance(targets[0], str) or Path(targets[0]).suffix.lower() != ".png":
        fail("每次須指定一個 PNG 輸出")
    p = job.get("parameters", {})
    if not isinstance(p, dict) or set(p) - {"width", "height", "seed", "prompt_language"}:
        fail("含不支援的圖片引數")
    for key in ("width", "height"):
        value = p.get(key, 768)
        if type(value) is not int or not 64 <= value <= 2048 or value % 32:
            fail("尺寸須為 64 至 2048 間的 32 倍數")
    seed = p.get("seed", 42)
    if type(seed) is not int or not 0 <= seed < 2**64:
        fail("種子須為無號 64 位整數")
    bindings = job.get("reference_bindings", [])
    if len(bindings) != 1 or bindings[0].get("role") != "reference_image" or bindings[0].get("order") != 1:
        fail("須提供一張外貌參考圖片")
    root = Path(job["project_root"]).resolve()
    relative = bindings[0].get("path")
    if not isinstance(relative, str) or Path(relative).is_absolute():
        fail("參考圖須為專案相對路徑")
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or not path.is_file() or path.stat().st_size > 30 * 1024**2:
        fail("參考圖遺失、過大或超出專案")
    if not path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
        fail("此測試介面須輸入 PNG 參考圖")
    if not isinstance(job.get("output_root"), str) or not job["output_root"]:
        fail("缺少暫存輸出目錄")
    return p, path


def build(job, p, filename):
    graph = json.loads(Path(__file__).with_name("edit_image_qwen_turbo_api.json").read_text())
    graph["100"] = {"class_type": "LoadImage", "inputs": {"image": filename}}
    graph["474"]["inputs"]["prompt"] = job["prompt"]
    graph["456"]["inputs"].update(width=p.get("width", 768), height=p.get("height", 768))
    graph["504"]["inputs"]["noise_seed"] = p.get("seed", 42)
    graph["9"]["inputs"]["filename_prefix"] = "drama-keyframe-" + uuid.uuid4().hex
    return graph


def run(job):
    p, path = preflight(job)
    base, token = base_url(), auth_token()
    prompt_id = job.get("collect_provider_job_id")
    if prompt_id is not None and (not isinstance(prompt_id, str) or not prompt_id):
        fail("取回任務編號不合法")
    if prompt_id is None:
        graph = build(job, p, path.name)
        check_nodes(graph, request_json(base + "/object_info", token=token))
        graph["100"]["inputs"]["image"] = upload(base, token, path)
        response = request_json(base + "/prompt", payload={"prompt": graph, "client_id": str(uuid.uuid4())}, token=token)
        prompt_id = response.get("prompt_id") if isinstance(response, dict) else None
        if not isinstance(prompt_id, str) or not prompt_id:
            raise AdapterFailure("未取得任務編號", submitted=True, code="missing_prompt_id")
        save_handle(job.get("handle_path"), prompt_id)
    try:
        deadline = time.monotonic() + 3300
        while time.monotonic() < deadline:
            history = get_history(base, prompt_id, token)
            status = history.get("status", {})
            if status.get("status_str") == "error":
                raise AdapterFailure("首幀工作流執行失敗", code="workflow_failed")
            images = history.get("outputs", {}).get("9", {}).get("images", [])
            if images:
                out = Path(job["output_root"])
                out.mkdir(parents=True, exist_ok=True)
                target = out / "keyframe.png"
                download_image(base, images[0], target, token)
                if not target.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
                    fail("回收圖片不是 PNG")
                return {"outputs": [{"target": job["outputs"][0], "source": str(target)}], "provider_job_id": prompt_id}
            if status.get("completed"):
                raise AdapterFailure("工作流完成但沒有圖片", code="missing_image")
            time.sleep(2)
        raise AdapterFailure("輪詢逾時；請取回原任務", code="comfyui_timeout", retryable=True)
    except AdapterFailure as exc:
        exc.submitted, exc.request_id = True, prompt_id
        raise
    except Exception as exc:
        raise AdapterFailure("首幀回收失敗；請 collect 原任務", category="provider_response", code="collection_failed", submitted=True, request_id=prompt_id, retryable=True) from exc


if __name__ == "__main__":
    try:
        print(json.dumps(run(read_job()), ensure_ascii=False))
    except AdapterFailure as exc:
        print(json.dumps({"error": {"provider": "comfyui-local-edit", "category": exc.category,
              "code": exc.code, "detail": str(exc), "retryable": exc.retryable,
              "submitted": exc.submitted, "request_id": exc.request_id}}, ensure_ascii=False))
        raise SystemExit(1)
    except Exception:
        print(json.dumps({"error": {"provider": "comfyui-local-edit", "category": "provider_response",
              "code": "adapter_error", "detail": "參考圖編輯介面發生非預期錯誤", "retryable": False,
              "submitted": False}}, ensure_ascii=False))
        raise SystemExit(1)
