// Deck v10 — van phong hoc thuat (bo van noi). Cau truc: 1.Bai toan  2.Du lieu(3 bo: MobileViews/AndroidControl/ScreenSpot)
//   3.Pipeline mot-man/nhieu-man (+bang can cu)  4.Metric moi loai (+vi du+can cu).  IT CHU, NHIEU HINH. KHONG dung "DG1/DG2".
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Luan van thac si";
pres.title = "Sinh tu dong huong dan su dung phan mem";

const TF = "Cambria", BF = "Segoe UI";
const INK = "1C2530", BODY = "3C434B", MUTE = "8A929B", ACCENT = "8A2433";
const STEEL = "5B6B7A", RULE = "D7DCE1", FILL = "F4F6F8", WHITE = "FFFFFF", HILO = "F2E3E6", GOOD = "1E6B43";
const W = 13.33, H = 7.5, M = 0.9;
let PAGE = 1, s;

function base(kicker, title) {
  s = pres.addSlide(); s.background = { color: WHITE };
  s.addText(kicker.toUpperCase(), { x: M, y: 0.55, w: W - 2 * M, h: 0.3, fontFace: BF, fontSize: 12, bold: true, color: ACCENT, charSpacing: 3, margin: 0 });
  s.addText(title, { x: M, y: 0.9, w: W - 2 * M, h: 0.9, fontFace: TF, fontSize: 27, bold: true, color: INK, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: M, y: 1.62, w: 0.7, h: 0.05, fill: { color: ACCENT }, line: { type: "none" } });
}
function pageNum() { PAGE++; s.addText(String(PAGE).padStart(2, "0"), { x: W - 1.1, y: H - 0.5, w: 0.7, h: 0.3, fontFace: BF, fontSize: 10, color: MUTE, align: "right" }); }
function vrule(x, y, h, c) { s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.06, h, fill: { color: c || ACCENT }, line: { type: "none" } }); }
function panel(x, y, w, h, c) { s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.06, fill: { color: c || FILL }, line: { type: "none" } }); }
function box(x, y, w, h, c, lc) { s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.06, fill: { color: c || WHITE }, line: { color: lc || RULE, width: 1 } }); }
function arrow(x, y, w, c) { s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: c || ACCENT, width: 2.5, endArrowType: "triangle" } }); }
function chip(x, y, w, t, c, tc) { s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.42, rectRadius: 0.21, fill: { color: c || FILL }, line: { type: "none" } }); s.addText(t, { x, y, w, h: 0.42, align: "center", valign: "middle", fontFace: BF, fontSize: 13, bold: true, color: tc || INK, margin: 0 }); }
function img(path, x, y, w, h) { try { s.addImage({ path: "_img/" + path, x, y, w, h, sizing: { type: "contain", w, h } }); } catch (e) {} }
function shot(path, x, y, w, h, cap) { box(x - 0.08, y - 0.08, w + 0.16, h + (cap ? 0.5 : 0.16)); img(path, x, y, w, h); if (cap) s.addText(cap, { x: x - 0.08, y: y + h + 0.02, w: w + 0.16, h: 0.36, align: "center", valign: "middle", fontFace: BF, fontSize: 12, bold: true, color: INK, margin: 0 }); }
function bignum(x, y, n, lab) {
  box(x, y, 3.0, 1.25);
  s.addText(n, { x: x, y: y + 0.1, w: 3.0, h: 0.7, align: "center", fontFace: TF, fontSize: 34, bold: true, color: ACCENT, margin: 0 });
  s.addText(lab, { x: x + 0.1, y: y + 0.78, w: 2.8, h: 0.45, align: "center", fontFace: BF, fontSize: 11.5, color: BODY, margin: 0 });
}

// ============================================================ S1 · TIÊU ĐỀ
s = pres.addSlide(); s.background = { color: WHITE };
s.addShape(pres.shapes.RECTANGLE, { x: M, y: 2.0, w: 0.9, h: 0.08, fill: { color: ACCENT }, line: { type: "none" } });
s.addText("LUẬN VĂN THẠC SĨ — KHOA HỌC MÁY TÍNH", { x: M, y: 2.25, w: 11, h: 0.4, fontFace: BF, fontSize: 13, bold: true, color: ACCENT, charSpacing: 3 });
s.addText("Sinh tự động hướng dẫn sử dụng phần mềm\ntừ ảnh màn hình và câu hỏi người dùng", { x: M - 0.02, y: 2.7, w: 11.9, h: 1.7, fontFace: TF, fontSize: 36, bold: true, color: INK, lineSpacingMultiple: 1.05 });
s.addText("kèm phương pháp đánh giá trong điều kiện không có bản hướng dẫn mẫu", { x: M, y: 4.55, w: 11.5, h: 0.5, fontFace: TF, fontSize: 19, italic: true, color: BODY });
s.addText("Học viên ………    ·    Giảng viên hướng dẫn ………    ·    2026", { x: M, y: 6.45, w: 11, h: 0.4, fontFace: BF, fontSize: 13.5, color: MUTE });

