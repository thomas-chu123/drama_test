# EP001 圖片製作批次規劃

## 盤點與範圍

- 設定圖共 38 張，段譽人物圖已完成，餘 37 張：人物／動物／群像 13、服裝 9、場景 4、道具 11。
- 鏡頭首幀共 38 張，第二鏡已有介面試拍圖，暫沿用，餘 37 張。第二鏡左右手與摺扇狀態仍為已知品質差異，不列入本批自動重出。
- 本批只提交 37 張設定圖，不提交影片、不重出既有圖。每項先產出一張候選，生成後檢視，不等同自動正式定稿。

## 本批設定與順序

- 沿用已成功的本機 Z-Image-Turbo 文生圖 adapter `comfyui-local`；1024×1024、8 步、種子 42。
- 提示詞逐項讀取 `episodes/EP001/image-prompts.md`，不額外偷偷加詞；目前描述為中性美術設定，人物五官等細節仍須看片確認。
- 依清單循序生成，人物與動物／群像 → 服裝 → 場景 → 道具；不並行占用 GPU。批次遇錯即停，成功項可斷點跳過，不自動反覆重跑。
- 產出集中於 `episodes/EP001/production/images/`；保留所有既有圖。

## 預估時間

既有單張設定圖約 18 秒，參考圖首幀約 14 秒，樣本各僅一張，不能當作穩定產速。以下是假設無其他 GPU 任務、無大幅模型切換延遲的本機排程估計，不含等待創作者回覆或未授權重跑：

| 階段 | 預估 |
| --- | --- |
| 37 張設定圖循序生成 | 約 10–25 分鐘 |
| 檢視、整理與必要參考繫結 | 約 20–40 分鐘 |
| 多圖首幀介面補齊與代表多人鏡頭驗證 | 約 20–40 分鐘 |
| 37 張首幀循序生成 | 約 10–30 分鐘，依多圖參考耗時修正 |
| 首幀檢視與綁定 | 約 20–40 分鐘 |

整體先預留約 1.5–3 小時；首批完成後依實測速度更新。若品質需修改或重跑，另行估算。

## 確認與依賴

- 設定圖整批只確認一次；確認後按既定任務順序連續執行，不逐張詢問。
- 首幀依賴尚未生成的參考圖，待設定圖產出並確認可沿用、補齊多人多圖輸入後，建立首幀批次再整批確認一次；不能用尚不存在的圖片偽造確認摘要。
- 參數、提示詞或參考圖若需改動，只處理受影響任務；不把本次確認當成無限重跑授權。
- 技術與內容分別檢視：格式／尺寸／可讀性，以及臉型、服裝、手部、受傷狀態、場景與道具一致性。

## 設定圖清單

