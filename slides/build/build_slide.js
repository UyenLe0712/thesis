// Deck v9 - PPTX theo style bài giảng mẫu (Beamer cổ điển): khổ 4:3, thanh tiêu đề chàm 322164,
// khối xám E9E8EC bo góc đổ bóng, chữ serif, footline 4 ô. Nội dung theo report/103 (bản 3/8).
// Bản 2 (4/8): rút gọn chữ ~40%, chi tiết dồn xuống speaker notes, bỏ từ gượng.
// Xuất: ../LUAN_VAN_SLIDE.pptx + _preview/preview.html
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const pres = new pptxgen();
pres.defineLayout({ name: "A43", width: 10, height: 7.5 });
pres.layout = "A43";
pres.author = "Luan van thac si";
pres.title = "Sinh huong dan su dung phan mem tu anh man hinh";

const TF = "Cambria", MONO = "Consolas";
const NAVY = "322164", INK = "1A1A1A";
const FOOTA = "191132", FOOTB = "25194B", FOOTC = "4F417A", FOOTD = "7A7099";
const BLOCK = "E9E8EC", TEAL = "006666", BLUE = "1414BE", RED = "B22222", MAROON = "990000";
const WHITE = "FFFFFF";
const W = 10, H = 7.5, M = 0.55;

const PX = 96;
const FMAP = { "Cambria": "'DejaVu Serif',Georgia,serif", "Consolas": "'DejaVu Sans Mono',monospace" };
let htmlSlides = [], cur = "";
function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
function plain(c) { return typeof c === "string" ? c : c.map(r => r.text).join(""); }
function hpush(html) { cur += html; }
let s, PAGE = 0, TOTAL = 27;
function slide() { if (cur) htmlSlides.push(cur + "</div>"); s = pres.addSlide(); s.background = { color: WHITE }; cur = `<div class="slide" style="background:#fff">`; }
function done() { if (cur) { htmlSlides.push(cur + "</div>"); cur = ""; } }
function text(content, o) {
  const opt = Object.assign({ x: 0, y: 0, w: 4, h: 1, fontSize: 13, color: INK, fontFace: TF, align: "left", valign: "top", margin: o.margin != null ? o.margin : 4 }, o);
  if (o.lh) opt.lineSpacingMultiple = o.lh;
  s.addText(content, opt);
  const jc = opt.align === "center" ? "center" : opt.align === "right" ? "flex-end" : "flex-start";
  const ai = opt.valign === "middle" ? "center" : opt.valign === "bottom" ? "flex-end" : "flex-start";
  const pad = (opt.margin || 0) / PX;
  const st = `position:absolute;left:${opt.x * PX}px;top:${opt.y * PX}px;width:${opt.w * PX}px;height:${opt.h * PX}px;display:flex;justify-content:${jc};align-items:${ai};padding:${pad}in;box-sizing:border-box;font-family:${FMAP[opt.fontFace] || FMAP[TF]};font-size:${opt.fontSize}px;color:#${opt.color};text-align:${opt.align};line-height:${o.lh || 1.2};` + (opt.bold ? "font-weight:700;" : "") + (opt.italic ? "font-style:italic;" : "");
  hpush(`<div style="${st}"><div style="white-space:pre-line;width:100%">${esc(plain(content))}</div></div>`);
}
function rect(x, y, w, h, fill, o) {
  o = o || {};
  const shp = o.radius ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE;
  const p = { x, y, w, h, fill: fill === "none" ? { type: "none" } : { color: fill }, line: o.line ? { color: o.line, width: o.lw || 1 } : { type: "none" } };
  if (o.radius) p.rectRadius = o.radius;
  if (o.shadow) p.shadow = { type: "outer", color: "8C8C99", blur: 5, offset: 2.5, angle: 45, opacity: 0.45 };
  s.addShape(shp, p);
  const st = `position:absolute;left:${x * PX}px;top:${y * PX}px;width:${w * PX}px;height:${h * PX}px;` + (fill === "none" ? "" : `background:#${fill};`) + (o.radius ? `border-radius:${o.radius * PX}px;` : "") + (o.line ? `border:${o.lw || 1}px solid #${o.line};box-sizing:border-box;` : "") + (o.shadow ? "box-shadow:2px 2px 5px rgba(140,140,153,.45);" : "");
  hpush(`<div style="${st}"></div>`);
}
function arrow(x, y, w, c) {
  s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: c || FOOTC, width: 2, endArrowType: "triangle" } });
  hpush(`<div style="position:absolute;left:${x * PX}px;top:${y * PX - 1}px;width:${w * PX}px;height:0;border-top:2px solid #${c || FOOTC}"></div>`);
}
function note(t) { s.addNotes(t.trim()); }

// thanh tiêu đề chàm chạy hết chiều ngang (như frametitle của mẫu)
function bar(t) {
  rect(0, 0, W, 0.6, NAVY);
  text(t, { x: 0.22, y: 0, w: W - 0.44, h: 0.6, fontSize: 19, bold: true, color: WHITE, valign: "middle", margin: 0 });
}
// footline 4 ô
function foot() {
  PAGE++;
  const yy = H - 0.26, hh = 0.26;
  rect(0, yy, 3.0, hh, FOOTA);
  rect(3.0, yy, 3.7, hh, FOOTB);
  rect(6.7, yy, 1.9, hh, FOOTC);
  rect(8.6, yy, 1.4, hh, FOOTD);
  text("luận văn thạc sĩ", { x: 0, y: yy, w: 3.0, h: hh, fontSize: 8, color: WHITE, align: "center", valign: "middle", margin: 0, fontFace: MONO });
  text("Sinh hướng dẫn sử dụng phần mềm", { x: 3.0, y: yy, w: 3.7, h: hh, fontSize: 8, color: WHITE, align: "center", valign: "middle", margin: 0 });
  text("Lê Đoàn Phương Uyên", { x: 6.7, y: yy, w: 1.9, h: hh, fontSize: 8, color: WHITE, align: "center", valign: "middle", margin: 0 });
  text(`${PAGE}/${TOTAL}`, { x: 8.6, y: yy, w: 1.4, h: hh, fontSize: 8, color: WHITE, align: "center", valign: "middle", margin: 0 });
}
// khối xám bo góc đổ bóng (như block của mẫu)
function block(x, y, w, h) { rect(x, y, w, h, BLOCK, { radius: 0.06, shadow: true }); }