// ============================================================ S2 · BÀI TOÁN
base("Bài toán", "Đầu vào: ảnh và câu hỏi — Đầu ra: hướng dẫn theo bước");
shot("real_mv_1.png", M + 0.35, 2.15, 2.5, 3.9, "Ảnh màn hình");
panel(4.4, 2.35, 3.3, 1.05, FILL);
s.addText("Câu hỏi của người dùng", { x: 4.65, y: 2.45, w: 2.9, h: 0.3, fontFace: BF, fontSize: 12, bold: true, color: ACCENT, margin: 0 });
s.addText("“Cần thao tác gì để đặt giờ 20:35 và xác nhận?”", { x: 4.65, y: 2.78, w: 2.95, h: 0.6, fontFace: BF, fontSize: 13.5, color: INK, margin: 0 });
arrow(7.85, 2.9, 0.6);
panel(8.6, 2.15, 3.9, 3.9, HILO);
s.addText("Hướng dẫn sinh ra", { x: 8.9, y: 2.35, w: 3.4, h: 0.35, fontFace: BF, fontSize: 12.5, bold: true, color: ACCENT, margin: 0 });
s.addText("1.  Chọn giờ “8”, phút “35”\n2.  Chọn buổi “PM”\n3.  Chọn “OK”", { x: 8.9, y: 2.85, w: 3.4, h: 3.0, fontFace: BF, fontSize: 17, color: INK, lineSpacingMultiple: 1.4, margin: 0 });
s.addText("Đầu vào một ảnh: tác vụ trong một màn. Đầu vào nhiều ảnh: tác vụ trải nhiều màn — mô hình phải tự suy ra thứ tự.", { x: M, y: 6.35, w: 11.5, h: 0.4, fontFace: BF, fontSize: 13, italic: true, color: MUTE, margin: 0 });
pageNum();

// ============================================================ S3 · THÁCH THỨC
base("Bài toán", "Ba thách thức trọng tâm");
const hk = [
  ["Ảo giác giao diện", "Mô hình tham chiếu nút không tồn tại trên màn hình; người dùng không thể thực hiện theo."],
  ["Thiếu bản hướng dẫn mẫu", "Không có tập hướng dẫn chuẩn do con người biên soạn cho mọi ứng dụng để làm mốc đánh giá."],
  ["Thứ tự các màn", "Với nhiều ảnh bị xáo trộn, mô hình phải tự suy ra thứ tự đúng — dựa vào căn cứ nào?"],
];
hk.forEach((c, i) => {
  const x = M + i * 3.95;
  box(x, 2.2, 3.65, 3.5);
  s.addText(String(i + 1), { x: x + 0.25, y: 2.4, w: 1, h: 0.9, fontFace: TF, fontSize: 46, bold: true, color: ACCENT, margin: 0 });
  s.addText(c[0], { x: x + 0.25, y: 3.4, w: 3.15, h: 0.9, fontFace: TF, fontSize: 18, bold: true, color: INK, margin: 0 });
  s.addText(c[1], { x: x + 0.25, y: 4.35, w: 3.15, h: 1.3, fontFace: BF, fontSize: 13.5, color: BODY, lineSpacingMultiple: 1.2, margin: 0 });
});
pageNum();

// ============================================================ S4 · DỮ LIỆU — vai trò 3 bộ
base("Dữ liệu", "Ba bộ dữ liệu — vai trò phân định");
const drows = [
  [{ text: "Bộ dữ liệu", options: { bold: true, color: INK, fill: FILL } },
   { text: "Nội dung", options: { bold: true, color: INK, fill: FILL } },
   { text: "Nhãn có sẵn", options: { bold: true, color: INK, fill: FILL, align: "center" } },
   { text: "Vai trò trong luận văn", options: { bold: true, color: INK, fill: FILL } }],
  [{ text: "MobileViews\n(một màn)", options: { bold: true, color: INK } },
   { text: "Ảnh + cây phân cấp giao diện + toạ độ nút" },
   { text: "Không có\nquỹ đạo vàng", options: { align: "center", color: ACCENT } },
   { text: "Đánh giá độ trung thực với giao diện trên một màn" }],
  [{ text: "AndroidControl\n(nhiều màn)", options: { bold: true, color: INK } },
   { text: "Chuỗi màn của một tác vụ + cây trợ năng + thao tác đúng từng bước" },
   { text: "Có\nquỹ đạo vàng", options: { align: "center", color: GOOD, bold: true } },
   { text: "Đánh giá sắp thứ tự màn & hoàn thành tác vụ" }],
  [{ text: "ScreenSpot-v2\n(đối chứng)", options: { bold: true, color: INK } },
   { text: "Ảnh + toạ độ nút chuẩn cho bài trỏ đúng nút" },
   { text: "Có toạ độ\nchuẩn", options: { align: "center", color: GOOD } },
   { text: "Kiểm định độc lập độ chính xác “trỏ đúng nút”" }],
];
s.addTable(drows, { x: M, y: 2.2, w: W - 2 * M, colW: [2.5, 4.2, 1.9, 2.9], rowH: 1.0, fontFace: BF, fontSize: 12.5, border: { type: "solid", color: RULE, pt: 1 }, valign: "middle" });
s.addText("Trục phân định: có hay không có quỹ đạo vàng. MobileViews và AndroidControl đều cung cấp danh sách nút thật làm mốc neo; ScreenSpot bổ sung một chuẩn đã bình duyệt cho phép đo trỏ đúng nút.", { x: M, y: 6.5, w: 11.5, h: 0.6, fontFace: BF, fontSize: 12.5, italic: true, color: MUTE, lineSpacingMultiple: 1.15, margin: 0 });
pageNum();

