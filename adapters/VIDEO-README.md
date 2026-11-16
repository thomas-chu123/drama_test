# 本機 MiniMax H3 影片介面

## 執行設定

- 介面名稱：comfyui-local-video；程式：adapters/comfyui_video_adapter.py。
- API 工作流：gen_video_fl2va_api.json、gen_video_ref2va_api.json；來自 /mnt/data/ComfyUI/user/default/workflows/ 的兩份 MiniMax 工作流。
- 已建立專案外設定：/tmp/drama-test-comfyui-adapters.json，含圖片及影片介面。暫存目錄可能被清理，長期使用請複製至專案外持久位置。
- COMFYUI_BASE_URL 預設 http://127.0.0.1:8188；COMFYUI_TOKEN 優先讀環境變數，否則從 /mnt/data/ComfyUI/.env 讀取。COMFYUI_ENV_FILE 可指定其他檔案。
- COMFYUI_VIDEO_TIMEOUT_SECONDS 預設 3300（1–3500）；COMFYUI_POLL_INTERVAL_SECONDS 預設 2（0.2–60）。
- 不使用 MiniMax 供應商 API；未修改 ComfyUI 原始工作流。
- API 模板移除範例提示詞、範例圖片及原本特定風格 LoRA，保留模型與採樣設定。

## 模式與引數

| 引數 | 設定 |
| --- | --- |
| workflow | fl2va（預設）：一張 first_frame，可選一張 last_frame；ref2va：1–9 張 reference_image |
| width、height | 預設 768，64–2048，32 的倍數；實際能力受節點與顯存限制 |
| duration／frames | 至少一項；合法 frames 為 17k+5；兩項並存須一致 |
| frame_policy | exact（預設）或明確指定 ceil 向上取整 |
| fps | 固定 24 |
| seed、steps | 預設 42、8；種子為無號 64 位整數，steps 1–100 |
| audio | false；true 才接入解碼音訊 |
| allow_long_video | false；超過 362 幀先攔截，true 只代表允許未驗證長片段 |
| prompt_language | 任務說明語種，不送節點 |

exact 不默默改時長：3 秒需 72 幀而不符合格點，會回報錯誤。ceil 將 3 秒取為 73 幀（3.0417 秒），6 秒取 158 幀（6.5833 秒）。直接指定 frames=124 則為 5.1667 秒。取整差需由分鏡／剪輯處理。
本機節點標示已訓練範圍約 124–362 幀；更短片段雖語法合法，品質未實測。32 秒鏡頭應優先回分鏡拆段。
fl2va 允許只給首幀，未提供尾幀時不接尾幀；不複製首幀當尾幀。ref2va 不把首幀角色偷換為普通參考。不支援參考影片或參考音訊。
EP001 目前的首幀＋段譽外貌圖，需先用外貌圖製作首幀，再由分鏡及影片提示詞階段整理投產參考為單一首幀，重新預覽確認；不能靜默丟棄第二張圖。

## 使用方式

任務 modality 設 video、adapter 設 comfyui-local-video，outputs 指向 episodes/EP001/production/videos/ 下的一個 MP4；參考圖須先從 PLAN 改綁真實 REF。
任務 parameters 範例：

~~~json
{
  "prompt_language": "zh-TW",
  "workflow": "fl2va",
  "duration": 4,
  "frame_policy": "ceil",
  "width": 768,
  "height": 768,
  "seed": 42,
  "steps": 8,
  "audio": false
}
~~~

依 short-drama-produce 的 prepare／confirm／run 流程；run 帶 --adapter-config /tmp/drama-test-comfyui-adapters.json。
先從已確認快照核對圖片路徑與檔頭，再上傳至 ComfyUI。prompt_id 取得後先原子寫入 handle_path，之後輪詢並下載 SaveVideo MP4。中斷時先 audit，再 collect 原任務；collect 不重新生成。
每次產出一個 MP4。標準輸入／輸出符合 production_tool 協議；錯誤摘要不輸出憑據、提示詞或本機路徑。

## 已完成檢查

已核對本機 object_info 的節點與模型選項，完成 Python 語法解析及離線模擬檢查：兩種接線、幀數取整、非法長度攔截、音訊開關、collect 不重新提交。
2026-11-16 已在 sandbox 內完成 fl2va 實跑：768×768、24 fps、107 幀、4.456 秒、無音軌；提交、輪詢、下載與 ffmpeg 全片解碼皆通過，未提權。另已完成同規格 audio=true 測試，輸出非靜音 AAC 32 kHz 雙聲道音軌，影音全片解碼通過；聽感品質待驗收，詳見 SHOT002-AUDIO-RESULT.md。尚未驗證 ref2va 與其他尺寸。詳細紀錄見 SHOT002-TEST.md。

提交前檢查輪詢設定；取得任務編號後若 handle 保存或回收失敗，錯誤回應保留任務編號。下載斷線可用 collect 重試，勿重送生成。
