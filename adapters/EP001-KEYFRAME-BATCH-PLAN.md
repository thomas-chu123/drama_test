# EP001 剩餘三十七張首幀批次

- 範圍：第一鏡、第三至第三十八鏡，共 37 張；第二鏡原圖保留。
- Qwen Image 2.1 Turbo 多圖參考、768×768、既有 8 步固定 sigma、種子 42。參考圖解析度參數為 512，降低多圖輸入負擔；實際縮放按節點保留比例處理。
- 一次整批確認後循序執行，每鏡先產一張候選，不自動追加重跑。
- 每鏡綁定 1–7 張實際參考，確切張數見清單。人物只鎖外貌衣著，起手、傷勢、埋土與肢體狀態以本鏡首幀文字為準。
- 不沿用未修好的藥瓶與鐵銬形制圖，也不沿用帶門樓的山道空鏡；改用本鏡文字指定形制與自然山路，不能保證模型必然遵循。
- 已改善的高個老者、去帳篷營地、合扇與花鞋採 FIX01 版本。
- 既有人物年齡、司空玄的狀態板、群像辨識、文字生成與複雜多人站位仍有風險，產出須檢視；不把候選參考當成已正式定稿。
- 營地多人鏡、埋土鏡與胸口可讀毒字鏡為重點檢查，不因一次不理想而自動無限重跑。
- 多圖參考目前僅完成離線接線與本機節點規格查驗，尚無多人鏡頭實跑品質結論。
- 預估純生成約 15–35 分鐘（暫估，多圖可能高於單圖）；另留約 20–40 分鐘檢視與整理，待首批實測後更新。

| 鏡頭 | 名稱 | 參考數 | 輸出 |
| --- | --- | --- | --- |
| SHOT-EP001-001 | 敗者退場 | 4 | `episodes/EP001/production/images/EP001-SHOT001-START.png` |
| SHOT-EP001-003 | 掌門點名 | 3 | `episodes/EP001/production/images/EP001-SHOT003-START.png` |
| SHOT-EP001-004 | 段譽拒比 | 3 | `episodes/EP001/production/images/EP001-SHOT004-START.png` |
| SHOT-EP001-005 | 劍尖抵胸 | 4 | `episodes/EP001/production/images/EP001-SHOT005-START.png` |
| SHOT-EP001-006 | 當眾掌摑 | 3 | `episodes/EP001/production/images/EP001-SHOT006-START.png` |
| SHOT-EP001-007 | 摔落與扶起 | 4 | `episodes/EP001/production/images/EP001-SHOT007-START.png` |
| SHOT-EP001-008 | 拳頭逼近 | 3 | `episodes/EP001/production/images/EP001-SHOT008-START.png` |
| SHOT-EP001-009 | 赤蛇制腕 | 2 | `episodes/EP001/production/images/EP001-SHOT009-START.png` |
| SHOT-EP001-010 | 梁上少女現身 | 3 | `episodes/EP001/production/images/EP001-SHOT010-START.png` |
| SHOT-EP001-011 | 斬蛇與放貂 | 7 | `episodes/EP001/production/images/EP001-SHOT011-START.png` |
| SHOT-EP001-012 | 劍光擦臉 | 5 | `episodes/EP001/production/images/EP001-SHOT012-START.png` |
| SHOT-EP001-013 | 遺體撞入 | 4 | `episodes/EP001/production/images/EP001-SHOT013-START.png` |
| SHOT-EP001-014 | 胸口毒字 | 1 | `episodes/EP001/production/images/EP001-SHOT014-START.png` |
| SHOT-EP001-015 | 毒信發作 | 4 | `episodes/EP001/production/images/EP001-SHOT015-START.png` |
| SHOT-EP001-016 | 鍾靈報毒 | 3 | `episodes/EP001/production/images/EP001-SHOT016-START.png` |
| SHOT-EP001-017 | 山道被封 | 4 | `episodes/EP001/production/images/EP001-SHOT017-START.png` |
| SHOT-EP001-018 | 貂咬右腕 | 6 | `episodes/EP001/production/images/EP001-SHOT018-START.png` |
| SHOT-EP001-019 | 夜坡青煙 | 3 | `episodes/EP001/production/images/EP001-SHOT019-START.png` |
| SHOT-EP001-020 | 試招摔倒 | 3 | `episodes/EP001/production/images/EP001-SHOT020-START.png` |
| SHOT-EP001-021 | 手帕與道歉 | 3 | `episodes/EP001/production/images/EP001-SHOT021-START.png` |
| SHOT-EP001-022 | 決意同行 | 3 | `episodes/EP001/production/images/EP001-SHOT022-START.png` |
| SHOT-EP001-023 | 山道盤問 | 3 | `episodes/EP001/production/images/EP001-SHOT023-START.png` |
| SHOT-EP001-024 | 引入營地 | 3 | `episodes/EP001/production/images/EP001-SHOT024-START.png` |
| SHOT-EP001-025 | 幫主高坐 | 5 | `episodes/EP001/production/images/EP001-SHOT025-START.png` |
| SHOT-EP001-026 | 反剪擒人 | 5 | `episodes/EP001/production/images/EP001-SHOT026-START.png` |
| SHOT-EP001-027 | 貂襲圍攻 | 6 | `episodes/EP001/production/images/EP001-SHOT027-START.png` |
| SHOT-EP001-028 | 藥瓶逼退 | 5 | `episodes/EP001/production/images/EP001-SHOT028-START.png` |
| SHOT-EP001-029 | 藥煙昏迷 | 5 | `episodes/EP001/production/images/EP001-SHOT029-START.png` |
| SHOT-EP001-030 | 埋至頸邊 | 4 | `episodes/EP001/production/images/EP001-SHOT030-START.png` |
| SHOT-EP001-031 | 閃電貂反咬 | 5 | `episodes/EP001/production/images/EP001-SHOT031-START.png` |
| SHOT-EP001-032 | 斬臂止毒 | 4 | `episodes/EP001/production/images/EP001-SHOT032-START.png` |
| SHOT-EP001-033 | 七日之限 | 6 | `episodes/EP001/production/images/EP001-SHOT033-START.png` |
| SHOT-EP001-034 | 吞下毒藥 | 2 | `episodes/EP001/production/images/EP001-SHOT034-START.png` |
| SHOT-EP001-035 | 交易成立 | 5 | `episodes/EP001/production/images/EP001-SHOT035-START.png` |
| SHOT-EP001-036 | 花鞋作信物 | 4 | `episodes/EP001/production/images/EP001-SHOT036-START.png` |
| SHOT-EP001-037 | 記路與叮囑 | 4 | `episodes/EP001/production/images/EP001-SHOT037-START.png` |
| SHOT-EP001-038 | 七日啟程 | 4 | `episodes/EP001/production/images/EP001-SHOT038-START.png` |

## 整批確認

`CONFIRM BATCH EP001-KEYFRAMES-REMAINING-37 80b7bae9cbdd`
