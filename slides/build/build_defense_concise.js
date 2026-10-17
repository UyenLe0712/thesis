const pptxgen = require('pptxgenjs');

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
let slide, PAGE=0, BPAGE=0; const TOTAL=28;

function addText(t,o={}){ slide.addText(t,Object.assign({fontFace:TF,fontSize:BODY_FS,color:INK,margin:0},o)); }
function rect(x,y,w,h,fill,o={}){ slide.addShape(o.radius?pptx.ShapeType.roundRect:pptx.ShapeType.rect,{x,y,w,h,fill:{color:fill},line:o.line?{color:o.line,width:o.lw||1}:{color:fill,transparency:100},radius:o.radius||0}); }
function line(x,y,w,h,c=RULE,lw=1,end=false){ slide.addShape(pptx.ShapeType.line,{x,y,w,h,line:{color:c,width:lw,endArrowType:end?'triangle':'none'}}); }
function bar(title){ rect(0,0,W,0.6,BAR); addText(title,{x:0.22,y:0,w:W-0.44,h:0.6,fontSize:TITLE_FS,bold:true,color:WHITE,valign:'mid'}); }
function footRow(label){ const y=H-0.26,h=0.26; rect(0,y,3,h,FOOTA);rect(3,y,3.7,h,FOOTB);rect(6.7,y,1.9,h,FOOTC);rect(8.6,y,1.4,h,FOOTD); addText('Luận văn thạc sĩ',{x:0,y,w:3,h,fontFace:MONO,fontSize:8,bold:true,color:WHITE,align:'center',valign:'mid'}); addText('Phát sinh tự động hướng dẫn sử dụng phần mềm dựa trên LLM',{x:3,y,w:3.7,h,fontSize:8,color:WHITE,align:'center',valign:'mid'}); addText('Lê Đoàn Phương Uyên',{x:6.7,y,w:1.9,h,fontSize:8,color:WHITE,align:'center',valign:'mid'}); addText(label,{x:8.6,y,w:1.4,h,fontSize:8,color:WHITE,align:'center',valign:'mid'}); }
function foot(){ PAGE++; footRow(`${PAGE}/${TOTAL}`); }
function footB(){ BPAGE++; footRow(`dự phòng ${BPAGE}`); }
function newSlide(title){ slide=pptx.addSlide(); slide.background={color:WHITE}; if(title) bar(title); }
function bullets(items,x,y,w,o={}){ const gap=o.gap||0.88; items.forEach((it,i)=>{ const yy=y+i*gap; slide.addShape(pptx.ShapeType.ellipse,{x:x+0.02,y:yy+0.15,w:0.07,h:0.07,fill:{color:o.dot||ACCENT},line:{color:o.dot||ACCENT,transparency:100}}); addText(it,{x:x+0.23,y:yy,w:w-0.23,h:o.h||0.72,fontSize:o.fs||BODY_FS,color:o.color||INK,fit:'shrink',valign:'top',lineSpacingMultiple:1.12}); }); }
function box(x,y,w,h,t,o={}){ rect(x,y,w,h,o.fill||WHITE,{radius:0.05,line:o.line||ACCENT2,lw:o.lw||1}); addText(t,{x,y,w,h,fontSize:o.fs||BODY_FS,bold:o.bold,color:o.color||INK,align:'center',valign:'mid',fit:'shrink'}); }
function source(t){ addText(t,{x:M,y:6.92,w:W-2*M,h:0.15,fontSize:8,italic:true,color:GREY,align:'right'}); }
function metricBadge(x,y,w,value,label,color=ACCENT){ addText(value,{x,y,w,h:0.55,fontSize:24,bold:true,color,align:'center',valign:'mid'}); addText(label,{x,y:y+0.58,w,h:0.45,fontSize:SMALL_FS,bold:true,color:INK,align:'center',valign:'mid',fit:'shrink'}); }
function table(x,y,colW,rows,o={}){ let yy=y; rows.forEach(r=>{ const h=r.h||0.48; if(r.fill) rect(x,yy,colW.reduce((a,b)=>a+b,0),h,r.fill); let xx=x; r.cells.forEach((c,i)=>{ const cell=typeof c==='string'?{t:c}:c; addText(cell.t,{x:xx,y:yy,w:colW[i],h,fontSize:cell.fs||r.fs||o.fs||TABLE_FS,bold:cell.bold!=null?cell.bold:r.bold,color:cell.color||r.color||INK,align:cell.align||(o.align&&o.align[i])||'left',valign:'mid',fit:'shrink',italic:cell.italic}); xx += colW[i]; }); if(r.rule) line(x,yy+h,colW.reduce((a,b)=>a+b,0),0,r.rule===true?RULE:r.rule,1); yy += h; }); }
function note(t){ slide.addNotes(t); }

newSlide();
rect(0,0,W,0.66,FOOTA);
addText('ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH  -  TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN',{x:0,y:0,w:W,h:0.66,fontSize:14,bold:true,color:WHITE,align:'center',valign:'mid'});
rect(0.8,1.18,W-1.6,2.5,FOOTB,{radius:0.08});
addText('LUẬN VĂN THẠC SĨ  -  NGÀNH TRÍ TUỆ NHÂN TẠO',{x:0.8,y:1.45,w:W-1.6,h:0.35,fontSize:14,bold:true,color:WHITE,align:'center'});
addText('PHÁT SINH TỰ ĐỘNG HƯỚNG DẪN SỬ DỤNG PHẦN MỀM\nDỰA TRÊN LLM TỪ CÁC TRƯỜNG HỢP SỬ DỤNG\nVÀ GIAO DIỆN NGƯỜI DÙNG',{x:0.95,y:1.96,w:W-1.9,h:1.45,fontSize:21,bold:true,color:WHITE,align:'center',valign:'mid',fit:'shrink'});
addText('Học viên thực hiện: Lê Đoàn Phương Uyên',{x:0.8,y:4.55,w:W-1.6,h:0.4,fontSize:16,bold:true,align:'center'});
addText('Giáo viên hướng dẫn: TS. Nguyễn Hồng Bửu Long',{x:0.8,y:5.0,w:W-1.6,h:0.4,fontSize:16,bold:true,align:'center'});
addText('TP. Hồ Chí Minh - 2026',{x:0.8,y:5.88,w:W-1.6,h:0.35,fontSize:13,align:'center'});
note('Mở đầu ngắn: đề tài sinh một câu hướng dẫn cho bước tiếp theo từ màn hình và mục tiêu người dùng.');
foot();

