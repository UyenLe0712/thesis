// Build deck v5 — HỌC THUẬT TỐI GIẢN + HÌNH MINH HOẠ.
// Khung mới: ĐA BƯỚC = SẮP THỨ TỰ MÀN (Screen-Ordering). Bỏ hẳn Tier B/observability gap/k*.
// Tiêu đề serif (Cambria), thân Segoe UI (đều hỗ trợ tiếng Việt). 1 màu nhấn kín đáo.
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.author = "Luan van thac si";
pres.title = "Sinh tu dong huong dan su dung phan mem (Screen-Ordering)";

const TF = "Cambria";   // title (serif, học thuật)
const BF = "Segoe UI";  // body
const INK = "1C2530", BODY = "3C434B", MUTE = "8A929B", ACCENT = "8A2433"; // burgundy nhấn
const STEEL = "5B6B7A";
const RULE = "D7DCE1", FILL = "F4F6F8", WHITE = "FFFFFF", HILO = "F2E3E6";
const W = 13.33, H = 7.5, M = 0.8;
let PAGE = 1;
let s;

function base(kicker, title) {
  s = pres.addSlide(); s.background = { color: WHITE };
  s.addText(kicker.toUpperCase(), { x: M, y: 0.55, w: W - 2 * M, h: 0.3, fontFace: BF, fontSize: 11.5, bold: true, color: ACCENT, charSpacing: 3, margin: 0 });
  s.addText(title, { x: M, y: 0.86, w: W - 2 * M, h: 0.8, fontFace: TF, fontSize: 27, bold: true, color: INK, margin: 0 });
}
function pageNum() { PAGE++; s.addText(String(PAGE).padStart(2, "0"), { x: W - 1.1, y: H - 0.48, w: 0.7, h: 0.3, fontFace: BF, fontSize: 10, color: MUTE, align: "right" }); }
function vrule(x, y, h, color) { s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.05, h, fill: { color: color || ACCENT }, line: { type: "none" } }); }
function note(y, text) { s.addText(text, { x: M, y, w: W - 2 * M, h: 0.5, fontFace: BF, fontSize: 13, italic: true, color: MUTE, lineSpacingMultiple: 1.05, margin: 0 }); }
function arrow(x, y, w, h, color) { s.addShape(pres.shapes.LINE, { x, y, w, h, line: { color: color || ACCENT, width: 2.25, endArrowType: "triangle", beginArrowType: "none" } }); }

// mockup "màn hình điện thoại": title bar + vài dòng nội dung; dòng `hi` được tô nhấn.
function phone(x, y, w, h, bar, rows, hi, badge, badgeColor) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.06, fill: { color: WHITE }, line: { color: "B9C0C8", width: 1 } });
  s.addShape(pres.shapes.RECTANGLE, { x: x + 0.07, y: y + 0.08, w: w - 0.14, h: 0.22, fill: { color: FILL }, line: { type: "none" } });
  s.addText(bar, { x: x + 0.11, y: y + 0.08, w: w - 0.22, h: 0.22, fontFace: BF, fontSize: 8, bold: true, color: BODY, margin: 0, valign: "middle" });
  let ly = y + 0.4;
  rows.forEach((r, i) => {
    const on = (i === hi);
    s.addShape(pres.shapes.RECTANGLE, { x: x + 0.1, y: ly, w: w - 0.2, h: 0.27, fill: { color: on ? HILO : WHITE }, line: { color: on ? ACCENT : "DCE1E6", width: on ? 1 : 0.5 } });
    s.addText(r, { x: x + 0.17, y: ly, w: w - 0.32, h: 0.27, fontFace: BF, fontSize: 8, color: on ? ACCENT : BODY, bold: on, margin: 0, valign: "middle" });
    ly += 0.33;
  });
  if (badge) {
    s.addShape(pres.shapes.OVAL, { x: x + w - 0.36, y: y - 0.17, w: 0.36, h: 0.36, fill: { color: badgeColor || ACCENT }, line: { color: WHITE, width: 1.5 } });
    s.addText(badge, { x: x + w - 0.36, y: y - 0.17, w: 0.36, h: 0.36, align: "center", valign: "middle", fontFace: BF, fontSize: 12, bold: true, color: WHITE, margin: 0 });
  }
}

// ===== S1 TITLE =====
s = pres.addSlide(); s.background = { color: WHITE };
s.addShape(pres.shapes.RECTANGLE, { x: M, y: 1.85, w: 0.9, h: 0.08, fill: { color: ACCENT }, line: { type: "none" } });
s.addText("ĐỀ CƯƠNG LUẬN VĂN THẠC SĨ", { x: M, y: 2.1, w: 11, h: 0.4, fontFace: BF, fontSize: 13, bold: true, color: ACCENT, charSpacing: 3 });
s.addText("Sinh tự động hướng dẫn sử dụng phần mềm\ntừ ảnh màn hình + câu hỏi", { x: M - 0.02, y: 2.55, w: 11.8, h: 1.7, fontFace: TF, fontSize: 36, bold: true, color: INK, lineSpacingMultiple: 1.05 });
s.addText("và đánh giá khi không có bản hướng dẫn mẫu", { x: M, y: 4.35, w: 11, h: 0.5, fontFace: TF, fontSize: 20, italic: true, color: BODY });
s.addText("Mạch trình bày:  Bài toán → Dữ liệu → Đa bước (sắp thứ tự màn) → Pipeline → Cách chấm → Khả thi", { x: M, y: 5.2, w: 11.6, h: 0.4, fontFace: BF, fontSize: 13.5, color: MUTE });
s.addText("Học viên: ………………       GVHD: ………………       2026", { x: M, y: 6.55, w: 11, h: 0.4, fontFace: BF, fontSize: 13.5, color: BODY });

