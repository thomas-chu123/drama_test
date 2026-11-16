# 七張代表首幀修正結果

## 執行與檢視

- 批次：`EP001-KEYFRAME-REPAIR-PILOT-07`；七項全數技術成功，每項只生成一次。
- 修正版皆為可完整解碼的 768×768 PNG；原圖保留，另存 `-START-FIX01.png`。
- 已逐張開啟原尺寸檢視，本文件為生產後自檢，非獨立審查 verdict。
- 五張有不同程度局部改善，兩張關鍵問題未改善；這不是五張已全部通過。尚未將任何一張自動改綁為正式影片起始幀。

## 原圖與修正版並排

每組左側 B01 為原圖，右側 FIX01 為本輪修正版。

- [006、011、025 比對](../episodes/EP001/production/contact-sheets/keyframe-repair-pilot-01.jpg)
- [030、032 比對](../episodes/EP001/production/contact-sheets/keyframe-repair-pilot-02.jpg)
- [033、037 比對](../episodes/EP001/production/contact-sheets/keyframe-repair-pilot-03.jpg)

## 逐鏡結果

| 鏡頭 | 自檢狀態 | 可見結果 | 修正版 |
| --- | --- | --- | --- |
| 006 | 局部改善，仍待驗收 | 已補出抬掌且掌未碰臉；掌心朝向、解剖左右手與手指需確認，臉型及背景保留。 | [原圖](../episodes/EP001/production/images/EP001-SHOT006-START-FIX01.png) |
| 011 | 局部改善，仍需修正 | 四位人物已齊，蛇纏腕與肩上青蛇部分呈現；劍仍非半出鞘，梁上鍾靈比例仍小，需核對皮囊手勢。 | [原圖](../episodes/EP001/production/images/EP001-SHOT011-START-FIX01.png) |
| 025 | 關鍵問題未改善 | 右側青衫段譽與鍾靈分身仍在，沒有改成兩名幫眾，五人總數並不能證明身份數量正確。 | [原圖](../episodes/EP001/production/images/EP001-SHOT025-START-FIX01.png) |
| 030 | 不可採用，仍需修正 | 第三人的頭雖消失，身體與衣服仍留土中；兩位主角仍露肩胸且未閉眼，未達土埋至頸邊的要求。 | [原圖](../episodes/EP001/production/images/EP001-SHOT030-START-FIX01.png) |
| 032 | 局部改善，仍需修正 | 側邊新增持布與遞刀的幫眾，但前臂仍有纏繞材質，司空玄仍握白色物件，未完成斬臂前去包紮狀態。 | [原圖](../episodes/EP001/production/images/EP001-SHOT032-START-FIX01.png) |
| 033 | 關鍵問題未改善 | 段譽、鍾靈仍站在地面，未埋至頸邊；司空玄右臂殘端包紮不清楚，不符合本鏡起點。 | [原圖](../episodes/EP001/production/images/EP001-SHOT033-START-FIX01.png) |
| 037 | 主要指定問題改善，仍待驗收 | 鍾靈已赤足，鞋只留段譽手中；鍾靈腕銬保留，段譽大部分腕銬已移除，但近側手腕仍有環狀細節，視線也未明確落在腳尖。 | [原圖](../episodes/EP001/production/images/EP001-SHOT037-START-FIX01.png) |

## 方法判斷與剩餘工作

- 小範圍新增起手、補人物或改鞋子可見改善；不能因此推論刪除分身、提高覆土或重排多人畫面也同樣可靠。
- 以同一失敗底圖做全圖文字編輯，仍可能沿用原本人物位置與身體；第 030 鏡顯示移除局部還會留下錯誤殘部。
- 暫停把相同全圖文字修法直接擴大到其餘鏡頭。下一步應先驗證可限制修改區域的遮罩編輯或分層重建，再建立新的批次；目前 adapter 尚未接入遮罩輸入，不能宣稱已能直接執行。
- 首幀修正整體仍未完成：需處理本輪未通過內容及 EP001-KEYFRAME-REPAIR-PLAN.md 所列其他鏡頭。
- 未自動追加重跑，未生成影片。後續變更生成方法或參考圖時重新整批預覽確認。
