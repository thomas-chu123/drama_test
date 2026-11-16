# EP001 三十七張首幀產出與自檢

## 技術執行結果

- 批次：`EP001-KEYFRAMES-REMAINING-37`；37 個任務全數成功，每鏡僅生成一次，未自動重跑。
- 新增 37 個 PNG，均為 768×768，已完整解碼檢查；第二鏡既有圖保留。現有首幀共 38 張。
- 任務平均 10.1 秒，首項開始至末項完成約 8.4 分鐘，含分段執行與檢視間隔。
- 使用 Qwen Image 2.1 Turbo，每鏡 1–7 張參考，參考圖解析度參數 512、8 步固定 sigma、種子 42。多圖實跑技術流程已通過。

## 內容自檢限制

本文件為生產後縮圖自檢，非獨立審查 verdict。已檢視全部分類縮圖，並抽看首批原圖；不能把技術成功當成 37 張都可正式投產。多張仍有構圖、肢體、人物數量、埋土高度與傷勢連戲偏差，須集中修正或選擇可接受的候選。尚未將候選圖自動改綁為下游正式影片起始幀，也未生成新影片。

## 分類縮圖

- [第一至十鏡](../episodes/EP001/production/contact-sheets/keyframes-001-010.jpg)
- [第十一至二十鏡](../episodes/EP001/production/contact-sheets/keyframes-011-020.jpg)
- [第二十一至三十鏡](../episodes/EP001/production/contact-sheets/keyframes-021-030.jpg)
- [第三十一至三十八鏡](../episodes/EP001/production/contact-sheets/keyframes-031-038.jpg)

## 逐鏡觀察