// ===== S2 BÀI TOÁN =====
base("Bài toán", "Vào 1 ảnh + 1 câu hỏi  →  Ra hướng dẫn từng bước");
vrule(M, 2.1, 1.4); s.addText("VÀO", { x: M + 0.25, y: 2.1, w: 5, h: 0.35, fontFace: BF, fontSize: 14, bold: true, color: ACCENT, margin: 0 });
s.addText("• 1 ảnh chụp màn hình UI\n• 1 câu hỏi bằng lời thường", { x: M + 0.25, y: 2.5, w: 5.2, h: 1.0, fontFace: BF, fontSize: 16, color: BODY, lineSpacingMultiple: 1.2, margin: 0 });
vrule(M, 3.9, 1.4); s.addText("RA", { x: M + 0.25, y: 3.9, w: 5, h: 0.35, fontFace: BF, fontSize: 14, bold: true, color: ACCENT, margin: 0 });
s.addText("Hướng dẫn bấm TỪNG BƯỚC, cho người đọc, bám sát ngữ cảnh ảnh.", { x: M + 0.25, y: 4.3, w: 5.2, h: 1.0, fontFace: BF, fontSize: 16, color: BODY, lineSpacingMultiple: 1.2, margin: 0 });
s.addShape(pres.shapes.RECTANGLE, { x: 7.2, y: 2.1, w: 5.3, h: 4.0, fill: { color: FILL }, line: { type: "none" } });
s.addText("VÍ DỤ — app eTax  (minh hoạ)", { x: 7.5, y: 2.3, w: 4.8, h: 0.35, fontFace: BF, fontSize: 13, bold: true, color: ACCENT, margin: 0 });
s.addText([{ text: "Câu hỏi: ", options: { bold: true } }, { text: "“Kiểm tra đã nộp thuế chưa thì vào đâu?”" }], { x: 7.5, y: 2.75, w: 4.8, h: 0.9, fontFace: BF, fontSize: 15, color: INK, italic: true, lineSpacingMultiple: 1.1, margin: 0 });
s.addText("Máy trả lời:", { x: 7.5, y: 3.75, w: 4.8, h: 0.3, fontFace: BF, fontSize: 13, bold: true, color: BODY, margin: 0 });
s.addText("1. Bấm “Tra cứu nghĩa vụ thuế”\n2. Chọn kỳ tính thuế\n3. Xem trạng thái đã / chưa nộp", { x: 7.5, y: 4.1, w: 4.8, h: 1.8, fontFace: BF, fontSize: 15, color: INK, lineSpacingMultiple: 1.3, margin: 0 });
note(6.45, "Lúc chạy thật, máy CHỈ thấy ảnh + câu hỏi — không có gì thêm. Sản phẩm nhận cả 1 ảnh (đơn bước) lẫn nhiều ảnh (đa bước).");
pageNum();

// ===== S3 BA THÁCH THỨC =====
base("Vì sao khó", "Ba thách thức cốt lõi");
const kho = [
  ["1.  Không có bản hướng dẫn mẫu", "Không ai viết sẵn hướng dẫn chuẩn cho từng app để máy học/đối chiếu → phải nghĩ cách CHẤM ĐIỂM khi không có cái để so."],
  ["2.  Máy hay “bịa” nút", "Mô hình nhìn-ảnh-viết-chữ (VLM) khi viết tự do thường nhắc tới nút KHÔNG có trên màn → hướng dẫn sai. Cần cơ chế chống bịa."],
  ["3.  Đa bước: phải biết TRẬT TỰ màn", "Một việc trải nhiều màn. Khi đưa nhiều ảnh các màn (có thể lộn xộn), máy phải SUY RA màn nào trước–sau rồi mới hướng dẫn đúng thứ tự."]
];
let ky = 2.15;
kho.forEach(k => { vrule(M, ky, 1.05); s.addText(k[0], { x: M + 0.28, y: ky, w: 11.4, h: 0.4, fontFace: TF, fontSize: 18, bold: true, color: INK, margin: 0 }); s.addText(k[1], { x: M + 0.28, y: ky + 0.42, w: 11.0, h: 0.7, fontFace: BF, fontSize: 14.5, color: BODY, lineSpacingMultiple: 1.08, margin: 0 }); ky += 1.45; });
note(6.5, "Thách thức #3 là trọng tâm thầy quan tâm — slide “Đa bước = sắp thứ tự màn” trả lời thẳng.");
pageNum();

// ===== S4 DỮ LIỆU =====
base("Dữ liệu", "Ba bộ dữ liệu — mỗi bộ làm một việc");
s.addText("Em dùng 3 bộ dữ liệu công khai (app tiếng Anh). Hình dung đơn giản:", { x: M, y: 1.95, w: 11.6, h: 0.4, fontFace: BF, fontSize: 15, color: BODY, margin: 0 });
const ds = [
  ["MobileViews", "kho ẢNH chụp màn hình điện thoại, mỗi ảnh kèm một BẢN LIỆT KÊ mọi nút (tên nút + vị trí).", "→ làm “đáp án” chấm máy có chỉ đúng nút trên MÀN ĐẦU không (Đóng góp 1)."],
  ["AndroidControl", "các KỊCH BẢN thao tác thật: có mục tiêu + ghi rõ từng bước bấm gì, ở đâu, theo THỨ TỰ.", "→ xáo trộn các màn rồi bắt máy XẾP LẠI → chấm đa bước (Đóng góp 2)."],
  ["ScreenSpot", "mỗi mẫu rất gọn: 1 câu lệnh + 1 nút đích (kèm vị trí).", "→ ĐỐI CHỨNG riêng việc “chỉ đúng chỗ”."]
];
let dy = 2.5;
ds.forEach(d => {
  vrule(M, dy, 1.15);
  s.addText([{ text: d[0] + "  ", options: { bold: true, color: INK } }, { text: "— là gì: ", options: { italic: true, color: MUTE } }, { text: d[1], options: { color: BODY } }], { x: M + 0.28, y: dy, w: 11.3, h: 0.7, fontFace: BF, fontSize: 15, lineSpacingMultiple: 1.06, margin: 0 });
  s.addText(d[2], { x: M + 0.28, y: dy + 0.66, w: 11.3, h: 0.4, fontFace: BF, fontSize: 14, bold: true, color: ACCENT, margin: 0 });
  dy += 1.28;
});
note(6.4, "“Bản liệt kê nút” (View Hierarchy) chỉ dùng LÚC CHẤM. AndroidControl: 15.283 kịch bản, trung bình ~5,5 bước (có luồng tới 13 bước). Tiếng Việt chưa có dữ liệu loại này → chỉ demo định tính.");
pageNum();

