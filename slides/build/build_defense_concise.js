const pptxgen = require('pptxgenjs');
const path = require('path');

const pptx = new pptxgen();
pptx.defineLayout({ name: 'A43', width: 10, height: 7.5 });
pptx.layout = 'A43';
pptx.author = 'Le Doan Phuong Uyen';
pptx.subject = 'Master thesis defense';
pptx.title = 'Phat sinh tu dong huong dan su dung phan mem dua tren LLM';
pptx.lang = 'vi-VN';

const W = 10, H = 7.5, M = 0.55;
const TF = 'Cambria', MONO = 'Consolas';
const FOOTA='191132', FOOTB='25194B', FOOTC='4F417A', FOOTD='7A7099';
const BAR=FOOTB, ACCENT=FOOTC, ACCENT2=FOOTD;
const WHITE='FFFFFF', INK='1A1A1A', GREY='5A5A66', LIGHT='F3F2F5', RULE='D9D6DF';
const TITLE_FS=20, SECTION_FS=17, BODY_FS=16, TABLE_FS=13.2, SMALL_FS=12.5;
let slide, PAGE=0, BPAGE=0; const TOTAL=24;

function addText(t,o={}){ slide.addText(t,Object.assign({fontFace:TF,fontSize:BODY_FS,color:INK,margin:0},o)); }
function rect(x,y,w,h,fill,o={}){ slide.addShape(o.radius?pptx.ShapeType.roundRect:pptx.ShapeType.rect,{x,y,w,h,fill:{color:fill},line:o.line?{color:o.line,width:o.lw||1}:{color:fill,transparency:100},radius:o.radius||0}); }
function line(x,y,w,h,c=RULE,lw=1,end=false){ slide.addShape(pptx.ShapeType.line,{x,y,w,h,line:{color:c,width:lw,endArrowType:end?'triangle':'none'}}); }
function bar(title){ rect(0,0,W,0.6,BAR); addText(title,{x:0.22,y:0,w:W-0.44,h:0.6,fontSize:TITLE_FS,bold:true,color:WHITE,valign:'mid'}); }
function footRow(label){ const y=H-0.26,h=0.26; rect(0,y,3,h,FOOTA);rect(3,y,3.7,h,FOOTB);rect(6.7,y,1.9,h,FOOTC);rect(8.6,y,1.4,h,FOOTD); addText('Luận văn thạc sĩ',{x:0,y,w:3,h,fontFace:MONO,fontSize:8,bold:true,color:WHITE,align:'center',valign:'mid'}); addText('Phát sinh tự động hướng dẫn sử dụng phần mềm dựa trên LLM',{x:3,y,w:3.7,h,fontSize:8,color:WHITE,align:'center',valign:'mid'}); addText('Lê Đoàn Phương Uyên',{x:6.7,y,w:1.9,h,fontSize:8,color:WHITE,align:'center',valign:'mid'}); addText(label,{x:8.6,y,w:1.4,h,fontSize:8,color:WHITE,align:'center',valign:'mid'}); }
function foot(){ PAGE++; footRow(`${PAGE}/${TOTAL}`); }
function footB(){ BPAGE++; footRow(''); }
function newSlide(title){ slide=pptx.addSlide(); slide.background={color:WHITE}; if(title) bar(title); }
function bullets(items,x,y,w,o={}){ const gap=o.gap||0.88; items.forEach((it,i)=>{ const yy=y+i*gap; slide.addShape(pptx.ShapeType.ellipse,{x:x+0.02,y:yy+0.15,w:0.07,h:0.07,fill:{color:o.dot||ACCENT},line:{color:o.dot||ACCENT,transparency:100}}); addText(it,{x:x+0.23,y:yy,w:w-0.23,h:o.h||0.72,fontSize:o.fs||BODY_FS,color:o.color||INK,fit:'shrink',valign:'top',lineSpacingMultiple:1.12}); }); }
function box(x,y,w,h,t,o={}){ rect(x,y,w,h,o.fill||WHITE,{radius:0.05,line:o.line||ACCENT2,lw:o.lw||1}); addText(t,{x,y,w,h,fontSize:o.fs||BODY_FS,bold:o.bold,color:o.color||INK,align:'center',valign:'mid',fit:'shrink'}); }
function source(t){ addText(t,{x:M,y:6.92,w:W-2*M,h:0.15,fontSize:8,italic:true,color:GREY,align:'right'}); }
function metricBadge(x,y,w,value,label,color=ACCENT){ addText(value,{x,y,w,h:0.55,fontSize:24,bold:true,color,align:'center',valign:'mid'}); addText(label,{x,y:y+0.58,w,h:0.52,fontSize:SMALL_FS,bold:true,color:INK,align:'center',valign:'mid',fit:'shrink'}); }
function table(x,y,colW,rows,o={}){ let yy=y; rows.forEach(r=>{ const h=r.h||0.48; if(r.fill) rect(x,yy,colW.reduce((a,b)=>a+b,0),h,r.fill); let xx=x; r.cells.forEach((c,i)=>{ const cell=typeof c==='string'?{t:c}:c; addText(cell.t,{x:xx,y:yy,w:colW[i],h,fontSize:cell.fs||r.fs||o.fs||TABLE_FS,bold:cell.bold!=null?cell.bold:r.bold,color:cell.color||r.color||INK,align:cell.align||(o.align&&o.align[i])||'left',valign:'mid',fit:'shrink',italic:cell.italic}); xx += colW[i]; }); if(r.rule) line(x,yy+h,colW.reduce((a,b)=>a+b,0),0,r.rule===true?RULE:r.rule,1); yy += h; }); }