| 順序 | 條目 | 圖片名稱 | 輸出 |
| --- | --- | --- | --- |
| 1 | IMG-ZHONGLING-CHARACTER | 鍾靈人物設定圖 | `episodes/EP001/production/images/EP001-ZHONGLING-CHARACTER.png` |
| 2 | IMG-ZUOZIMU-CHARACTER | 左子穆人物設定圖 | `episodes/EP001/production/images/EP001-ZUOZIMU-CHARACTER.png` |
| 3 | IMG-XINSHUANGQING-CHARACTER | 辛雙清人物設定圖 | `episodes/EP001/production/images/EP001-XINSHUANGQING-CHARACTER.png` |
| 4 | IMG-GONGGUANGJIE-CHARACTER | 龔光傑人物設定圖 | `episodes/EP001/production/images/EP001-GONGGUANGJIE-CHARACTER.png` |
| 5 | IMG-CHU-DISCIPLE-CHARACTER | 褚姓弟子人物設定圖 | `episodes/EP001/production/images/EP001-CHU-DISCIPLE-CHARACTER.png` |
| 6 | IMG-MAWUDE-CHARACTER | 馬五德人物設定圖 | `episodes/EP001/production/images/EP001-MAWUDE-CHARACTER.png` |
| 7 | IMG-MINK-CHARACTER | 閃電貂動物設定圖 | `episodes/EP001/production/images/EP001-MINK-CHARACTER.png` |
| 8 | IMG-RONGZIJU-CHARACTER | 容子矩人物狀態圖 | `episodes/EP001/production/images/EP001-RONGZIJU-CHARACTER.png` |
| 9 | IMG-SIKONGXUAN-CHARACTER | 司空玄人物傷勢設定圖 | `episodes/EP001/production/images/EP001-SIKONGXUAN-CHARACTER.png` |
| 10 | IMG-TALL-ELDER-CHARACTER | 神農幫高個老者人物狀態圖 | `episodes/EP001/production/images/EP001-TALL-ELDER-CHARACTER.png` |
| 11 | IMG-SHENNONG-GUARD | 神農幫守道幫眾人物設定圖 | `episodes/EP001/production/images/EP001-SHENNONG-GUARD.png` |
| 12 | IMG-SHENNONG-GROUP | 神農幫幫眾群像設定圖 | `episodes/EP001/production/images/EP001-SHENNONG-GROUP.png` |
| 13 | IMG-EAST-DISCIPLE | 東宗攔路弟子人物設定圖 | `episodes/EP001/production/images/EP001-EAST-DISCIPLE.png` |
| 14 | IMG-DUANYU-OUTFIT | 段譽青衫造型設定圖 | `episodes/EP001/production/images/EP001-DUANYU-OUTFIT.png` |
| 15 | IMG-ZHONGLING-OUTFIT | 鍾靈青衫造型設定圖 | `episodes/EP001/production/images/EP001-ZHONGLING-OUTFIT.png` |
| 16 | IMG-ZUOZIMU-OUTFIT | 左子穆掌門長袍設定圖 | `episodes/EP001/production/images/EP001-ZUOZIMU-OUTFIT.png` |
| 17 | IMG-XINSHUANGQING-OUTFIT | 辛雙清道姑常服設定圖 | `episodes/EP001/production/images/EP001-XINSHUANGQING-OUTFIT.png` |
| 18 | IMG-GONGGUANGJIE-OUTFIT | 龔光傑東宗弟子服設定圖 | `episodes/EP001/production/images/EP001-GONGGUANGJIE-OUTFIT.png` |
| 19 | IMG-CHU-WEST-OUTFIT | 褚姓弟子西宗弟子服設定圖 | `episodes/EP001/production/images/EP001-CHU-WEST-OUTFIT.png` |
| 20 | IMG-MAWUDE-OUTFIT | 馬五德旅裝設定圖 | `episodes/EP001/production/images/EP001-MAWUDE-OUTFIT.png` |
| 21 | IMG-SIKONGXUAN-OUTFIT | 司空玄神農幫主服設定圖 | `episodes/EP001/production/images/EP001-SIKONGXUAN-OUTFIT.png` |
| 22 | IMG-EAST-DISCIPLE-OUTFIT | 東宗弟子服設定圖 | `episodes/EP001/production/images/EP001-EAST-DISCIPLE-OUTFIT.png` |
| 23 | IMG-WULIANG-HALL | 劍湖宮練武廳空鏡 | `episodes/EP001/production/images/EP001-WULIANG-HALL.png` |
| 24 | IMG-HILLSIDE-NIGHT | 劍湖宮外山坡夜景空鏡 | `episodes/EP001/production/images/EP001-HILLSIDE-NIGHT.png` |
| 25 | IMG-SHENNONG-PATH | 神農幫山道夜景空鏡 | `episodes/EP001/production/images/EP001-SHENNONG-PATH.png` |
| 26 | IMG-SHENNONG-CAMP | 神農幫營地夜景空鏡 | `episodes/EP001/production/images/EP001-SHENNONG-CAMP.png` |
| 27 | IMG-DUANYU-FAN | 段譽的摺扇道具圖 | `episodes/EP001/production/images/EP001-DUANYU-FAN.png` |
| 28 | IMG-WULIANG-SWORD | 無量劍佩劍道具圖 | `episodes/EP001/production/images/EP001-WULIANG-SWORD.png` |
| 29 | IMG-MINK-POUCH | 閃電貂皮囊道具圖 | `episodes/EP001/production/images/EP001-MINK-POUCH.png` |
| 30 | IMG-VENOMOUS-SNAKES | 鍾靈的毒蛇道具圖 | `episodes/EP001/production/images/EP001-VENOMOUS-SNAKES.png` |
| 31 | IMG-SHENNONG-LETTER | 神農幫毒信道具圖 | `episodes/EP001/production/images/EP001-SHENNONG-LETTER.png` |
| 32 | IMG-FLOWER-SHOES | 鍾靈的繡花鞋道具圖 | `episodes/EP001/production/images/EP001-FLOWER-SHOES.png` |
| 33 | IMG-SIKONG-MEDICINE | 司空玄的藥瓶道具圖 | `episodes/EP001/production/images/EP001-SIKONG-MEDICINE.png` |
| 34 | IMG-BURNING-HERBS | 燃燒藥草道具圖 | `episodes/EP001/production/images/EP001-BURNING-HERBS.png` |
| 35 | IMG-DUANCHANG-SAN | 斷腸散道具圖 | `episodes/EP001/production/images/EP001-DUANCHANG-SAN.png` |
| 36 | IMG-HANDCUFFS | 鍾靈的手銬道具圖 | `episodes/EP001/production/images/EP001-HANDCUFFS.png` |
| 37 | IMG-BANDAGE | 止血布條道具圖 | `episodes/EP001/production/images/EP001-BANDAGE.png` |

## 批次確認

`CONFIRM BATCH EP001-ASSETS-REMAINING-37 0d3ff8ec7d19`