// ===== S5 VÍ DỤ THẬT =====
base("Dữ liệu", "Một bản ghi THẬT trông như thế nào");
vrule(M, 2.05, 1.5);
s.addText("AndroidControl — một “kịch bản” thật (dùng làm THỨ TỰ ĐÚNG)", { x: M + 0.28, y: 2.05, w: 11.3, h: 0.35, fontFace: TF, fontSize: 16, bold: true, color: INK, margin: 0 });
s.addText([{ text: "Mục tiêu: ", options: { bold: true } }, { text: "“Trên app CruiseDeals, xem lịch tàu 4 đêm New York → Canada.”   " }, { text: "Lời giải mẫu (3 bước): ", options: { bold: true } }, { text: "① mở app CruiseDeals → ② bấm điểm (313, 742) → ③ vuốt lên.   " }, { text: "→ Xáo trộn 3 màn này rồi bắt máy XẾP LẠI cho đúng.", options: { color: ACCENT, bold: true } }], { x: M + 0.28, y: 2.45, w: 11.3, h: 1.1, fontFace: BF, fontSize: 14.5, color: BODY, lineSpacingMultiple: 1.12, margin: 0 });
vrule(M, 3.75, 1.2);
s.addText("ScreenSpot — một mẫu thật", { x: M + 0.28, y: 3.75, w: 11.3, h: 0.35, fontFace: TF, fontSize: 16, bold: true, color: INK, margin: 0 });
s.addText([{ text: "Cho 1 ảnh + câu lệnh " }, { text: "“close” (đóng)", options: { bold: true } }, { text: ". Đáp án: nút Đóng (✕) ở GÓC TRÊN–PHẢI.   " }, { text: "→ Máy phải trỏ điểm vào đúng nút đó.", options: { color: ACCENT, bold: true } }], { x: M + 0.28, y: 4.15, w: 11.3, h: 0.8, fontFace: BF, fontSize: 14.5, color: BODY, lineSpacingMultiple: 1.12, margin: 0 });
vrule(M, 5.15, 1.2);
s.addText("MobileViews — một màn hình", { x: M + 0.28, y: 5.15, w: 11.3, h: 0.35, fontFace: TF, fontSize: 16, bold: true, color: INK, margin: 0 });
s.addText([{ text: "Gồm 1 ảnh + 1 bản liệt kê, ghi từng nút kiểu: " }, { text: "«nút X, nằm trong ô (trái,trên)–(phải,dưới), bấm được».   " }, { text: "→ Máy nói “bấm (x,y)” thì kiểm (x,y) có rơi trong ô đúng nút không.", options: { color: ACCENT, bold: true } }], { x: M + 0.28, y: 5.55, w: 11.3, h: 0.85, fontFace: BF, fontSize: 14.5, color: BODY, lineSpacingMultiple: 1.12, margin: 0 });
note(6.62, "Ba bộ ghi toạ độ 3 kiểu (pixel · tỷ lệ 0–1 · điểm bấm) → code chấm phải quy về cùng một kiểu.");
pageNum();

// ===== S6 ⭐ ĐA BƯỚC = SẮP THỨ TỰ MÀN (ĐINH) =====
base("Đóng góp 2 — slide quan trọng nhất", "Đa bước = SẮP THỨ TỰ MÀN");
s.addText("Đưa N ảnh các màn ĐÃ XÁO TRỘN + mục tiêu → máy phải (1) suy ra THỨ TỰ đúng, (2) sinh hướng dẫn theo thứ tự đó.", { x: M, y: 1.7, w: 11.7, h: 0.4, fontFace: BF, fontSize: 14.5, italic: true, color: MUTE, margin: 0 });
// Hàng XÁO TRỘN — số thứ tự nằm TRONG thanh tiêu đề (không dùng badge nổi để tránh đè nhãn)
s.addText("XÁO TRỘN (đầu vào)", { x: M, y: 2.16, w: 4.6, h: 0.3, fontFace: BF, fontSize: 11.5, bold: true, color: STEEL, charSpacing: 1, margin: 0 });
phone(0.95, 2.5, 1.3, 1.35, "?   Nhập giờ", ["07 : 00", "Huỷ    OK"], 1);
phone(2.5, 2.5, 1.3, 1.35, "?   Báo thức", ["Danh sách", "+ Thêm"], 1);
phone(4.05, 2.5, 1.3, 1.35, "?   Đồng hồ", ["Báo thức", "Hẹn giờ"], 0);
arrow(3.1, 3.95, 0, 0.3);
s.addText("Máy tự xếp — dựa ORDERING CUES (nút OK ⇒ drill-down; “+ Thêm” ⇒ màn danh sách đứng trước)", { x: 0.85, y: 4.32, w: 5.6, h: 0.42, fontFace: BF, fontSize: 10.5, italic: true, color: ACCENT, lineSpacingMultiple: 1.0, margin: 0 });
// Hàng ĐÃ SẮP
s.addText("ĐÃ SẮP ĐÚNG (đầu ra)", { x: M, y: 4.92, w: 4.6, h: 0.3, fontFace: BF, fontSize: 11.5, bold: true, color: ACCENT, charSpacing: 1, margin: 0 });
phone(0.95, 5.26, 1.3, 1.35, "①   Đồng hồ", ["Báo thức", "Hẹn giờ"], 0);
phone(2.5, 5.26, 1.3, 1.35, "②   Báo thức", ["Danh sách", "+ Thêm"], 1);
phone(4.05, 5.26, 1.3, 1.35, "③   Nhập giờ", ["07 : 00", "Huỷ    OK"], 1);
s.addText("(ví dụ minh hoạ: đặt báo thức 7:00 · app Đồng hồ)", { x: 0.85, y: 6.64, w: 5.4, h: 0.3, fontFace: BF, fontSize: 10, italic: true, color: MUTE, margin: 0 });
// Panel phải: metric + ordering gap
s.addShape(pres.shapes.RECTANGLE, { x: 6.55, y: 2.2, w: 5.95, h: 4.55, fill: { color: FILL }, line: { type: "none" } });
s.addText("CÁCH ĐO", { x: 6.85, y: 2.4, w: 5.4, h: 0.3, fontFace: BF, fontSize: 11.5, bold: true, color: ACCENT, charSpacing: 2, margin: 0 });
s.addText([{ text: "Kendall τ-b", options: { bold: true, color: INK } }, { text: "  — máy xếp giống thứ tự đúng tới đâu. Chấm ", options: { color: BODY } }, { text: "theo thứ-tự-bộ-phận", options: { bold: true, color: ACCENT } }, { text: ": chỉ phạt khi đảo cặp BẮT BUỘC (vào tab trước khi nhập giờ); cặp tự-do (điền email/sđt) đảo vẫn ĐÚNG.", options: { color: BODY } }], { x: 6.85, y: 2.75, w: 5.4, h: 1.25, fontFace: BF, fontSize: 13, lineSpacingMultiple: 1.12, margin: 0 });
s.addText([{ text: "ordering gap", options: { bold: true, color: INK } }, { text: " = chất-lượng(ảnh ĐÃ sắp đúng) − chất-lượng(ảnh xáo trộn, tự xếp) = ", options: { color: BODY } }, { text: "“cái giá của việc không biết trật tự”.", options: { bold: true, color: ACCENT } }], { x: 6.85, y: 4.05, w: 5.4, h: 0.95, fontFace: BF, fontSize: 13, lineSpacingMultiple: 1.12, margin: 0 });
// mini 2 cột gap
s.addShape(pres.shapes.RECTANGLE, { x: 7.55, y: 5.25, w: 0.95, h: 1.15, fill: { color: STEEL }, line: { type: "none" } });
s.addText("ORACLE\n(đã sắp)", { x: 7.35, y: 6.42, w: 1.35, h: 0.32, align: "center", fontFace: BF, fontSize: 9, color: BODY, margin: 0 });
s.addShape(pres.shapes.RECTANGLE, { x: 9.15, y: 5.7, w: 0.95, h: 0.7, fill: { color: ACCENT }, line: { type: "none" } });
s.addText("SELF\n(tự xếp)", { x: 8.95, y: 6.42, w: 1.35, h: 0.32, align: "center", fontFace: BF, fontSize: 9, color: BODY, margin: 0 });
s.addShape(pres.shapes.LINE, { x: 8.5, y: 5.25, w: 0.65, h: 0.45, line: { color: INK, width: 1.25, beginArrowType: "oval", endArrowType: "oval" } });
s.addText("gap", { x: 8.4, y: 4.95, w: 0.9, h: 0.28, align: "center", fontFace: BF, fontSize: 10, bold: true, italic: true, color: INK, margin: 0 });
s.addText("Sanity cứng: ORACLE ≥ SELF ở mọi episode.", { x: 10.3, y: 5.55, w: 2.0, h: 0.8, fontFace: BF, fontSize: 10.5, italic: true, color: MUTE, lineSpacingMultiple: 1.05, margin: 0 });
pageNum();

