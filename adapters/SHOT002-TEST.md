# 段譽「笑聲引視」介面試拍

## 任務預覽

- 範圍：第二鏡 SHOT-EP001-002，只有段譽入畫。左手掩嘴、右手握合扇，低笑後收笑抬眼，鏡頭緩推。
- 首幀：本機 Qwen Image 2.1 Turbo，參考既有段譽三視圖；單張寫實敘事畫面，768×768，8 步手動 sigma，CFG 1，種子 42。停用提示詞增強，避免改寫原定動作。
- 首幀輸出：`episodes/EP001/production/images/EP001-SHOT002-START.png`。
- 影片：本機 MiniMax H3 fl2va，首幀單圖輸入，768×768、24 fps、107 幀，約 4.458 秒，8 步，種子 42，無音軌。約第 4 秒完成表演，餘下時間穩住表情。原分鏡 4 秒不變。
- 影片輸出：`episodes/EP001/production/videos/EP001-SHOT002-fl2va-test.mp4`。
- 本次未測 ref2va，也不測聲音；107 幀低於節點標示約 124 幀的已訓練下限，需由實際成片評估品質。

## 準備與驗證結果

- 新增 `comfyui_edit_adapter.py` 與 `edit_image_qwen_turbo_api.json`，從本機參考圖工作流轉換；沿用模型、快取及採樣設定，啟用單張 768×768 目標畫布。
- 首幀任務已完成 production_tool 的 prepare，狀態為待確認。任務單見 `jobs/duanyu-shot002-keyframe.json`。
- 影片任務單見 `jobs/duanyu-shot002-video.json`；首幀尚未生成，故尚不能 prepare 或確認影片。首幀完成並檢視後再將分鏡、影片提示詞的 PLAN 槽位改綁實圖，移除影片不再需要的外貌參考。
- 通過 Python 語法、真實參考圖輸入及既存 object_info 快照的節點／模型檢查。未完成即時節點查驗。
- 通過模擬回收測試：collect 既有任務不重送、不重傳圖片；缺少參考圖會在提交前攔截。
- ComfyUI MCP 可讀取佇列；shell 的 socket 建立遭沙箱拒絕（Operation not permitted），因此 production adapter 無法在目前環境直接連線。未提交圖片或影片生成，沒有實機通過結論。
- 專案外設定 `/tmp/drama-test-comfyui-adapters.json` 已加入 `comfyui-local-edit`。金鑰未寫入專案。
- production_tool 的 source_entry 解析器僅接受其規定的中文創作檔名；本專案使用英文檔名，因此任務明確攜帶提示詞和參考繫結，以整份 source 文件摘要核驗。後續修改該來源文件須重新 prepare。

## 待執行

在允許 adapter 連線本機 ComfyUI 的執行環境，取得創作者對上述首幀預覽的明確確認後：

```bash
python3 /home/skynet/.codex/skills/short-drama-produce/scripts/production_tool.py confirm . --job-id EP001-SHOT002-keyframe-test --confirmation 'CONFIRM EP001-SHOT002-keyframe-test 9858886982d9'
python3 /home/skynet/.codex/skills/short-drama-produce/scripts/production_tool.py run . --job-id EP001-SHOT002-keyframe-test --adapter-config /tmp/drama-test-comfyui-adapters.json
```

首幀完成後先檢視人物、手勢與單人構圖，再同步 REF 並準備影片預覽；不得代填創作者確認或用三視圖冒充首幀。

## 2026-11-16 sandbox 實跑結果

- 使用者分別確認首幀與影片任務後，兩項皆透過 sandbox 內的 adapter 成功提交、生成並下載，未使用提權。先前連線受阻與待執行描述為歷史紀錄。
- 首幀：`episodes/EP001/production/images/EP001-SHOT002-START.png`。圖片左右手與設定相反，扇子略微展開；已向使用者揭露後取得影片測試確認。未視為正式創作定稿，未改綁創作文件。
- 影片：`episodes/EP001/production/videos/EP001-SHOT002-fl2va-test.mp4`。
- 任務編號：`cbde7bb6-c965-491d-883d-3cefa5066891`；執行紀錄：`20261116T131114-a9387e18`；狀態：成功。
- ffprobe 確認 H.264、768×768、24 fps、107 幀、4.456 秒、1,185,903 位元組，無音軌。ffmpeg 全片解碼通過，未回報錯誤。
- 結論：本次 fl2va 影片的提交、輪詢與 MP4 下載完整通過；未測 ref2va、音訊及其他尺寸。