// ============================================================ S5 · DỮ LIỆU · MobileViews
base("Dữ liệu · minh hoạ", "MobileViews — một màn kèm danh sách nút thật");
shot("real_mv_1.png", M + 0.4, 2.2, 2.6, 4.0);
shot("real_mv_2.png", 4.15, 2.2, 2.6, 4.0);
panel(7.4, 2.2, 5.0, 4.0, FILL);
s.addText("Mỗi ảnh đi kèm (không cung cấp cho mô hình khi sinh):", { x: 7.7, y: 2.4, w: 4.5, h: 0.6, fontFace: BF, fontSize: 14, bold: true, color: ACCENT, margin: 0 });
s.addText("•  Danh sách nút và nhãn hiển thị\n    ví dụ: OK · Cancel · hour · minute · PM\n\n•  Toạ độ khung mỗi nút  [l, t, r, b]", { x: 7.7, y: 3.15, w: 4.5, h: 1.6, fontFace: BF, fontSize: 14.5, color: BODY, lineSpacingMultiple: 1.3, margin: 0 });
panel(7.7, 4.85, 4.4, 1.2, HILO);
s.addText("Danh sách nút chỉ tham gia ở bước đánh giá, không cung cấp cho mô hình ở bước sinh (tránh rò rỉ thông tin).", { x: 7.9, y: 4.95, w: 4.0, h: 1.0, valign: "middle", fontFace: BF, fontSize: 13, bold: true, color: INK, lineSpacingMultiple: 1.15, margin: 0 });
pageNum();

// ============================================================ S6 · DỮ LIỆU · AndroidControl
base("Dữ liệu · minh hoạ", "AndroidControl — chuỗi nhiều màn kèm quỹ đạo vàng");
[["ac_o1.png", "Màn 1"], ["ac_o2.png", "Màn 2"], ["ac_o3.png", "Màn 3"]].forEach((im, i) => {
  const x = M + 0.2 + i * 2.55;
  shot(im[0], x, 2.2, 2.1, 3.4, im[1]);
  if (i < 2) arrow(x + 2.2, 3.85, 0.28, STEEL);
});
panel(8.9, 2.2, 3.5, 3.4, FILL);
s.addText("Nhãn đi kèm (dùng khi đánh giá):", { x: 9.15, y: 2.4, w: 3.1, h: 0.6, fontFace: BF, fontSize: 13.5, bold: true, color: ACCENT, margin: 0 });
s.addText("•  Thứ tự đúng của các màn\n\n•  Thao tác đúng ở mỗi màn\n    (loại thao tác, đối tượng, vị trí)", { x: 9.15, y: 3.1, w: 3.1, h: 2.4, fontFace: BF, fontSize: 14, color: BODY, lineSpacingMultiple: 1.3, margin: 0 });
s.addText("Khi thử nghiệm, các màn được xáo trộn để mô hình tự sắp xếp lại; quỹ đạo vàng chỉ dùng để đối chiếu. Nguồn: Li et al., NeurIPS 2024 (Datasets & Benchmarks).", { x: M, y: 5.95, w: 11.5, h: 0.5, fontFace: BF, fontSize: 12.5, italic: true, color: MUTE, lineSpacingMultiple: 1.15, margin: 0 });
pageNum();