// ===== S7 HAI ĐÓNG GÓP =====
base("Bức tranh lớn", "Hai đóng góp (phân biệt bằng: có sẵn đáp án để so không?)");
vrule(M, 2.35, 1.7, ACCENT);
s.addText("Đóng góp 1 — đánh giá MÀN-0  (MobileViews)", { x: M + 0.28, y: 2.35, w: 11.3, h: 0.4, fontFace: TF, fontSize: 17, bold: true, color: INK, margin: 0 });
s.addText("KHÔNG có hướng dẫn mẫu của người. “Đáp án để chấm” = bản liệt kê nút (View Hierarchy) do máy xuất — chấm grounding + chống-bịa + rõ-ràng. Đây là đóng góp về CÁCH ĐÁNH GIÁ (reference-free, neo bằng VH-silver).", { x: M + 0.28, y: 2.78, w: 11.2, h: 1.0, fontFace: BF, fontSize: 14.5, color: BODY, lineSpacingMultiple: 1.1, margin: 0 });
vrule(M, 4.25, 2.0, STEEL);
s.addText("Đóng góp 2 — SUY LUẬN TRẬT TỰ MÀN  (AndroidControl)", { x: M + 0.28, y: 4.25, w: 11.3, h: 0.4, fontFace: TF, fontSize: 17, bold: true, color: INK, margin: 0 });
s.addText("CÓ sẵn chuỗi thao tác đúng để so. Đưa N ảnh xáo trộn → máy tự xếp + sinh hướng dẫn; headline Kendall τ-b + ordering gap. Trả lời thẳng câu hỏi thầy “làm sao model biết trật tự?” bằng ordering cues + signal-attribution.", { x: M + 0.28, y: 4.68, w: 11.2, h: 1.1, fontFace: BF, fontSize: 14.5, color: BODY, lineSpacingMultiple: 1.1, margin: 0 });
s.addText("Đóng góp CHÍNH = một CÁCH ĐÁNH GIÁ mới — không phải “hệ thống của em phải thắng”. Hai nửa bổ trợ: sau khi xếp đúng trật tự (ĐG2), mỗi màn được chấm grounding bằng chính metric của ĐG1.", { x: M, y: 6.2, w: 11.7, h: 0.6, fontFace: BF, fontSize: 13.5, bold: true, color: ACCENT, lineSpacingMultiple: 1.05, margin: 0 });
pageNum();

// ===== S8 PIPELINE + ROUTER =====
base("Hệ thống (pipeline: ReOrder-Tutor)", "Một hệ duy nhất, có “bộ định tuyến” theo số ảnh");
// router diagram
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: 2.1, w: 2.0, h: 0.7, rectRadius: 0.05, fill: { color: INK }, line: { type: "none" } });
s.addText("Ảnh + mục tiêu", { x: M, y: 2.1, w: 2.0, h: 0.7, align: "center", valign: "middle", fontFace: BF, fontSize: 12, bold: true, color: WHITE, margin: 0 });
arrow(2.85, 2.45, 0.55, 0);
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 3.45, y: 2.1, w: 1.5, h: 0.7, rectRadius: 0.05, fill: { color: WHITE }, line: { color: ACCENT, width: 1.5 } });
s.addText("Router", { x: 3.45, y: 2.1, w: 1.5, h: 0.7, align: "center", valign: "middle", fontFace: BF, fontSize: 12, bold: true, color: ACCENT, margin: 0 });
// nhánh N=1
arrow(5.0, 2.26, 0.7, 0);
s.addText("N = 1", { x: 5.0, y: 1.98, w: 0.9, h: 0.25, fontFace: BF, fontSize: 10, bold: true, color: MUTE, margin: 0 });
s.addShape(pres.shapes.RECTANGLE, { x: 5.8, y: 1.95, w: 6.7, h: 0.62, fill: { color: FILL }, line: { type: "none" } });
s.addText("Đơn bước (DG1) — Stage 0 rỗng → chạy thẳng 5 bước dưới", { x: 5.95, y: 1.95, w: 6.5, h: 0.62, valign: "middle", fontFace: BF, fontSize: 12.5, color: BODY, margin: 0 });
// nhánh N>=2
arrow(5.0, 3.09, 0.72, 0);
s.addText("N ≥ 2", { x: 5.0, y: 2.82, w: 0.8, h: 0.25, fontFace: BF, fontSize: 10, bold: true, color: ACCENT, margin: 0 });
s.addShape(pres.shapes.RECTANGLE, { x: 5.8, y: 2.78, w: 6.7, h: 0.62, fill: { color: HILO }, line: { type: "none" } });
s.addText([{ text: "Stage 0 — Screen-Ordering", options: { bold: true, color: ACCENT } }, { text: "  (xếp các màn xáo trộn theo thứ tự đúng) →  rồi mới chạy 5 bước dưới", options: { color: BODY } }], { x: 5.95, y: 2.78, w: 6.5, h: 0.62, valign: "middle", fontFace: BF, fontSize: 12.5, margin: 0 });
// 5 bước
s.addText("5 BƯỚC TRÊN TỪNG MÀN — biến bài “tự luận” (hay bịa) thành “trắc nghiệm” (ép chỉ vào số):", { x: M, y: 3.75, w: 11.7, h: 0.35, fontFace: BF, fontSize: 13, italic: true, color: MUTE, margin: 0 });
const steps = [
  ["1.  Dò & đánh số nút", "OmniParser tìm nút + OCR đọc chữ → mỗi nút một SỐ + ô bao."],
  ["2.  Vẽ số lên ảnh", "Vẽ ①②③ đè lên ảnh tại vị trí nút (Set-of-Mark)."],
  ["3.  Sinh có ràng buộc  (cốt lõi)", "ÉP máy chỉ được trỏ vào SỐ đã có → không bịa nút mới."],
  ["4.  Kiểm 3 tầng", "V1 = code (số có thật?) · V2 = một AI khác (đúng ý?) · V3 = tự sửa."],
  ["5.  Đổi số → toạ độ", "Tra số ra ô/toạ độ để hiển thị cho người + để chấm."]
];
let py = 4.2; steps.forEach((st, i) => { vrule(M, py, 0.5, i === 2 ? ACCENT : STEEL); s.addText(st[0], { x: M + 0.28, y: py - 0.04, w: 4.7, h: 0.55, fontFace: TF, fontSize: 14, bold: true, color: INK, valign: "middle", margin: 0 }); s.addText(st[1], { x: 5.7, y: py - 0.04, w: 6.8, h: 0.55, fontFace: BF, fontSize: 12.5, color: BODY, valign: "middle", lineSpacingMultiple: 1.0, margin: 0 }); py += 0.56; });
pageNum();

