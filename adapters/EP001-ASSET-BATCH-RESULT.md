# EP001 設定圖批次產出與自檢

## 執行結果

- 批次：`EP001-ASSETS-REMAINING-37`；37 個任務全部成功，每項僅生成一次。
- 全部 37 個 PNG 均可完整解碼，尺寸皆為 1024×1024。
- 任務平均 14.6 秒；包含程序中斷回收與人工操作間隔，首項開始至末項完成約 10.7 分鐘。
- 兩次本機批次程序中斷後，使用 collect 回收原遠端任務，沒有重複生成；之後以同批確認下的小段循序執行完成。
- 未重出既有段譽圖與第二鏡首幀；未生成其他 37 張首幀，也未將本批候選圖自動綁入正式創作文件。

## 檢視範圍與限制

本文件是生產後自檢，非獨立審查 verdict。已按四張分類縮圖檢視全部圖片並標註可見問題；未逐張做完整放大審稿，未標註者不代表正式定稿。文字可讀性、手部細節與人物年齡仍需個別確認。

- [人物、動物與群像縮圖](../episodes/EP001/production/contact-sheets/characters.jpg)
- [服裝縮圖](../episodes/EP001/production/contact-sheets/outfits.jpg)
- [場景縮圖](../episodes/EP001/production/contact-sheets/scenes.jpg)
- [道具縮圖](../episodes/EP001/production/contact-sheets/props.jpg)

## 下一步

先集中修正角色身份／傷勢、現代元素與持物狀態，再選定可用圖片綁定首幀參考。不能只憑檔案生成成功就把錯誤延續到 37 個首幀。修正任務可一次整批預覽確認；本次不自動重跑。多人首幀仍需補齊編輯 adapter 的多圖參考支援。

## 圖片自檢清單