// ============================================================ S7 · DỮ LIỆU · ScreenSpot
base("Dữ liệu · minh hoạ", "ScreenSpot-v2 — đối chứng cho phép đo “trỏ đúng nút”");
shot("ss_mobile.png", M + 0.3, 2.2, 2.4, 3.9);
panel(3.9, 2.2, 8.5, 1.9, FILL);
s.addText("Vai trò", { x: 4.2, y: 2.35, w: 8.0, h: 0.35, fontFace: TF, fontSize: 16, bold: true, color: ACCENT, margin: 0 });
s.addText("Là chuẩn đã được bình duyệt cho bài toán trỏ đúng nút từ mô tả. Dùng để kiểm định độc lập độ chính xác của bộ trỏ nút trong luận văn, tách khỏi dữ liệu chính.", { x: 4.2, y: 2.75, w: 8.0, h: 1.25, fontFace: BF, fontSize: 14, color: BODY, lineSpacingMultiple: 1.3, margin: 0 });
panel(3.9, 4.3, 8.5, 1.8, HILO);
s.addText("Vì sao cần bộ đối chứng này", { x: 4.2, y: 4.45, w: 8.0, h: 0.35, fontFace: TF, fontSize: 15.5, bold: true, color: ACCENT, margin: 0 });
s.addText("•  MobileViews hiện là bản tiền ấn phẩm → cần một chuẩn đã bình duyệt để củng cố độ tin cậy.\n•  Cho phép báo cáo độ chính xác “trỏ đúng nút” trên dữ liệu độc lập, không trùng với tập đánh giá chính.", { x: 4.2, y: 4.85, w: 8.0, h: 1.15, fontFace: BF, fontSize: 13.5, color: BODY, lineSpacingMultiple: 1.25, margin: 0 });
s.addText("ScreenSpot-v2: bản làm sạch nhãn (OS-Atlas, ICLR 2025); ScreenSpot gốc từ SeeClick, ACL 2024.", { x: M, y: 6.35, w: 11.5, h: 0.4, fontFace: BF, fontSize: 12, italic: true, color: MUTE, margin: 0 });
pageNum();

// ============================================================ S8 · PIPELINE một màn — lý thuyết
base("Phương pháp · một màn", "Sinh trước, đối chiếu danh sách nút thật sau");
panel(M, 2.15, W - 2 * M, 1.55, FILL);
chip(M + 0.3, 2.42, 2.0, "BƯỚC 1 · SINH", ACCENT, WHITE);
s.addText("Mô hình chỉ nhận:  ảnh  +  câu hỏi", { x: M + 2.5, y: 2.4, w: 5.4, h: 0.45, fontFace: BF, fontSize: 15.5, bold: true, color: INK, margin: 0, valign: "middle" });
arrow(8.1, 2.63, 0.55);
chip(8.75, 2.42, 3.1, "bản sinh gốc (baseline)", HILO, INK);
s.addText("Danh sách nút thật không được cung cấp ở bước này để tránh rò rỉ thông tin.", { x: M + 0.3, y: 3.15, w: 11, h: 0.45, fontFace: BF, fontSize: 13.5, italic: true, color: ACCENT, margin: 0 });
panel(M, 3.95, W - 2 * M, 2.05, HILO);
chip(M + 0.3, 4.22, 2.7, "BƯỚC 2 · ĐỐI CHIẾU", STEEL, WHITE);
s.addText("Thuật toán so khớp từng bước với danh sách nút thật", { x: M + 3.2, y: 4.2, w: 6.5, h: 0.45, fontFace: BF, fontSize: 15.5, bold: true, color: INK, margin: 0, valign: "middle" });
s.addText("•  Bước tham chiếu nút có thật  →  giữ nguyên\n•  Bước tham chiếu nút không tồn tại  →  thay bằng mô tả khái quát, không suy đoán nút thay thế", { x: M + 0.3, y: 4.85, w: 11.3, h: 1.05, fontFace: BF, fontSize: 14.5, color: BODY, lineSpacingMultiple: 1.3, margin: 0 });
s.addText("Bước đối chiếu là thuật toán so khớp ngữ nghĩa, không phải một mô hình ngôn ngữ. Bước mô tả thay thế dùng khuôn cố định, không suy đoán chức năng. Danh sách nút chỉ tham gia ở bước 2.", { x: M, y: 6.2, w: 11.5, h: 0.4, fontFace: BF, fontSize: 12.5, italic: true, color: MUTE, margin: 0 });
pageNum();

// ============================================================ S9 · PIPELINE một màn — ví dụ
base("Phương pháp · một màn · minh hoạ", "Đối chiếu từng bước với danh sách nút thật");
shot("real_mv_1.png", M + 0.1, 2.2, 2.3, 3.6);
s.addText("Danh sách nút thật:  hour · minute · PM · OK · Cancel", { x: 3.0, y: 2.15, w: 9.3, h: 0.35, fontFace: BF, fontSize: 13, bold: true, color: STEEL, margin: 0 });
const erows = [
  [{ text: "Mô hình sinh ra", options: { bold: true, fill: FILL, color: INK } }, { text: "Nút thật gần nhất", options: { bold: true, fill: FILL, color: INK } }, { text: "Kết luận", options: { bold: true, fill: FILL, color: INK, align: "center" } }],
  [{ text: "Chọn giờ và phút" }, { text: "hour / minute" }, { text: "hợp lệ", options: { align: "center", color: GOOD, bold: true } }],
  [{ text: "Chọn “PM”" }, { text: "PM" }, { text: "hợp lệ", options: { align: "center", color: GOOD, bold: true } }],
  [{ text: "Mở “Cài đặt”" }, { text: "(không có nút tương ứng)", options: { color: MUTE } }, { text: "ẢO GIÁC", options: { align: "center", color: ACCENT, bold: true } }],
];
s.addTable(erows, { x: 3.0, y: 2.6, w: 9.3, colW: [3.5, 3.4, 2.4], rowH: 0.62, fontFace: BF, fontSize: 14.5, border: { type: "solid", color: RULE, pt: 1 }, valign: "middle" });
s.addText("Quy tắc: độ giống ngữ nghĩa ≥ ngưỡng τ → nút hợp lệ; dưới τ → ảo giác.", { x: 3.0, y: 5.05, w: 9.3, h: 0.3, fontFace: BF, fontSize: 12.5, italic: true, color: STEEL, margin: 0 });
panel(3.0, 5.4, 9.3, 1.0, HILO);
s.addText("Lớp đối chiếu chỉ can thiệp vào bước ảo giác:  “Mở Cài đặt”  →  “Tìm mục cài đặt liên quan trên màn hình”.  Các bước hợp lệ được giữ nguyên.", { x: 3.25, y: 5.4, w: 8.85, h: 1.0, valign: "middle", fontFace: BF, fontSize: 14, color: INK, lineSpacingMultiple: 1.2, margin: 0 });
pageNum();