// ===== S9 ORDERING CUES + bar =====
base("Trả lời câu hỏi thầy", "Model dựa vào ĐÂU để biết trật tự?  (5 ordering cues)");
const cues = [
  ["gating", "đăng nhập / cấp quyền phải đứng trước"],
  ["nav-affordance", "nút Next / Back / breadcrumb"],
  ["state-delta", "toggle off→on, ô trống→đã điền, badge 0→1"],
  ["title-progression", "tiêu đề tiến theo phiếu (1/3 → 2/3)"],
  ["drill-down", "màn sau = chi tiết của item màn trước"]
];
let cy = 2.15; cues.forEach(c => { vrule(M, cy, 0.6); s.addText(c[0], { x: M + 0.26, y: cy, w: 2.7, h: 0.6, fontFace: BF, fontSize: 14, bold: true, color: ACCENT, valign: "middle", margin: 0 }); s.addText(c[1], { x: 3.5, y: cy, w: 3.4, h: 0.6, fontFace: BF, fontSize: 12.5, color: BODY, valign: "middle", lineSpacingMultiple: 1.0, margin: 0 }); cy += 0.7; });
// bar chart per-cue (vẽ bằng shape — không nhúng xlsx)
s.addText("Độ chính xác xếp đúng theo cue (minh hoạ)", { x: 7.1, y: 1.72, w: 5.4, h: 0.3, fontFace: BF, fontSize: 11.5, bold: true, color: STEEL, margin: 0 });
const cueVals = [0.93, 0.86, 0.71, 0.78, 0.9];
const bx = 7.3, bw = 4.4;
[0.5, 1.0].forEach(g => { const gx = bx + g * bw; s.addShape(pres.shapes.LINE, { x: gx, y: 2.15, w: 0, h: 0.4 + 4 * 0.7, line: { color: "E6EAEE", width: 0.75 } }); s.addText(Math.round(g * 100) + "%", { x: gx - 0.3, y: 2.15 + 0.4 + 4 * 0.7 + 0.02, w: 0.6, h: 0.22, align: "center", fontFace: BF, fontSize: 8, color: MUTE, margin: 0 }); });
cueVals.forEach((v, i) => { const yy = 2.15 + i * 0.7; s.addShape(pres.shapes.RECTANGLE, { x: bx, y: yy, w: bw, h: 0.4, fill: { color: "EEF1F4" }, line: { type: "none" } }); s.addShape(pres.shapes.RECTANGLE, { x: bx, y: yy, w: bw * v, h: 0.4, fill: { color: ACCENT }, line: { type: "none" } }); s.addText(Math.round(v * 100) + "%", { x: bx + bw * v + 0.06, y: yy, w: 0.6, h: 0.4, valign: "middle", fontFace: BF, fontSize: 9.5, bold: true, color: ACCENT, margin: 0 }); });
note(6.35, "Signal-attribution = chỉ giữ cặp màn khác đúng MỘT cue rồi đo riêng → biết cue nào thực sự giúp. KHÔNG che pixel. Baseline đối chứng: GOAL-ONLY (che hết ảnh) + RANDOM-ORDER.");
pageNum();

// ===== S10 PRIOR-ART (KZ') =====
base("Đặt mình ở đâu", "Khảo sát liên quan & điểm mới (cổng KZ′)");
s.addText("ĐÃ CÓ (lineage — em thừa nhận)", { x: M, y: 2.05, w: 5.6, h: 0.35, fontFace: BF, fontSize: 13.5, bold: true, color: MUTE, margin: 0 });
s.addText("• Sort-Story (EMNLP 2016) — xếp ảnh+caption bị xáo\n• Sequencing Multimodal Manuals (ACL 2022) — xếp bước hướng dẫn đa phương thức\n• RankGPT (EMNLP 2023) — LLM sinh thứ tự theo mục tiêu\n• Thước đo thứ tự: Kendall τ, Spearman (kinh điển)", { x: M, y: 2.5, w: 5.6, h: 2.7, fontFace: BF, fontSize: 14, color: BODY, lineSpacingMultiple: 1.3, margin: 0 });
vrule(7.0, 2.05, 3.0, ACCENT);
s.addText("ĐIỂM MỚI CỦA EM", { x: 7.28, y: 2.05, w: 5.2, h: 0.35, fontFace: BF, fontSize: 13.5, bold: true, color: ACCENT, margin: 0 });
s.addText("KHÔNG claim “xếp ảnh xáo là mới”. Điểm mới = TỔ HỢP + domain:", { x: 7.28, y: 2.5, w: 5.2, h: 0.7, fontFace: BF, fontSize: 14.5, color: INK, lineSpacingMultiple: 1.1, margin: 0 });
s.addText("(a) domain GUI màn hình\n(b) điều kiện theo mục tiêu/use-case\n(c) gắn ordering → SINH tutorial\n(d) signal-attribution theo ordering cue", { x: 7.28, y: 3.3, w: 5.2, h: 1.8, fontFace: BF, fontSize: 14.5, bold: true, color: BODY, lineSpacingMultiple: 1.3, margin: 0 });
note(6.3, "Cổng KZ′ (tuần 1) đã rà — không thấy công trình trùng khít; đóng khung độ mới trung thực theo lineage trên.");
pageNum();

