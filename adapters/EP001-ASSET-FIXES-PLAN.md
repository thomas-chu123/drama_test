# EP001 指定素材修正批次

- 共 9 張：高個老者、營地、合扇、兩種藥瓶、繡花鞋、鐵銬，以及鍾靈人物板與服裝板的鞋型同步。
- 只修使用者指定問題；鍾靈人物的年齡觀感、其他未指定圖片問題留待後續，不藉此重做全批。
- 原圖全部保留，修正版以 `-FIX01.png` 另存。
- 高個老者採 Z-Image-Turbo 重新生成年長男性；其餘八張採 Qwen Image 2.1 Turbo 參考圖編輯。
- 全部 1024×1024、種子 42；兩個工作流均為 8 步，Qwen 使用既有固定 sigma。
- 鞋型三圖共用同一結構描述，分別編輯各自原圖；目前單圖 adapter 無法同時引用鞋圖與人物圖，產出後仍須比較一致性，不保證逐像素保留。
- 預估生成與模型切換約 3–8 分鐘，檢視另約 5–10 分鐘；每項先修一次，不自動追加重跑。

| 條目 | 修正內容 | 介面 | 新輸出 |
| --- | --- | --- | --- |
| IMG-TALL-ELDER-CHARACTER | 將錯誤女性重新生成人物設定中的年長高個男子；保留採藥幫眾衣著與坐倒傷勢。 | `comfyui-local` | `episodes/EP001/production/images/EP001-TALL-ELDER-CHARACTER-FIX01.png` |
| IMG-SHENNONG-CAMP | 移除現代帳篷，原區域回復裸岩與草叢。 | `comfyui-local-edit` | `episodes/EP001/production/images/EP001-SHENNONG-CAMP-FIX01.png` |
| IMG-DUANYU-FAN | 完全合扇，不留展開弧面。 | `comfyui-local-edit` | `episodes/EP001/production/images/EP001-DUANYU-FAN-FIX01.png` |
| IMG-SIKONG-MEDICINE | 旋蓋改木塞，移除手掌與現代瓶口結構。 | `comfyui-local-edit` | `episodes/EP001/production/images/EP001-SIKONG-MEDICINE-FIX01.png` |
| IMG-DUANCHANG-SAN | 開口瓶去螺紋，補同套木塞，保留紅藥末與瓷匙。 | `comfyui-local-edit` | `episodes/EP001/production/images/EP001-DUANCHANG-SAN-FIX01.png` |
| IMG-FLOWER-SHOES | 修正鞋扣、扣帶與厚白底為古式薄布底套腳鞋。 | `comfyui-local-edit` | `episodes/EP001/production/images/EP001-FLOWER-SHOES-FIX01.png` |
| IMG-HANDCUFFS | 現代警用結構改為粗鍛鐵環與簡單插銷。 | `comfyui-local-edit` | `episodes/EP001/production/images/EP001-HANDCUFFS-FIX01.png` |
| IMG-ZHONGLING-CHARACTER | 只同步人物三視圖鞋型；此次不改人物臉型或年齡。 | `comfyui-local-edit` | `episodes/EP001/production/images/EP001-ZHONGLING-CHARACTER-FIX01.png` |
| IMG-ZHONGLING-OUTFIT | 只同步服裝板鞋型，服裝其餘內容保留。 | `comfyui-local-edit` | `episodes/EP001/production/images/EP001-ZHONGLING-OUTFIT-FIX01.png` |

## 整批確認

`CONFIRM BATCH EP001-ASSET-FIXES-09 714740098996`