// ============================================================ S10 · PIPELINE nhiều màn
base("Phương pháp · nhiều màn", "Sắp thứ tự bằng so cặp và tổng hợp Copeland");
s.addText("Các màn được xáo trộn. Mô hình so sánh từng cặp (“màn nào trước?”), sau đó tổng hợp bằng điểm Copeland — số cặp mà mỗi màn thắng.", { x: M, y: 2.05, w: 11.5, h: 0.5, fontFace: BF, fontSize: 14.5, color: BODY, lineSpacingMultiple: 1.15, margin: 0 });
[["ac_o1.png", "A"], ["ac_o2.png", "B"], ["ac_o3.png", "C"]].forEach((im, i) => {
  const x = M + 0.1 + i * 1.95;
  shot(im[0], x, 2.75, 1.55, 2.5, "Màn " + im[1]);
});
panel(6.9, 2.75, 5.5, 2.85, FILL);
s.addText("Ví dụ ba màn", { x: 7.2, y: 2.9, w: 5.0, h: 0.35, fontFace: BF, fontSize: 13, bold: true, color: ACCENT, margin: 0 });
s.addText("A trước B ·  A trước C ·  B trước C\n\n→  A thắng 2,  B thắng 1,  C thắng 0\n\n→  thứ tự suy ra:   A  <  B  <  C", { x: 7.2, y: 3.3, w: 5.0, h: 2.2, fontFace: BF, fontSize: 15.5, color: INK, lineSpacingMultiple: 1.25, margin: 0 });
s.addText("Chuỗi đã sắp được đưa lần lượt qua nhánh một màn — một hệ thống thống nhất; đầu vào một ảnh là trường hợp không cần sắp xếp. Gặp mâu thuẫn vòng thì loại phán đoán cặp có độ tin cậy thấp nhất. Khi sắp xếp, mô hình chỉ thấy ảnh (đã che thanh trạng thái) và mục tiêu.", { x: M, y: 5.78, w: 11.5, h: 0.55, fontFace: BF, fontSize: 11.5, italic: true, color: MUTE, lineSpacingMultiple: 1.1, margin: 0 });
s.addText("So với các công trình sắp thứ tự ảnh trước đây (Sort-Story, EMNLP 2016; RankGPT, EMNLP 2023): điểm mới là miền giao diện, điều kiện hoá theo mục tiêu, và chấm thứ-tự-bộ-phận theo quỹ đạo vàng.", { x: M, y: 6.4, w: 11.5, h: 0.5, fontFace: BF, fontSize: 11, italic: true, color: STEEL, lineSpacingMultiple: 1.08, margin: 0 });
pageNum();

// ============================================================ S11 · CĂN CỨ PIPELINE (bảng)
base("Phương pháp", "Căn cứ lựa chọn — tổng hợp");
const wrows = [
  [{ text: "Thách thức", options: { bold: true, fill: FILL, color: INK } }, { text: "Giải pháp", options: { bold: true, fill: FILL, color: INK } }, { text: "Căn cứ", options: { bold: true, fill: FILL, color: INK } }],
  [{ text: "Ảo giác giao diện", options: { bold: true, color: BODY } }, { text: "Sinh trước, đối chiếu nút thật sau" }, { text: "Đo được tỉ lệ ảo giác, không rò rỉ thông tin" }],
  [{ text: "Thiếu bản mẫu", options: { bold: true, color: BODY } }, { text: "Neo bằng danh sách nút thật (nhãn bạc)" }, { text: "Có mốc đánh giá khách quan, không cần biên soạn thủ công" }],
  [{ text: "Hiệu chỉnh gây lỗi ngầm", options: { bold: true, color: BODY } }, { text: "Chỉ mô tả khái quát, không suy đoán nút" }, { text: "Tránh dẫn người dùng đến thao tác sai" }],
  [{ text: "Thứ tự nhiều màn", options: { bold: true, color: BODY } }, { text: "So cặp và tổng hợp Copeland" }, { text: "Đơn giản, diễn giải được, tránh vòng lặp luận lý" }],
];
s.addTable(wrows, { x: M, y: 2.25, w: W - 2 * M, colW: [3.0, 3.9, 4.6], rowH: 0.85, fontFace: BF, fontSize: 13.5, border: { type: "solid", color: RULE, pt: 1 }, valign: "middle" });
s.addText("Mỗi lựa chọn nhắm một thách thức xác định; không thành phần nào được thêm mà không có căn cứ.", { x: M, y: 6.6, w: 11.5, h: 0.4, fontFace: BF, fontSize: 12.5, italic: true, color: MUTE, margin: 0 });
pageNum();