// ===== S11 CHẤM ĐG1 =====
base("Cách chấm — Đóng góp 1", "Chấm màn-0, neo vào bản liệt kê nút");
const t1 = [
  [{ text: "Tiêu chí", options: { bold: true, color: INK, fill: { color: FILL } } }, { text: "Đo gì", options: { bold: true, color: INK, fill: { color: FILL } } }, { text: "Cách đo", options: { bold: true, color: INK, fill: { color: FILL } } }],
  ["Grounding", "Chỗ bấm có trúng nút thật?", "điểm máy chỉ có nằm trong ô của nút (point-in-bbox, SeeClick ACL 2024)"],
  ["Hallucination", "Có nhắc nút không tồn tại?", "1 − HER (tỷ lệ nút bịa); ý tưởng từ CHAIR (EMNLP 2018)"],
  ["Coverage", "Có bỏ sót nút quan trọng?", "đếm xem nhắc đủ các nút cần không"],
  ["Clarity / Format", "Có đánh số? có động từ? rõ?", "IFEval (luật) + G-Eval (một AI chấm 1–5, EMNLP 2023)"]
];
s.addTable(t1, { x: M, y: 2.05, w: W - 2 * M, colW: [2.6, 4.1, 5.03], rowH: [0.5, 0.78, 0.78, 0.7, 0.7], fontFace: BF, fontSize: 14.5, color: BODY, valign: "middle", border: { type: "solid", pt: 0.75, color: RULE }, align: "left", margin: [4, 8, 4, 8] });
note(6.45, "Con số grounding báo theo 2 cách: RAW (số thật) và ORACLE (giả định bộ-dò-hoàn-hảo) — lý do ở slide rủi ro.");
pageNum();

// ===== S12 CHẤM ĐG2 + τ-b curve =====
base("Cách chấm — Đóng góp 2", "Đo thứ tự (Kendall τ-b) + Tier A tham chiếu");
// τ-b curve (vẽ bằng shape — không nhúng xlsx)
const px0 = 1.55, px1 = 6.7, pyTop = 2.5, pyBot = 5.35;
const yOf = v => pyBot - v * (pyBot - pyTop);
s.addShape(pres.shapes.LINE, { x: px0, y: pyTop - 0.1, w: 0, h: (pyBot - pyTop) + 0.1, line: { color: MUTE, width: 1 } });
s.addShape(pres.shapes.LINE, { x: px0, y: pyBot, w: (px1 - px0) + 0.2, h: 0, line: { color: MUTE, width: 1 } });
[[1, "1.0"], [0.5, "0.5"], [0, "0"]].forEach(t => { const ty = yOf(t[0]); s.addText(t[1], { x: px0 - 0.75, y: ty - 0.12, w: 0.55, h: 0.24, align: "right", fontFace: BF, fontSize: 9, color: MUTE, margin: 0 }); if (t[0] > 0) s.addShape(pres.shapes.LINE, { x: px0, y: ty, w: px1 - px0 + 0.2, h: 0, line: { color: "EEF1F4", width: 0.5 } }); });
const selfV = [0.88, 0.79, 0.7, 0.62, 0.55, 0.5], lbl = ["3", "4", "5", "6", "7", "8"];
const xs = selfV.map((_, k) => px0 + k * ((px1 - px0) / (selfV.length - 1)));
for (let k = 0; k < selfV.length - 1; k++) s.addShape(pres.shapes.LINE, { x: xs[k], y: yOf(selfV[k]), w: xs[k + 1] - xs[k], h: yOf(selfV[k + 1]) - yOf(selfV[k]), line: { color: ACCENT, width: 2.5 } });
selfV.forEach((v, k) => { s.addShape(pres.shapes.OVAL, { x: xs[k] - 0.065, y: yOf(v) - 0.065, w: 0.13, h: 0.13, fill: { color: ACCENT }, line: { color: WHITE, width: 1 } }); s.addText("N=" + lbl[k], { x: xs[k] - 0.32, y: pyBot + 0.06, w: 0.64, h: 0.22, align: "center", fontFace: BF, fontSize: 9, color: MUTE, margin: 0 }); });
s.addShape(pres.shapes.LINE, { x: px0, y: yOf(0.04), w: px1 - px0, h: 0, line: { color: "9AA3AC", width: 1.5, dashType: "dash" } });
s.addText("SELF-ORDER (máy tự xếp)", { x: xs[2] - 0.2, y: yOf(selfV[2]) - 0.34, w: 2.6, h: 0.24, fontFace: BF, fontSize: 10.5, bold: true, color: ACCENT, margin: 0 });
s.addText("RANDOM ≈ 0 (xếp bừa)", { x: px1 - 1.95, y: yOf(0.04) - 0.26, w: 1.95, h: 0.22, align: "right", fontFace: BF, fontSize: 9.5, italic: true, color: MUTE, margin: 0 });
s.addText("Kendall τ-b theo độ dài N (minh hoạ): càng nhiều màn càng khó.", { x: M, y: 5.75, w: 6.6, h: 0.3, fontFace: BF, fontSize: 11, italic: true, color: MUTE, margin: 0 });
vrule(7.85, 2.05, 1.1, ACCENT);
s.addText("Headline = Kendall τ-b", { x: 8.1, y: 2.05, w: 4.4, h: 0.32, fontFace: TF, fontSize: 15, bold: true, color: ACCENT, margin: 0 });
s.addText("Chấm partial-order-aware (chỉ phạt cặp bắt buộc). Phụ: pairwise + position-acc. Bỏ Exact-Match (N=3 trúng bừa ~17%).", { x: 8.1, y: 2.42, w: 4.4, h: 1.0, fontFace: BF, fontSize: 13, color: BODY, lineSpacingMultiple: 1.1, margin: 0 });
vrule(7.85, 3.7, 1.7, STEEL);
s.addText("Tier A — tham chiếu chuẩn ngành", { x: 8.1, y: 3.7, w: 4.4, h: 0.5, fontFace: TF, fontSize: 15, bold: true, color: INK, lineSpacingMultiple: 1.0, margin: 0 });
s.addText("Đưa màn THẬT mỗi bước rồi chấm Action-Type / Grounding@14% / Step-SR. Giữ làm mốc đối sánh — KHÔNG còn là “đa bước chính”, KHÔNG claim ngang leaderboard.", { x: 8.1, y: 4.18, w: 4.4, h: 1.3, fontFace: BF, fontSize: 13, color: BODY, lineSpacingMultiple: 1.1, margin: 0 });
note(6.35, "ORACLE-ORDER (ảnh đã sắp đúng) là cận-trên của trục thứ tự; ordering gap = ORACLE − SELF.");
pageNum();