// 1 · Bìa
newSlide();
rect(0,0,W,0.66,FOOTA);
addText('ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH  -  TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN',{x:0,y:0,w:W,h:0.66,fontSize:14,bold:true,color:WHITE,align:'center',valign:'mid'});
rect(0.8,1.18,W-1.6,2.5,FOOTB,{radius:0.08});
addText('LUẬN VĂN THẠC SĨ  -  NGÀNH TRÍ TUỆ NHÂN TẠO',{x:0.8,y:1.45,w:W-1.6,h:0.35,fontSize:14,bold:true,color:WHITE,align:'center'});
addText('PHÁT SINH TỰ ĐỘNG HƯỚNG DẪN SỬ DỤNG PHẦN MỀM\nDỰA TRÊN LLM TỪ CÁC TRƯỜNG HỢP SỬ DỤNG\nVÀ GIAO DIỆN NGƯỜI DÙNG',{x:0.95,y:1.96,w:W-1.9,h:1.45,fontSize:21,bold:true,color:WHITE,align:'center',valign:'mid',fit:'shrink'});
addText('Học viên thực hiện: Lê Đoàn Phương Uyên',{x:0.8,y:4.55,w:W-1.6,h:0.4,fontSize:16,bold:true,align:'center'});
addText('Giáo viên hướng dẫn: TS. Nguyễn Hồng Bửu Long',{x:0.8,y:5.0,w:W-1.6,h:0.4,fontSize:16,bold:true,align:'center'});
addText('TP. Hồ Chí Minh - 2026',{x:0.8,y:5.88,w:W-1.6,h:0.35,fontSize:13,align:'center'});
foot();

