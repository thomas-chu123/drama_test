# ComfyUI adapter

此 adapter 供 `$short-drama-produce` 呼叫本機 ComfyUI 的文字生圖 workflow。

## 內容

- `comfyui_image_adapter.py`：讀取標準 production job JSON，提交工作、輪詢 ComfyUI 歷史、下載結果到暫存輸出目錄，並回傳 production_tool 所需的輸出 JSON。
- `gen_image_api.json`：依 `/mnt/data/ComfyUI/user/default/workflows/gen_image.json` 的 Z-Image-Turbo 子圖翻成 ComfyUI API 格式；保留模型、CLIP、VAE、AuraFlow、8 steps、CFG 1、res_multistep、simple scheduler 等設定。

## 啟用方式

1. 將 `comfyui-adapter-config.example.json` 複製到專案目錄之外，作為 `--adapter-config`。
2. 如 ComfyUI API 不在預設的 `http://127.0.0.1:8188`，設定環境變數 `COMFYUI_BASE_URL`。
3. 使用 adapter 名稱 `comfyui-local` 建立圖片任務。workflow 目前支援 PNG 文生圖，不支援參考圖編輯。
4. 單條任務可設定 `parameters.width`、`height`、`size`（如 `1024x1024`）、`seed`、`steps`；省略時使用 workflow 預設值。一次任務可指定 1–16 個 PNG 輸出，ComfyUI 以 batch_size 執行。

## ComfyUI 端點

預設 ComfyUI 網址為 http://127.0.0.1:8188，並從環境變數 COMFYUI_TOKEN 或 /mnt/data/ComfyUI/.env 讀取 COMFYUI_TOKEN，以 Bearer Authorization 標頭驗證；token 不會寫入專案或 adapter 設定檔，也不會輸出到記錄。可用 COMFYUI_ENV_FILE 指定其他 .env 路徑，COMFYUI_TIMEOUT_SECONDS（預設 900）與 COMFYUI_POLL_INTERVAL_SECONDS（預設 2）調整等待時間。

## 影片生成

已新增 comfyui-local-video，支援 MiniMax H3 首幀／首尾幀及多圖參考。詳見 [VIDEO-README.md](VIDEO-README.md)。

## 單圖與多圖參考首幀

`comfyui-local-edit` 使用 Qwen Image 2.1 Turbo，可依 `reference_bindings` 順序輸入 1–16 張 PNG，角色均為 `reference_image`。每張上限 30 MiB，合計上限 48 MiB；以 `<image1>`、`<image2>` 等在提示詞中區分人物、道具與場景用途。

`parameters.reference_resolution` 對應編碼節點的參考圖解析度，預設 0 保留既有單圖行為；多圖首幀批次使用 512 控制輸入負擔。輸出尺寸仍由 width／height 決定，步數維持模板的 8 步固定 sigma。collect 僅回收既有任務，不重新上傳或提交。

離線驗證：`python3 adapters/test_edit_multireference.py`；本機節點宣告支援至 image_16。多人鏡頭的實際品質與耗時仍須生成後驗收。