// ============================================================ S12 · METRIC một màn
base("Đánh giá · một màn", "Ba thước đo và căn cứ");
const m1 = [
  ["Độ trung thực", "Có tham chiếu nút không tồn tại?", "1 − (bước ảo giác) / (bước có tham chiếu nút)", "ví dụ 1/3 ảo giác → 67%"],
  ["Độ đúng nhãn", "Gọi đúng tên hiển thị của nút?", "(bước gọi đúng tên) / (bước tham chiếu nút hợp lệ)", "“Confirm” ≠ “OK” → sai nhãn"],
  ["Độ đúng vị trí", "Điểm bấm có trúng khung nút?", "điểm (x, y) nằm trong khung [l, t, r, b]", "minh hoạ ở hình bên"],
];
m1.forEach((mt, i) => {
  const y = 2.15 + i * 1.05; box(M, y, 7.4, 0.92); vrule(M, y, 0.92, STEEL);
  s.addText(mt[0], { x: M + 0.28, y: y + 0.06, w: 2.1, h: 0.8, valign: "middle", fontFace: TF, fontSize: 15, bold: true, color: INK, margin: 0 });
  s.addText(mt[1], { x: M + 2.2, y: y + 0.06, w: 2.6, h: 0.8, valign: "middle", fontFace: BF, fontSize: 12, color: BODY, margin: 0 });
  s.addText([{ text: mt[2] + "\n", options: { color: INK, bold: true } }, { text: mt[3], options: { color: MUTE, italic: true } }], { x: M + 4.8, y: y + 0.06, w: 2.45, h: 0.8, valign: "middle", fontFace: BF, fontSize: 10.5, lineSpacingMultiple: 1.1, margin: 0 });
});
shot("real_ground_1.png", 9.0, 2.35, 3.1, 3.3);
s.addText("Độ đúng vị trí: điểm bấm rơi trong khung nút lật ống kính → hợp lệ.", { x: 8.7, y: 5.75, w: 3.7, h: 0.7, align: "center", fontFace: BF, fontSize: 12, italic: true, color: BODY, lineSpacingMultiple: 1.1, margin: 0 });
s.addText("Toạ độ (x, y) do bộ trỏ nút độc lập (kiểu ScreenSpot) dự đoán từ tên nút và ảnh, không lấy tâm khung nút đã khớp; độ chính xác đo riêng trên ScreenSpot-v2. Căn cứ: point-in-bbox (SeeClick, ACL 2024); so khớp ngữ nghĩa (ALOHa, NAACL 2024).", { x: M, y: 6.5, w: 11.5, h: 0.55, fontFace: BF, fontSize: 11, italic: true, color: MUTE, lineSpacingMultiple: 1.12, margin: 0 });
pageNum();