// ═══════════════ 1 · BÌA ═══════════════
slide();
rect(0, 0, W, 0.66, NAVY);
text("LUẬN VĂN THẠC SĨ  -  CÔNG NGHỆ THÔNG TIN  -  2026", { x: 0, y: 0, w: W, h: 0.66, fontSize: 17, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
rect(0.8, 1.25, W - 1.6, 2.5, NAVY, { radius: 0.09, shadow: true });
text("Đề tài", { x: 0.8, y: 1.55, w: W - 1.6, h: 0.4, fontSize: 16, bold: true, color: WHITE, align: "center", margin: 0 });
text("SINH HƯỚNG DẪN SỬ DỤNG\nPHẦN MỀM TỪ ẢNH MÀN HÌNH", { x: 0.8, y: 2.15, w: W - 1.6, h: 1.3, fontSize: 26, bold: true, color: WHITE, align: "center", margin: 0, lh: 1.25 });
text("Học viên:  Lê Đoàn Phương Uyên          GVHD:  . . . . . . . . . . . . . . .", { x: 0.8, y: 4.45, w: W - 1.6, h: 0.4, fontSize: 14, bold: true, color: INK, align: "center", margin: 0 });
text("Trường Đại học . . . . . . . . . . . . . . . . . . . . . . . .", { x: 0.8, y: 5.15, w: W - 1.6, h: 0.35, fontSize: 12, color: INK, align: "center", margin: 0 });
text("- - - -  Năm 2026  - - - -", { x: 0.8, y: 5.65, w: W - 1.6, h: 0.35, fontSize: 12, color: INK, align: "center", margin: 0 });
foot(); done();

// ═══════════════ 2 · NỘI DUNG ═══════════════
slide();
bar("Nội dung");
block(M, 1.0, W - 2 * M, 0.72);
text([{ text: "Đề tài.  ", options: { bold: true, color: RED } }, { text: "NHÌN ẢNH MÀN HÌNH, VIẾT HƯỚNG DẪN CHO NGƯỜI ĐỌC", options: { bold: true, color: BLUE } }], { x: M + 0.2, y: 1.0, w: W - 2 * M - 0.4, h: 0.72, fontSize: 14, valign: "middle", margin: 0 });
const toc = ["Bài toán, và cái khó nằm ở đâu", "Chấm bằng cách nào", "Dạy mô hình thế nào", "Thiết kế so sánh", "Đã làm được tới đâu", "Giới hạn và việc còn lại"];
toc.forEach((t, i) => {
  text([{ text: (i + 1) + ".", options: { bold: true, color: TEAL } }, { text: "   " + t, options: { bold: true, color: NAVY } }], { x: 1.5, y: 2.2 + i * 0.72, w: 7, h: 0.5, fontSize: 17, margin: 0 });
});
foot(); done();

// ═══════════════ 4 · BÀI TOÁN ═══════════════
slide();
bar("Bài toán");
block(M, 1.1, W - 2 * M, 1.0);
text("Người dùng bí trong một ứng dụng: chụp màn hình, đặt câu hỏi", { x: M + 0.22, y: 1.1, w: W - 2 * M - 0.44, h: 1.0, fontSize: 14.5, valign: "middle", margin: 0, lh: 1.35 });
block(M, 2.45, W - 2 * M, 1.5);
text([{ text: "Ví dụ.  ", options: { bold: true, color: BLUE } }, { text: "“Làm sao chia sẻ playlist này cho bạn tôi?”", options: { italic: true } }], { x: M + 0.22, y: 2.65, w: W - 2 * M - 0.44, h: 0.5, fontSize: 14.5, margin: 0 });
text("→  “Chạm vào biểu tượng chia sẻ ở góc trên bên phải màn hình.”", { x: M + 0.94, y: 3.25, w: W - 2 * M - 1.2, h: 0.55, fontSize: 14.5, italic: true, margin: 0 });
text([{ text: "Mô hình giao diện hiện nay:  ", options: { bold: true, color: TEAL } }, { text: "tự bấm thay người, đầu ra là toạ độ nút cần bấm, dạng  click(732, 173)\nLuận văn: đầu ra là câu chữ cho người đọc", options: {} }], { x: M, y: 4.4, w: W - 2 * M, h: 1.0, fontSize: 14.5, margin: 0, lh: 1.4 });
text("Cỡ mô hình nhắm tới chạy tại máy người dùng, không gọi dịch vụ ngoài", { x: M, y: 5.75, w: W - 2 * M, h: 0.5, fontSize: 14, italic: true, color: MAROON, margin: 0 });
note(`Mở đầu bằng tình huống thật. Nhấn chỗ khác biệt: cả dòng nghiên cứu đang làm agent bấm máy (đầu ra kiểu click(732,173)), còn đề tài này sinh câu chữ. Chạy offline nghĩa là ảnh màn hình - thứ hay chứa thông tin riêng tư - không phải gửi đi đâu; đó là lý do tồn tại của mô hình nhỏ.`);
foot(); done();

// ═══════════════ 4 · ĐÃ CÓ AI LÀM CHƯA ═══════════════
slide();
bar("Đã có ai làm chưa?");
text("Các nghiên cứu trước", { x: M, y: 0.95, w: 4.35, h: 0.4, fontSize: 15, bold: true, color: NAVY, align: "center", margin: 0 });
text("Luận văn này", { x: 5.1, y: 0.95, w: 4.35, h: 0.4, fontSize: 15, bold: true, color: RED, align: "center", margin: 0 });
block(M, 1.42, 4.35, 2.75);
block(5.1, 1.42, 4.35, 2.75);
const cmpL = ["UI-Ins, Aguvis:  sinh toạ độ để máy bấm,\nchất lượng câu không được đánh giá", "AndroidControl (NeurIPS 24):\ncâu người viết dùng làm đầu vào", "GuideMe (CHI 2026):  gọi\nGPT-5, không huấn luyện gì"];
const cmpR = ["Sinh câu cho người đọc,\ncâu là thứ duy nhất đem chấm", "Dùng chính câu đó\nlàm đích để sinh", "Huấn luyện mô hình riêng,\ncó thước chấm định lượng"];
cmpL.forEach((t, i) => text(t, { x: M + 0.25, y: 1.6 + i * 0.87, w: 3.9, h: 0.8, fontSize: 12.5, margin: 0, lh: 1.35 }));
cmpR.forEach((t, i) => text(t, { x: 5.35, y: 1.6 + i * 0.87, w: 3.9, h: 0.8, fontSize: 12.5, margin: 0, lh: 1.35 }));
block(M, 4.5, W - 2 * M, 1.2);
text([{ text: "Vị trí:  ", options: { bold: true, color: BLUE } }, { text: "mô hình mở đầu tiên được huấn luyện cho tác vụ này.", options: { bold: true } }], { x: M + 0.22, y: 4.5, w: W - 2 * M - 0.44, h: 1.2, fontSize: 14.5, valign: "middle", margin: 0, lh: 1.35 });
note(`Slide chặn trước câu hỏi về tính mới. Ba hàng là ba phía đã kiểm độc lập, tận trang gốc từng bài. GuideMe là bài sát nhất: họ prompting GPT-5 qua mạng, đánh giá bằng khảo sát 18 người dùng, không có thước nào chấm chất lượng câu - mình huấn luyện và có thước định lượng, đó là ranh giới. Các cơ chế bên trong đều có tiền lệ, sẽ khai rõ ở phần sau, không nhận chữ "mới" cho chúng.`);
foot(); done();

// ═══════════════ 6 · DỮ LIỆU ═══════════════
slide();
bar("Dữ liệu:  AndroidControl");
block(M, 1.1, W - 2 * M, 2.15);
text("15.283 tác vụ do người thật thao tác trên Android (NeurIPS 2024). Mỗi bước có:", { x: M + 0.22, y: 1.24, w: W - 2 * M - 0.44, h: 0.55, fontSize: 14, margin: 0, lh: 1.3 });
["ảnh màn hình", "toạ độ chỗ người đó chạm", "câu mô tả do chính người đó viết"].forEach((t, i) => {
  text("-  " + t, { x: M + 0.5, y: 1.88 + i * 0.42, w: W - 2 * M - 1, h: 0.4, fontSize: 13.5, margin: 0 });
});
block(M, 3.55, W - 2 * M, 1.75);
text([{ text: "Nhưng câu người viết rất cụt", options: { bold: true, color: RED } }, { text: " - trung vị chỉ 6 từ:", options: {} }], { x: M + 0.22, y: 3.7, w: W - 2 * M - 0.44, h: 0.5, fontSize: 14, margin: 0 });
text("“click on OK”      “Click on the screen.”      “Select the search result”", { x: M, y: 4.3, w: W - 2 * M, h: 0.5, fontSize: 15, italic: true, align: "center", margin: 0 });
note(`Toạ độ chạm là nhãn sạch tuyệt đối, phủ 100% bước chạm - cách huấn luyện thường bỏ phí nguồn này, còn đề tài dùng nó làm ô toạ độ trong dòng khai báo. Câu người viết cụt (gần nửa dưới 5 từ) là lý do có khâu viết lại: cho học bắt chước nguyên bản thì mô hình học đúng giọng cụt đó.`);
foot(); done();

// ═══════════════ 7 · BỆNH ĐÃ CHẨN ═══════════════
slide();
bar("Mô hình thường sai kiểu gì?");
block(M, 1.1, W - 2 * M, 1.45);
text("Soi tay 40 ca sai: bịa nút không có thật chỉ 0-2%\nLỗi số một là câu mơ hồ - “biểu tượng tìm kiếm” khi màn có hai biểu tượng tìm kiếm", { x: M + 0.22, y: 1.1, w: W - 2 * M - 0.44, h: 1.45, fontSize: 14, valign: "middle", margin: 0, lh: 1.4 });
block(M, 2.9, W - 2 * M, 1.9);
text("300 câu chuẩn của tập kiểm, chấm bằng đúng cách sẽ chấm mô hình - chia đôi theo độ dài:", { x: M + 0.22, y: 3.05, w: W - 2 * M - 0.44, h: 0.5, fontSize: 13.5, margin: 0 });
text([{ text: "câu ngắn  ", options: {} }, { text: "62%", options: { bold: true, color: MAROON, fontSize: 24 } }, { text: "        câu dài hơn  ", options: {} }, { text: "79%", options: { bold: true, color: NAVY, fontSize: 24 } }], { x: M, y: 3.6, w: W - 2 * M, h: 0.7, fontSize: 15, align: "center", valign: "middle", margin: 0 });
text("Cả hai mức đóng góp đều nhắm vào lỗi mơ hồ này  ·  trung bình hai nhóm = 70%, xem slide sau", { x: M, y: 5.15, w: W - 2 * M, h: 0.5, fontSize: 14, bold: true, color: NAVY, margin: 0 });
note(`Cặp 62/79 đo ngày 12/8 trên 300 bước của tập kiểm, bằng CHÍNH bộ trỏ UGround và CHÍNH luật chấm sẽ dùng cho kết quả (ô Voronoi), chia đôi theo trung vị 7 từ. Trung bình hai nhóm ra đúng 70,0% - tức là con số "điểm cao nhất 70" ở slide sau chính là hai số này gộp lại. Bản cũ là 32/69 nhưng đo bằng gpt-4o-mini trên 76 câu với luật chấm khác - bộ trỏ yếu hơn nhiều nên khoảng cách bị thổi rộng; số mới đáng tin hơn và vẫn cùng chiều. Đã kiểm nhiễu "câu dài hay đi kèm nút dễ trỏ hơn" và kết quả NGƯỢC lại: nhóm câu dài nhắm nút KHÓ hơn - chỉ 65,2% nút có tên so với 76,7% ở nhóm ngắn, cỡ nút trung vị 0,007 màn so với 0,015, khoảng cách tới nút hàng xóm như nhau (168 vs 169 px). Lọc chỉ giữ nút có tên thì khoảng cách vẫn còn: 59,0% so với 79,3%. Tức nhiễu chạy ngược chiều hiệu ứng, không phải cùng chiều. Giới hạn CÒN LẠI phải khai: đây là quan sát trên câu chuẩn, không phải thí nghiệm. Phép thử nhân quả thật chính là so S1 với S2.`);
foot(); done();

// ═══════════════ BẢN LỀ · HAI VIỆC PHẢI LÀM ═══════════════
slide();
bar("Hai việc phải làm");
block(M, 1.6, W - 2 * M, 2.0);
text("1", { x: M + 0.3, y: 1.6, w: 0.6, h: 1.75, fontSize: 30, bold: true, color: TEAL, valign: "middle", margin: 0 });
text("Chấm bằng cách nào?", { x: M + 1.0, y: 1.95, w: 6.5, h: 0.5, fontSize: 16, bold: true, color: NAVY, margin: 0 });
text("Có câu chuẩn do người viết, nhưng SO CHỮ với nó thì không dùng được:\nđo trên 51 ca thật, AUC 0,34 - tệ hơn đoán mò.", { x: M + 1.0, y: 2.5, w: W - 2 * M - 1.3, h: 0.9, fontSize: 13.5, margin: 0, lh: 1.4 });
block(M, 4.1, W - 2 * M, 2.0);
text("2", { x: M + 0.3, y: 4.1, w: 0.6, h: 1.75, fontSize: 30, bold: true, color: TEAL, valign: "middle", margin: 0 });
text("Dạy thế nào cho câu bớt mơ hồ?", { x: M + 1.0, y: 4.45, w: 6.5, h: 0.5, fontSize: 16, bold: true, color: NAVY, margin: 0 });
text("Dạy thẳng ra câu thì mô hình không bị buộc phải phân biệt\nnút đích với mấy nút giống nó bên cạnh.", { x: M + 1.0, y: 5.0, w: W - 2 * M - 1.3, h: 0.9, fontSize: 13.5, margin: 0, lh: 1.4 });
note(`⚠ Câu hỏi chắc chắn bị hỏi: "AndroidControl CÓ câu chuẩn mà, sao không so với nó?" — trả lời: có, nhưng so chữ với câu chuẩn đã ĐO và RỚT. Trên 51 ca viết tay, AUC 0,336, tức tệ hơn đoán mò. Lý do bản chất: embedding đo độ gần CHỦ ĐỀ, nên "inbox ↔ outbox" (hai nút KHÁC nhau) được 0,76, cao hơn "search ↔ magnifying glass" (CÙNG một nút) chỉ 0,55. Cùng-nút trung bình 0,62 mà khác-nút trung bình 0,67 - khác-nút còn cao hơn. Không ngưỡng nào tách được, hạ ngưỡng chỉ làm lọt nhiều hơn. Đó là lý do phải đổi sang cách chấm bằng bộ trỏ: không so chữ với chữ, mà xem câu có dẫn được tới đúng nút không.

Slide bản lề, đặt ở đây để người nghe có khung bám. Vì sao chấm trước dạy sau: thước đo là thứ quyết định có kết luận được gì không, và nó cũng là chỗ rủi ro nhất - nếu thước hỏng thì mọi việc phía sau vô nghĩa. Đó cũng là lý do trình tự thật của dự án là kiểm thước xong mới huấn luyện.`);
foot(); done();

// ═══════════════ 16 · CÁCH CHẤM ═══════════════
slide();
bar("Chấm bằng cách nào khi không có đáp án chuẩn?");
block(M, 1.0, W - 2 * M, 1.15);
text([{ text: "Bộ trỏ  ", options: { bold: true, color: RED } }, { text: "= mô hình chuyên làm ĐÚNG MỘT VIỆC:  đọc một câu, chỉ ra toạ độ trên ảnh.", options: {} }], { x: M + 0.22, y: 1.0, w: W - 2 * M - 0.44, h: 0.55, fontSize: 14.5, valign: "middle", margin: 0 });
text("UGround-2B · khác họ với mô hình đem chấm · đã kiểm: không học AndroidControl", { x: M + 0.35, y: 1.55, w: W - 2 * M - 0.7, h: 0.5, fontSize: 12.5, italic: true, color: FOOTC, margin: 0 });
const bcs = [["câu mô hình viết", BLOCK, INK], ["bộ trỏ", NAVY, WHITE], ["một điểm (x, y)", BLOCK, INK]];
bcs.forEach((t, i) => {
  const x = 0.75 + i * 3.05;
  if (t[1] === NAVY) rect(x, 2.45, 2.5, 0.7, NAVY, { radius: 0.06, shadow: true }); else block(x, 2.45, 2.5, 0.7);
  text(t[0], { x, y: 2.45, w: 2.5, h: 0.7, fontSize: 13, bold: true, color: t[2], align: "center", valign: "middle", margin: 0 });
  if (i < 2) arrow(x + 2.55, 2.8, 0.45);
});
block(M, 3.55, W - 2 * M, 1.05);
text([{ text: "Tính ĐÚNG khi:  ", options: { bold: true, color: TEAL } }, { text: "điểm đó rơi vào đúng nút mà người thật đã chạm.", options: {} }], { x: M + 0.22, y: 3.55, w: W - 2 * M - 0.44, h: 1.05, fontSize: 14.5, valign: "middle", margin: 0 });
text("Barem là toạ độ người dùng đã chạm, có sẵn trong dữ liệu - không mô hình nào tự cho điểm.\nCâu tốt = câu mà người chưa biết đáp án vẫn lần ra đúng nút.  Cách chấm này có từ 2016.", { x: M, y: 4.8, w: W - 2 * M, h: 0.9, fontSize: 13, italic: true, margin: 0, lh: 1.45 });
note(`Đây là chỗ hay bị hỏi nhất. Phân biệt cho rõ: LLM-as-a-judge là hỏi mô hình "câu này mấy điểm" - cần rubric, và mô hình có thể ảo giác hoặc thiên vị. Cách của luận văn: không hỏi ý kiến mô hình nào, bắt bộ trỏ LÀM một việc rồi so kết quả với toạ độ gold. Nó ảo giác thì trỏ trượt, mà trỏ trượt thì thành kết oan câu đúng - đó chính là hai tiêu chí rớt ở slide sau, và là lý do có cổng sai số 3%. Ba tinh chỉnh trong mã: tính trúng theo nút gần nhất (dung sai vòng tròn quá dễ dãi, 63% bước có nút khác lọt vòng) · gom tap/click/open · luật riêng cho công tắc bật/tắt. Bộ trỏ khác họ với mô hình được chấm, và không đưa vào vòng huấn luyện vì nó là giám khảo.`);
foot(); done();

// ═══════════════ 17 · THƯỚC ĐÁNG TIN ═══════════════
slide();
bar("Thước đo này có đáng tin không?");
block(M, 1.1, W - 2 * M, 2.35);
text("Cấy lỗi biết trước vào câu, xem thước có bắt được không: đạt 8/10.\nHai tiêu chí chưa đạt:", { x: M + 0.22, y: 1.22, w: W - 2 * M - 0.44, h: 0.8, fontSize: 14, margin: 0, lh: 1.4 });
text("-  Bộ trỏ lệch 3% thì kết oan 0% số câu đúng; lệch 8% thì oan 24%\n    → đặt sai số 3% thành CỔNG bắt buộc, phải qua mới được chạy tiếp", { x: M + 0.35, y: 2.1, w: W - 2 * M - 0.7, h: 0.9, fontSize: 13.5, margin: 0, lh: 1.45 });
text("-  Luật bắt từ ngược nghĩa chỉ bắt được cặp có sẵn trong bảng", { x: M + 0.35, y: 3.0, w: W - 2 * M - 0.7, h: 0.45, fontSize: 13.5, margin: 0 });
block(M, 3.8, W - 2 * M, 1.35);
text([{ text: "Cổng đã kiểm ngày 9/8:  ĐẠT.  ", options: { bold: true, color: RED } }, { text: "Sai số trung vị 0,7% - ngưỡng 3%.\nXác nhận thêm bằng dụng cụ thật: dưới 3% thì 100% số ca chấm đúng (n = 188).", options: {} }], { x: M + 0.22, y: 3.8, w: W - 2 * M - 0.44, h: 1.35, fontSize: 13.5, valign: "middle", margin: 0, lh: 1.4 });
text("Sẽ làm khi có câu mô hình sinh: chấm tay 100 câu (hai người) · cắt theo độ dài câu · báo hai cách chấm", { x: M, y: 5.35, w: W - 2 * M, h: 0.5, fontSize: 12.5, italic: true, margin: 0 });
note(`Phương pháp bơm lỗi lấy từ Sai và cộng sự, EMNLP 2021 - không tự nghĩ ra cách kiểm. Mười tiêu chí chia hai nhóm: ba tiêu chí "không được kết oan câu đúng" và bảy tiêu chí "phải bắt được lỗi". Ngưỡng đậu rớt khoá cứng trong mã trước khi chạy.

ĐƯỜNG CONG KẾT OAN đo thế nào, nếu thầy hỏi: lấy câu ĐÚNG (viết lại cùng nghĩa từ câu chuẩn), rồi cố ý dời điểm trỏ ra xa chỗ người chạm đúng x% bề ngang màn, xem thước có đánh rớt oan câu đó không. Chạy ở các mức 1, 3, 5, 8, 13%. Kết quả trên dụng cụ thật (cây trợ năng + Voronoi): 3% -> 0%, 5% -> 7,5%, 8% -> 24,1%, 13% -> 55%. Vì vậy 3% thành ngưỡng cổng: dưới mức đó thước gần như không kết oan.

⚠ ĐỪNG dùng bộ số cũ 3% -> 2,6% / 8% -> 42%: bộ đó đo trên hộp OmniParser với luật hộp-gần-nhất, không phải dụng cụ sẽ chấm, và đã bị rút (report/108).

TIÊU CHÍ RỚT THỨ HAI: luật bắt câu đảo nghĩa chỉ dò theo một bảng cặp từ soạn tay - on/off, enable/disable, show/hide, mute/unmute, expand/collapse, check/uncheck, select/deselect, start/stop. Cặp nào ngoài bảng, ví dụ next/previous hay add/remove, thì thước không thấy. Khai thẳng chứ không nhét thêm từ vào bảng cho điểm đẹp.`);
foot(); done();

// ═══════════════ 18 · TRẦN CỦA THƯỚC (mới ở v10) ═══════════════
slide();
bar("Điểm cao nhất thực tế là 70, không phải 100");
block(M, 1.1, W - 2 * M, 1.6);
text("Đem CHÍNH câu người viết đi chấm, bằng đúng cách chấm ở slide trước:", { x: M + 0.22, y: 1.25, w: W - 2 * M - 0.44, h: 0.5, fontSize: 14, margin: 0 });
text([{ text: "bộ trỏ chỉ lần ra đúng nút   ", options: {} }, { text: "70%", options: { bold: true, color: RED, fontSize: 30 } }, { text: "   số bước", options: {} }], { x: M, y: 1.8, w: W - 2 * M, h: 0.75, fontSize: 15, align: "center", valign: "middle", margin: 0 });
block(M, 3.1, W - 2 * M, 1.15);
text("Câu người viết cụt  →  bộ trỏ khó lần ra  →  30% hụt là do dụng cụ, không phải do mô hình", { x: M + 0.22, y: 3.1, w: W - 2 * M - 0.44, h: 1.15, fontSize: 13.5, bold: true, color: NAVY, valign: "middle", align: "center", margin: 0, lh: 1.4 });
block(M, 4.55, W - 2 * M, 1.45);
text([{ text: "Nên đọc kết quả thế nào:   ", options: { bold: true, color: TEAL } }, { text: "mô hình được 55 nghĩa là 55 trên nền 70,\nkhông phải 55 trên 100.  Và con số công bố là HIỆU giữa hai bản.", options: {} }], { x: M + 0.22, y: 4.55, w: W - 2 * M - 0.44, h: 1.45, fontSize: 13.5, valign: "middle", margin: 0, lh: 1.45 });
note(`Cách nói cho dễ hiểu: coi như đề thi này không ai được 10, vì chính đáp án mẫu đem đi chấm cũng chỉ được 7. Ba lý do câu chuẩn mất 30 điểm: câu người viết cụt (trung vị 6 từ), bộ trỏ đôi khi trỏ trượt, và màn hình nhiều nút na ná nhau.

Vì sao phải trình con số này TRƯỚC khi trình kết quả: nếu đợi có điểm rồi mới nói "à nhưng trần chỉ 70" thì nghe như biện bạch. Con số này đo xong ngày 9/8, có ghi ngày trong bản đăng ký.

Nếu thầy hỏi "vậy mô hình có thể vượt 70 không": có thể - nếu nó viết câu rõ hơn cả câu người viết. Đây không phải trần toán học, mà là mốc thực tế vì mô hình học viết theo câu người. Vượt được thì đó là kết quả đáng nói và sẽ khai rõ.

Và vì phép so chính là hiệu giữa hai bản chấm bằng cùng một dụng cụ, phần thiệt chung triệt tiêu trong hiệu số.`);
foot(); done();

// ═══════════════ 8 · PIPELINE TOÀN CẢNH ═══════════════
slide();
bar("Toàn bộ quy trình, nhìn từ trên xuống");
const st1 = [["1. Đọc chữ\ntrên ảnh"], ["2. Dựng dòng\nkhai báo"], ["3. Ghép thành\nbộ dữ liệu"]];
st1.forEach((t, i) => {
  const x = 0.85 + i * 2.95;
  block(x, 1.35, 2.45, 0.95);
  text(t[0], { x, y: 1.35, w: 2.45, h: 0.95, fontSize: 13.5, bold: true, color: NAVY, align: "center", valign: "middle", margin: 0, lh: 1.25 });
  if (i < 2) arrow(x + 2.5, 1.82, 0.4);
});
const st2 = [["4. Huấn luyện\nBản thường  vs\nBản khai báo", 6.75, WHITE, NAVY], ["5. Chạy thật", 3.80, RED, BLOCK]];
st2.forEach(t => {
  if (t[3] === NAVY) rect(t[1], 2.85, 2.45, 0.95, NAVY, { radius: 0.06, shadow: true }); else block(t[1], 2.85, 2.45, 0.95);
  text(t[0], { x: t[1], y: 2.85, w: 2.45, h: 0.95, fontSize: 13.5, bold: true, color: t[2], align: "center", valign: "middle", margin: 0, lh: 1.25 });
});
// mũi tên: 3 xuống 4 (dọc, bên phải), rồi 4 sang 5 (ngang, chỉ sang TRÁI)
s.addShape(pres.shapes.LINE, { x: 7.97, y: 2.34, w: 0, h: 0.48, line: { color: FOOTC, width: 2, endArrowType: "triangle" } });
hpush(`<div style="position:absolute;left:${7.97 * PX}px;top:${2.34 * PX}px;height:${0.48 * PX}px;border-left:2px solid #4F417A"></div>`);
s.addShape(pres.shapes.LINE, { x: 6.3, y: 3.32, w: 0.4, h: 0, line: { color: FOOTC, width: 2, beginArrowType: "triangle" } });
hpush(`<div style="position:absolute;left:${6.3 * PX}px;top:${3.32 * PX - 1}px;width:${0.4 * PX}px;height:0;border-top:2px solid #4F417A"></div>`);
block(M, 4.5, W - 2 * M, 1.25);
text("Khâu 1-3: dựng dữ liệu, tự động hoàn toàn - không dán nhãn tay, không nhãn máy sinh\nKhâu 4: Bản thường (S1) viết thẳng ra câu · Bản khai báo (S2) tả nút trước rồi mới viết câu\n            Hai bản khác nhau đúng một chỗ: đích sinh. Cùng dữ liệu, cùng mô hình gốc.", { x: M + 0.22, y: 4.5, w: W - 2 * M - 0.44, h: 1.25, fontSize: 14, valign: "middle", margin: 0, lh: 1.45 });
note(`Bản đồ cả phần thực nghiệm. Ý cần nhấn: ba khâu đầu kiểm được trước khi huấn luyện, nên sai sót lộ ra sớm. Đích sinh là câu do người thao tác viết, lấy nguyên từ bộ dữ liệu - không có mô hình nào sinh nhãn. Đến khâu 6, trên máy người dùng chỉ còn bộ đọc chữ và mô hình - mọi thứ đắt đỏ chỉ tồn tại lúc dựng dữ liệu và lúc chấm.`);
foot(); done();

// ═══════════════ 9 · KHÂU 1-2 ═══════════════
slide();
bar("Đầu vào và đích sinh:  cái gì có sẵn, cái gì phải dựng");
block(M, 1.05, W - 2 * M, 1.85);
text([{ text: "ĐÍCH SINH  =  câu do chính người thao tác viết", options: { bold: true, color: RED } }], { x: M + 0.22, y: 1.15, w: W - 2 * M - 0.44, h: 0.4, fontSize: 15, margin: 0 });
text("Lấy nguyên từ bộ dữ liệu, không qua mô hình nào.\nKhông có nhãn do máy sinh trong vòng huấn luyện.", { x: M + 0.35, y: 1.6, w: W - 2 * M - 0.7, h: 0.85, fontSize: 13.5, margin: 0, lh: 1.45 });
text('“Click on the search bar”      “open the Clock app”', { x: M + 0.35, y: 2.42, w: W - 2 * M - 0.7, h: 0.4, fontSize: 12.5, color: BLUE, fontFace: MONO, margin: 0 });
block(M, 3.15, W - 2 * M, 1.25);
text([{ text: "Khâu 1 - đọc chữ trên ảnh (OCR).  ", options: { bold: true, color: TEAL } }, { text: "Danh sách chữ + vị trí, nối vào đầu vào.\nChạy ngay trên điện thoại.  Nút hình - dấu cộng, mũi tên - thì OCR chịu.", options: {} }], { x: M + 0.22, y: 3.15, w: W - 2 * M - 0.44, h: 1.25, fontSize: 13.5, valign: "middle", margin: 0, lh: 1.4 });
block(M, 4.65, W - 2 * M, 1.35);
text([{ text: "Giá phải trả:  ", options: { bold: true, color: MAROON } }, { text: "câu người viết rất cụt - trung vị 6 từ, 43% câu từ 5 từ trở xuống.\nMô hình học viết cụt theo.  Đây chính là lý do trần của thước chỉ tới 70%.", options: {} }], { x: M + 0.22, y: 4.65, w: W - 2 * M - 0.44, h: 1.35, fontSize: 13.5, valign: "middle", margin: 0, lh: 1.4 });
note(`Chỗ này phải nói thật rõ vì nó vừa là điểm mạnh vừa là giới hạn. Điểm mạnh: toàn bộ đích sinh là câu người thật viết ra lúc họ đang thao tác - không có mô hình lớn nào viết nhãn, nên không ai vặn được là nhãn máy sinh có sạch không. Giới hạn: câu người viết trung vị chỉ 6 từ và 43% từ 5 từ trở xuống, nên mô hình học viết cụt theo, và đó là lý do đưa chính mấy câu đó cho bộ trỏ thì cũng chỉ lần ra đúng nút 70%. Hai chuyện này là một. Nếu thầy hỏi sao không nhờ mô hình lớn viết lại cho đầy đủ hơn: có cân nhắc, nhưng làm vậy là đưa nhãn máy sinh vào vòng huấn luyện, và phải chứng minh được nó không viết sai - chi phí kiểm lớn hơn cái lợi, nên chọn giữ nguyên câu người viết.`);
foot(); done();

// ═══════════════ 10 · KHÂU 3 (TRỌNG TÂM) ═══════════════
slide();
bar("Ý chính:  tả nút trước, viết câu sau");
block(M, 1.05, W - 2 * M, 0.8);
text("Mô hình phải viết một dòng khai báo bốn ô, rồi mới tới câu:", { x: M + 0.22, y: 1.05, w: W - 2 * M - 0.44, h: 0.8, fontSize: 14, valign: "middle", margin: 0 });
text("[  vai trò  |  tên  |  toạ độ  |  dấu hiệu phân biệt  ]", { x: M, y: 2.03, w: W - 2 * M, h: 0.45, fontSize: 16, bold: true, color: RED, align: "center", margin: 0 });
block(M, 2.68, W - 2 * M, 2.0);
text("Dạy thường", { x: M + 0.22, y: 2.86, w: 1.6, h: 0.4, fontSize: 13, bold: true, color: TEAL, margin: 0 });
text("Click on the search bar at the top of the screen", { x: M + 1.95, y: 2.86, w: W - 2 * M - 2.2, h: 0.4, fontSize: 11.5, fontFace: MONO, margin: 0 });
text("Dạy kiểu mới", { x: M + 0.22, y: 3.42, w: 1.6, h: 0.4, fontSize: 13, bold: true, color: RED, margin: 0 });
text("<desc>ô nhập liệu | Drive C | <point>297,88</point>\n      | ô nhập liệu duy nhất trên màn</desc>\nClick on the search bar at the top of the screen", { x: M + 1.95, y: 3.36, w: W - 2 * M - 2.2, h: 1.2, fontSize: 11.5, fontFace: MONO, margin: 0, lh: 1.4 });
text([{ text: "Toạ độ = chỗ người thật đã chạm, quy về thang 0-1000.  ", options: { bold: true, color: NAVY } }, { text: "Khi chạy thật, dòng khai báo bị cắt - người dùng chỉ nhận câu.", options: {} }], { x: M, y: 4.9, w: W - 2 * M, h: 0.9, fontSize: 14, margin: 0, lh: 1.4 });
note(`Đây là mức 1 của đóng góp. Dòng khai báo tồn tại chỉ để ép mô hình xác định rõ mục tiêu trước khi viết. Toạ độ chạm là nhãn sạch 100% mà cách dạy thường bỏ phí. Ràng buộc "có cấu trúc chặt, có toạ độ" là học từ các bài trước: để bước trung gian là văn tự do thì kết quả âm (slide bằng chứng).`);
foot(); done();

// ═══════════════ 11 · BẰNG CHỨNG CHO THIẾT KẾ ═══════════════
slide();
bar("Vì sao phải tả có cấu trúc và có toạ độ?");
block(M, 1.05, W - 2 * M, 2.35);
text("Kiểu “sinh bước trung gian trước đáp án” đã có nhiều bài thử:", { x: M + 0.22, y: 1.2, w: W - 2 * M - 0.44, h: 0.45, fontSize: 13.5, margin: 0 });
const ev = [
  ["Aguvis (ICML 2025)", "bỏ tầng trung gian, trên chính AndroidControl", "tụt 11,4", MAROON],
  ["GCoT (bản thảo)", "huấn luyện sinh định vị trước", "+4,5 / +5,8", INK],
  ["CogCoM (ICLR 2025)", "chuỗi thao tác trung gian", "+6,6 / +0,2 / +0,9", INK],
  ["Shikra - văn tự do", "bước trung gian viết bằng văn xuôi", "tụt 7,4", MAROON],
  ["Shikra - có toạ độ", "cùng mô hình, chỉ đổi dạng trung gian", "+5,9", TEAL]
];
ev.forEach((r, i) => {
  const y = 1.7 + i * 0.34;
  text(r[0], { x: M + 0.3, y, w: 2.6, h: 0.32, fontSize: 12, bold: true, color: NAVY, margin: 0 });
  text(r[1], { x: M + 3.0, y, w: 4.5, h: 0.32, fontSize: 12, margin: 0 });
  text(r[2], { x: M + 7.55, y, w: 1.2, h: 0.32, fontSize: 12, bold: true, color: r[3], align: "right", margin: 0 });
});
block(M, 3.65, W - 2 * M, 1.55);
text("Bước trung gian phải có cấu trúc và có toạ độ - để là văn xuôi thì kết quả âm\nĐó là lý do dòng khai báo bắt buộc có ô toạ độ", { x: M + 0.22, y: 3.65, w: W - 2 * M - 0.44, h: 1.55, fontSize: 13.5, valign: "middle", margin: 0, lh: 1.45 });
text("Các bài trên: sinh trung gian để ra toạ độ - luận văn: để ra câu chữ cho người đọc", { x: M, y: 5.35, w: W - 2 * M, h: 0.5, fontSize: 13, italic: true, color: MAROON, margin: 0 });
note(`NGUỒN SỐ - thủ sẵn nếu thầy hỏi "in ở đâu trong bài": Aguvis = Table 6, hiệu hai dòng 80,5 - 69,1 · Shikra = Table 1, ba số 88,07 / 80,68 / 93,97 · GCoT = Table 5, cột Average A-Acc 70,0 -> 74,5 và 70,6 -> 76,4 · CogCoM = Table 4, bài in thẳng "↑6.6". Ba trong bốn số là hiệu tự trừ từ bảng của họ, không phải số in sẵn - khai luôn nếu bị vặn. Ảnh bốn bảng gốc nằm ở report/105. Các bài dùng thước khác nhau nên số chỉ nói lên chiều và cỡ, không so thẳng. Nếu thầy hỏi GCoT: số âm hay được trích là ở chế độ prompting mô hình chưa huấn luyện; huấn luyện hẳn thì +4,5/+5,8. Và bảng của họ huấn luyện kèm dữ liệu quen đề nên không tách được nguyên nhân - phép so của mình cùng bộ dữ liệu, chỉ đổi đích sinh, tách được. Chỗ này mình chặt hơn họ.`);
foot(); done();

// ═══════════════ 12 · KHÂU 4 ═══════════════
slide();
bar("Ghép thành bộ dữ liệu dạy");
block(M, 1.1, 4.35, 2.2);
text("ĐỀ BÀI  (đầu vào)", { x: M + 0.2, y: 1.24, w: 4, h: 0.35, fontSize: 12.5, bold: true, color: TEAL, margin: 0 });
text("ảnh màn hình\nmục tiêu của tác vụ\ndanh sách chữ khâu 1 đọc ra", { x: M + 0.2, y: 1.66, w: 4, h: 1.5, fontSize: 13, margin: 0, lh: 1.55 });
arrow(5.0, 2.2, 0.4);
block(5.55, 1.1, 3.9, 2.2);
text("ĐÁP ÁN MẪU  (phải học viết ra)", { x: 5.75, y: 1.24, w: 3.6, h: 0.35, fontSize: 12.5, bold: true, color: RED, margin: 0 });
text("dòng khai báo  (khâu 2)\n+  câu người thao tác viết", { x: 5.75, y: 1.66, w: 3.6, h: 1.0, fontSize: 13, margin: 0, lh: 1.55 });
block(M, 3.75, W - 2 * M, 1.5);
text("Chỉ ghép nhãn, chưa mô hình nào sinh gì\nDòng khai báo nằm bên đáp án - lúc chạy, mô hình phải tự viết ra", { x: M + 0.22, y: 3.75, w: W - 2 * M - 0.44, h: 1.5, fontSize: 14.5, valign: "middle", margin: 0, lh: 1.4 });
note(`Slide dễ hiểu nhầm nhất nên nói chậm. Ba chi tiết: ảnh trong đề bài là ảnh sạch (dấu khoanh chỉ có ở khâu 2); toạ độ đúng chỉ dùng để dựng nhãn rồi biến mất; nhãn dựng hoàn toàn tự động, đo trên 1.068 bước thì 77% có tên rõ (số làm việc 70-75%), ô toạ độ sạch 100%.`);
foot(); done();

// ═══════════════ 13 · VÍ DỤ THẬT ═══════════════
slide();
bar("Một bước thật, đi hết quy trình");
block(M, 1.0, W - 2 * M, 1.42);
text([{ text: "Có sẵn trong dữ liệu\n", options: { bold: true, color: TEAL } }, { text: "Tác vụ: tìm áo thun đen trong app Zalando\nNgười dùng chạm điểm (499, 545) trên ảnh 1080 × 2400\nCâu người đó viết:  “Tap on the colour filter”", options: {} }], { x: M + 0.22, y: 1.0, w: W - 2 * M - 0.44, h: 1.42, fontSize: 13.5, valign: "middle", margin: 0, lh: 1.4 });
block(M, 2.57, W - 2 * M, 1.42);
text([{ text: "Khâu 1-3 dựng thêm\n", options: { bold: true, color: TEAL } }, { text: "Cây trợ năng: hộp nhỏ nhất chứa điểm chạm = [435,514] - [565,577]\nloại “chữ bấm được”, trên màn có 19 phần tử cùng loại\nOCR đọc chữ trong hộp:  “Colour”   (cây trợ năng không ghi tên)", options: {} }], { x: M + 0.22, y: 2.57, w: W - 2 * M - 0.44, h: 1.42, fontSize: 13.5, valign: "middle", margin: 0, lh: 1.4 });
block(M, 4.14, W - 2 * M, 1.5);
text("Nhãn dạy dựng ra", { x: M + 0.22, y: 4.24, w: 3, h: 0.35, fontSize: 13, bold: true, color: RED, margin: 0 });
text("<desc>chữ bấm được | Colour | <point>462,227</point>\n      | bên phải chữ “Brand”</desc>\nTap on the colour filter", { x: M + 0.3, y: 4.62, w: W - 2 * M - 0.6, h: 0.95, fontSize: 11.5, fontFace: MONO, margin: 0, lh: 1.4 });
text("Toàn bộ dựng tự động - không dán nhãn tay", { x: M, y: 5.85, w: W - 2 * M, h: 0.5, fontSize: 13, italic: true, color: MAROON, margin: 0 });
note(`Bước thật, số thật, lấy từ episode 11495 của AndroidControl. Điểm chạm (499,545) nằm đúng trong hộp trợ năng - đã kiểm. Đây là ca thuận lợi: OCR moi được tên. Ca khó là nút hình, ví dụ biểu tượng chia sẻ của Wynk Music tại (766,211): OCR không đọc được gì nên ô tên để trống, ba ô còn lại vẫn dựng bình thường. Đo trên 1.068 bước: 77% có tên rõ, 20% để trống, ô toạ độ sạch 100%.`);
foot(); done();

// ═══════════════ 14 · MỨC 2 ═══════════════
slide();
bar("Mức 2:  phạt khi câu vẫn mơ hồ   (thiết kế - chưa chạy)");
block(M, 1.1, W - 2 * M, 2.1);
text("Màn có hai kính lúp giống hệt nhau - cần hướng dẫn bấm cái bên trái.", { x: M + 0.22, y: 1.22, w: W - 2 * M - 0.44, h: 0.5, fontSize: 14, margin: 0 });
const rows = [["", "lúp trái", "lúp phải"], ["“Tap the search icon”", "khớp", "cũng khớp  →  bị phạt"], ["“... on the left, next to Contacts”", "khớp", "không khớp"]];
rows.forEach((r, i) => {
  const y = 1.8 + i * 0.44;
  text(r[0], { x: M + 0.35, y, w: 3.9, h: 0.42, fontSize: 13, italic: i > 0, bold: i === 0, margin: 0 });
  text(r[1], { x: 4.9, y, w: 1.5, h: 0.42, fontSize: 13, bold: i === 0, color: i === 0 ? NAVY : INK, align: "center", margin: 0 });
  text(r[2], { x: 6.5, y, w: 2.9, h: 0.42, fontSize: 13, bold: i === 0, color: i === 0 ? NAVY : (i === 1 ? MAROON : INK), align: "center", margin: 0 });
});
block(M, 3.55, W - 2 * M, 1.45);
text("Dựng khai báo giả từ nút hàng xóm - câu phải khớp bên thật rõ hơn bên giả\nKhớp cả hai như nhau là mơ hồ, bị phạt.", { x: M + 0.22, y: 3.55, w: W - 2 * M - 0.44, h: 1.45, fontSize: 14, valign: "middle", margin: 0, lh: 1.45 });
text("Tiền lệ từ 2016 bên ảnh tự nhiên - miền giao diện chưa ai làm.\nHàm phạt CHƯA cài; thử trên lát nhỏ trước, có tín hiệu mới mở rộng.", { x: M, y: 5.2, w: W - 2 * M, h: 0.7, fontSize: 12.5, italic: true, color: MAROON, margin: 0, lh: 1.35 });
note(`Mức khớp đo bằng chính xác suất mô hình gán cho câu đích khi được đưa từng khai báo - không cần ai phán, chạy tự động hàng nghìn lần mỗi lượt học. Nếu thầy hỏi giới hạn: lúc học mô hình được đưa sẵn khai báo, lúc chạy nó tự sinh - tín hiệu học lệch một nhịp so với lúc dùng. Cách vá đã ghi sẵn: đặt thêm khoản phạt ngay ở tầng sinh khai báo (phạt khi khai báo sinh ra đem áp vào nút hàng xóm cũng khớp).`);
foot(); done();

// ═══════════════ 15 · KHÂU 5-6 ═══════════════
slide();
bar("Huấn luyện, và lúc chạy thật");
block(M, 1.1, W - 2 * M, 1.35);
text([{ text: "Huấn luyện.  ", options: { bold: true, color: TEAL } }, { text: "Qwen2.5-VL-3B, mô hình mở 3 tỉ tham số, tinh chỉnh bằng QLoRA.", options: {} }], { x: M + 0.22, y: 1.1, w: W - 2 * M - 0.44, h: 1.35, fontSize: 14.5, valign: "middle", margin: 0, lh: 1.4 });
block(M, 2.85, W - 2 * M, 1.3);
text("ảnh + câu hỏi  →  bộ đọc chữ  →  mô hình  →  [khai báo] + câu  →  cắt khai báo  →  người dùng", { x: M + 0.2, y: 2.85, w: W - 2 * M - 0.4, h: 1.3, fontSize: 13.5, bold: true, color: NAVY, align: "center", valign: "middle", margin: 0, lh: 1.4 });
text([{ text: "Lúc chạy chỉ cần bộ đọc chữ và mô hình.  ", options: { bold: true } }, { text: "Không cần cây trợ năng, không cần bộ trỏ -\nhai thứ đó chỉ tồn tại lúc dựng dữ liệu và lúc chấm.", options: {} }], { x: M, y: 4.5, w: W - 2 * M, h: 0.9, fontSize: 14.5, margin: 0, lh: 1.4 });
note(`Những thứ đắt - toạ độ đúng, cây trợ năng, mô hình lớn, bộ trỏ - chỉ tồn tại lúc dựng dữ liệu và lúc chấm. Câu hỏi phải chủ động nêu: khai báo sai thì câu sai theo (lỗi lan truyền); cách phát hiện là so khai báo mô hình sinh với nhãn đã dựng.`);
foot(); done();

// ═══════════════ 19 · BỘ THÍ NGHIỆM ═══════════════
slide();
bar("Sáu phiên bản đem so với nhau");
block(M, 1.1, W - 2 * M, 3.55);
text("Cùng dữ liệu, cùng mô hình gốc, chỉ khác một chỗ - khoá danh sách trước khi nhìn kết quả", { x: M + 0.22, y: 1.22, w: W - 2 * M - 0.44, h: 0.55, fontSize: 13.5, margin: 0, lh: 1.3 });
const exps = [
  ["Bản thường (S1)", "học viết thẳng ra câu - mốc so sánh", false],
  ["Bản khai báo (S2)", "viết khai báo trước, rồi tới câu - câu hỏi chính", true],
  ["Khai báo giả (S2r)", "nội dung lấy từ màn khác, cùng độ dài - thắng nhờ dài thêm?", false],
  ["Bỏ toạ độ (S2-nopoint)", "khai báo thiếu ô toạ độ - tách phần công của toạ độ", false],
  ["Đưa sẵn lúc chạy (B-infer)", "không huấn luyện, chỉ đưa mô tả vào đầu vào lúc chạy", false],
  ["Thử mức 2 (S3-pilot)", "thử khoản phạt câu mơ hồ trên lát dữ liệu nhỏ", false]
];
exps.forEach((r, i) => {
  const y = 1.86 + i * 0.46;
  text(r[0], { x: M + 0.3, y, w: 2.45, h: 0.44, fontSize: 12.5, bold: true, color: r[2] ? RED : NAVY, margin: 0 });
  text(r[1], { x: M + 2.85, y, w: W - 2 * M - 3.2, h: 0.44, fontSize: 12.5, bold: r[2], margin: 0 });
});
text("Kèm ba lớp phân tích: cắt theo độ dài câu · theo độ dễ nhầm của màn · chấm tay 100 câu", { x: M, y: 4.85, w: W - 2 * M, h: 0.5, fontSize: 13, margin: 0 });
note(`Còn một phép thử rẻ chạy trước khi tiêu tiền huấn luyện S2: lấy S1 đã huấn luyện, nhét khai báo chuẩn vào đầu vào so với một đoạn đệm vô nghĩa cùng độ dài. Nếu đưa tận tay khai báo đúng mà điểm đứng yên thì S2 khó có cửa - biết sớm, bằng một phép thử rẻ, thay vì biết sau khi đã huấn luyện xong.`);
foot(); done();

// ═══════════════ 19 · VÌ SAO ĐỌC ĐƯỢC ═══════════════
slide();
bar("Làm sao biết chênh lệch là thật?");
block(M, 1.1, W - 2 * M, 1.55);
text("Lo nhất là can thiệp có tác dụng thật mà phép đo không thấy.\nMDE = mức chênh nhỏ nhất còn phân biệt được với may rủi.\nChấm đủ 4.463 bước chạm của tập kiểm, không lấy mẫu.", { x: M + 0.22, y: 1.1, w: W - 2 * M - 0.44, h: 1.55, fontSize: 14, valign: "middle", margin: 0, lh: 1.45 });
text("Đã đo: 1.091 cụm, hiệu dụng 454 - MDE ước 3,9 đến 6,6 điểm, tác dụng kỳ vọng 3-8.", { x: M + 0.22, y: 2.6, w: W - 2 * M - 0.44, h: 0.4, fontSize: 13, bold: true, color: TEAL, margin: 0 });
block(M, 3.0, W - 2 * M, 1.1);
text("Trình tự cứng:  huấn luyện Bản thường (S1) trước → chấm đủ → đo MDE thật → khoá ngưỡng → mới huấn luyện Bản khai báo (S2).", { x: M + 0.22, y: 3.0, w: W - 2 * M - 0.44, h: 1.1, fontSize: 13.5, bold: true, color: NAVY, valign: "middle", margin: 0, lh: 1.4 });
text("Hai lớp chống nhiễu: mỗi bản huấn luyện 2-3 lần với hạt giống khác nhau\nGom bước theo ứng dụng khi tính khoảng tin cậy", { x: M, y: 4.4, w: W - 2 * M, h: 0.9, fontSize: 13.5, margin: 0, lh: 1.4 });
note(`Số 4-7 là ước tính từ giả định, nên mới có trình tự "đo thật rồi mới khoá ngưỡng". Chênh giữa hai lần chạy S1 chính là cỡ nhiễu huấn luyện đo bằng số thật - mọi hiệu ứng công bố phải vượt cỡ đó. Gom theo ứng dụng vì các bước cùng một ứng dụng na ná nhau, không phải bằng chứng độc lập.`);
foot(); done();

// ═══════════════ 20 · KẾ HOẠCH ═══════════════
slide();
bar("Trình tự chạy, và ba chốt chặn");
block(M, 1.1, W - 2 * M, 1.75);
text("Đăng ký trước  →  kiểm bộ trỏ  →  Bản thường, 2 hạt giống + đo MDE thật\n→  khoá ngưỡng  →  Bản khai báo  →  các nhánh đối chứng\n→  thử mức 2  →  chấm tay + demo tiếng Việt", { x: M + 0.22, y: 1.1, w: W - 2 * M - 0.44, h: 1.75, fontSize: 14, valign: "middle", margin: 0, lh: 1.6 });
block(M, 3.2, W - 2 * M, 1.15);
text([{ text: "Đang ở bước 3.  ", options: { bold: true, color: RED } }, { text: "Bản thường, hạt giống thứ nhất, đang huấn luyện - xong sáng mai.\nMỗi lượt 8.072 bước, hai lượt duyệt qua toàn bộ 64.567 mẫu.", options: {} }], { x: M + 0.22, y: 3.2, w: W - 2 * M - 0.44, h: 1.15, fontSize: 13.5, valign: "middle", margin: 0, lh: 1.4 });
text("Ba chốt chặn, tiêu chí ghi sẵn từ trước:\nsau Bản thường - còn chỗ chứng minh không\nsau đối chứng - chênh rõ mới chạy tiếp\ntrước chương kết quả - đóng băng mọi con số", { x: M, y: 4.55, w: W - 2 * M, h: 1.0, fontSize: 13.5, margin: 0, lh: 1.5 });
note(`Ba chốt chặn là chỗ đáng nhấn về phương pháp: tiêu chí đậu rớt viết ra trước, không phải nhìn số rồi mới đặt. Nếu thầy hỏi về cấu hình huấn luyện: em chạy 16 lượt thăm dò ngắn để chọn, và đã kiểm rằng cấu hình chọn ra cho ra loss trùng tới chữ số thứ tư so với cấu hình gốc - tức là chỉ đổi tốc độ, không đổi phép tính. Đổi card cũng ra cùng loss, dùng được cho câu tái lập.`);
foot(); done();

// ═══════════════ 3 · ĐÃ LÀM ĐƯỢC GÌ (mới ở v10) ═══════════════
slide();
bar("Đã làm được tới đâu");
const moc = [
  ["Cổng bộ trỏ", "ĐẠT", "sai số trung vị 0,7% bề ngang màn - ngưỡng đặt trước là 3%", true],
  ["Dữ liệu dạy", "XONG", "64.567 bước · 12.895 tác vụ · đọc chữ phủ 100% · 9/9 bất biến", false],
  ["Rò rỉ dạy-kiểm", "= 0", "lần đầu kiểm ở quy mô đủ: 0 tác vụ trùng giữa 12.895 và 1.432", false],
  ["Huấn luyện", "ĐANG CHẠY", "bản thường, hạt giống 101, trên A100 - xong sáng mai", true]
];
moc.forEach((r, i) => {
  const y = 1.25 + i * 1.22;
  block(M, y, W - 2 * M, 0.98);
  text(r[0], { x: M + 0.22, y, w: 2.35, h: 0.98, fontSize: 13.5, bold: true, color: NAVY, valign: "middle", margin: 0 });
  text(r[1], { x: M + 2.6, y, w: 1.35, h: 0.98, fontSize: 14, bold: true, color: r[3] ? RED : TEAL, valign: "middle", margin: 0 });
  text(r[2], { x: M + 4.05, y, w: W - 2 * M - 4.3, h: 0.98, fontSize: 12.5, valign: "middle", margin: 0, lh: 1.3 });
});
note(`Slide này đặt sớm là cố ý: thầy từng bác hướng chỉ ghép công cụ, nên phải cho thấy ngay là mô hình thật đang chạy, mỗi mắt xích có một con số. Cổng bộ trỏ là rủi ro số một của cả thiết kế, vì mọi thước chấm treo trên nó; nó đã đạt với biên rất rộng (0,7 so với ngưỡng 3). Rò rỉ dạy-kiểm là loại sai không sửa được sau khi train, nên đây là chốt chặn thật chứ không phải thủ tục. Nếu thầy hỏi vì sao giờ mới train: trình tự khoá từ đầu là kiểm cho chắc thước đo và dữ liệu trước, rồi mới huấn luyện - vì sai ở hai chỗ đó thì huấn luyện xong cũng bỏ.`);
foot(); done();

// ═══════════════ 22 · GIỚI HẠN TỰ KHAI (mới ở v10) ═══════════════
slide();
bar("Giới hạn của thiết kế");
const yeu = [
  ["Tập kiểm không phải\n\"ứng dụng chưa từng thấy\"",
   "92% ứng dụng trong tập kiểm cũng có ở tập dạy - giữ riêng theo TÁC VỤ,\nkhông phải theo ứng dụng.\nPhép so chính S1 vs S2:  vẫn đúng, hai bản đối xứng, 0 tác vụ trùng.\nMốc gpt-4o-mini:  hạ xuống tham khảo - lợi thế sân nhà."],
  ["Bộ trỏ chấm còn một\nkiểu hỏng riêng",
   "15,3% số lần nó bỏ cuộc theo chiều ngang:  trả về giữa màn rồi đoán chiều dọc.\nCó sẵn bốn dấu hiệu để dò, in cạnh con số chính."],
  ["Nhánh đưa sẵn lúc chạy\nbị thiệt ba mặt",
   "Câu nhắc dài gấp 2,4 lần vùng đã học · cắt còn 40/72 phần tử · 14,1% có tên.\nNhánh này thua thì không kết luận được gì."]
];
yeu.forEach((r, i) => {
  const y = 1.05 + i * 1.72;
  block(M, y, W - 2 * M, 1.55);
  text(r[0], { x: M + 0.22, y, w: 2.5, h: 1.55, fontSize: 12.5, bold: true, color: NAVY, valign: "middle", margin: 0, lh: 1.3 });
  text(r[1], { x: M + 2.85, y, w: W - 2 * M - 3.15, h: 1.55, fontSize: 11.5, valign: "middle", margin: 0, lh: 1.35 });
});
text("Cả ba ghi trong bản đăng ký, trước khi có kết quả.", { x: M, y: 6.3, w: W - 2 * M, h: 0.45, fontSize: 13, italic: true, color: MAROON, margin: 0 });
note(`Slide này cố ý đặt trước phần tóm tắt. Lý do: ba chỗ này thầy hoặc hội đồng sẽ tìm ra, tự khai trước thì mất ít điểm hơn nhiều so với bị vặn. Chỗ thứ nhất là nặng nhất, và đừng nhận lỗi dài dòng - chỉ cần nói đây là tập giữ riêng theo tác vụ chứ không theo ứng dụng, em kiểm ra và khai luôn. Điều quan trọng phải nói kèm: phép so chính không hỏng vì hai bản dùng chung dữ liệu dạy, chung mô hình gốc, chung tập kiểm - chỉ khác đúng đích sinh.`);
foot(); done();

// ═══════════════ 21 · RỦI RO ═══════════════
slide();
bar("Rủi ro chính");
const risks = [
  ["Bộ trỏ không đủ chính xác để chấm", "đã kiểm: 0,7% so với ngưỡng 3% - rủi ro số một, nay loại được"],
  ["Tác dụng thật quá nhỏ để đo thấy", "chấm đủ tập kiểm để ép MDE xuống hết mức; không thấy chênh thì vẫn là kết quả đọc được"],
  ["Nhãn khai báo nhiễu, kéo Bản khai báo xuống", "thiếu tên thì để trống chứ không đoán; tách phân tích theo nguồn tên"],
  ["Mô hình học vẹt cú pháp khai báo", "nhánh Khai báo giả sinh ra để bắt đúng chuyện này"]
];
risks.forEach((r, i) => {
  block(M, 1.1 + i * 1.15, W - 2 * M, 1.0);
  text(r[0], { x: M + 0.22, y: 1.1 + i * 1.15, w: 3.6, h: 1.0, fontSize: 13, bold: true, color: NAVY, valign: "middle", margin: 0, lh: 1.3 });
  text(r[1], { x: M + 3.95, y: 1.1 + i * 1.15, w: W - 2 * M - 4.25, h: 1.0, fontSize: 13, valign: "middle", margin: 0, lh: 1.3 });
});
text("Mỗi rủi ro đều có cách phát hiện sớm và đường xử lý ghi sẵn", { x: M, y: 5.85, w: W - 2 * M, h: 0.5, fontSize: 13.5, italic: true, color: MAROON, margin: 0 });
note(`Rủi ro số một là cổng bộ trỏ - cả thước chấm treo trên nó nên đo ngay tuần đầu, trước mọi khoản chi lớn. Kế hoạch B: nới cách chấm và khai tỉ lệ oan; tệ nữa thì gộp nhiều bộ trỏ; vẫn không xong thì so thứ hạng tương đối giữa các bản và nâng chấm tay lên 200 câu.`);
foot(); done();

// ═══════════════ BA KỊCH BẢN — VIỆC CẦN THẦY QUYẾT ═══════════════
slide();
bar("Kết quả sẽ rơi vào một trong ba kịch bản");
block(M, 1.0, W - 2 * M, 0.68);
text("Xin thống nhất cách đọc cả ba TRƯỚC khi có số.", { x: M + 0.22, y: 1.0, w: W - 2 * M - 0.44, h: 0.68, fontSize: 14.5, bold: true, color: NAVY, valign: "middle", margin: 0 });
const kb = [
  ["Thắng rõ", "vượt ngưỡng đã khoá", "Đóng góp chính đứng vững."],
  ["Chênh nhỏ\nhoặc ngang", "trong khoảng nhiễu", "Luận điểm chuyển sang:  ngang chất lượng nhưng mô hình 3 tỉ\ntham số, chạy tại máy, không gửi ảnh lên mạng.  Kèm phân tích."],
  ["Không chênh", "dưới ngưỡng đo được", "Đọc là kết quả âm có kiểm soát:  đăng ký trước, có đối chứng,\ncó phân tích.  Chương đo lường lên vai chính."]
];
kb.forEach((r, i) => {
  const y = 1.95 + i * 1.35;
  block(M, y, W - 2 * M, 1.2);
  text(r[0], { x: M + 0.25, y, w: 1.75, h: 1.2, fontSize: 14, bold: true, color: i === 0 ? TEAL : NAVY, valign: "middle", margin: 0, lh: 1.25 });
  text(r[1], { x: M + 2.05, y, w: 1.85, h: 1.2, fontSize: 11.5, italic: true, color: FOOTC, valign: "middle", margin: 0 });
  text(r[2], { x: M + 4.0, y, w: W - 2 * M - 4.3, h: 1.2, fontSize: 12.5, valign: "middle", margin: 0, lh: 1.35 });
});
text("Ba phần của luận văn độc lập nhau - một phần không ra kết quả, hai phần kia vẫn đứng.", { x: M, y: 6.15, w: W - 2 * M, h: 0.45, fontSize: 13, italic: true, color: MAROON, align: "center", margin: 0 });
note(`Đây là việc duy nhất buổi này phải chốt được. Lý do phải thống nhất trước khi có số: nếu đợi thấy kết quả rồi mới bàn cách kể thì mọi cách kể đều mang tiếng chọn cho hợp số. Ba phần độc lập là: mô hình tự huấn luyện, thành phần huấn luyện hai mức, và chương đo lường. Kịch bản ba không phải là hỏng - kết quả âm có đăng ký trước vẫn công bố được, và chương đo lường đã có sản phẩm riêng.`);
foot(); done();

// ═══════════════ 23 · TÓM TẮT ═══════════════
slide();
bar("Tóm tắt");
const sums = [
  ["Sản phẩm", "Mô hình 3 tỉ tham số: nhìn ảnh và câu hỏi, viết hướng dẫn cho người đọc"],
  ["Đóng góp", "Bắt mô hình xác định rõ mục tiêu trước khi viết: dòng khai báo trước câu, và khoản phạt câu mơ hồ"],
  ["Đang ở đâu", "Thiết kế đã khoá, có mốc thời gian · thước đã kiểm và qua cổng · dữ liệu đã dựng đủ · bản thường đang huấn luyện, sáng mai có điểm đầu tiên"],
  ["Xin thầy cho ý kiến", "Cách đọc kết quả cho cả ba kịch bản, chốt trước khi số về"]
];
sums.forEach((r, i) => {
  block(M, 1.1 + i * 1.32, W - 2 * M, 1.15);
  text(r[0], { x: M + 0.22, y: 1.1 + i * 1.32, w: 2.3, h: 1.15, fontSize: 14, bold: true, color: i >= 2 ? RED : NAVY, valign: "middle", margin: 0 });
  text(r[1], { x: M + 2.6, y: 1.1 + i * 1.32, w: W - 2 * M - 2.9, h: 1.15, fontSize: 12.5, valign: "middle", margin: 0, lh: 1.35 });
});
foot(); done();

// ═══════════════ 23 · CẢM ƠN ═══════════════
slide();
rect(0, 0, W, 0.66, NAVY);
rect(0.8, 2.3, W - 1.6, 2.2, NAVY, { radius: 0.09, shadow: true });
text("XIN CẢM ƠN\nTHẦY CÔ VÀ HỘI ĐỒNG!", { x: 0.8, y: 2.3, w: W - 1.6, h: 2.2, fontSize: 28, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0, lh: 1.35 });
text("Rất mong nhận được góp ý của thầy cô", { x: 0.8, y: 5.0, w: W - 1.6, h: 0.5, fontSize: 14, italic: true, color: INK, align: "center", margin: 0 });
foot(); done();


// ═══════════════ SLIDE DỰ PHÒNG (ẩn) - bảng gốc của 4 bài ═══════════════
// Không nằm trong mạch chính; đã bật Hide Slide sẵn.
// Lúc trình chiếu muốn mở: gõ số slide rồi Enter, hoặc bỏ ẩn trong PowerPoint.
function backup(title, img, caption, iw, noteTxt) {
  if (cur) htmlSlides.push(cur + "</div>");
  s = pres.addSlide(); s.hidden = true; s.background = { color: WHITE };
  cur = `<div class="slide" style="background:#fff;outline:3px dashed #b22222">`;
  bar(title);
  const ix = (W - iw) / 2;
  s.addImage({ path: img, x: ix, y: 1.05, w: iw, h: 4.3, sizing: { type: "contain", w: iw, h: 4.3 } });
  hpush(`<div style="position:absolute;left:${ix * PX}px;top:${1.05 * PX}px;width:${iw * PX}px;height:${4.3 * PX}px;border:1px solid #ccc"></div>`);
  text(caption, { x: M, y: 5.5, w: W - 2 * M, h: 1.1, fontSize: 13, margin: 0, lh: 1.4 });
  rect(0, H - 0.26, W, 0.26, FOOTC);
  text("slide dự phòng - chỉ mở khi được hỏi", { x: 0, y: H - 0.26, w: W, h: 0.26, fontSize: 8, color: WHITE, align: "center", valign: "middle", margin: 0 });
  if (noteTxt) note(noteTxt);
  done();
}

backup("Nguồn số:  Aguvis (ICML 2025), Table 6", "../../report/paper_figures/aguvis_table6.png",
  "Cột AndroidControl Low-Level:  80,5 → 69,1 khi bỏ tầng trung gian, tức tụt 11,4\nHai cột kia cho thấy hiệu ứng dồn đúng chỗ:  High-Level chỉ tụt 1,2 · ScreenSpot tụt 5,1", 9.0,
  `Số 11,4 là hiệu hai dòng, bài không in sẵn - khai luôn nếu bị vặn. Đây là bài duy nhất trong bảng chạy trên chính AndroidControl. Họ đo độ đúng thao tác, không đo chất lượng câu, nên chỉ mượn để nói chiều.`);

backup("Nguồn số:  Shikra, Table 1", "../../report/paper_figures/shikra_table1.png",
  "Cùng mô hình, cùng bài kiểm, chỉ đổi dạng bước trung gian:\nkhông có bước trung gian 88,07  ·  văn xuôi 80,68 (−7,4)  ·  có toạ độ 93,97 (+5,9)", 6.4,
  `Cặp số quyết định thiết kế. Điểm yếu phải tự khai, ghi ngay trong chú thích bảng: "three toy models of Shikra-7B (without using additional datasets) on the CLEVR dataset" - mô hình thí nghiệm nhỏ, chưa tiền huấn luyện, ảnh hình khối nhân tạo. Bằng chứng yếu nhất trong bảng.`);

backup("Nguồn số:  GCoT, Table 5", "../../report/paper_figures/gcot_table5.png",
  "Cột Average → A-Acc:  LLaVA-7B 70,0 → 74,5 (+4,5)  ·  LLaVA-13B 70,6 → 76,4 (+5,8)\nSố âm hay được trích nằm ở Table 3 và 4 - đó là chế độ ra lệnh cho mô hình chưa huấn luyện", 8.4,
  `Bài hay bị hiểu ngược. Huấn luyện hẳn theo thứ tự định-vị-trước thì tăng cả ba cột, không đánh đổi. Điểm yếu của họ, chủ động khai: họ thay bộ dữ liệu dạy bằng dữ liệu cùng phân bố với bộ đề rồi train lại từ đầu, nên +4,5/+5,8 trộn hai nguyên nhân mà bài không tách. Phép so của mình cùng một bộ dữ liệu, chỉ đổi đích sinh, nên tách được.`);

backup("Nguồn số:  CogCoM (ICLR 2025), Table 4", "../../report/paper_figures/cogcom_table4.png",
  "Bỏ 70K dữ liệu chuỗi trung gian ra khỏi huấn luyện:\nTextVQA ↑6,6  ·  MMVet ↑0,2  ·  MathVista ↑0,9 - phải trích cả cụm ba số\nHiệu ứng chỉ nổi ở bài đòi đọc chữ trong ảnh", 8.6,
  `Số duy nhất trong bốn bài mà tác giả in thẳng mức tăng. Trích cả cụm để không mang tiếng chọn số đẹp.`);

// ---- xuất ----
fs.mkdirSync("_preview", { recursive: true });
const page = `<!doctype html><meta charset="utf-8"><style>@page{size:${W}in ${H}in;margin:0}*{margin:0;box-sizing:border-box}.slide{position:relative;width:${W}in;height:${H}in;overflow:hidden;page-break-after:always;border-bottom:1px solid #ccc}</style>` + htmlSlides.join("\n");
fs.writeFileSync("_preview/preview.html", page);
pres.writeFile({ fileName: "../LUAN_VAN_SLIDE.pptx" }).then(f => console.log("PPTX ->", f, "| slides:", htmlSlides.length)).catch(e => console.error("ERR", e));