| 條目 | 名稱 | 縮圖觀察與建議 | 原圖 |
| --- | --- | --- | --- |
| IMG-ZHONGLING-CHARACTER | 鍾靈人物設定圖 | 外觀偏幼，鞋底近現代運動鞋；作為十六歲上下少女與古裝造型參考前需調整。 | [原圖](../episodes/EP001/production/images/EP001-ZHONGLING-CHARACTER.png) |
| IMG-ZUOZIMU-CHARACTER | 左子穆人物設定圖 | 年齡與長鬚的呈現較設定年輕、短，需核對人物造型意圖。 | [原圖](../episodes/EP001/production/images/EP001-ZUOZIMU-CHARACTER.png) |
| IMG-XINSHUANGQING-CHARACTER | 辛雙清人物設定圖 | 縮圖未見上述明顯問題，仍待放大與創作者確認。 | [原圖](../episodes/EP001/production/images/EP001-XINSHUANGQING-CHARACTER.png) |
| IMG-GONGGUANGJIE-CHARACTER | 龔光傑人物設定圖 | 縮圖未見上述明顯問題，仍待放大與創作者確認。 | [原圖](../episodes/EP001/production/images/EP001-GONGGUANGJIE-CHARACTER.png) |
| IMG-CHU-DISCIPLE-CHARACTER | 褚姓弟子人物設定圖 | 縮圖未見上述明顯問題，仍待放大與創作者確認。 | [原圖](../episodes/EP001/production/images/EP001-CHU-DISCIPLE-CHARACTER.png) |
| IMG-MAWUDE-CHARACTER | 馬五德人物設定圖 | 縮圖未見上述明顯問題，仍待放大與創作者確認。 | [原圖](../episodes/EP001/production/images/EP001-MAWUDE-CHARACTER.png) |
| IMG-MINK-CHARACTER | 閃電貂動物設定圖 | 三個視圖以直立姿態為主，側面資訊不足，兩個背部視圖相近；四足動態參考有限。 | [原圖](../episodes/EP001/production/images/EP001-MINK-CHARACTER.png) |
| IMG-RONGZIJU-CHARACTER | 容子矩人物狀態圖 | 胸口字跡不能確認符合指定全文，需放大逐字核對或後期製作；不可當作文字特寫定稿。 | [原圖](../episodes/EP001/production/images/EP001-RONGZIJU-CHARACTER.png) |
| IMG-SIKONGXUAN-CHARACTER | 司空玄人物傷勢設定圖 | 頭頂與下半身被裁切；可見包紮前臂與手部，未清楚呈現右臂已截去、寬袖垂落的設定，不可作該傷勢定稿。 | [原圖](../episodes/EP001/production/images/EP001-SIKONGXUAN-CHARACTER.png) |
| IMG-TALL-ELDER-CHARACTER | 神農幫高個老者人物狀態圖 | 年長高個男子被生成為年輕女性，角色身份明顯不符，暫不綁定首幀。 | [原圖](../episodes/EP001/production/images/EP001-TALL-ELDER-CHARACTER.png) |
| IMG-SHENNONG-GUARD | 神農幫守道幫眾人物設定圖 | 縮圖未見上述明顯問題，仍待放大與創作者確認。 | [原圖](../episodes/EP001/production/images/EP001-SHENNONG-GUARD.png) |
| IMG-SHENNONG-GROUP | 神農幫幫眾群像設定圖 | 三人臉型、髮型高度相似，群像區分不足，需避免當作三個穩定身份。 | [原圖](../episodes/EP001/production/images/EP001-SHENNONG-GROUP.png) |
| IMG-EAST-DISCIPLE | 東宗攔路弟子人物設定圖 | 縮圖未見上述明顯問題，仍待放大與創作者確認。 | [原圖](../episodes/EP001/production/images/EP001-EAST-DISCIPLE.png) |
| IMG-DUANYU-OUTFIT | 段譽青衫造型設定圖 | 縮圖未見上述明顯問題，仍待放大與創作者確認。 | [原圖](../episodes/EP001/production/images/EP001-DUANYU-OUTFIT.png) |
| IMG-ZHONGLING-OUTFIT | 鍾靈青衫造型設定圖 | 鞋型帶現代感，且服裝顏色與人物候選圖有差異，需選定同一版後統一。 | [原圖](../episodes/EP001/production/images/EP001-ZHONGLING-OUTFIT.png) |
| IMG-ZUOZIMU-OUTFIT | 左子穆掌門長袍設定圖 | 縮圖未見上述明顯問題，仍待放大與創作者確認。 | [原圖](../episodes/EP001/production/images/EP001-ZUOZIMU-OUTFIT.png) |
| IMG-XINSHUANGQING-OUTFIT | 辛雙清道姑常服設定圖 | 縮圖未見上述明顯問題，仍待放大與創作者確認。 | [原圖](../episodes/EP001/production/images/EP001-XINSHUANGQING-OUTFIT.png) |
| IMG-GONGGUANGJIE-OUTFIT | 龔光傑東宗弟子服設定圖 | 原要求服裝圖不含長劍，結果加入持劍人物與手部；只宜裁取服裝局部或修正後使用。 | [原圖](../episodes/EP001/production/images/EP001-GONGGUANGJIE-OUTFIT.png) |
| IMG-CHU-WEST-OUTFIT | 褚姓弟子西宗弟子服設定圖 | 服裝展示仍帶人物手部；需避免將多餘人體資訊當作角色身份參考。 | [原圖](../episodes/EP001/production/images/EP001-CHU-WEST-OUTFIT.png) |
| IMG-MAWUDE-OUTFIT | 馬五德旅裝設定圖 | 縮圖未見上述明顯問題，仍待放大與創作者確認。 | [原圖](../episodes/EP001/production/images/EP001-MAWUDE-OUTFIT.png) |
| IMG-SIKONGXUAN-OUTFIT | 司空玄神農幫主服設定圖 | 採有頭部與手部的裁切人物展示；不適合作為純服裝、完整全身板直接沿用。 | [原圖](../episodes/EP001/production/images/EP001-SIKONGXUAN-OUTFIT.png) |
| IMG-EAST-DISCIPLE-OUTFIT | 東宗弟子服設定圖 | 縮圖未見上述明顯問題，仍待放大與創作者確認。 | [原圖](../episodes/EP001/production/images/EP001-EAST-DISCIPLE-OUTFIT.png) |
| IMG-WULIANG-HALL | 劍湖宮練武廳空鏡 | 畫面偏正對空場，兩宗席位與外客座席的相對方位不夠清楚；需核對站位後再當空間參考。 | [原圖](../episodes/EP001/production/images/EP001-WULIANG-HALL.png) |
| IMG-HILLSIDE-NIGHT | 劍湖宮外山坡夜景空鏡 | 路面帶現代整平礫石路觀感，月亮與前景亮度需配合既定夜景風格核對。 | [原圖](../episodes/EP001/production/images/EP001-HILLSIDE-NIGHT.png) |
| IMG-SHENNONG-PATH | 神農幫山道夜景空鏡 | 新增了提示詞排除的門樓與拱門，暫不作山道首幀空間定稿。 | [原圖](../episodes/EP001/production/images/EP001-SHENNONG-PATH.png) |
| IMG-SHENNONG-CAMP | 神農幫營地夜景空鏡 | 出現現代帳篷，土坑與高岩坐席辨識不足，與禁止帳篷及營地佈局要求不符。 | [原圖](../episodes/EP001/production/images/EP001-SHENNONG-CAMP.png) |
| IMG-DUANYU-FAN | 段譽的摺扇道具圖 | 合起的摺扇被畫成完全展開，不能用於本集要求的合扇持物連戲。 | [原圖](../episodes/EP001/production/images/EP001-DUANYU-FAN.png) |
| IMG-WULIANG-SWORD | 無量劍佩劍道具圖 | 多出有刻度直尺，劍的長度與尺寸參照需重新核對；不宜直接沿用整張。 | [原圖](../episodes/EP001/production/images/EP001-WULIANG-SWORD.png) |
| IMG-MINK-POUCH | 閃電貂皮囊道具圖 | 皮囊帶現代金屬雞眼、五金與徽記感裝飾，需簡化為古裝軟皮囊。 | [原圖](../episodes/EP001/production/images/EP001-MINK-POUCH.png) |
| IMG-VENOMOUS-SNAKES | 鍾靈的毒蛇道具圖 | 多出竹編容器邊緣，未見明確赤練蛇配色；需依鏡頭可見需求選用或修正。 | [原圖](../episodes/EP001/production/images/EP001-VENOMOUS-SNAKES.png) |
| IMG-SHENNONG-LETTER | 神農幫毒信道具圖 | 只見空白展開紙件，信箋與信封分件及書信行列資訊不足，需依實際持物鏡確認。 | [原圖](../episodes/EP001/production/images/EP001-SHENNONG-LETTER.png) |
| IMG-FLOWER-SHOES | 鍾靈的繡花鞋道具圖 | 出現扣帶、鞋扣與厚白底，與無鞋扣古式布鞋設定不符；須與人物鞋型一起統一。 | [原圖](../episodes/EP001/production/images/EP001-FLOWER-SHOES.png) |
| IMG-SIKONG-MEDICINE | 司空玄的藥瓶道具圖 | 現代螺紋塑膠瓶蓋，且多出手掌；不符合古裝塞蓋、無手的道具圖要求。 | [原圖](../episodes/EP001/production/images/EP001-SIKONG-MEDICINE.png) |
| IMG-BURNING-HERBS | 燃燒藥草道具圖 | 燃燒一欄接近線香束，煙量不明顯，需修正為藥草燃燒的形態。 | [原圖](../episodes/EP001/production/images/EP001-BURNING-HERBS.png) |
| IMG-DUANCHANG-SAN | 斷腸散道具圖 | 藥瓶有現代螺紋瓶口，需與藥瓶造型一併統一。 | [原圖](../episodes/EP001/production/images/EP001-DUANCHANG-SAN.png) |
| IMG-HANDCUFFS | 鍾靈的手銬道具圖 | 現代警用手銬輪廓與機械結構明顯，未符合簡單手工鍛打古式鐵銬。 | [原圖](../episodes/EP001/production/images/EP001-HANDCUFFS.png) |
| IMG-BANDAGE | 止血布條道具圖 | 縮圖未見上述明顯問題，仍待放大與創作者確認。 | [原圖](../episodes/EP001/production/images/EP001-BANDAGE.png) |