// ============================================================ S13 · METRIC nhiều màn
base("Đánh giá · nhiều màn", "Hai thước đo và căn cứ");
box(M, 2.15, 5.7, 2.2);
s.addText("① Độ đúng thứ tự", { x: M + 0.3, y: 2.3, w: 5.1, h: 0.4, fontFace: TF, fontSize: 17, bold: true, color: INK, margin: 0 });
s.addText("τ = (cặp thuận − cặp nghịch) / (cặp bắt buộc)", { x: M + 0.3, y: 2.75, w: 5.1, h: 0.4, fontFace: BF, fontSize: 12.5, bold: true, color: BODY, margin: 0 });
s.addText("Quỹ đạo vàng A<B<C, mô hình xếp A, C, B → hai cặp thuận, một cặp nghịch → τ = +0,33. Chỉ tính phạt trên cặp bắt buộc; cặp không ràng buộc thứ tự (ví dụ điền email và số điện thoại) đảo vẫn hợp lệ.", { x: M + 0.3, y: 3.2, w: 5.1, h: 1.1, fontFace: BF, fontSize: 12, color: BODY, lineSpacingMultiple: 1.2, margin: 0 });
box(6.9, 2.15, 5.5, 2.2, HILO);
s.addText("② Độ hoàn thành tác vụ (Step-SR, teacher-forced)", { x: 7.2, y: 2.3, w: 5.1, h: 0.4, fontFace: TF, fontSize: 14.5, bold: true, color: INK, margin: 0 });
s.addText("(bước thực hiện đúng) / (bước của quỹ đạo vàng)", { x: 7.2, y: 2.75, w: 5.0, h: 0.4, fontFace: BF, fontSize: 12.5, bold: true, color: BODY, margin: 0 });
s.addText("Một bước đúng khi: đúng loại thao tác và điểm bấm sai lệch không quá 14% kích thước màn. Đây là bằng chứng định lượng cho mức độ đạt mục tiêu — điều nhánh một màn chưa đo được.", { x: 7.2, y: 3.2, w: 5.0, h: 1.1, fontFace: BF, fontSize: 12, color: BODY, lineSpacingMultiple: 1.2, margin: 0 });
panel(M, 4.55, W - 2 * M, 1.85, FILL);
s.addText("Căn cứ", { x: M + 0.3, y: 4.68, w: 11, h: 0.35, fontFace: TF, fontSize: 15.5, bold: true, color: ACCENT, margin: 0 });
s.addText("•  Độ đúng thứ tự đo riêng năng lực sắp xếp; nhãn “cặp bắt buộc” suy từ quỹ đạo vàng theo quy tắc nhân quả, không lấy từ mô hình → độc lập với đối tượng được chấm.\n•  Độ hoàn thành đo mức đạt mục tiêu. Căn cứ: ngưỡng dung sai 14% (AITW, NeurIPS 2023); độ tương quan thứ-tự-bộ-phận (Fagin et al., 2003).", { x: M + 0.3, y: 5.08, w: 11.3, h: 1.25, fontFace: BF, fontSize: 12.5, color: BODY, lineSpacingMultiple: 1.3, margin: 0 });
pageNum();

// ============================================================ S14 · TÍNH HỢP LỆ
base("Tính hợp lệ của đánh giá", "Chống vòng lặp luận lý và kiểm định thước đo");
box(M, 2.15, 5.6, 2.55);
s.addText("Tách công cụ quyết định và chấm điểm", { x: M + 0.3, y: 2.3, w: 5.0, h: 0.7, fontFace: TF, fontSize: 15, bold: true, color: INK, margin: 0 });
s.addText("Lá chắn chính: con số công bố là tỉ lệ ảo giác của bản sinh gốc, không phải con số gần 100% sau hiệu chỉnh. Bổ trợ: công cụ quyết định và công cụ chấm điểm khác nhau, kèm một bộ thẩm định khác họ.", { x: M + 0.3, y: 3.0, w: 5.0, h: 1.6, fontFace: BF, fontSize: 12.5, color: BODY, lineSpacingMultiple: 1.25, margin: 0 });
box(6.9, 2.15, 5.5, 2.55, HILO);
s.addText("Kiểm định độ nhạy bằng nhiễu loạn có kiểm soát", { x: 7.2, y: 2.3, w: 5.0, h: 0.7, fontFace: TF, fontSize: 15, bold: true, color: INK, margin: 0 });
s.addText("Chèn lỗi đã biết vào hướng dẫn đúng rồi kiểm tra thước đo có phát hiện. Thêm nút không tồn tại thì độ trung thực phải giảm; thay tên đồng nghĩa thì độ trung thực giữ nguyên, độ đúng nhãn giảm. Đây là điều kiện cần (độ nhạy), chưa phải tương quan với đánh giá của con người. Tiền lệ: Sai et al., EMNLP 2021.", { x: 7.2, y: 3.0, w: 5.0, h: 1.65, fontFace: BF, fontSize: 11.5, color: BODY, lineSpacingMultiple: 1.2, margin: 0 });
panel(M, 4.9, W - 2 * M, 1.5, FILL);
s.addText("Thiết kế thống kê", { x: M + 0.3, y: 5.02, w: 11, h: 0.35, fontFace: BF, fontSize: 13.5, bold: true, color: STEEL, margin: 0 });
s.addText("Tính khoảng tin cậy theo cụm ứng dụng (các màn cùng ứng dụng không độc lập) · khoảng tin cậy 95% · hiệu chỉnh đa kiểm định Holm · cố định hạt giống ngẫu nhiên · đăng ký giả thuyết và ngưỡng trước khi quan sát kết quả.", { x: M + 0.3, y: 5.4, w: 11.3, h: 1.0, fontFace: BF, fontSize: 12.5, color: BODY, lineSpacingMultiple: 1.25, margin: 0 });
pageNum();