newSlide('1. Bài toán thực tế');
addText('Mục tiêu',{x:M,y:1.0,w:1.2,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
addText('Từ trạng thái giao diện hiện tại, sinh một câu hướng dẫn để người dùng biết chính xác bước tiếp theo cần làm.',{x:M,y:1.48,w:8.9,h:0.75,fontSize:17,bold:true,color:INK,fit:'shrink'});
box(0.75,2.75,2.15,1.05,'Màn hình hiện tại',{bold:true,fill:LIGHT,line:FOOTD});
line(3.05,3.28,0.65,0,FOOTC,2,true);
box(3.85,2.75,2.15,1.05,'Mô hình sinh câu',{bold:true,fill:LIGHT,line:FOOTB});
line(6.15,3.28,0.65,0,FOOTC,2,true);
box(6.95,2.55,2.30,1.45,'“Chạm vào\nNot now”',{bold:true,fill:LIGHT,line:FOOTC});
addText('Sản phẩm cuối là câu dành cho người dùng, không phải tọa độ để agent tự thao tác.',{x:M,y:4.85,w:8.9,h:0.6,fontSize:16,bold:true,color:FOOTB,align:'center'});
source('Luận văn Chương 1'); foot();

newSlide('2. Định nghĩa bài toán');
addText('Đầu vào',{x:M,y:0.98,w:1.2,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Ảnh màn hình hiện tại.','Mục tiêu người dùng.','Các bước đã thực hiện trước đó.','Thông tin OCR trên giao diện.'],M,1.40,4.1,{gap:0.72,fs:15.5,h:0.58});
addText('Đầu ra',{x:5.15,y:0.98,w:1.2,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
rect(5.15,1.48,4.30,2.20,LIGHT,{radius:0.05,line:FOOTD});
addText('Một câu hướng dẫn cho\nbước tiếp theo',{x:5.45,y:1.88,w:3.70,h:0.8,fontSize:19,bold:true,color:FOOTB,align:'center',valign:'mid'});
addText('Ví dụ: “Tap Not now to continue.”',{x:5.45,y:2.95,w:3.70,h:0.45,fontSize:15,italic:true,color:FOOTC,align:'center'});
addText('Yêu cầu quan trọng: câu phải đủ rõ để phân biệt đúng phần tử cần thao tác.',{x:M,y:5.15,w:8.9,h:0.65,fontSize:16,bold:true,color:FOOTB,align:'center'});
source('Luận văn §1.2–§1.3'); foot();

newSlide('3. Thách thức của câu hướng dẫn GUI');
addText('Một câu có thể đúng ngữ pháp nhưng vẫn không giúp người dùng thao tác đúng.',{x:M,y:1.0,w:8.9,h:0.55,fontSize:17,bold:true,color:FOOTB,align:'center'});
rect(M,1.95,4.15,2.75,LIGHT,{radius:0.05,line:FOOTD});
addText('Câu mơ hồ',{x:M+0.2,y:2.2,w:3.75,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB,align:'center'});
addText('“Tap the button.”',{x:M+0.25,y:3.0,w:3.65,h:0.48,fontSize:19,italic:true,color:FOOTD,align:'center'});
addText('Không biết phải chạm nút nào khi màn hình có nhiều nút.',{x:M+0.3,y:3.75,w:3.55,h:0.7,fontSize:15,align:'center',fit:'shrink'});
rect(5.30,1.95,4.15,2.75,LIGHT,{radius:0.05,line:FOOTC});
addText('Câu đủ rõ',{x:5.50,y:2.2,w:3.75,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB,align:'center'});
addText('“Tap Not now.”',{x:5.55,y:3.0,w:3.65,h:0.48,fontSize:19,italic:true,color:FOOTC,align:'center'});
addText('Chỉ ra đúng phần tử cần thao tác.',{x:5.60,y:3.75,w:3.55,h:0.7,fontSize:15,bold:true,align:'center'});
addText('→ Thách thức chính là tính phân biệt và khả năng dẫn tới đúng thao tác.',{x:M,y:5.35,w:8.9,h:0.55,fontSize:16,bold:true,color:FOOTB,align:'center'});
source('Luận văn Chương 1'); foot();

newSlide('4. Khoảng trống đánh giá');
addText('Các thước đo so sánh câu chưa trực tiếp phản ánh điều người dùng thực sự cần.',{x:M,y:1.0,w:8.9,h:0.55,fontSize:17,bold:true,color:FOOTB,align:'center'});
box(0.70,2.05,2.55,1.2,'BLEU / ROUGE\nCâu giống reference đến đâu?',{bold:true,fill:LIGHT,line:FOOTD,fs:15});
box(3.72,2.05,2.55,1.2,'SPICE / CIDEr\nNội dung có tương đồng?',{bold:true,fill:LIGHT,line:FOOTD,fs:15});
box(6.75,1.85,2.55,1.6,'Điều cần biết\nCâu có dẫn tới đúng\nphần tử hay không?',{bold:true,fill:LIGHT,line:FOOTC,fs:15});
addText('Vì vậy luận văn báo cáo cả chất lượng câu, chất lượng định vị và Executability.',{x:M,y:4.55,w:8.9,h:0.65,fontSize:16,bold:true,color:FOOTB,align:'center'});
source('Luận văn Chương 5'); foot();

newSlide('5. Đóng góp của luận văn');
bullets(['GRPO + SPICE: tối ưu trực tiếp câu hướng dẫn cuối cùng.','ACE: dùng ví dụ tham chiếu có chọn lọc để cải thiện cách diễn đạt.','Executability: đo câu có đủ rõ để định vị đúng phần tử trên giao diện hay không.','Phân tích ablation và các hướng đã thử để xác định vai trò của từng thành phần.'],M,1.25,8.9,{gap:1.08,fs:16,h:0.88});
rect(M,5.65,8.9,0.65,LIGHT,{radius:0.05,line:FOOTD});
addText('Kết quả chính: 60,7% Executability, cao hơn S1 1,57 điểm; KTC 95% [+0,86; +2,31].',{x:M+0.18,y:5.65,w:8.54,h:0.65,fontSize:15.5,bold:true,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
source('Luận văn §1.6, §6.2'); foot();

newSlide('6. Tổng quan phương pháp');
box(0.55,1.35,0.80,0.9,'S1',{bold:true,line:FOOTD});
line(1.45,1.80,0.35,0,FOOTC,2,true);
box(1.90,1.35,1.85,0.9,'GRPO + SPICE',{bold:true,fill:LIGHT,line:FOOTB,fs:15});
line(3.85,1.80,0.30,0,FOOTC,2,true);
box(4.25,1.20,1.75,1.20,'Câu hướng dẫn\nban đầu',{bold:true,fill:WHITE,line:FOOTD,fs:14.5});
line(6.10,1.80,0.30,0,FOOTC,2,true);
box(6.50,1.35,0.90,0.9,'ACE',{bold:true,fill:LIGHT,line:FOOTC});
line(7.50,1.80,0.30,0,FOOTC,2,true);
box(7.90,1.20,1.55,1.20,'Câu hướng dẫn\ncuối',{bold:true,fill:WHITE,line:FOOTD,fs:14.5});
addText('Thành phần 1',{x:M,y:3.45,w:1.8,h:0.45,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['GRPO học từ nhiều câu ứng viên trong cùng một tình huống.','SPICE cung cấp tín hiệu về mức độ đúng nội dung.'],M,4.00,4.25,{gap:0.82,fs:15,h:0.67});
addText('Thành phần 2',{x:5.05,y:3.45,w:1.8,h:0.45,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['ACE truy hồi 4 ví dụ tương tự.','Chỉ thay câu hướng dẫn ban đầu khi thỏa điều kiện chọn lọc.'],5.05,4.00,4.40,{gap:0.82,fs:15,h:0.67});
source('Luận văn Chương 4'); foot();

newSlide('7. Mô hình nền S1');
addText('Backbone',{x:M,y:1.0,w:1.3,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
addText('Qwen2.5-VL-3B-Instruct + QLoRA 4-bit',{x:M,y:1.45,w:8.9,h:0.55,fontSize:19,bold:true,color:INK,align:'center'});
metricBadge(0.85,2.55,2.2,'47,6%','Mô hình gốc',FOOTD);
metricBadge(3.90,2.55,2.2,'59,1%','S1 - seed 101',FOOTB);
metricBadge(6.95,2.55,2.2,'59,6%','S1 - seed 202',FOOTC);
addText('SFT đã tạo ra bước nhảy lớn; phương pháp đề xuất tiếp tục tối ưu từ S1.',{x:M,y:4.50,w:8.9,h:0.6,fontSize:16,bold:true,color:FOOTB,align:'center'});
addText('Vision tower / projector được đóng băng; khoảng 15 triệu tham số được huấn luyện.',{x:M,y:5.32,w:8.9,h:0.45,fontSize:14.5,color:GREY,align:'center'});
source('Luận văn §4.3, §6.1'); foot();

newSlide('8. Cách GRPO hoạt động');
addText('Thay vì học từ một câu duy nhất, mô hình tự tạo nhiều cách hướng dẫn cho cùng tình huống rồi học từ sự khác biệt giữa chúng.',{x:M,y:1.05,w:8.9,h:0.75,fontSize:17,bold:true,color:FOOTB,align:'center',fit:'shrink'});
box(0.65,2.35,1.50,0.9,'1 tình huống',{bold:true,fill:LIGHT,line:FOOTD});
line(2.28,2.80,0.45,0,FOOTC,2,true);
box(2.85,2.15,1.70,1.3,'8 câu\nhướng dẫn',{bold:true,fill:LIGHT,line:FOOTB});
line(4.68,2.80,0.45,0,FOOTC,2,true);
box(5.25,2.15,1.70,1.3,'Chấm từng câu\nbằng SPICE',{bold:true,fill:LIGHT,line:FOOTC,fs:15});
line(7.08,2.80,0.45,0,FOOTC,2,true);
box(7.65,2.15,1.70,1.3,'GRPO học từ\nso sánh trong nhóm',{bold:true,fill:LIGHT,line:FOOTD,fs:15});
addText('Câu tốt hơn trong cùng nhóm được tăng ưu tiên; câu kém hơn bị giảm ưu tiên.',{x:M,y:4.65,w:8.9,h:0.55,fontSize:16,bold:true,color:FOOTB,align:'center'});
source('Luận văn §4.5'); foot();

newSlide('9. Quy trình GRPO + SPICE');
addText('Mục tiêu',{x:M,y:0.95,w:1.3,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
addText('Giúp mô hình ưu tiên những câu hướng dẫn đúng nội dung và ít mơ hồ hơn.',{x:M,y:1.40,w:8.9,h:0.55,fontSize:17,bold:true,color:INK,align:'center'});
bullets(['Với cùng một tình huống, mô hình sinh 8 câu hướng dẫn khác nhau.','SPICE đánh giá mức độ tương đồng về nội dung của mỗi câu với câu chuẩn.','GRPO so sánh các câu trong cùng nhóm để cập nhật mô hình.'],M,2.35,8.9,{gap:0.94,fs:15.8,h:0.78});
rect(M,5.25,8.9,0.85,LIGHT,{radius:0.05,line:FOOTD});
addText('Chi tiết huấn luyện như 500 updates, KL β = 0,04 và length penalty được để ở slide dự phòng.',{x:M+0.2,y:5.25,w:8.5,h:0.85,fontSize:14.5,color:GREY,align:'center',valign:'mid',fit:'shrink'});
source('Luận văn §4.5'); foot();

newSlide('10. Hiệu quả riêng của GRPO + SPICE');
rect(M,1.0,4.60,4.75,LIGHT,{radius:0.05,line:FOOTD});
addText('Ví dụ',{x:M+0.2,y:1.28,w:4.2,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB,align:'center'});
addText('Cần chạm: Not now',{x:M+0.25,y:1.95,w:4.1,h:0.35,fontSize:15,bold:true,align:'center'});
addText('S1: “Click on the Allow button …”',{x:M+0.25,y:2.75,w:4.1,h:0.45,fontSize:15,italic:true,color:FOOTD,align:'center',fit:'shrink'});
addText('→ sai phần tử',{x:M+0.25,y:3.28,w:4.1,h:0.32,fontSize:13,color:FOOTD,align:'center'});
addText('GRPO + SPICE: “Click on Not now …”',{x:M+0.25,y:3.92,w:4.1,h:0.45,fontSize:15,italic:true,color:FOOTC,align:'center',fit:'shrink'});
addText('→ đúng phần tử',{x:M+0.25,y:4.45,w:4.1,h:0.32,fontSize:13,color:FOOTC,align:'center'});
addText('Kết quả định lượng',{x:5.45,y:1.0,w:3.8,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB,align:'center'});
table(5.35,1.65,[1.35,1.35,1.35],[{cells:['Metric','S1','GRPO'],fill:FOOTB,color:WHITE,bold:true,h:0.45},{cells:['Exec.','59,11','60,65'],h:0.58,rule:true},{cells:['SPICE','44,37','45,79'],h:0.58,rule:true},{cells:['CIDEr-D','416,12','430,05'],h:0.58}],{align:['left','center','center'],fs:13.5});
addText('+1,55 điểm Executability',{x:5.45,y:4.25,w:3.8,h:0.5,fontSize:18,bold:true,color:FOOTC,align:'center'});
source('Luận văn §6.3'); foot();

newSlide('11. Động lực của ACE');
addText('Tập huấn luyện chứa nhiều câu chuẩn có thể giúp diễn đạt tốt hơn, nhưng sao chép không chọn lọc có thể làm sai thao tác.',{x:M,y:1.05,w:8.9,h:0.78,fontSize:17,bold:true,color:FOOTB,align:'center',fit:'shrink'});
rect(M,2.25,4.15,2.55,LIGHT,{radius:0.05,line:FOOTC});
addText('Cơ hội',{x:M+0.2,y:2.55,w:3.75,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB,align:'center'});
addText('Một bước mới có thể rất giống\nmột bước đã thấy trong train.',{x:M+0.3,y:3.25,w:3.55,h:0.8,fontSize:16,align:'center',valign:'mid'});
rect(5.30,2.25,4.15,2.55,LIGHT,{radius:0.05,line:FOOTD});
addText('Rủi ro',{x:5.50,y:2.55,w:3.75,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB,align:'center'});
addText('Ví dụ gần giống nhưng khác thao tác\n→ sao chép sai câu sẽ làm hỏng kết quả.',{x:5.60,y:3.25,w:3.55,h:0.8,fontSize:16,align:'center',valign:'mid'});
addText('ACE chỉ thay câu hướng dẫn ban đầu khi câu mới khớp với ví dụ tham chiếu và cùng loại thao tác.',{x:M,y:5.35,w:8.9,h:0.7,fontSize:15.5,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn §4.6'); foot();

newSlide('12. Quy trình ACE');
box(0.55,1.45,1.75,1.0,'Câu hướng dẫn\nban đầu',{bold:true,fill:WHITE,line:FOOTD,fs:15});
line(2.40,1.95,0.40,0,FOOTC,2,true);
box(2.90,1.35,2.05,1.2,'Truy hồi 4 ví dụ\ntương tự',{bold:true,fill:LIGHT,line:FOOTB,fs:15});
line(5.05,1.95,0.40,0,FOOTC,2,true);
box(5.55,1.35,1.65,1.2,'Bộ sinh\nđề xuất câu',{bold:true,fill:LIGHT,line:FOOTC,fs:15});
line(7.30,1.95,0.40,0,FOOTC,2,true);
box(7.80,1.35,1.65,1.2,'Kiểm tra\nđiều kiện chọn lọc',{bold:true,fill:LIGHT,line:FOOTD,fs:14.5});
addText('Nếu đạt điều kiện',{x:5.45,y:3.35,w:1.7,h:0.35,fontSize:14.5,bold:true,color:FOOTB,align:'center'});
line(6.30,3.75,0,0.55,FOOTC,2,true);
box(5.25,4.45,2.10,0.9,'Dùng câu mới',{bold:true,fill:LIGHT,line:FOOTC});
addText('Nếu không đạt',{x:7.60,y:3.35,w:1.7,h:0.35,fontSize:14.5,bold:true,color:FOOTB,align:'center'});
line(8.45,3.75,0,0.55,FOOTD,2,true);
box(7.45,4.45,2.00,0.9,'Giữ câu ban đầu',{bold:true,fill:WHITE,line:FOOTD,fs:15});
source('Luận văn §4.6'); foot();

newSlide('13. Điều kiện chọn lọc của ACE');
addText('ACE chỉ thay câu hướng dẫn ban đầu khi đồng thời thỏa hai điều kiện.',{x:M,y:1.05,w:8.9,h:0.55,fontSize:17,bold:true,color:FOOTB,align:'center'});
metricBadge(1.05,2.25,2.8,'1','Câu mới trùng nguyên văn\nmột ví dụ tham chiếu',FOOTC);
metricBadge(6.10,2.25,2.8,'2','Cùng loại thao tác với\ncâu hướng dẫn ban đầu',FOOTC);
addText('Mục đích của hai điều kiện: chỉ tận dụng ví dụ khi có bằng chứng mạnh rằng câu đó phù hợp.',{x:M,y:4.65,w:8.9,h:0.65,fontSize:16,bold:true,color:FOOTB,align:'center'});
source('Luận văn §4.6'); foot();

newSlide('14. Bằng chứng cho điều kiện chọn lọc');
metricBadge(0.75,1.35,2.25,'402','câu được ACE thay',FOOTB);
metricBadge(3.85,1.35,2.25,'9,0%','tổng số touch steps',FOOTC);
metricBadge(6.95,1.35,2.25,'−1,25','điểm Exec. nếu dùng\nbộ sinh ở mọi bước',FOOTD);
line(M,3.25,8.9,0,RULE,1);
bullets(['Trong 402 câu được thay: 15 bước được sửa đúng, 14 bước bị làm sai.','Full ACE gần như giữ nguyên Executability so với GRPO: +0,02 điểm.','Nhưng cải thiện đồng thời 7/7 metric chất lượng câu.'],M,3.65,8.9,{gap:0.82,fs:15.5,h:0.67});
addText('→ Vai trò của ACE là cải thiện câu một cách chọn lọc, không phải thay toàn bộ câu hướng dẫn ban đầu.',{x:M,y:5.88,w:8.9,h:0.66,fontSize:14.5,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn §6.4'); foot();

newSlide('15. Khung đánh giá');
addText('Luận văn đánh giá ở ba góc nhìn bổ sung cho nhau.',{x:M,y:1.0,w:8.9,h:0.45,fontSize:17,bold:true,color:FOOTB,align:'center'});
rect(0.65,1.85,2.65,3.15,LIGHT,{radius:0.05,line:FOOTB});
addText('Executability',{x:0.85,y:2.18,w:2.25,h:0.4,fontSize:18,bold:true,color:FOOTB,align:'center'});
addText('Câu có đủ rõ để tìm đúng phần tử cần thao tác?',{x:0.90,y:3.0,w:2.15,h:0.9,fontSize:15,align:'center',valign:'mid'});
rect(3.68,1.85,2.65,3.15,LIGHT,{radius:0.05,line:FOOTC});
addText('Location metrics',{x:3.88,y:2.18,w:2.25,h:0.4,fontSize:18,bold:true,color:FOOTB,align:'center'});
addText('AndroidControl Box\nAitW Euclid',{x:3.93,y:3.0,w:2.15,h:0.9,fontSize:15,align:'center',valign:'mid'});
rect(6.70,1.85,2.65,3.15,LIGHT,{radius:0.05,line:FOOTD});
addText('Text metrics',{x:6.90,y:2.18,w:2.25,h:0.4,fontSize:18,bold:true,color:FOOTB,align:'center'});
addText('BLEU, METEOR, ROUGE-L,\nCIDEr-D, SPICE, chrF, BERTScore',{x:6.95,y:2.85,w:2.15,h:1.15,fontSize:14.5,align:'center',valign:'mid',fit:'shrink'});
addText('Kết luận chính dựa trên Executability; các nhóm còn lại giúp kiểm tra vị trí và chất lượng câu.',{x:M,y:5.55,w:8.9,h:0.6,fontSize:15.5,bold:true,color:FOOTB,align:'center'});
source('Luận văn Chương 5–6'); foot();

newSlide('16. Executability - ý nghĩa');
addText('Executability đo xem câu hướng dẫn có chứa đủ thông tin để một mô hình độc lập nhìn màn hình và tìm đúng phần tử cần thao tác hay không.',{x:M,y:1.0,w:8.9,h:0.85,fontSize:17,bold:true,color:FOOTB,align:'center',fit:'shrink'});
box(0.65,2.45,2.20,1.0,'“Tap Not now”',{bold:true,fill:WHITE,line:FOOTD});
line(2.98,2.95,0.50,0,FOOTC,2,true);
box(3.62,2.45,2.20,1.0,'Màn hình',{bold:true,fill:LIGHT,line:FOOTB});
line(5.95,2.95,0.50,0,FOOTC,2,true);
box(6.58,2.45,2.20,1.0,'Mô hình định vị',{bold:true,fill:LIGHT,line:FOOTC});
line(7.68,3.60,0,0.55,FOOTC,2,true);
box(6.45,4.35,2.45,0.9,'Chọn đúng “Not now”',{bold:true,fill:LIGHT,line:FOOTC,fs:15});
addText('Chọn đúng phần tử → câu được tính là executable.',{x:M,y:5.70,w:8.9,h:0.5,fontSize:17,bold:true,color:FOOTB,align:'center'});
source('Luận văn Chương 5'); foot();

newSlide('17. Executability - cách đánh giá');
addText('Một bước được tính đúng khi đồng thời thỏa ba điều kiện.',{x:M,y:1.0,w:8.9,h:0.45,fontSize:17,bold:true,color:FOOTB,align:'center'});
metricBadge(0.85,1.85,2.3,'1','Đúng loại thao tác',FOOTC);
metricBadge(3.85,1.85,2.3,'2','Không đảo nghĩa',FOOTC);
metricBadge(6.85,1.85,2.3,'3','Điểm rơi thuộc đúng\nphần tử cần chạm',FOOTC);
rect(M,4.05,8.9,1.25,LIGHT,{radius:0.05,line:FOOTD});
addText('Chi tiết kỹ thuật của điều kiện 3',{x:M+0.2,y:4.28,w:8.5,h:0.32,fontSize:14.5,bold:true,color:FOOTB,align:'center'});
addText('Điểm phải nằm trong dung sai ±14% theo hai trục và trong vùng Voronoi của phần tử đúng.',{x:M+0.25,y:4.75,w:8.4,h:0.38,fontSize:14.5,align:'center',fit:'shrink'});
addText('Mô hình định vị không biết tọa độ đáp án và không tham gia huấn luyện phương pháp.',{x:M,y:5.90,w:8.9,h:0.42,fontSize:14.5,bold:true,color:FOOTB,align:'center'});
source('Luận văn §5.2–§5.4'); foot();

newSlide('18. Độ tin cậy của Executability');
metricBadge(0.75,1.35,2.1,'75,7%','Câu chuẩn',FOOTB);
metricBadge(3.95,1.35,2.1,'12,0%','“Tap the button.”',FOOTC);
metricBadge(7.15,1.35,2.1,'6,1%','Câu từ màn hình khác',FOOTD);
line(M,3.05,8.9,0,RULE,1);
bullets(['Viết lại câu mà giữ nguyên nghĩa gần như không làm điểm thay đổi.','Đổi mô hình định vị sang UI-Venus vẫn giữ khoảng 94% độ lớn chênh S1 − Base.','Phi-4 ngoài họ Qwen vẫn giữ thứ tự: Câu chuẩn > S1 > Base > Câu chung chung.'],M,3.45,8.9,{gap:0.82,fs:15.2,h:0.67});
addText('→ Executability phản ánh nội dung hướng dẫn, không chỉ cách diễn đạt.',{x:M,y:5.86,w:8.9,h:0.66,fontSize:14.5,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn §5.5–§5.10'); foot();

newSlide('19. Dữ liệu AndroidControl');
addText('Phân chia dữ liệu',{x:M,y:1.0,w:2.0,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
table(M,1.48,[2.7,2.0,2.0,2.2],[{cells:['','Huấn luyện','Kiểm tra','Ghi chú'],fill:FOOTB,color:WHITE,bold:true,h:0.46},{cells:['Số bước','64.567','6.958','chia theo tác vụ'],h:0.52,rule:true},{cells:['Bước chạm','41.191','4.463','dùng để tính Executability'],h:0.52,rule:true},{cells:['Số tác vụ','12.895','1.432','task-held-out'],h:0.52}],{align:['left','center','center','left'],fs:13.5});
addText('Đặc điểm cần lưu ý',{x:M,y:3.75,w:2.2,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Train/test không trùng tác vụ.','95,6% bước test gán được app thuộc các app đã thấy trong train.','17,3% câu chuẩn test xuất hiện nguyên văn trong train.'],M,4.20,8.9,{gap:0.68,fs:15,h:0.56});
source('Luận văn Chương 3, §6.8'); foot();

newSlide('20. Thiết lập thực nghiệm');
addText('S1',{x:M,y:1.0,w:1.0,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Qwen2.5-VL-3B-Instruct + QLoRA 4-bit.','2 epochs, batch hiệu dụng 16, learning rate 1e−4.'],M,1.42,4.1,{gap:0.78,fs:15,h:0.63});
addText('GRPO + SPICE',{x:5.05,y:1.0,w:2.0,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['8 câu / prompt, 500 updates.','Learning rate 1e−5, KL β = 0,04.'],5.05,1.42,4.35,{gap:0.78,fs:15,h:0.63});
line(M,3.28,8.9,0,RULE,1);
addText('ACE',{x:M,y:3.62,w:1.0,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Truy hồi 4 ví dụ theo mục tiêu + bước trước.','Kho truy hồi loại các task nội bộ val/test.'],M,4.04,4.1,{gap:0.78,fs:15,h:0.63});
addText('Đánh giá',{x:5.05,y:3.62,w:1.2,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['4.463 touch steps.','KTC 95% và kiểm định cặp cho các so sánh chính.'],5.05,4.04,4.35,{gap:0.78,fs:15,h:0.63});
source('Luận văn §4.3–§4.6, Chương 6'); foot();

newSlide('21. Kết quả khả năng thao tác');
table(M,1.05,[3.0,1.75,1.75,1.75],[{cells:['Mô hình','Executability','Box','Euclid'],fill:FOOTB,color:WHITE,bold:true,h:0.48},{cells:['Mô hình gốc','47,60','53,60','63,40'],h:0.54,rule:true},{cells:['S1','59,11','65,49','74,37'],h:0.54,rule:true},{cells:['GRPO + SPICE','60,65','67,02','76,25'],h:0.54,rule:true},{cells:[{t:'Phương pháp đề xuất',bold:true,color:FOOTB},{t:'60,68',bold:true,color:FOOTB},{t:'67,11',bold:true,color:FOOTB},{t:'76,32',bold:true,color:FOOTB}],h:0.58,rule:true},{cells:['Câu chuẩn','75,70','—','—'],h:0.54}],{align:['left','center','center','center'],fs:13.5});
rect(M,4.72,8.9,1.05,LIGHT,{radius:0.05,line:FOOTD});
addText('Phương pháp đề xuất − S1 = +1,57 điểm Executability\nKTC 95% [+0,86; +2,31], p < 0,001',{x:M+0.2,y:4.83,w:8.5,h:0.82,fontSize:17,bold:true,color:FOOTB,align:'center',valign:'mid'});
source('4.463 bước chạm · Luận văn §6.2, §6.6'); foot();

newSlide('22. Kết quả chất lượng câu');
table(M,1.05,[2.10,1.20,1.40,1.40,1.40,1.40],[{cells:['Mô hình','BLEU-4','ROUGE-L','CIDEr-D','SPICE','BERTScore'],fill:FOOTB,color:WHITE,bold:true,h:0.48,fs:12.7},{cells:['S1','51,56','67,35','416,12','44,37','66,33'],h:0.52,rule:true},{cells:['GRPO + SPICE','52,36','68,36','430,05','45,79','67,07'],h:0.52,rule:true},{cells:[{t:'Đề xuất',bold:true,color:FOOTB},{t:'53,47',bold:true,color:FOOTB},{t:'69,08',bold:true,color:FOOTB},{t:'442,02',bold:true,color:FOOTB},{t:'47,13',bold:true,color:FOOTB},{t:'67,73',bold:true,color:FOOTB}],h:0.56}],{align:['left','center','center','center','center','center'],fs:13});
addText('Mức tăng của ACE so với GRPO + SPICE',{x:M,y:3.20,w:4.25,h:0.55,fontSize:SECTION_FS,bold:true,color:FOOTB,fit:'shrink'});
metricBadge(0.72,3.82,1.45,'+1,11','BLEU-4',FOOTC);
metricBadge(2.43,3.82,1.45,'+0,74','ROUGE-L',FOOTC);
metricBadge(4.14,3.82,1.45,'+11,98','CIDEr-D',FOOTC);
metricBadge(5.85,3.82,1.45,'+1,34','SPICE',FOOTC);
metricBadge(7.56,3.82,1.45,'+0,66','BERTScore',FOOTC);
addText('METEOR và chrF cũng tăng → ACE cải thiện 7/7 metric chất lượng câu.',{x:M,y:5.62,w:8.9,h:0.45,fontSize:15.5,bold:true,color:FOOTB,align:'center'});
source('Luận văn §6.4, §6.6'); foot();

newSlide('23. Đóng góp của từng thành phần');
rect(M,1.15,4.20,4.75,LIGHT,{radius:0.05,line:FOOTD});
addText('GRPO + SPICE',{x:M+0.22,y:1.45,w:3.7,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB,align:'center'});
metricBadge(M+0.35,2.15,1.55,'+1,55','điểm Exec.',FOOTC);
addText('159 bước sai được sửa đúng',{x:M+0.30,y:3.15,w:3.7,h:0.38,fontSize:15,bold:true,align:'center'});
addText('90 bước đúng bị làm sai',{x:M+0.30,y:3.72,w:3.7,h:0.38,fontSize:15,align:'center'});
addText('Nguồn chính của cải thiện khả năng thao tác',{x:M+0.30,y:4.45,w:3.7,h:0.6,fontSize:14.5,bold:true,color:FOOTB,align:'center',fit:'shrink'});
rect(5.25,1.15,4.20,4.75,LIGHT,{radius:0.05,line:FOOTD});
addText('ACE',{x:5.47,y:1.45,w:3.7,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB,align:'center'});
metricBadge(5.60,2.15,1.55,'+0,02','điểm Exec.',FOOTC);
addText('Cải thiện 7/7 metric chất lượng câu',{x:5.52,y:3.15,w:3.65,h:0.45,fontSize:15,bold:true,align:'center'});
addText('Dùng bộ sinh ở mọi bước: −1,25 điểm Exec.',{x:5.52,y:3.78,w:3.65,h:0.64,fontSize:14.5,align:'center',fit:'shrink'});
addText('→ Điều kiện chọn lọc của ACE là cần thiết',{x:5.52,y:4.55,w:3.65,h:0.55,fontSize:14.5,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn §6.3–§6.4'); foot();

newSlide('24. Các hướng đã thử và bài học');
table(M,1.0,[3.0,1.25,4.55],[{cells:['Hướng','Exec.','Bài học'],fill:FOOTB,color:WHITE,bold:true,h:0.46,fs:12.5},{cells:['Mô tả phần tử trước câu','57,2','Bước trung gian đúng thì giúp; sai thì làm câu giảm mạnh.'],h:0.62,rule:true},{cells:['Phần thưởng tọa độ','60,1','Vị trí tốt hơn nhưng câu gần như không đổi.'],h:0.62,rule:true},{cells:['Chọn ứng viên','56,1','Khi chọn thì tốt nhưng từ chối quá nhiều.'],h:0.62,rule:true},{cells:['TAGE crop editor','60,2','Bộ sửa câu không vượt câu hướng dẫn ban đầu.'],h:0.62}],{align:['left','center','left'],fs:12.5});
rect(M,4.85,8.9,1.0,LIGHT,{radius:0.05,line:FOOTD});
addText('Bài học chung: cải thiện biểu diễn trung gian chưa chắc truyền được sang câu cuối → phương pháp cuối tối ưu trực tiếp câu hướng dẫn.',{x:M+0.2,y:4.85,w:8.5,h:1.0,fontSize:15,bold:true,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
source('Luận văn §6.10, Phụ lục A'); foot();

newSlide('25. Hạn chế và hướng phát triển');
addText('Hạn chế',{x:M,y:0.95,w:1.2,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Chưa có SFT control cùng số bước để tách riêng tác dụng của phần thưởng SPICE.','Executability vẫn phụ thuộc mô hình định vị, dù đã được đối chiếu với các mô hình khác.','Thực nghiệm chính trên AndroidControl, giao diện tiếng Anh và một backbone 3B.','Lịch sử bước trước dùng gold history.'],M,1.38,8.9,{gap:0.75,fs:15.2,h:0.62});
addText('Hướng phát triển',{x:M,y:4.62,w:2.2,h:0.55,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Thêm same-step SFT control và human evaluation.','Đánh giá trên test chính thức / dataset thứ hai / giao diện tiếng Việt.'],M,5.20,8.9,{gap:0.68,fs:15.2,h:0.56});
source('Luận văn §7.2–§7.3'); foot();

newSlide('26. Kết luận');
bullets(['Đề xuất pipeline S1 → GRPO + SPICE → ACE để sinh hướng dẫn GUI rõ và ổn định hơn.','Executability bổ sung góc nhìn thực tế: câu có dẫn tới đúng phần tử cần thao tác hay không.','Phương pháp hoàn chỉnh đạt 60,7% Executability, hơn S1 1,57 điểm với khác biệt có ý nghĩa thống kê.','GRPO tạo phần lớn mức tăng khả năng thao tác; ACE cải thiện chất lượng câu mà gần như không làm giảm Executability.'],M,1.28,8.9,{gap:1.02,fs:16,h:0.84});
source('Luận văn Chương 7'); foot();

newSlide('Trân trọng cảm ơn');
addText('TRÂN TRỌNG CẢM ƠN',{x:0.8,y:2.05,w:8.4,h:0.65,fontSize:26,bold:true,color:FOOTB,align:'center',valign:'mid'});
addText('HỎI ĐÁP VÀ THẢO LUẬN',{x:0.8,y:3.0,w:8.4,h:0.55,fontSize:20,bold:true,color:FOOTC,align:'center',valign:'mid'});
addText('Lê Đoàn Phương Uyên',{x:0.8,y:4.45,w:8.4,h:0.4,fontSize:16,color:GREY,align:'center'});
foot();

newSlide('Dự phòng · Định nghĩa Executability');
addText('Một bước đúng khi đồng thời:',{x:M,y:0.98,w:3.6,h:0.55,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Đúng loại thao tác.','Không đảo nghĩa.','|px−gx| ≤ 0,14W; |py−gy| ≤ 0,14H.','Điểm p nằm trong ô Voronoi của phần tử cần chạm.'],M,1.5,8.9,{gap:0.82,fs:15.5,h:0.67});
addText('Executability = số bước đúng / tổng số touch steps.',{x:M,y:5.25,w:8.9,h:0.5,fontSize:17,bold:true,color:FOOTB,align:'center'}); footB();

newSlide('Dự phòng · Toàn bộ metric');
table(M,0.88,[2.35,1.2,1.2,1.35,1.35,1.25],[{cells:['Metric','Base','S1','GRPO','Đề xuất','Δ ACE'],fill:FOOTB,color:WHITE,bold:true,h:0.42,fs:12},{cells:['Executability','47,60','59,11','60,65','60,68','+0,02'],h:0.42,rule:true},{cells:['Box','53,60','65,49','67,02','67,11','+0,09'],h:0.42,rule:true},{cells:['Euclid','63,40','74,37','76,25','76,32','+0,07'],h:0.42,rule:true},{cells:['BLEU-4','15,30','51,56','52,36','53,47','+1,11'],h:0.42,rule:true},{cells:['METEOR','24,60','36,79','37,92','38,37','+0,46'],h:0.42,rule:true},{cells:['ROUGE-L','42,30','67,35','68,36','69,08','+0,74'],h:0.42,rule:true},{cells:['CIDEr-D','88,00','416,12','430,05','442,02','+11,98'],h:0.42,rule:true},{cells:['SPICE','18,50','44,37','45,79','47,13','+1,34'],h:0.42,rule:true},{cells:['chrF','40,20','61,26','62,87','63,44','+0,58'],h:0.42,rule:true},{cells:['BERTScore','40,10','66,33','67,07','67,73','+0,66'],h:0.42}],{align:['left','center','center','center','center','center'],fs:11.7}); footB();

newSlide('Dự phòng · Cross-listener validation');
table(M,1.2,[3.5,2.5,2.5],[{cells:['Phép so','UGround','UI-Venus'],fill:FOOTB,color:WHITE,bold:true,h:0.46},{cells:['S1 − Base',{t:'+10,35',bold:true},{t:'+9,68',bold:true}],h:0.58,rule:true},{cells:['S2 − S1','−1,93','−1,21'],h:0.58,rule:true},{cells:['Câu chuẩn','70,0','69,3'],h:0.58}],{align:['left','center','center'],fs:13});
addText('Phi-4 ngoài họ Qwen vẫn giữ thứ tự: Câu chuẩn > S1 > Base > Câu chung chung.',{x:M,y:4.35,w:8.9,h:0.65,fontSize:15.5,bold:true,color:FOOTB,align:'center'}); footB();

newSlide('Dự phòng · Cấu hình huấn luyện');
table(M,1.0,[3.0,5.8],[{cells:['Hạng mục','Giá trị'],fill:FOOTB,color:WHITE,bold:true,h:0.44},{cells:['Backbone','Qwen2.5-VL-3B-Instruct'],h:0.48,rule:true},{cells:['Fine-tuning','QLoRA NF4 4-bit, rank 8, alpha 16, dropout 0,05'],h:0.48,rule:true},{cells:['SFT','2 epochs = 8.072 steps, batch hiệu dụng 16, LR 1e−4'],h:0.48,rule:true},{cells:['GRPO','8 samples/prompt, 500 updates, LR 1e−5, KL β 0,04'],h:0.48,rule:true},{cells:['Hardware','1 × A100, vision tower frozen'],h:0.48}],{align:['left','left'],fs:12.7}); footB();

pptx.writeFile({ fileName:'../LUAN_VAN_SLIDE_BAO_VE_CONCISE.pptx' });