// 2 · Bài toán (gộp hai slide cũ)
newSlide('1. Bài toán');
addText('Từ trạng thái giao diện hiện tại, sinh một câu hướng dẫn để người dùng biết chính xác bước tiếp theo cần làm.',{x:M,y:0.98,w:8.9,h:0.62,fontSize:17,bold:true,color:FOOTB,align:'center',fit:'shrink'});
box(0.65,2.02,2.05,0.95,'Màn hình hiện tại',{bold:true,fill:LIGHT,line:FOOTD});
line(2.82,2.50,0.48,0,FOOTC,2,true);
box(3.42,2.02,2.05,0.95,'Mô hình sinh câu',{bold:true,fill:LIGHT,line:FOOTB});
line(5.59,2.50,0.48,0,FOOTC,2,true);
box(6.20,1.88,2.95,1.22,'“Chạm vào Not now”',{bold:true,fill:LIGHT,line:FOOTC,fs:17});
addText('Đầu vào',{x:M,y:3.70,w:1.1,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Ảnh màn hình hiện tại','Mục tiêu người dùng','Lịch sử thao tác trước đó','Thông tin OCR trên giao diện'],M,4.10,4.25,{gap:0.55,fs:14.5,h:0.46});
rect(5.15,3.78,4.20,1.80,LIGHT,{radius:0.05,line:FOOTD});
addText('Đầu ra',{x:5.40,y:4.05,w:3.7,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB,align:'center'});
addText('Một câu hướng dẫn cho\nbước tiếp theo',{x:5.45,y:4.55,w:3.60,h:0.72,fontSize:18,bold:true,color:INK,align:'center',valign:'mid'});
addText('Đầu ra của luận văn là câu hướng dẫn cho người dùng, không phải tọa độ để agent tự thao tác.',{x:M,y:6.08,w:8.9,h:0.45,fontSize:14.5,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn §1.2–§1.3'); foot();

// 3 · Thách thức
newSlide('2. Thách thức của câu hướng dẫn GUI');
addText('Một câu nghe hoàn toàn tự nhiên vẫn có thể không đủ thông tin để người dùng chọn đúng phần tử.',{x:M,y:1.0,w:8.9,h:0.58,fontSize:17,bold:true,color:FOOTB,align:'center',fit:'shrink'});
rect(M,1.95,4.15,2.75,LIGHT,{radius:0.05,line:FOOTD});
addText('Câu mơ hồ',{x:M+0.2,y:2.2,w:3.75,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB,align:'center'});
addText('“Tap the button.”',{x:M+0.25,y:3.0,w:3.65,h:0.48,fontSize:19,italic:true,color:FOOTD,align:'center'});
addText('Không biết phải chạm nút nào khi màn hình có nhiều nút.',{x:M+0.3,y:3.75,w:3.55,h:0.7,fontSize:15,align:'center',fit:'shrink'});
rect(5.30,1.95,4.15,2.75,LIGHT,{radius:0.05,line:FOOTC});
addText('Câu đủ rõ',{x:5.50,y:2.2,w:3.75,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB,align:'center'});
addText('“Tap Not now.”',{x:5.55,y:3.0,w:3.65,h:0.48,fontSize:19,italic:true,color:FOOTC,align:'center'});
addText('Chỉ ra đúng phần tử cần thao tác.',{x:5.60,y:3.75,w:3.55,h:0.7,fontSize:15,bold:true,align:'center'});
addText('Vì vậy, câu hướng dẫn không chỉ cần đúng nội dung mà còn phải phân biệt được đúng phần tử cần thao tác.',{x:M,y:5.32,w:8.9,h:0.7,fontSize:15.5,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn Chương 1'); foot();

// 4 · Khoảng trống đánh giá
newSlide('3. Khoảng trống đánh giá');
addText('Các thước đo so sánh câu chưa trực tiếp phản ánh điều người dùng thực sự cần.',{x:M,y:1.0,w:8.9,h:0.55,fontSize:17,bold:true,color:FOOTB,align:'center'});
box(0.70,2.05,2.55,1.2,'BLEU / ROUGE\nCâu giống reference đến đâu?',{bold:true,fill:LIGHT,line:FOOTD,fs:15});
box(3.72,2.05,2.55,1.2,'SPICE / CIDEr\nNội dung có tương đồng?',{bold:true,fill:LIGHT,line:FOOTD,fs:15});
box(6.75,1.85,2.55,1.6,'Điều cần biết\nCâu có giúp xác định đúng\nphần tử và thao tác?',{bold:true,fill:LIGHT,line:FOOTC,fs:15});
addText('Do đó, luận văn đánh giá cả mức tương đồng với câu tham chiếu và khả năng xác định đúng phần tử, đúng loại thao tác.',{x:M,y:4.55,w:8.9,h:0.70,fontSize:16,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn Chương 5'); foot();

// 5 · Đóng góp
newSlide('4. Đóng góp của luận văn');
rect(M,1.15,2.75,3.35,LIGHT,{radius:0.05,line:FOOTB});
addText('1 · Phương pháp đề xuất',{x:M+0.15,y:1.43,w:2.45,h:0.52,fontSize:16.5,bold:true,color:FOOTB,align:'center',fit:'shrink'});
addText('Hai thành phần nối tiếp: GRPO + SPICE sinh câu ban đầu; ACE chỉ hiệu chỉnh khi câu ví dụ thỏa điều kiện chọn lọc.',{x:M+0.25,y:2.12,w:2.25,h:1.55,fontSize:14.2,align:'center',valign:'mid',fit:'shrink'});
rect(3.63,1.15,2.75,3.35,LIGHT,{radius:0.05,line:FOOTC});
addText('2 · Executability',{x:3.78,y:1.48,w:2.45,h:0.4,fontSize:17,bold:true,color:FOOTB,align:'center'});
addText('Dùng một mô hình định vị tách biệt để kiểm tra câu có giúp xác định đúng phần tử và đúng loại thao tác hay không.',{x:3.88,y:2.10,w:2.25,h:1.55,fontSize:14.2,align:'center',valign:'mid',fit:'shrink'});
rect(6.70,1.15,2.75,3.35,LIGHT,{radius:0.05,line:FOOTD});
addText('3 · Phân tích thực nghiệm',{x:6.85,y:1.43,w:2.45,h:0.52,fontSize:16.5,bold:true,color:FOOTB,align:'center',fit:'shrink'});
addText('Phân tích các phương án đã thử để làm rõ vì sao cải thiện ở bước trung gian chưa chắc tạo ra câu hướng dẫn tốt hơn.',{x:6.95,y:2.10,w:2.25,h:1.55,fontSize:14.2,align:'center',valign:'mid',fit:'shrink'});
addText('Bên cạnh ba đóng góp chính, luận văn còn xây dựng tự động tập giám sát từ AndroidControl để phục vụ huấn luyện và đánh giá.',{x:M,y:4.82,w:8.9,h:0.58,fontSize:13.2,color:GREY,align:'center',fit:'shrink'});
rect(M,5.62,8.9,0.68,LIGHT,{radius:0.05,line:FOOTD});
addText('Kết quả chính: 60,7% Executability, cao hơn S1/101 1,57 điểm; KTC 95% [+0,86; +2,31].',{x:M+0.18,y:5.62,w:8.54,h:0.68,fontSize:15.5,bold:true,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
source('Luận văn §1.6, §6.2'); foot();

// 6 · Tổng quan phương pháp
newSlide('5. Tổng quan phương pháp');
box(0.55,1.35,0.80,0.9,'S1',{bold:true,line:FOOTD});
line(1.45,1.80,0.35,0,FOOTC,2,true);
box(1.90,1.35,1.85,0.9,'GRPO + SPICE',{bold:true,fill:LIGHT,line:FOOTB,fs:15});
line(3.85,1.80,0.30,0,FOOTC,2,true);
box(4.25,1.20,1.75,1.20,'Câu hướng dẫn\nban đầu',{bold:true,fill:WHITE,line:FOOTD,fs:14.5});
line(6.10,1.80,0.30,0,FOOTC,2,true);
box(6.50,1.35,0.90,0.9,'ACE',{bold:true,fill:LIGHT,line:FOOTC});
line(7.50,1.80,0.30,0,FOOTC,2,true);
box(7.90,1.20,1.55,1.20,'Câu hướng dẫn\ncuối',{bold:true,fill:WHITE,line:FOOTD,fs:14.5});
addText('GRPO + SPICE',{x:M,y:3.45,w:2.2,h:0.45,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Sinh nhiều câu cho cùng một tình huống.','Dùng SPICE kèm phạt độ dài làm tín hiệu cập nhật.'],M,4.00,4.25,{gap:0.82,fs:15,h:0.67});
addText('ACE',{x:5.05,y:3.45,w:1.8,h:0.45,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Truy hồi 4 câu ví dụ và sinh một câu ứng viên.','Chỉ thay câu ban đầu khi đủ điều kiện chọn lọc.'],5.05,4.00,4.40,{gap:0.82,fs:15,h:0.67});
source('Luận văn Chương 4'); foot();

// 7 · Dữ liệu
newSlide('6. Dữ liệu AndroidControl');
addText('Phân chia dữ liệu',{x:M,y:1.0,w:2.0,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
table(M,1.48,[2.7,2.0,2.0,2.2],[{cells:['','Huấn luyện','Kiểm tra','Ghi chú'],fill:FOOTB,color:WHITE,bold:true,h:0.46},{cells:['Số bước','64.567','6.958','chia theo tác vụ'],h:0.52,rule:true},{cells:['Bước chạm','41.191','4.463','dùng để tính Executability'],h:0.52,rule:true},{cells:['Số tác vụ','12.895','1.432','không trùng tác vụ'],h:0.52}],{align:['left','center','center','left'],fs:13.5});
addText('Đặc điểm cần lưu ý',{x:M,y:3.75,w:2.2,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Train/test của đề tài không trùng tác vụ; không tương đương cách chia kiểm tra chính thức của AndroidControl.','Chỉ 45,0% bước test xác định được tên ứng dụng; trong phần này, 95,6% thuộc ứng dụng đã xuất hiện trong train.','45,5% câu tham chiếu ở test xuất hiện nguyên câu trong train; 77,7% có ít nhất một cụm 4 token đã thấy.'],M,4.16,8.9,{gap:0.70,fs:13.8,h:0.60});
source('Luận văn Chương 3, §6.8'); foot();

// 8 · S1
newSlide('7. Mô hình nền S1');
addText('Mô hình nền',{x:M,y:1.0,w:1.3,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
addText('Qwen2.5-VL-3B-Instruct + QLoRA 4-bit',{x:M,y:1.45,w:8.9,h:0.55,fontSize:19,bold:true,color:INK,align:'center'});
metricBadge(0.85,2.55,2.2,'47,6%','Mô hình gốc',FOOTD);
metricBadge(3.90,2.55,2.2,'59,1%','S1 - seed 101',FOOTB);
metricBadge(6.95,2.55,2.2,'59,6%','S1 - seed 202',FOOTC);
addText('SFT đã tạo ra bước nhảy lớn; phương pháp đề xuất tiếp tục tối ưu từ S1.',{x:M,y:4.50,w:8.9,h:0.6,fontSize:16,bold:true,color:FOOTB,align:'center'});
addText('Tháp thị giác và tầng chiếu đa phương thức được đóng băng; khoảng 15 triệu tham số được huấn luyện.',{x:M,y:5.32,w:8.9,h:0.45,fontSize:14.5,color:GREY,align:'center'});
source('Luận văn §4.3, §6.1'); foot();

// 9 · Khung đánh giá
newSlide('8. Khung đánh giá');
addText('Kết quả được xem xét theo ba nhóm thước đo.',{x:M,y:1.0,w:8.9,h:0.45,fontSize:17,bold:true,color:FOOTB,align:'center'});
rect(0.65,1.85,2.65,3.15,LIGHT,{radius:0.05,line:FOOTB});
addText('Executability',{x:0.85,y:2.18,w:2.25,h:0.4,fontSize:18,bold:true,color:FOOTB,align:'center'});
addText('Câu có giúp xác định đúng phần tử và đúng loại thao tác?',{x:0.90,y:3.0,w:2.15,h:0.9,fontSize:14.7,align:'center',valign:'mid',fit:'shrink'});
rect(3.68,1.85,2.65,3.15,LIGHT,{radius:0.05,line:FOOTC});
addText('Thước đo vị trí',{x:3.88,y:2.18,w:2.25,h:0.4,fontSize:18,bold:true,color:FOOTB,align:'center'});
addText('Quy tắc hộp phần tử\nKhoảng cách Euclid',{x:3.93,y:3.0,w:2.15,h:0.9,fontSize:14.5,align:'center',valign:'mid',fit:'shrink'});
rect(6.70,1.85,2.65,3.15,LIGHT,{radius:0.05,line:FOOTD});
addText('Thước đo văn bản',{x:6.90,y:2.18,w:2.25,h:0.4,fontSize:18,bold:true,color:FOOTB,align:'center'});
addText('BLEU, METEOR, ROUGE-L,\nCIDEr-D, SPICE, chrF, BERTScore',{x:6.95,y:2.85,w:2.15,h:1.15,fontSize:14.5,align:'center',valign:'mid',fit:'shrink'});
addText('Kết luận chính dựa trên Executability; các nhóm còn lại bổ sung góc nhìn về vị trí và mức tương đồng với câu tham chiếu.',{x:M,y:5.55,w:8.9,h:0.6,fontSize:15.2,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn Chương 5–6'); foot();

// 10 · Executability ý nghĩa
newSlide('9. Executability - ý nghĩa');
addText('Executability kiểm tra liệu câu hướng dẫn có giúp xác định đúng phần tử, đồng thời mô tả đúng loại thao tác cần thực hiện hay không.',{x:M,y:1.0,w:8.9,h:0.72,fontSize:16.5,bold:true,color:FOOTB,align:'center',fit:'shrink'});
box(0.65,2.45,2.20,1.0,'“Tap Not now”',{bold:true,fill:WHITE,line:FOOTD});
line(2.98,2.95,0.50,0,FOOTC,2,true);
box(3.62,2.45,2.20,1.0,'Màn hình',{bold:true,fill:LIGHT,line:FOOTB});
line(5.95,2.95,0.50,0,FOOTC,2,true);
box(6.58,2.45,2.20,1.0,'Mô hình định vị',{bold:true,fill:LIGHT,line:FOOTC});
line(7.68,3.60,0,0.55,FOOTC,2,true);
box(6.45,4.35,2.45,0.9,'Chọn đúng “Not now”',{bold:true,fill:LIGHT,line:FOOTC,fs:15});
addText('Ví dụ trên minh họa phần định vị; khi tính điểm còn phải đúng loại thao tác và không gọi trạng thái đối nghịch.',{x:M,y:5.62,w:8.9,h:0.66,fontSize:14.8,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn Chương 5'); foot();

// 11 · Executability cách đánh giá
newSlide('10. Executability - cách đánh giá');
addText('Một bước được tính đúng khi đồng thời thỏa ba điều kiện.',{x:M,y:1.0,w:8.9,h:0.45,fontSize:17,bold:true,color:FOOTB,align:'center'});
metricBadge(0.85,1.85,2.3,'1','Đúng loại thao tác',FOOTC);
metricBadge(3.85,1.85,2.3,'2','Không gọi trạng thái\nđối nghịch',FOOTC);
metricBadge(6.85,1.85,2.3,'3','Điểm rơi thuộc đúng\nphần tử cần chạm',FOOTC);
rect(M,4.05,8.9,1.25,LIGHT,{radius:0.05,line:FOOTD});
addText('Chi tiết kỹ thuật của điều kiện 3',{x:M+0.2,y:4.28,w:8.5,h:0.32,fontSize:14.5,bold:true,color:FOOTB,align:'center'});
addText('Điểm phải nằm trong dung sai ±14% theo hai trục và trong vùng Voronoi của phần tử đúng.',{x:M+0.25,y:4.75,w:8.4,h:0.38,fontSize:14.5,align:'center',fit:'shrink'});
addText('Mô hình định vị không biết tọa độ đáp án và không tham gia huấn luyện phương pháp.',{x:M,y:5.90,w:8.9,h:0.42,fontSize:14.5,bold:true,color:FOOTB,align:'center'});
source('Luận văn §5.2–§5.4'); foot();

// 12 · Độ tin cậy metric
newSlide('11. Độ tin cậy của Executability');
metricBadge(0.75,1.35,2.1,'74,9%','Câu tham chiếu',FOOTB);
metricBadge(3.95,1.35,2.1,'12,0%','“Tap the button.”',FOOTC);
metricBadge(7.15,1.35,2.1,'6,1%','Câu từ màn hình khác',FOOTD);
addText('Ba mốc trên được tính trên cùng mẫu ngẫu nhiên 800 bước.',{x:M,y:2.70,w:8.9,h:0.30,fontSize:12.8,color:GREY,align:'center'});
line(M,3.05,8.9,0,RULE,1);
bullets(['Các biến đổi giữ nguyên nghĩa chỉ làm thay đổi kết quả ở 30/1.139 câu; hiệu ròng +0,35 điểm, KTC chứa 0.','Khi đổi sang UI-Venus, phương pháp đề xuất vẫn cao hơn cả hai seed của S1; ACE gần như không đổi so với thành phần thứ nhất.','Phi-4 vẫn giữ rõ chênh lệch S1 − Base, nhưng không tách được phương pháp đề xuất khỏi S1 seed 202.'],M,3.38,8.9,{gap:0.80,fs:13.8,h:0.66});
addText('Độ đo phản ứng rõ khi mất thông tin quy chiếu, nhưng kết quả vẫn cần được đọc cùng giới hạn của mô hình đánh giá.',{x:M,y:5.88,w:8.9,h:0.55,fontSize:13.8,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn §5.5–§5.10'); foot();

// 13 · GRPO
newSlide('12. Cách GRPO hoạt động');
addText('Với cùng một tình huống, mô hình sinh nhiều câu hướng dẫn rồi học từ phần thưởng dựa trên SPICE trong từng nhóm.',{x:M,y:1.05,w:8.9,h:0.72,fontSize:17,bold:true,color:FOOTB,align:'center',fit:'shrink'});
box(0.65,2.35,1.50,0.9,'1 tình huống',{bold:true,fill:LIGHT,line:FOOTD});
line(2.28,2.80,0.45,0,FOOTC,2,true);
box(2.85,2.15,1.70,1.3,'8 câu\nhướng dẫn',{bold:true,fill:LIGHT,line:FOOTB});
line(4.68,2.80,0.45,0,FOOTC,2,true);
box(5.25,2.15,1.70,1.3,'SPICE\n− phạt độ dài',{bold:true,fill:LIGHT,line:FOOTC,fs:15});
line(7.08,2.80,0.45,0,FOOTC,2,true);
box(7.65,2.15,1.70,1.3,'GRPO học từ\nso sánh trong nhóm',{bold:true,fill:LIGHT,line:FOOTD,fs:15});
addText('Câu có điểm cao hơn trong cùng nhóm được tăng ưu tiên; câu có điểm thấp hơn bị giảm ưu tiên.',{x:M,y:4.65,w:8.9,h:0.62,fontSize:16,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn §4.5'); foot();

// 14 · GRPO evidence
newSlide('13. Kết quả GRPO + SPICE');
rect(M,1.0,4.60,4.75,LIGHT,{radius:0.05,line:FOOTD});
addText('Ví dụ',{x:M+0.2,y:1.28,w:4.2,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB,align:'center'});
addText('Cần chạm: Not now',{x:M+0.25,y:1.95,w:4.1,h:0.35,fontSize:15,bold:true,align:'center'});
addText('S1: “Click on the Allow button …”',{x:M+0.25,y:2.75,w:4.1,h:0.45,fontSize:15,italic:true,color:FOOTD,align:'center',fit:'shrink'});
addText('→ sai phần tử',{x:M+0.25,y:3.28,w:4.1,h:0.32,fontSize:13,color:FOOTD,align:'center'});
addText('GRPO + SPICE: “Click on Not now …”',{x:M+0.25,y:3.92,w:4.1,h:0.45,fontSize:15,italic:true,color:FOOTC,align:'center',fit:'shrink'});
addText('→ đúng phần tử',{x:M+0.25,y:4.45,w:4.1,h:0.32,fontSize:13,color:FOOTC,align:'center'});
addText('Lượt 1 · toàn tập kiểm tra',{x:5.45,y:1.0,w:3.8,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB,align:'center'});
table(5.35,1.65,[1.35,1.35,1.35],[{cells:['Metric','S1','GRPO'],fill:FOOTB,color:WHITE,bold:true,h:0.45},{cells:['Exec.','59,11','60,65'],h:0.58,rule:true},{cells:['SPICE','44,37','45,79'],h:0.58,rule:true},{cells:['CIDEr-D','416,12','430,05'],h:0.58}],{align:['left','center','center'],fs:13.5});
addText('+1,55 điểm Executability',{x:5.45,y:4.25,w:3.8,h:0.5,fontSize:18,bold:true,color:FOOTC,align:'center'});
addText('Lượt huấn luyện thứ hai đạt 59,94% Exec. (+0,83 so với S1/101) và không khác S1/202 có ý nghĩa → chiều tăng giữ, độ lớn chưa ổn định.',{x:5.25,y:5.02,w:4.10,h:0.68,fontSize:11.9,color:GREY,align:'center',fit:'shrink'});
source('Luận văn §6.3, §6.7.2'); foot();

// 15 · ACE motivation
newSlide('14. Động lực của ACE');
addText('Một bước mới có thể giống bước đã thấy trong tập huấn luyện, nhưng dùng lại câu không chọn lọc dễ dẫn tới sai thao tác.',{x:M,y:1.05,w:8.9,h:0.78,fontSize:17,bold:true,color:FOOTB,align:'center',fit:'shrink'});
rect(M,2.25,4.15,2.55,LIGHT,{radius:0.05,line:FOOTC});
addText('Cơ hội',{x:M+0.2,y:2.55,w:3.75,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB,align:'center'});
addText('Một bước mới có thể rất giống\nmột bước đã thấy trong tập huấn luyện.',{x:M+0.3,y:3.25,w:3.55,h:0.8,fontSize:16,align:'center',valign:'mid'});
rect(5.30,2.25,4.15,2.55,LIGHT,{radius:0.05,line:FOOTD});
addText('Rủi ro',{x:5.50,y:2.55,w:3.75,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB,align:'center'});
addText('Ví dụ gần giống nhưng khác thao tác\n→ dùng lại câu có thể làm sai kết quả.',{x:5.60,y:3.25,w:3.55,h:0.8,fontSize:16,align:'center',valign:'mid'});
addText('Vì vậy ACE không dùng câu truy hồi ở mọi bước; câu ban đầu chỉ được thay khi thỏa điều kiện chọn lọc.',{x:M,y:5.35,w:8.9,h:0.7,fontSize:15.5,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn §4.6'); foot();

// 16 · ACE process + conditions merged
newSlide('15. Quy trình ACE');
box(0.45,1.25,1.65,0.95,'Câu hướng dẫn\nban đầu',{bold:true,fill:WHITE,line:FOOTD,fs:14.5});
line(2.20,1.73,0.38,0,FOOTC,2,true);
box(2.68,1.15,1.90,1.15,'Truy hồi 4 câu ví dụ\ntương tự',{bold:true,fill:LIGHT,line:FOOTB,fs:14});
line(4.68,1.73,0.38,0,FOOTC,2,true);
box(5.16,1.15,1.55,1.15,'Bộ sinh\nđề xuất câu',{bold:true,fill:LIGHT,line:FOOTC,fs:14});
line(6.81,1.73,0.38,0,FOOTC,2,true);
box(7.29,1.05,2.20,1.35,'Kiểm tra\n2 điều kiện chọn lọc',{bold:true,fill:LIGHT,line:FOOTD,fs:14});
addText('Hai điều kiện',{x:M,y:3.05,w:1.8,h:0.4,fontSize:SECTION_FS,bold:true,color:FOOTB});
rect(M,3.55,4.20,1.05,LIGHT,{radius:0.05,line:FOOTC});
addText('1 · Câu ứng viên phải là một trong bốn câu ví dụ được truy hồi.',{x:M+0.18,y:3.55,w:3.84,h:1.05,fontSize:14.2,bold:true,align:'center',valign:'mid',fit:'shrink'});
rect(5.25,3.55,4.20,1.05,LIGHT,{radius:0.05,line:FOOTC});
addText('2 · Động từ đầu câu thuộc cùng lớp thao tác với câu hướng dẫn ban đầu.',{x:5.43,y:3.55,w:3.84,h:1.05,fontSize:14.0,bold:true,align:'center',valign:'mid',fit:'shrink'});
box(1.95,5.15,2.55,0.8,'Đủ điều kiện → dùng câu mới',{bold:true,fill:LIGHT,line:FOOTC,fs:14});
box(5.50,5.15,2.55,0.8,'Không đủ → giữ câu ban đầu',{bold:true,fill:WHITE,line:FOOTD,fs:14});
source('Luận văn §4.6'); foot();

// 17 · ACE evidence
newSlide('16. Bằng chứng cho điều kiện chọn lọc');
metricBadge(0.75,1.25,2.25,'402','câu được ACE thay',FOOTB);
metricBadge(3.85,1.25,2.25,'9,0%','tổng số bước chạm',FOOTC);
metricBadge(6.95,1.25,2.25,'−1,25','điểm Exec. nếu luôn\ndùng câu mô hình sinh',FOOTD);
line(M,3.05,8.9,0,RULE,1);
bullets(['Trong 402 câu được thay: 15 bước chuyển từ sai sang đúng, 14 bước theo chiều ngược lại.','Sau ACE, Executability gần như không đổi: +0,02 điểm, KTC 95% [−0,21; +0,26].','Điểm quan sát của cả 7 thước đo dựa trên câu tham chiếu đều tăng.'],M,3.45,8.9,{gap:0.82,fs:14.6,h:0.67});
addText('ACE chỉ can thiệp ở 9,0% số bước: giữ gần như nguyên khả năng thao tác, đồng thời làm đầu ra gần câu tham chiếu hơn theo các thước đo văn bản.',{x:M,y:5.82,w:8.9,h:0.72,fontSize:13.8,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn §6.4'); foot();

// 18 · Setup
newSlide('17. Thiết lập thực nghiệm');
addText('S1',{x:M,y:1.0,w:1.0,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Qwen2.5-VL-3B-Instruct + QLoRA 4-bit.','2 epochs, batch hiệu dụng 16, tốc độ học 1e−4.'],M,1.42,4.1,{gap:0.78,fs:15,h:0.63});
addText('GRPO + SPICE',{x:5.05,y:1.0,w:2.0,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['8 câu cho mỗi đầu vào, 500 bước cập nhật.','Phần thưởng: SPICE − phạt độ dài; tốc độ học 1e−5, KL β = 0,04.'],5.05,1.42,4.35,{gap:0.78,fs:14.6,h:0.63});
line(M,3.28,8.9,0,RULE,1);
addText('ACE',{x:M,y:3.62,w:1.0,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Mô hình sinh câu ứng viên học tiếp 250 bước trên 3.991 bước có ảnh.','Suy luận: truy hồi 4 ví dụ; kho không chứa tác vụ của tập kiểm định nội bộ hoặc tập kiểm tra.'],M,4.04,4.1,{gap:0.78,fs:14.2,h:0.63});
addText('Đánh giá',{x:5.05,y:3.62,w:1.2,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['4.463 bước chạm.','KTC 95% và kiểm định cặp cho các so sánh chính.'],5.05,4.04,4.35,{gap:0.78,fs:15,h:0.63});
source('Luận văn §4.3–§4.6, Chương 6'); foot();

// 19 · Main result
newSlide('18. Kết quả khả năng thao tác');
table(M,1.05,[3.0,1.75,1.75,1.75],[{cells:['Mô hình','Executability','Hộp phần tử','Euclid'],fill:FOOTB,color:WHITE,bold:true,h:0.48,fs:12.6},{cells:['Mô hình gốc','47,60','53,60','63,40'],h:0.54,rule:true},{cells:['S1','59,11','65,49','74,37'],h:0.54,rule:true},{cells:['GRPO + SPICE','60,65','67,02','76,25'],h:0.54,rule:true},{cells:[{t:'Phương pháp đề xuất',bold:true,color:FOOTB},{t:'60,68',bold:true,color:FOOTB},{t:'67,11',bold:true,color:FOOTB},{t:'76,32',bold:true,color:FOOTB}],h:0.58,rule:true},{cells:['Câu tham chiếu (mốc)','75,70','—','—'],h:0.54}],{align:['left','center','center','center'],fs:13.2});
rect(M,4.72,8.9,1.05,LIGHT,{radius:0.05,line:FOOTD});
addText('Phương pháp đề xuất − S1/101 = +1,57 điểm Executability\nKTC 95% [+0,86; +2,31], p < 0,001',{x:M+0.2,y:4.83,w:8.5,h:0.82,fontSize:17,bold:true,color:FOOTB,align:'center',valign:'mid'});
source('4.463 bước chạm · Luận văn §6.2, §6.6'); foot();

// 20 · Text metrics simplified
newSlide('19. Kết quả các thước đo dựa trên câu tham chiếu');
addText('So với GRPO + SPICE, sau ACE điểm quan sát của cả 7 thước đo dựa trên câu tham chiếu đều tăng.',{x:M,y:1.02,w:8.9,h:0.62,fontSize:16.5,bold:true,color:FOOTB,align:'center',fit:'shrink'});
metricBadge(0.85,2.05,2.25,'+11,98','CIDEr-D',FOOTC);
metricBadge(3.88,2.05,2.25,'+1,34','SPICE',FOOTC);
metricBadge(6.90,2.05,2.25,'+0,66','BERTScore',FOOTC);
rect(1.05,3.70,7.90,1.05,LIGHT,{radius:0.05,line:FOOTD});
addText('BLEU-4, METEOR, ROUGE-L và chrF cũng tăng → 7/7 thước đo dựa trên câu tham chiếu đều tăng.',{x:1.28,y:3.70,w:7.44,h:1.05,fontSize:15.5,bold:true,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
addText('Executability chỉ thay đổi +0,02 điểm [−0,21; +0,26]. Các mức tăng của 7 thước đo văn bản hiện chưa có khoảng tin cậy.',{x:M,y:5.28,w:8.9,h:0.78,fontSize:14.6,align:'center',fit:'shrink'});
source('Bảng đầy đủ ở slide bổ sung · Luận văn §6.4, §6.6'); foot();

// 21 · Negative results
newSlide('20. Một số hướng đã thử và bài học');
table(M,1.0,[3.0,1.25,4.55],[{cells:['Hướng','Exec.','Điều rút ra'],fill:FOOTB,color:WHITE,bold:true,h:0.46,fs:12.5},{cells:['Mô tả phần tử trước câu','57,2','Bước trung gian đúng thì giúp; sai thì làm câu giảm mạnh.'],h:0.62,rule:true},{cells:['Phần thưởng tọa độ','60,1','Vị trí tốt hơn nhưng câu gần như không đổi.'],h:0.62,rule:true},{cells:['Chọn ứng viên*','56,1','Các trường hợp được chọn có chất lượng tốt, nhưng tỷ lệ từ chối quá cao.'],h:0.62,rule:true},{cells:['TAGE crop editor','60,2','Bộ sửa câu không vượt câu hướng dẫn ban đầu.'],h:0.62}],{align:['left','center','left'],fs:12.5});
rect(M,4.78,8.9,1.18,LIGHT,{radius:0.05,line:FOOTD});
addText('Điểm chung của các thử nghiệm này là cải thiện ở bước trung gian không bảo đảm câu hướng dẫn cuối tốt hơn. Vì vậy phương pháp cuối tác động trực tiếp lên câu được sinh.',{x:M+0.2,y:4.78,w:8.5,h:0.88,fontSize:14.0,bold:true,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
addText('* Cấu hình chọn ứng viên khác ba yếu tố thiết lập, nên chỉ so sánh trực tiếp được với Base.',{x:M+0.2,y:5.72,w:8.5,h:0.32,fontSize:10.8,color:GREY,align:'center',fit:'shrink'});
source('Luận văn §6.10, Phụ lục A'); foot();

// 22 · Limitations
newSlide('21. Hạn chế và hướng phát triển');
addText('Hạn chế',{x:M,y:0.95,w:1.2,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Mức tăng của GRPO + SPICE chưa ổn định giữa hai lượt huấn luyện; thiết lập sinh của S1 và GRPO cũng chưa hoàn toàn đồng nhất.','Executability vẫn là thước đo gián tiếp qua mô hình định vị và chưa được đối chiếu với đánh giá người dùng trên tập đủ lớn.','Trên 2.495 bước không chạm, GRPO + SPICE làm tỉ lệ đúng loại thao tác giảm 1,68 điểm; 7 thước đo văn bản của ACE hiện chưa có KTC.','Thực nghiệm chính mới dùng AndroidControl tiếng Anh, một backbone 3B và lịch sử thao tác tham chiếu.'],M,1.34,8.9,{gap:0.72,fs:13.4,h:0.62});
addText('Hướng phát triển',{x:M,y:4.62,w:2.2,h:0.40,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Đối chiếu Executability với đánh giá của người dùng và đồng nhất chặt hơn thiết lập giữa các mô hình.','Mở rộng sang tập kiểm tra chính thức, bộ dữ liệu thứ hai, bước không chạm và giao diện tiếng Việt.'],M,5.05,8.9,{gap:0.72,fs:13.8,h:0.60});
source('Luận văn §7.2–§7.4'); foot();

// 23 · Conclusion
newSlide('22. Kết luận');
bullets(['Phương pháp đề xuất gồm hai thành phần: GRPO + SPICE sinh câu ban đầu; ACE chỉ hiệu chỉnh có chọn lọc.','Lượt GRPO dùng trong phương pháp tạo phần lớn mức tăng Executability; ACE làm cả 7 thước đo dựa trên câu tham chiếu tăng và gần như giữ nguyên Executability.','Phương pháp đạt 60,7% Executability, cao hơn S1/101 1,57 điểm; KTC 95% [+0,86; +2,31].','Khi lặp lại GRPO + SPICE với seed khác, chiều cải thiện vẫn giữ nhưng độ lớn giảm; vì vậy +1,55 chưa được xem là mức tăng ổn định của phương pháp.'],M,1.15,8.9,{gap:1.02,fs:14.4,h:0.82});
rect(1.20,5.52,7.60,0.72,LIGHT,{radius:0.05,line:FOOTD});
addText('Executability là thước đo chính cho khả năng xác định đúng phần tử và thao tác; các thước đo khác bổ sung góc nhìn về vị trí và câu tham chiếu.',{x:1.42,y:5.52,w:7.16,h:0.72,fontSize:12.8,bold:true,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
source('Luận văn Chương 7'); foot();

// 24 · Cảm ơn — chỉ giữ đúng một câu theo yêu cầu
newSlide();
addText('Trân trọng cảm ơn Quý thầy cô đã lắng nghe.',{x:0.85,y:2.75,w:8.30,h:1.15,fontSize:27,bold:true,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
PAGE++;

// Slide bổ sung 1 · Định nghĩa Executability
newSlide('Định nghĩa Executability'); slide.hidden = true;
addText('Một bước đúng khi đồng thời:',{x:M,y:0.98,w:3.6,h:0.55,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Đúng loại thao tác.','Không mô tả thao tác theo nghĩa ngược.','|px−gx| ≤ 0,14W; |py−gy| ≤ 0,14H.','Điểm p nằm trong ô Voronoi của phần tử cần chạm.'],M,1.5,8.9,{gap:0.82,fs:15.5,h:0.67});
addText('Executability = số bước đúng / tổng số bước chạm.',{x:M,y:5.25,w:8.9,h:0.5,fontSize:17,bold:true,color:FOOTB,align:'center'}); footB();

// Slide bổ sung 2 · Toàn bộ metric
newSlide('Toàn bộ thước đo'); slide.hidden = true;
table(M,0.88,[2.35,1.2,1.2,1.35,1.35,1.25],[{cells:['Metric','Base','S1','GRPO','Đề xuất','Δ ACE'],fill:FOOTB,color:WHITE,bold:true,h:0.42,fs:12},{cells:['Executability','47,60','59,11','60,65','60,68','+0,02'],h:0.42,rule:true},{cells:['Box','53,60','65,49','67,02','67,11','+0,09'],h:0.42,rule:true},{cells:['Euclid','63,40','74,37','76,25','76,32','+0,07'],h:0.42,rule:true},{cells:['BLEU-4','15,30','51,56','52,36','53,47','+1,11'],h:0.42,rule:true},{cells:['METEOR','24,60','36,79','37,92','38,37','+0,46'],h:0.42,rule:true},{cells:['ROUGE-L','42,30','67,35','68,36','69,08','+0,74'],h:0.42,rule:true},{cells:['CIDEr-D','88,00','416,12','430,05','442,02','+11,98'],h:0.42,rule:true},{cells:['SPICE','18,50','44,37','45,79','47,13','+1,34'],h:0.42,rule:true},{cells:['chrF','40,20','61,26','62,87','63,44','+0,58'],h:0.42,rule:true},{cells:['BERTScore','40,10','66,33','67,07','67,73','+0,66'],h:0.42}],{align:['left','center','center','center','center','center'],fs:11.7}); footB();

// Slide bổ sung 3 · Cross-listener
newSlide('Cross-listener validation'); slide.hidden = true;
table(M,1.2,[3.5,2.5,2.5],[{cells:['Phép so','UGround','UI-Venus'],fill:FOOTB,color:WHITE,bold:true,h:0.46},{cells:['S1 − Base',{t:'+10,35',bold:true},{t:'+9,68',bold:true}],h:0.58,rule:true},{cells:['Mô tả phần tử trước câu (S2) − S1','−1,93','−1,21'],h:0.58,rule:true},{cells:['Câu chuẩn','70,0','69,3'],h:0.58}],{align:['left','center','center'],fs:13});
addText('Phi-4 giữ rõ chênh lệch S1 − Base, nhưng không tách được phương pháp đề xuất khỏi S1 seed 202.',{x:M,y:4.35,w:8.9,h:0.65,fontSize:14.5,bold:true,color:FOOTB,align:'center',fit:'shrink'}); footB();

// Slide bổ sung 4 · Cấu hình huấn luyện
newSlide('Cấu hình huấn luyện'); slide.hidden = true;
table(M,1.0,[3.0,5.8],[{cells:['Hạng mục','Giá trị'],fill:FOOTB,color:WHITE,bold:true,h:0.44},{cells:['Backbone','Qwen2.5-VL-3B-Instruct'],h:0.48,rule:true},{cells:['Fine-tuning','QLoRA NF4 4-bit, rank 8, alpha 16, dropout 0,05'],h:0.48,rule:true},{cells:['SFT','2 epochs = 8.072 steps, batch hiệu dụng 16, LR 1e−4'],h:0.48,rule:true},{cells:['GRPO','8 samples/prompt, 500 updates, LR 1e−5, KL β 0,04'],h:0.48,rule:true},{cells:['Phần cứng','1 × A100, vision tower không cập nhật tham số'],h:0.48}],{align:['left','left'],fs:12.7}); footB();

pptx.writeFile({ fileName:path.join(__dirname, '..', 'LUAN_VAN_SLIDE_BAO_VE_CONCISE.pptx') });