// ============================================================ S15 · KẾT QUẢ SƠ BỘ
base("Kết quả sơ bộ", "Số liệu ban đầu — nêu rõ phạm vi");
panel(M, 2.15, W - 2 * M, 1.75, FILL);
s.addText("Chạy thử trên mô hình gpt-4o-mini (nhánh một màn):", { x: M + 0.3, y: 2.3, w: 11, h: 0.35, fontFace: TF, fontSize: 15.5, bold: true, color: INK, margin: 0 });
s.addText("•  Tỉ lệ ảo giác của bản sinh gốc đáng kể — khoảng một phần tư số bước có tham chiếu nút.\n•  Lớp đối chiếu nâng độ trung thực ở mọi ngưỡng; cái giá là khoảng 19% số bước chuyển sang mô tả khái quát.", { x: M + 0.3, y: 2.72, w: 11.3, h: 1.1, fontFace: BF, fontSize: 14, color: BODY, lineSpacingMultiple: 1.3, margin: 0 });
panel(M, 4.1, W - 2 * M, 1.2, HILO);
s.addText("Phạm vi trung thực của con số", { x: M + 0.3, y: 4.22, w: 11, h: 0.35, fontFace: BF, fontSize: 13.5, bold: true, color: ACCENT, margin: 0 });
s.addText("Mẫu nhỏ · một mô hình · khoảng tin cậy còn chạm 0 → đang chạy bản chính trên hơn 80 màn của 17 ứng dụng, tính khoảng tin cậy theo cụm ứng dụng.", { x: M + 0.3, y: 4.58, w: 11.3, h: 0.65, fontFace: BF, fontSize: 13.5, color: BODY, lineSpacingMultiple: 1.15, margin: 0 });
s.addText("Nhánh nhiều màn (độ đúng thứ tự và độ hoàn thành tác vụ) đang được triển khai. Buổi này trình thiết kế và kết quả sơ bộ; con số định lượng đầy đủ sẽ bổ sung.", { x: M, y: 5.55, w: 11.5, h: 0.6, fontFace: BF, fontSize: 13, italic: true, color: MUTE, lineSpacingMultiple: 1.15, margin: 0 });
pageNum();

// ============================================================ S16 · GIỚI HẠN
base("Trung thực học thuật", "Giới hạn được nêu chủ động");
const lims = [
  "Nhánh một màn chỉ đo độ trung thực với giao diện, chưa đo mức đúng ý định; mức đúng ý định được đo ở nhánh nhiều màn qua độ hoàn thành tác vụ.",
  "Độ trung thực đạt gần 100% sau đối chiếu là trần do thiết kế; do đó báo cáo tỉ lệ ảo giác của bản sinh gốc và cái giá kèm theo (tỉ lệ bước phải chuyển sang mô tả khái quát).",
  "Danh sách nút thật có thể thiếu hoặc nhãn không đầy đủ (nút chỉ hiện sau khi cuộn, nhãn chung kiểu “Button”); các nút nhãn chung được loại khỏi mẫu số độ trung thực và độ phủ nhãn được đo, báo cáo để tránh phạt oan bước đúng.",
  "Triển khai từ ảnh đơn thuần cần bộ dò nút và chịu sai số; độ bao phủ được đo trước (điều kiện K1). Trên thiết bị, cây trợ năng do hệ điều hành cung cấp trực tiếp.",
  "Chưa có bảng số định lượng tiếng Việt do thiếu dữ liệu chuẩn; phần định lượng chạy trên dữ liệu tiếng Anh, tiếng Việt dừng ở minh hoạ định tính.",
];
lims.forEach((t, i) => { const y = 2.2 + i * 0.92; vrule(M, y + 0.05, 0.68, STEEL); s.addText(t, { x: M + 0.28, y: y, w: 11.4, h: 0.88, fontFace: BF, fontSize: 13.5, color: BODY, valign: "middle", lineSpacingMultiple: 1.15, margin: 0 }); });
pageNum();

// ============================================================ S16 · KẾT
s = pres.addSlide(); s.background = { color: INK };
s.addShape(pres.shapes.RECTANGLE, { x: M, y: 2.3, w: 0.9, h: 0.08, fill: { color: ACCENT }, line: { type: "none" } });
s.addText("KẾT LUẬN", { x: M, y: 2.5, w: 11, h: 0.4, fontFace: BF, fontSize: 13, bold: true, color: "E7B6BF", charSpacing: 3 });
s.addText("Trong điều kiện không có bản hướng dẫn mẫu, luận văn neo vào danh sách nút thật do nền tảng cung cấp — chỉ dùng khi đánh giá, không cung cấp cho mô hình khi sinh.", { x: M, y: 2.95, w: 11.5, h: 1.6, fontFace: TF, fontSize: 22, bold: true, color: WHITE, lineSpacingMultiple: 1.15 });
s.addText("Hai đóng góp song song: một hệ thống sinh hướng dẫn giảm ảo giác giao diện, và một phương pháp đánh giá độc lập với công cụ sinh, tự kiểm định độ nhạy và nêu rõ giới hạn.", { x: M, y: 4.85, w: 11.5, h: 1.4, fontFace: BF, fontSize: 16, color: "C9D0D7", lineSpacingMultiple: 1.3 });

pres.writeFile({ fileName: "../LUAN_VAN_SLIDE.pptx" }).then(f => console.log("DONE ->", f)).catch(e => console.error("ERR", e));