// ===== S13 METRIC + PAPER THẦY =====
base("Căn cứ", "Thước đo đều có nguồn bình duyệt (gồm paper của thầy)");
const t2 = [
  [{ text: "Tiêu chí", options: { bold: true, color: INK, fill: { color: FILL } } }, { text: "Thước đo", options: { bold: true, color: INK, fill: { color: FILL } } }, { text: "Nguồn", options: { bold: true, color: INK, fill: { color: FILL } } }],
  ["Khung gốc (paper thầy)", "Intrinsic / Extrinsic", "Computational Linguistics 2025 (tạp chí)"],
  ["Grounding", "Point-in-BBox", "ACL 2024 (SeeClick)"],
  ["Hallucination", "HER + ALOHa", "EMNLP 2018 · NAACL 2024"],
  ["Clarity / Format", "IFEval + G-Eval", "EMNLP 2023"],
  ["Thứ tự màn (ĐG2)", "Kendall τ-b + ordering gap", "Kendall 1938 · Gao et al. NAACL 2025"],
  ["Tham chiếu (Tier A)", "Action-Type / Grounding@14% / Step-SR", "NeurIPS 2024 · ngưỡng 14% từ AITW"]
];
s.addTable(t2, { x: M, y: 2.05, w: W - 2 * M, colW: [3.0, 4.2, 4.53], rowH: 0.55, fontFace: BF, fontSize: 13, color: BODY, valign: "middle", border: { type: "solid", pt: 0.75, color: RULE }, align: "left", margin: [3, 8, 3, 8] });
note(6.4, "Không thước đo nào tự chế. Công cụ (OmniParser/Qwen/SoM) là preprint — chỉ là “hiện vật kỹ thuật em DÙNG”, không trình như đã bình duyệt.");
pageNum();

// ===== S14 PILOT =====
base("Kiểm tra độ tin", "Đối chiếu người chấm (kế thừa paper của thầy)");
s.addText("Thước đo tự động phải được chứng minh đáng tin → chạy thử với chuyên gia chấm:", { x: M, y: 1.95, w: 11.6, h: 0.4, fontFace: BF, fontSize: 15, italic: true, color: MUTE, margin: 0 });
const pil = [
  ["BWS (Best-Worst Scaling)", "Cho chuyên gia chọn bản TỐT NHẤT & TỆ NHẤT → suy ra thứ hạng (ổn định hơn chấm điểm tuyệt đối)."],
  ["Spearman / Kendall", "Đo độ KHỚP máy↔người (gồm: thứ tự máy xếp có giống thứ tự người sắp không)."],
  ["Krippendorff α", "Đo độ ĐỒNG THUẬN giữa các người chấm với nhau."],
  ["Quy mô N ≥ 60–80", "Đủ tin; đóng khung là “kiểm tính khả dĩ”, không hứa tương quan cực chặt."]
];
let qy = 2.5; pil.forEach(p => { vrule(M, qy, 0.78); s.addText(p[0], { x: M + 0.28, y: qy, w: 11.3, h: 0.35, fontFace: TF, fontSize: 15.5, bold: true, color: INK, margin: 0 }); s.addText(p[1], { x: M + 0.28, y: qy + 0.36, w: 11.2, h: 0.42, fontFace: BF, fontSize: 13.5, color: BODY, lineSpacingMultiple: 1.05, margin: 0 }); qy += 0.95; });
pageNum();

// ===== S15 C0-C4 =====
base("Thí nghiệm", "Thang bậc C0 → C4: tách “cơ chế nào trả công”");
const t3 = [
  [{ text: "Bậc", options: { bold: true, color: INK, fill: { color: FILL } } }, { text: "Thêm gì", options: { bold: true, color: INK, fill: { color: FILL } } }, { text: "Trả lời câu hỏi", options: { bold: true, color: INK, fill: { color: FILL } } }],
  ["C0", "VLM trần", "đáy thô"],
  ["C1", "+ tự sửa (self-refine)", "BASELINE — mốc cơ sở để so"],
  ["C2", "+ đánh số nút (Set-of-Mark)", "vẽ số một mình có giúp?"],
  ["C3", "+ ép chọn số + kiểm tồn-tại (V1)", "ép “từ vựng đóng” có giúp?"],
  ["C4", "+ kiểm đúng-ý (V2) — đầy đủ", "kiểm intent có giúp?"]
];
s.addTable(t3, { x: M, y: 2.05, w: W - 2 * M, colW: [1.3, 5.4, 5.03], rowH: 0.6, fontFace: BF, fontSize: 14.5, color: BODY, valign: "middle", border: { type: "solid", pt: 0.75, color: RULE }, align: "left", margin: [3, 8, 3, 8] });
note(6.35, "Thêm từng món, đo từng nấc → biết chính xác món nào có ích. Đóng góp 2 đo thêm: τ-b theo N (SELF vs ORACLE) + bar per-cue accuracy.");
pageNum();

// ===== S16 RỦI RO =====
base("Rủi ro lớn nhất", "Hệ chỉ giỏi bằng bước dò nút + 3 cổng cho nhánh trật tự");
vrule(M, 2.1, 1.35, ACCENT);
s.addText("Nút nào bộ dò bỏ sót thì máy vĩnh viễn không nhắc được.", { x: M + 0.28, y: 2.1, w: 11.3, h: 0.45, fontFace: TF, fontSize: 17, bold: true, color: INK, margin: 0 });
s.addText("recall = trong 100 nút thật, bộ dò tìm ra bao nhiêu. Recall trên màn mobile dày CHƯA công bố rõ (tài liệu chỉ có “grounding accuracy ~57%”, là chỉ số khác).", { x: M + 0.28, y: 2.56, w: 11.2, h: 0.8, fontFace: BF, fontSize: 14.5, color: BODY, lineSpacingMultiple: 1.1, margin: 0 });
s.addText("Bộ kill-test tuần 1 (nói thẳng, không giấu):", { x: M, y: 3.75, w: 11, h: 0.35, fontFace: BF, fontSize: 14.5, bold: true, color: ACCENT, margin: 0 });
const risks = [
  ["K1", "TỰ ĐO recall bộ dò trước khi chốt (cổng go/no-go). Mọi số grounding kèm “điều kiện recall = X%”; báo RAW vs ORACLE."],
  ["KN", "Tự đếm histogram độ dài episode (sơ bộ mean ~5,5, p95 = 13) → loại N≤2, chốt trục N ∈ [3, ~10]."],
  ["KZ′", "Rà prior-art sắp-ảnh (đã khảo, GO) → đóng khung độ mới trung thực."],
  ["KB", "Chống leak thứ tự: xáo trộn phải strip metadata + tái mã hoá ảnh + đặt tên UUID (kẻo máy đọc lén thứ tự gốc)."]
];
let ry = 4.25; risks.forEach(r => { s.addShape(pres.shapes.OVAL, { x: M, y: ry, w: 0.62, h: 0.5, fill: { color: r[0] === "K1" ? ACCENT : STEEL }, line: { type: "none" } }); s.addText(r[0], { x: M, y: ry, w: 0.62, h: 0.5, align: "center", valign: "middle", fontFace: BF, fontSize: 11.5, bold: true, color: WHITE, margin: 0 }); s.addText(r[1], { x: M + 0.8, y: ry, w: 10.9, h: 0.5, valign: "middle", fontFace: BF, fontSize: 13, color: BODY, lineSpacingMultiple: 1.0, margin: 0 }); ry += 0.6; });
pageNum();