| 鏡頭 | 名稱 | 可見問題或待核對項 | 圖片 |
| --- | --- | --- | --- |
| SHOT-EP001-001 | 敗者退場 | 兩人落位與座椅交疊，腳部有踩到椅面的疑慮；褚姓弟子未明確以劍支撐，龔光傑半出鞘狀態不符。 | [原圖](../episodes/EP001/production/images/EP001-SHOT001-START.png) |
| SHOT-EP001-002 | 笑聲引視 | 既有介面試拍圖，本批未重畫；保留已知左右手與合扇狀態差異。 | [原圖](../episodes/EP001/production/images/EP001-SHOT002-START.png) |
| SHOT-EP001-003 | 掌門點名 | 過肩雙人構圖有呈現，左子穆未捻鬚；作為影片起手是否可接受需另確認。 | [原圖](../episodes/EP001/production/images/EP001-SHOT003-START.png) |
| SHOT-EP001-004 | 段譽拒比 | 人物朝向偏正面，沒有作揖，與面朝畫右的起點不同。 | [原圖](../episodes/EP001/production/images/EP001-SHOT004-START.png) |
| SHOT-EP001-005 | 劍尖抵胸 | 雙人與持劍關係有呈現；需放大核對劍尖是否落在胸前衣料，站位與手部接觸尚未定稿。 | [原圖](../episodes/EP001/production/images/EP001-SHOT005-START.png) |
| SHOT-EP001-006 | 當眾掌摑 | 龔光傑未抬掌，掌摑前起手缺失。 | [原圖](../episodes/EP001/production/images/EP001-SHOT006-START.png) |
| SHOT-EP001-007 | 摔落與扶起 | 抓衣襟變成扶肩，馬五德仍坐著；掌印亦不明顯。 | [原圖](../episodes/EP001/production/images/EP001-SHOT007-START.png) |
| SHOT-EP001-008 | 拳頭逼近 | 攔路關係有呈現，但段譽未明確朝廳門，左臉掌印不明顯，景別與起手需核對。 | [原圖](../episodes/EP001/production/images/EP001-SHOT008-START.png) |
| SHOT-EP001-009 | 赤蛇制腕 | 原定手腕近景變成上半身，蛇在肩上；應為梁上蛇頭接近拳頭、尚未碰腕。 | [原圖](../episodes/EP001/production/images/EP001-SHOT009-START.png) |
| SHOT-EP001-010 | 梁上少女現身 | 鍾靈未明確坐在高處木梁，較像座席；需要重建高度與仰拍關係。 | [原圖](../episodes/EP001/production/images/EP001-SHOT010-START.png) |
| SHOT-EP001-011 | 斬蛇與放貂 | 漏掉龔光傑與攔路弟子等主體，蛇纏腕與背上青蛇未建立；梁上人物比例過小。 | [原圖](../episodes/EP001/production/images/EP001-SHOT011-START.png) |
| SHOT-EP001-012 | 劍光擦臉 | 小貂落肩可見，但左子穆劍尖不在龔光傑臉側；小貂姿態與尺度需核對。 | [原圖](../episodes/EP001/production/images/EP001-SHOT012-START.png) |
| SHOT-EP001-013 | 遺體撞入 | 容子矩身份、門檻與尚未碰撞關係未建立，人物與座椅有不自然落位。 | [原圖](../episodes/EP001/production/images/EP001-SHOT013-START.png) |
| SHOT-EP001-014 | 胸口毒字 | 胸口特寫變為全身俯拍，指定毒字無法完整清楚辨認，不能作文字揭曉鏡。 | [原圖](../episodes/EP001/production/images/EP001-SHOT014-START.png) |
| SHOT-EP001-015 | 毒信發作 | 持信雙人關係有呈現；信封與摺疊信箋是否分件、頸側抓痕仍需放大核對。 | [原圖](../episodes/EP001/production/images/EP001-SHOT015-START.png) |
| SHOT-EP001-016 | 鍾靈報毒 | 梁上鍾靈與下方左子穆的高度關係有呈現；瓜子、持物與視線需放大核對。 | [原圖](../episodes/EP001/production/images/EP001-SHOT016-START.png) |
| SHOT-EP001-017 | 山道被封 | 鍾靈落在地面而非高梁，報信者位置與人物比例不符。 | [原圖](../episodes/EP001/production/images/EP001-SHOT017-START.png) |
| SHOT-EP001-018 | 貂咬右腕 | 三人與小貂可見，但挽臂關係、掌印與握劍狀態不明確；需核對影片起手。 | [原圖](../episodes/EP001/production/images/EP001-SHOT018-START.png) |
| SHOT-EP001-019 | 夜坡青煙 | 兩人面對面，未共同朝山下遠煙；掌印不明顯。 | [原圖](../episodes/EP001/production/images/EP001-SHOT019-START.png) |
| SHOT-EP001-020 | 試招摔倒 | 扣肩關係部分呈現，但近腳踝的試招站位、掌印與腳步需核對。 | [原圖](../episodes/EP001/production/images/EP001-SHOT020-START.png) |
| SHOT-EP001-021 | 手帕與道歉 | 手帕停在手腕附近，而不是覆鼻手外；鼻血、擦傷與動作焦點不足。 | [原圖](../episodes/EP001/production/images/EP001-SHOT021-START.png) |
| SHOT-EP001-022 | 決意同行 | 一前一後站位部分呈現，需核對面朝下坡方向及左臉、額角傷勢。 | [原圖](../episodes/EP001/production/images/EP001-SHOT022-START.png) |
| SHOT-EP001-023 | 山道盤問 | 只見一名守衛，未符合兩名守衛持短刀攔路；畫面有另一人物的遠處輪廓，需核對實際數量。 | [原圖](../episodes/EP001/production/images/EP001-SHOT023-START.png) |
| SHOT-EP001-024 | 引入營地 | 人物偏並排面向鏡頭，沒有建立一留守、一引路及來客尚未跟上的關係。 | [原圖](../episodes/EP001/production/images/EP001-SHOT024-START.png) |
| SHOT-EP001-025 | 幫主高坐 | 段譽與鍾靈出現重複人物，高岩坐席及兩側幫眾位置不符。 | [原圖](../episodes/EP001/production/images/EP001-SHOT025-START.png) |
| SHOT-EP001-026 | 反剪擒人 | 段譽背後幫眾關係部分呈現，但司空玄未坐高岩，需核對雙手仍自由的狀態。 | [原圖](../episodes/EP001/production/images/EP001-SHOT026-START.png) |
| SHOT-EP001-027 | 貂襲圍攻 | 高個老者沿用坐倒姿勢，未伸手接近鍾靈肩；段譽重複，反剪與貂頭露囊關係未建立。 | [原圖](../episodes/EP001/production/images/EP001-SHOT027-START.png) |
| SHOT-EP001-028 | 藥瓶逼退 | 持瓶、段譽與小貂可見；持瓶手、右掌、無咬傷及小貂伏地姿態需核對。 | [原圖](../episodes/EP001/production/images/EP001-SHOT028-START.png) |
| SHOT-EP001-029 | 藥煙昏迷 | 段譽倒地與外圍持藥草人物部分呈現，但倒地位置與前景火堆交疊，人物空間安全距離需修正。 | [原圖](../episodes/EP001/production/images/EP001-SHOT029-START.png) |
| SHOT-EP001-030 | 埋至頸邊 | 土坑中多出第三人，兩位主角仍露肩胸，未埋至頸邊，且未閉眼。 | [原圖](../episodes/EP001/production/images/EP001-SHOT030-START.png) |
| SHOT-EP001-031 | 閃電貂反咬 | 兩位主角未埋在土裡，露出身體，與起點不符。 | [原圖](../episodes/EP001/production/images/EP001-SHOT031-START.png) |
| SHOT-EP001-032 | 斬臂止毒 | 提早出現前臂包紮，缺少遞刀與持未用布條的幫眾。 | [原圖](../episodes/EP001/production/images/EP001-SHOT032-START.png) |
| SHOT-EP001-033 | 七日之限 | 主角站在地面，未只露埋土頭臉；司空玄右臂缺失與包紮需重新核對。 | [原圖](../episodes/EP001/production/images/EP001-SHOT033-START.png) |
| SHOT-EP001-034 | 吞下毒藥 | 段譽露出上身而非埋至頸邊；捏下頜與紅藥末尚未入口的起手需修正。 | [原圖](../episodes/EP001/production/images/EP001-SHOT034-START.png) |
| SHOT-EP001-035 | 交易成立 | 主角仍露肩胸，未埋至頸邊；司空玄手臂狀態與兩人間距需校正。 | [原圖](../episodes/EP001/production/images/EP001-SHOT035-START.png) |
| SHOT-EP001-036 | 花鞋作信物 | 半開土坑、段譽蹲姿與鍾靈仍穿花鞋部分呈現；腕銬、雙手空置與火堆距離需放大核對。 | [原圖](../episodes/EP001/production/images/EP001-SHOT036-START.png) |
| SHOT-EP001-037 | 記路與叮囑 | 鍾靈仍穿花鞋，同時段譽又持一雙鞋，違反交鞋後赤足連戲；腕銬不明確。 | [原圖](../episodes/EP001/production/images/EP001-SHOT037-START.png) |
| SHOT-EP001-038 | 七日啟程 | 段譽持鞋與鍾靈赤足坐坑部分呈現，但腕銬、身體朝向與鞋子數量需核對。 | [原圖](../episodes/EP001/production/images/EP001-SHOT038-START.png) |

## 後續分流

- 優先處理漏人／重複人物、起手缺失、埋土與斬臂時序、交鞋後赤足，以及胸口毒字特寫；這些會直接影響後續影片敘事。
- 同一問題若在多鏡反覆出現，先挑代表鏡頭改用更精簡的姿態描述、構圖參考或局部修圖，驗證有效後再擴大，不直接把全部鏡頭重抽一次。
- 通過內容確認後才同步更新分鏡與影片提示詞中的起始幀 REF。改版另存檔，依批次預覽確認後生成，不覆蓋既有候選。
- 正式有對白影片仍依 TODO.md 先處理角色聲音定型與聲音路線。