// ===== S17 NULL VẪN ĐẬU =====
base("Bảo hiểm khoa học", "Kết quả xấu vẫn ĐẬU");
s.addText("pre-registration = đăng ký giả thuyết + ngưỡng đánh giá TRƯỚC khi chạy → không thể “thua thì đổi đề”.", { x: M, y: 2.1, w: 11.6, h: 0.5, fontFace: BF, fontSize: 16, italic: true, color: MUTE, lineSpacingMultiple: 1.1, margin: 0 });
vrule(M, 3.0, 1.9, ACCENT);
s.addText("Nếu hệ KHÔNG thắng baseline (null result)…", { x: M + 0.28, y: 3.0, w: 11.3, h: 0.4, fontFace: TF, fontSize: 17, bold: true, color: INK, margin: 0 });
s.addText("…thì một kết quả null ĐƯỢC GIẢI THÍCH CƠ CHẾ (vd “recall bộ dò chặn trần lợi ích”) VẪN là đóng góp khoa học hợp lệ. Hơn nữa, thang bậc C0→C4 và đường cong τ-b theo N tự chúng đo được cơ chế nào trả công.", { x: M + 0.28, y: 3.45, w: 11.2, h: 1.4, fontFace: BF, fontSize: 15, color: BODY, lineSpacingMultiple: 1.15, margin: 0 });
s.addText("Luận văn KHÔNG phụ thuộc vào việc “hệ phải thắng”.", { x: M, y: 5.5, w: 11.6, h: 0.4, fontFace: BF, fontSize: 15, bold: true, color: ACCENT, margin: 0 });
pageNum();

// ===== S18 PHẠM VI + KHẢ THI =====
base("Đề nghị chốt", "Phạm vi & tính khả thi");
s.addText("TRONG LUẬN VĂN", { x: M, y: 2.1, w: 5.5, h: 0.35, fontFace: BF, fontSize: 13.5, bold: true, color: ACCENT, margin: 0 });
s.addText("• Chấm màn-0 (Đóng góp 1, reference-free)\n• Đa bước = SUY LUẬN TRẬT TỰ MÀN (Đóng góp 2): τ-b + ordering gap\n• Thang bậc C0–C4 + pilot người chấm", { x: M, y: 2.5, w: 5.6, h: 2.2, fontFace: BF, fontSize: 15, color: BODY, lineSpacingMultiple: 1.3, margin: 0 });
s.addText("FUTURE-WORK  (chưa có dữ liệu để chấm)", { x: 7.0, y: 2.1, w: 5.5, h: 0.35, fontFace: BF, fontSize: 13.5, bold: true, color: MUTE, margin: 0 });
s.addText("• Chấm định lượng tiếng Việt\n• World-model tự huấn luyện (cần train)\n• Mở rộng nhánh web (Mind2Web)", { x: 7.0, y: 2.5, w: 5.5, h: 2.0, fontFace: BF, fontSize: 15, color: BODY, lineSpacingMultiple: 1.3, margin: 0 });
s.addShape(pres.shapes.RECTANGLE, { x: M, y: 5.15, w: W - 2 * M, h: 0.95, fill: { color: FILL }, line: { type: "none" } });
s.addText("Khả thi: không huấn luyện model · 1 GPU 24GB + ~$100–300 (model rẻ + chạy theo lô) · lộ trình 6 pha có cổng kiểm tra.", { x: M + 0.3, y: 5.15, w: W - 2 * M - 0.6, h: 0.95, fontFace: BF, fontSize: 14.5, bold: true, color: INK, valign: "middle", lineSpacingMultiple: 1.1, margin: 0 });
pageNum();

// ===== S19 KẾT LUẬN =====
s = pres.addSlide(); s.background = { color: WHITE };
s.addShape(pres.shapes.RECTANGLE, { x: M, y: 0.9, w: 0.9, h: 0.08, fill: { color: ACCENT }, line: { type: "none" } });
s.addText("ĐỀ NGHỊ DUYỆT PHẠM VI", { x: M, y: 1.15, w: 11, h: 0.4, fontFace: BF, fontSize: 13, bold: true, color: ACCENT, charSpacing: 3 });
s.addText("Ba thứ luận văn mang lại", { x: M, y: 1.6, w: 11.5, h: 0.7, fontFace: TF, fontSize: 30, bold: true, color: INK });
const cc = [
  ["1", "Một CÁCH ĐÁNH GIÁ hướng-dẫn-từ-ảnh khi không có hướng dẫn mẫu (reference-free, neo VH-silver)."],
  ["2", "Bài toán SUY LUẬN TRẬT TỰ MÀN: đưa N ảnh xáo trộn → máy tự xếp + sinh hướng dẫn; đo Kendall τ-b + ordering gap + signal-attribution theo cue."],
  ["3", "Một THÍ NGHIỆM có kiểm soát (thang bậc C0–C4) + pilot người chấm."]
];
let zy = 2.75; cc.forEach(c => { s.addText(c[0] + ".", { x: M, y: zy, w: 0.5, h: 0.6, fontFace: TF, fontSize: 18, bold: true, color: ACCENT, margin: 0 }); s.addText(c[1], { x: M + 0.55, y: zy - 0.02, w: 11.0, h: 0.9, fontFace: BF, fontSize: 16, color: BODY, valign: "top", lineSpacingMultiple: 1.05, margin: 0 }); zy += 1.0; });
s.addShape(pres.shapes.RECTANGLE, { x: M, y: 5.85, w: W - 2 * M, h: 0.85, fill: { color: FILL }, line: { type: "none" } });
s.addText("Tuần 1: chạy kill-test — K1 (tự đo recall) + KN (độ dài episode) + KZ′ (prior-art) + KB (chống leak) — rồi báo lại thầy chốt.", { x: M + 0.3, y: 5.85, w: W - 2 * M - 0.6, h: 0.85, fontFace: BF, fontSize: 14.5, color: INK, valign: "middle", margin: 0 });
s.addText("Em cảm ơn thầy.", { x: M, y: 6.85, w: 6, h: 0.4, fontFace: TF, fontSize: 15, italic: true, color: MUTE });

pres.writeFile({ fileName: "../LUAN_VAN_SLIDE.pptx" }).then(f => console.log("WROTE", f));
