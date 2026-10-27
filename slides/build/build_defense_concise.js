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
let slide, PAGE=0, BPAGE=0; const TOTAL=25;
const SPICE_EXAMPLE = path.join(__dirname, '..', '..', 'thesis', 'figures', 'fig_vidu_spice.png');

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
newSlide('2. Câu hướng dẫn cần đủ thông tin để phân biệt đúng phần tử');
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
newSlide('3. Độ tương đồng chưa phản ánh đầy đủ khả năng thực hiện');
addText('Các thước đo dựa trên câu chuẩn và executability phản ánh hai khía cạnh bổ sung cho nhau.',{x:M,y:1.0,w:8.9,h:0.55,fontSize:17,bold:true,color:FOOTB,align:'center'});
box(0.70,2.05,2.55,1.2,'BLEU / ROUGE\nĐo mức giống câu chuẩn',{bold:true,fill:LIGHT,line:FOOTD,fs:15});
box(3.72,2.05,2.55,1.2,'SPICE / CIDEr\nĐo tương đồng nội dung',{bold:true,fill:LIGHT,line:FOOTD,fs:15});
box(6.75,1.85,2.55,1.6,'Executability\nXác định đúng phần tử\nvà đúng loại thao tác',{bold:true,fill:LIGHT,line:FOOTC,fs:15});
addText('Do đó, luận văn đánh giá cả mức tương đồng với câu chuẩn và khả năng xác định đúng phần tử, đúng loại thao tác.',{x:M,y:4.55,w:8.9,h:0.70,fontSize:16,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn Chương 5'); foot();

// 5 · Đóng góp
newSlide('4. Đóng góp của luận văn');
rect(M,1.05,2.75,3.25,LIGHT,{radius:0.05,line:FOOTB});
addText('1 · Phương pháp',{x:M+0.15,y:1.34,w:2.45,h:0.42,fontSize:17,bold:true,color:FOOTB,align:'center'});
addText('GRPO-SPICE tối ưu trực tiếp câu hướng dẫn; ACE nâng các thước chữ trong khi giữ executability.',{x:M+0.24,y:2.02,w:2.27,h:1.60,fontSize:14.0,align:'center',valign:'mid',fit:'shrink'});
rect(3.63,1.05,2.75,3.25,LIGHT,{radius:0.05,line:FOOTC});
addText('2 · Executability',{x:3.78,y:1.34,w:2.45,h:0.42,fontSize:17,bold:true,color:FOOTB,align:'center'});
addText('Một mô hình định vị tách biệt kiểm tra câu có dẫn tới đúng phần tử và đúng loại thao tác hay không.',{x:3.90,y:2.02,w:2.22,h:1.60,fontSize:14.0,align:'center',valign:'mid',fit:'shrink'});
rect(6.70,1.05,2.75,3.25,LIGHT,{radius:0.05,line:FOOTD});
addText('3 · Phân tích thực nghiệm',{x:6.84,y:1.28,w:2.48,h:0.55,fontSize:16.3,bold:true,color:FOOTB,align:'center',fit:'shrink'});
addText('Nhánh thưởng xáo, hai lượt GRPO, bốn công cụ đánh giá, ACU, lịch sử tự sinh và AitZ làm rõ phạm vi của mức tăng.',{x:6.95,y:2.02,w:2.25,h:1.60,fontSize:14.0,align:'center',valign:'mid',fit:'shrink'});
metricBadge(0.80,4.78,2.55,'+1,55','điểm trên tập kiểm chính',FOOTB);
metricBadge(3.72,4.78,2.55,'+4,58','điểm trên tác vụ chưa có trong tập dạy S1',FOOTC);
metricBadge(6.65,4.78,2.55,'7/7','thước chữ tăng sau ACE',FOOTD);
source('Luận văn §1.6, Chương 6'); foot();

// 6 · Dữ liệu
newSlide('5. Dữ liệu và cách chia tập');
addText('Tập huấn luyện và tập kiểm tra chính được tách theo tác vụ; không có tác vụ xuất hiện ở cả hai phía.',{x:M,y:0.96,w:8.9,h:0.55,fontSize:16.5,bold:true,color:FOOTB,align:'center',fit:'shrink'});
table(M,1.72,[2.75,1.85,1.85,2.45],[
  {cells:['','Huấn luyện','Kiểm tra chính','Ghi chú'],fill:FOOTB,color:WHITE,bold:true,h:0.46},
  {cells:['Số bước','64.567','6.958','chia theo tác vụ'],h:0.54,rule:true},
  {cells:['Bước có thao tác chạm','41.191','4.463','tập chính của executability'],h:0.54,rule:true},
  {cells:['Số tác vụ','12.895','1.432','không trùng tác vụ'],h:0.54}
],{align:['left','center','center','left'],fs:13.4});
rect(M,4.20,8.9,1.38,LIGHT,{radius:0.05,line:FOOTD});
addText('Đánh giá tổng quát hóa bổ sung',{x:M+0.22,y:4.34,w:2.8,h:0.55,fontSize:14.2,bold:true,color:FOOTB,valign:'mid',fit:'shrink'});
addText('ACU gồm 1.484 bước thuộc các tác vụ không xuất hiện trong tập huấn luyện của S1; đây là tập bổ sung theo tác vụ, không thay thế tập kiểm chính. AitZ dùng để kiểm tra khi đổi phân phối câu chuẩn.',{x:M+2.72,y:4.28,w:5.88,h:0.86,fontSize:13.5,align:'left',valign:'mid',fit:'shrink'});
source('Luận văn Chương 3, §6.8'); foot();

// 7 · Baseline và scale
newSlide('6. Trong thiết lập đã thử, 3B sau tinh chỉnh vượt 7B chỉ prompting');
metricBadge(0.62,1.45,2.00,'47,59%','3B · chưa tinh chỉnh',FOOTD);
metricBadge(2.88,1.45,2.00,'51,51%','7B · prompting',FOOTD);
metricBadge(5.14,1.45,2.00,'59,11%','3B · S1',FOOTB);
metricBadge(7.40,1.45,2.00,'60,65%','3B · GRPO-SPICE',FOOTC);
line(M,3.05,8.9,0,RULE,1);
rect(0.85,3.50,3.85,1.42,LIGHT,{radius:0.05,line:FOOTD});
addText('7B hơn 3B gốc',{x:1.05,y:3.75,w:3.45,h:0.35,fontSize:14.5,bold:true,color:FOOTB,align:'center'});
addText('+3,92 điểm',{x:1.05,y:4.18,w:3.45,h:0.45,fontSize:21,bold:true,color:FOOTD,align:'center'});
rect(5.30,3.50,3.85,1.42,LIGHT,{radius:0.05,line:FOOTC});
addText('3B sau GRPO-SPICE hơn 7B prompting',{x:5.50,y:3.70,w:3.45,h:0.52,fontSize:13.6,bold:true,color:FOOTB,align:'center',fit:'shrink'});
addText('+9,14 điểm',{x:5.50,y:4.18,w:3.45,h:0.45,fontSize:21,bold:true,color:FOOTC,align:'center'});
addText('So sánh này chỉ áp dụng cho thiết lập prompting đã thử; 7B dùng cùng prompt của Base và không được tối ưu prompt riêng.',{x:M,y:5.55,w:8.9,h:0.55,fontSize:13.8,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn §6.2'); foot();

// 8 · Executability
newSlide('7. Executability đánh giá khả năng câu dẫn tới đúng phần tử và thao tác');
box(0.65,1.72,1.90,0.92,'Câu hướng dẫn',{bold:true,fill:WHITE,line:FOOTD});
line(2.67,2.18,0.40,0,FOOTC,2,true);
box(3.18,1.58,2.25,1.20,'Mô hình định vị\ntách biệt',{bold:true,fill:LIGHT,line:FOOTB,fs:15});
line(5.55,2.18,0.40,0,FOOTC,2,true);
box(6.06,1.72,1.30,0.92,'Điểm (x,y)',{bold:true,fill:WHITE,line:FOOTD,fs:14});
line(7.48,2.18,0.40,0,FOOTC,2,true);
box(7.98,1.50,1.38,1.36,'Kiểm tra\nphần tử + thao tác',{bold:true,fill:LIGHT,line:FOOTC,fs:13.2});
addText('Một bước được tính đúng khi đồng thời:',{x:M,y:3.48,w:3.55,h:0.55,fontSize:15.5,bold:true,color:FOOTB,valign:'mid',fit:'shrink'});
bullets(['đúng loại thao tác','không diễn đạt ngược thao tác cần làm','điểm định vị thuộc vùng của phần tử cần chạm'],M,4.02,8.9,{gap:0.62,fs:15.0,h:0.52});
addText('Mô hình định vị không tham gia huấn luyện phương pháp và không biết tọa độ đáp án.',{x:M,y:5.98,w:8.9,h:0.45,fontSize:14.0,bold:true,color:FOOTB,align:'center'});
source('Luận văn Chương 5'); foot();

// 9 · Độ tin cậy metric
newSlide('8. Executability phản ứng rõ với mức thông tin trong câu hướng dẫn');
metricBadge(0.70,1.20,2.35,'75,7%','câu chuẩn',FOOTB);
metricBadge(3.82,1.20,2.35,'12,0%','“Tap the button.”',FOOTC);
metricBadge(6.94,1.20,2.35,'6,1%','câu của màn hình khác',FOOTD);
addText('Ba mốc được tính trên cùng mẫu 800 bước.',{x:M,y:2.62,w:8.9,h:0.30,fontSize:12.5,color:GREY,align:'center'});
line(M,3.02,8.9,0,RULE,1);
rect(M,3.42,8.9,1.55,LIGHT,{radius:0.05,line:FOOTD});
addText('Đổi công cụ đánh giá',{x:M+0.22,y:3.66,w:2.25,h:0.34,fontSize:15.0,bold:true,color:FOOTB});
addText('Chiều cải thiện của GRPO-SPICE so với S1 được giữ dưới UGround, UI-Venus, Phi-Ground và Phi-4. Hai công cụ sau nằm ngoài họ Qwen.',{x:M+2.25,y:3.48,w:6.35,h:0.92,fontSize:14.0,valign:'mid',fit:'shrink'});
addText('Kết luận chính không phụ thuộc vào một công cụ đánh giá duy nhất.',{x:M,y:5.55,w:8.9,h:0.50,fontSize:15.0,bold:true,color:FOOTB,align:'center'});
source('Luận văn §5.5–§5.10, §6.7.3'); foot();

// 10 · Tổng quan phương pháp
newSlide('9. Phương pháp đề xuất gồm GRPO-SPICE và ACE');
box(0.55,1.35,0.95,0.9,'S1',{bold:true,line:FOOTD});
line(1.62,1.80,0.35,0,FOOTC,2,true);
box(2.08,1.25,2.15,1.10,'GRPO-SPICE\nsinh câu ban đầu',{bold:true,fill:LIGHT,line:FOOTB,fs:15});
line(4.35,1.80,0.35,0,FOOTC,2,true);
box(4.82,1.25,2.15,1.10,'ACE\nhiệu chỉnh có chọn lọc',{bold:true,fill:LIGHT,line:FOOTC,fs:15});
line(7.10,1.80,0.35,0,FOOTC,2,true);
box(7.57,1.25,1.88,1.10,'Câu hướng dẫn\ncuối',{bold:true,fill:WHITE,line:FOOTD,fs:14});
addText('GRPO-SPICE',{x:M,y:3.42,w:2.15,h:0.40,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Sinh 8 câu cho cùng đầu vào.','SPICE + phạt độ dài làm tín hiệu cập nhật.'],M,3.92,4.15,{gap:0.72,fs:14.6,h:0.60});
addText('ACE',{x:5.05,y:3.42,w:1.2,h:0.40,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Truy hồi 4 câu ví dụ từ tập dạy.','Chỉ thay câu ban đầu khi thỏa điều kiện chọn lọc.'],5.05,3.92,4.35,{gap:0.72,fs:14.6,h:0.60});
addText('UGround không nằm trong hàm thưởng và không tham gia vào quá trình sinh câu.',{x:M,y:5.82,w:8.9,h:0.48,fontSize:14.2,bold:true,color:FOOTB,align:'center'});
source('Luận văn Chương 4'); foot();

// 11 · GRPO
newSlide('10. GRPO-SPICE tối ưu trực tiếp chất lượng nội dung của câu hướng dẫn');
box(0.60,1.85,1.55,0.92,'1 đầu vào',{bold:true,fill:LIGHT,line:FOOTD});
line(2.28,2.31,0.42,0,FOOTC,2,true);
box(2.82,1.66,1.75,1.30,'8 câu\nhướng dẫn',{bold:true,fill:LIGHT,line:FOOTB});
line(4.70,2.31,0.42,0,FOOTC,2,true);
box(5.24,1.66,1.80,1.30,'SPICE\n− phạt độ dài',{bold:true,fill:LIGHT,line:FOOTC,fs:15});
line(7.17,2.31,0.42,0,FOOTC,2,true);
box(7.71,1.60,1.70,1.42,'Cập nhật\nGRPO',{bold:true,fill:LIGHT,line:FOOTD,fs:15});
rect(M,3.65,8.9,1.72,LIGHT,{radius:0.05,line:FOOTD});
addText('Vai trò của SPICE',{x:M+0.22,y:3.90,w:2.15,h:0.35,fontSize:15.5,bold:true,color:FOOTB});
addText('SPICE so sánh các thành phần nội dung của câu thay vì chỉ dựa vào mức giống nhau của chuỗi từ. Mục tiêu là ưu tiên câu mô tả đúng đối tượng và quan hệ cần thiết để người dùng nhận ra phần tử.',{x:M+2.12,y:3.75,w:6.50,h:0.88,fontSize:14.0,valign:'mid',fit:'shrink'});
addText('500 bước cập nhật từ S1 · cùng một cấu hình được dùng cho nhánh xáo thưởng.',{x:M,y:5.82,w:8.9,h:0.43,fontSize:13.6,bold:true,color:FOOTB,align:'center'});
source('Luận văn §4.5'); foot();

// 12 · shuffled control
newSlide('11. Mức tăng không xuất hiện khi phần thưởng SPICE bị xáo');
addText('Nhánh kiểm tra chạy cùng 500 bước GRPO nhưng phần thưởng SPICE bị xáo giữa các mẫu.',{x:M,y:0.95,w:8.9,h:0.55,fontSize:16.3,bold:true,color:FOOTB,align:'center',fit:'shrink'});
metricBadge(0.78,1.82,2.45,'59,11%','S1',FOOTD);
metricBadge(3.78,1.82,2.45,'59,11%','GRPO · thưởng xáo',FOOTD);
metricBadge(6.78,1.82,2.45,'60,65%','GRPO-SPICE',FOOTC);
line(M,3.35,8.9,0,RULE,1);
rect(M,3.72,8.9,1.28,LIGHT,{radius:0.05,line:FOOTC});
addText('GRPO-SPICE cao hơn nhánh thưởng xáo +1,55 điểm',{x:M+0.20,y:3.90,w:8.5,h:0.42,fontSize:19,bold:true,color:FOOTB,align:'center'});
addText('KTC 95% [+0,81; +2,30] · p = 2×10⁻⁵',{x:M+0.20,y:4.38,w:8.5,h:0.36,fontSize:14.5,bold:true,color:FOOTC,align:'center'});
addText('Cả 6 thước chữ có KTC cũng tăng khi so GRPO-SPICE với nhánh thưởng xáo.',{x:M,y:5.52,w:8.9,h:0.50,fontSize:14.3,bold:true,color:FOOTB,align:'center'});
source('Luận văn §6.2–§6.5'); foot();

// 13 · main benchmark
newSlide('12. GRPO-SPICE cải thiện nhất quán trên tập kiểm chính');
addText('So với S1, GRPO-SPICE cao hơn ở toàn bộ 13 độ đo được báo cáo.',{x:M,y:0.95,w:8.9,h:0.52,fontSize:16.8,bold:true,color:FOOTB,align:'center'});
metricBadge(0.62,1.72,2.25,'+1,55','Executability',FOOTC);
metricBadge(2.96,1.72,2.25,'+1,52','Hộp phần tử',FOOTC);
metricBadge(5.30,1.72,2.25,'+1,88','AitW đầy đủ',FOOTC);
metricBadge(7.64,1.72,1.78,'7/7','thước chữ tăng',FOOTD);
rect(M,3.38,8.9,1.48,LIGHT,{radius:0.05,line:FOOTD});
addText('12/12 độ đo có khoảng tin cậy đều nằm trên 0',{x:M+0.22,y:3.66,w:8.45,h:0.42,fontSize:19,bold:true,color:FOOTB,align:'center'});
addText('METEOR tăng +1,13 điểm nhưng chưa có KTC trong thiết lập đánh giá hiện tại.',{x:M+0.30,y:4.18,w:8.30,h:0.38,fontSize:13.2,color:GREY,align:'center',fit:'shrink'});
addText('Hai lượt S1: 59,11 / 59,62 · Hai lượt GRPO-SPICE: 60,65 / 59,94 · Lượt GRPO thứ hai vẫn cao hơn S1 lượt đầu +0,83 điểm.',{x:M,y:5.38,w:8.9,h:0.72,fontSize:12.8,bold:true,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
source('Luận văn §6.2, §6.5–§6.7'); foot();

// 14 · ACU
newSlide('13. Mức tăng lớn hơn trên các tác vụ chưa có trong tập dạy S1');
addText('ACU gồm 1.484 bước thuộc các tác vụ không xuất hiện trong tập huấn luyện của S1.',{x:M,y:0.95,w:8.9,h:0.50,fontSize:16.0,bold:true,color:FOOTB,align:'center'});
metricBadge(0.80,1.72,2.50,'+4,58','GRPO-SPICE − S1',FOOTC);
metricBadge(3.75,1.72,2.50,'+4,04','lượt GRPO thứ hai − S1',FOOTC);
metricBadge(6.70,1.72,2.50,'+4,85','ACE − S1',FOOTD);
addText('Cả ba mức tăng đều có khoảng tin cậy nằm trên 0 và lớn hơn mức tăng quan sát được trên tập kiểm chính.',{x:M,y:3.18,w:8.9,h:0.62,fontSize:14.2,bold:true,color:FOOTB,align:'center',fit:'shrink'});
rect(M,4.08,8.9,1.32,LIGHT,{radius:0.05,line:FOOTD});
addText('Gộp tập kiểm chính + ACU = 5.947 bước',{x:M+0.22,y:4.24,w:3.40,h:0.52,fontSize:13.7,bold:true,color:FOOTB,valign:'mid',fit:'shrink'});
addText('GRPO-SPICE − S1 = +2,30  [ +1,62; +2,99 ]',{x:M+3.50,y:4.26,w:5.10,h:0.48,fontSize:17.2,bold:true,color:FOOTC,align:'center'});
addText('Trên ACU, 6/6 thước chữ có KTC cũng tăng; CIDEr-D +26,73 và SPICE +2,51.',{x:M,y:5.72,w:8.9,h:0.50,fontSize:13.8,bold:true,color:FOOTB,align:'center'});
addText('ACU là tập bổ sung theo tác vụ để kiểm tra tổng quát hóa, không thay thế tập kiểm chính.',{x:M,y:6.24,w:8.9,h:0.30,fontSize:10.8,color:GREY,align:'center',fit:'shrink'});
source('Luận văn §6.8'); foot();

// 15 · ACE process
newSlide('14. ACE chỉ hiệu chỉnh khi câu ví dụ đủ phù hợp');
box(0.45,1.25,1.65,0.95,'Câu ban đầu',{bold:true,fill:WHITE,line:FOOTD,fs:14.5});
line(2.20,1.73,0.38,0,FOOTC,2,true);
box(2.68,1.15,1.90,1.15,'Truy hồi 4 câu\nví dụ từ train',{bold:true,fill:LIGHT,line:FOOTB,fs:14});
line(4.68,1.73,0.38,0,FOOTC,2,true);
box(5.16,1.15,1.55,1.15,'Sinh câu\nứng viên',{bold:true,fill:LIGHT,line:FOOTC,fs:14});
line(6.81,1.73,0.38,0,FOOTC,2,true);
box(7.29,1.05,2.20,1.35,'Kiểm tra\n2 điều kiện chọn lọc',{bold:true,fill:LIGHT,line:FOOTD,fs:14});
rect(M,3.42,4.20,1.18,LIGHT,{radius:0.05,line:FOOTC});
addText('1 · Câu ứng viên phải giống hoàn toàn một trong bốn câu ví dụ được truy hồi.',{x:M+0.18,y:3.42,w:3.84,h:1.18,fontSize:14.0,bold:true,align:'center',valign:'mid',fit:'shrink'});
rect(5.25,3.42,4.20,1.18,LIGHT,{radius:0.05,line:FOOTC});
addText('2 · Động từ đầu câu phải cùng lớp thao tác với câu ban đầu.',{x:5.43,y:3.42,w:3.84,h:1.18,fontSize:14.0,bold:true,align:'center',valign:'mid',fit:'shrink'});
box(1.80,5.10,2.80,0.82,'Đủ điều kiện → dùng câu mới',{bold:true,fill:LIGHT,line:FOOTC,fs:14});
box(5.40,5.10,2.80,0.82,'Không đủ → giữ câu ban đầu',{bold:true,fill:WHITE,line:FOOTD,fs:14});
source('Luận văn §4.6'); foot();

// 16 · ACE result
newSlide('15. ACE nâng chất lượng câu trong khi giữ executability');
metricBadge(0.82,0.94,1.95,'60,68%','Executability',FOOTB);
metricBadge(3.00,0.94,1.95,'+0,02','so với GRPO-SPICE',FOOTD);
metricBadge(5.18,0.94,1.95,'7/7','thước chữ tăng',FOOTC);
metricBadge(7.36,0.94,1.95,'6/6','KTC chữ > 0',FOOTC);
table(0.72,2.30,[1.65,1.52,1.38,1.22,3.02],[
  {cells:['Thước','GRPO-SPICE','ACE','Δ ACE','KTC 95%'],fill:FOOTB,color:WHITE,bold:true,h:0.40,fs:11.6},
  {cells:['BLEU-4','52,36','53,47','+1,11','[+0,78; +1,42]'],h:0.42,rule:true},
  {cells:['METEOR','37,92','38,37','+0,45','—'],h:0.42,rule:true},
  {cells:['ROUGE-L','68,36','69,11','+0,74','[+0,54; +0,94]'],h:0.42,rule:true},
  {cells:['CIDEr-D','430,05','442,02','+11,97','[+8,24; +15,34]'],h:0.42,rule:true},
  {cells:['SPICE','45,79','47,13','+1,33','[+0,92; +1,75]'],h:0.42,rule:true},
  {cells:['chrF','62,87','63,44','+0,58','[+0,37; +0,80]'],h:0.42,rule:true},
  {cells:['BERTScore','67,07','67,73','+0,66','[+0,46; +0,86]'],h:0.42}
],{align:['left','center','center','center','center'],fs:11.4});
addText('METEOR cũng tăng nhưng chưa có KTC. Sáu thước còn lại đều có khoảng tăng nằm trên 0.',{x:M,y:5.95,w:8.9,h:0.44,fontSize:13.0,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn §6.4–§6.5'); foot();

// 17 · multi-tool
newSlide('16. Hướng tăng được giữ dưới bốn công cụ đánh giá');
addText('Chênh lệch GRPO-SPICE − S1',{x:M,y:0.98,w:8.9,h:0.40,fontSize:16.5,bold:true,color:FOOTB,align:'center'});
metricBadge(0.65,1.72,2.00,'+1,55','UGround',FOOTB);
metricBadge(2.92,1.72,2.00,'+1,55','UI-Venus',FOOTB);
metricBadge(5.19,1.72,2.00,'+0,78','Phi-Ground',FOOTC);
metricBadge(7.46,1.72,2.00,'+0,69','Phi-4',FOOTD);
rect(M,3.36,8.9,1.46,LIGHT,{radius:0.05,line:FOOTD});
addText('KTC của cả bốn chênh lệch đều nằm trên 0.',{x:M+0.20,y:3.62,w:8.50,h:0.38,fontSize:18,bold:true,color:FOOTB,align:'center'});
addText('Phi-Ground và Phi-4 nằm ngoài họ Qwen; mức tăng nhỏ hơn nhưng vẫn giữ cùng chiều.',{x:M+0.28,y:4.12,w:8.34,h:0.38,fontSize:13.5,color:GREY,align:'center'});
addText('Quan hệ S1 < GRPO-SPICE ≈ ACE được giữ ở cả bốn công cụ đánh giá.',{x:M,y:5.55,w:8.9,h:0.52,fontSize:14.4,bold:true,color:FOOTB,align:'center'});
source('Luận văn §6.7.3'); foot();

// 18 · history + AitZ
newSlide('17. Ưu thế executability được giữ khi lịch sử do chính mô hình sinh');
addText('Khi câu ở các bước trước được thay bằng đầu ra do chính mô hình sinh, cả hai nhánh đều giảm điểm nhưng khoảng cách vẫn được giữ.',{x:M,y:0.96,w:8.9,h:0.62,fontSize:15.8,bold:true,color:FOOTB,align:'center',fit:'shrink'});
metricBadge(0.72,1.82,2.45,'54,96%','S1 · lịch sử tự sinh',FOOTD);
metricBadge(3.78,1.82,2.45,'56,44%','GRPO-SPICE · lịch sử tự sinh',FOOTC);
metricBadge(6.83,1.82,2.45,'+1,48','GRPO-SPICE − S1',FOOTB);
rect(M,3.45,8.9,1.38,LIGHT,{radius:0.05,line:FOOTC});
addText('KTC 95% của chênh lệch: [+0,54; +2,43]',{x:M+0.22,y:3.70,w:8.45,h:0.40,fontSize:18,bold:true,color:FOOTB,align:'center'});
addText('Trên 3.492 bước thuộc các tác vụ có đủ ảnh ở mọi bước, chênh lệch là +1,66 [+0,60; +2,75].',{x:M+0.30,y:4.22,w:8.30,h:0.36,fontSize:13.3,color:GREY,align:'center',fit:'shrink'});
addText('Ưu thế về executability trên bước chạm không phụ thuộc vào việc lịch sử luôn dùng câu chuẩn.',{x:M,y:5.55,w:8.9,h:0.52,fontSize:14.5,bold:true,color:FOOTB,align:'center'});
source('Luận văn §6.8 · lịch sử tự sinh'); foot();

newSlide('18. SFT vẫn chuyển miền sang AitZ');
addText('AitZ dùng một phân phối câu chuẩn khác AndroidControl, nên được dùng để xác định phạm vi khi đổi miền dữ liệu.',{x:M,y:0.96,w:8.9,h:0.56,fontSize:15.5,bold:true,color:FOOTB,align:'center',fit:'shrink'});
metricBadge(0.72,1.72,2.45,'34,50%','Base',FOOTD);
metricBadge(3.78,1.72,2.45,'37,79%','S1',FOOTB);
metricBadge(6.83,1.72,2.45,'37,28%','GRPO-SPICE',FOOTC);
rect(M,3.25,4.18,1.48,LIGHT,{radius:0.05,line:FOOTB});
addText('S1 − Base',{x:M+0.18,y:3.48,w:3.82,h:0.34,fontSize:14.5,bold:true,color:FOOTB,align:'center'});
addText('+3,29  [+1,51; +5,03]',{x:M+0.18,y:3.92,w:3.82,h:0.42,fontSize:19,bold:true,color:FOOTB,align:'center'});
rect(5.27,3.25,4.18,1.48,LIGHT,{radius:0.05,line:FOOTD});
addText('GRPO-SPICE − S1',{x:5.45,y:3.48,w:3.82,h:0.34,fontSize:14.5,bold:true,color:FOOTB,align:'center'});
addText('−0,51  [−1,39; +0,36]',{x:5.45,y:3.92,w:3.82,h:0.42,fontSize:19,bold:true,color:FOOTD,align:'center'});
addText('Về metric chữ, GRPO-SPICE và S1 gần tương đương; BLEU-4, SPICE và chrF là ba metric có KTC nằm trên 0.',{x:M,y:5.18,w:8.9,h:0.52,fontSize:13.7,align:'center',fit:'shrink'});
addText('Lợi ích bổ sung của SPICE phụ thuộc vào phân phối câu chuẩn.',{x:M,y:5.85,w:8.9,h:0.48,fontSize:15.0,bold:true,color:FOOTB,align:'center'});
source('Luận văn §6.8 · AitZ'); foot();

newSlide('19. GRPO-SPICE sửa được lỗi quy chiếu tới sai phần tử');
slide.addImage({path:SPICE_EXAMPLE,x:0.65,y:0.95,w:4.25,h:4.91});
addText('Bước cần thực hiện',{x:5.28,y:1.08,w:3.95,h:0.34,fontSize:15.5,bold:true,color:FOOTB,align:'center'});
box(5.45,1.52,3.62,0.72,'Chạm nút “Not now”',{bold:true,fill:LIGHT,line:FOOTB,fs:16});
addText('S1',{x:5.28,y:2.70,w:3.95,h:0.32,fontSize:15.5,bold:true,color:FOOTD,align:'center'});
box(5.45,3.08,3.62,0.92,'Gọi nhầm “Allow”\n→ định vị sai phần tử',{bold:true,fill:WHITE,line:FOOTD,fs:14.5});
addText('GRPO-SPICE',{x:5.28,y:4.42,w:3.95,h:0.32,fontSize:15.5,bold:true,color:FOOTC,align:'center'});
box(5.45,4.80,3.62,0.92,'Gọi đúng “Not now”\n→ định vị đúng phần tử',{bold:true,fill:LIGHT,line:FOOTC,fs:14.5});
addText('Ví dụ minh họa trực tiếp ý nghĩa của executability: câu chuyển từ quy chiếu sai nút sang đúng nút cần chạm.',{x:M,y:6.12,w:8.9,h:0.48,fontSize:13.8,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn Hình 6.1'); foot();

newSlide('20. Mức cải thiện được giữ qua nhiều điều kiện đánh giá');
const ev=[
 ['1','Cùng số bước huấn luyện','Nhánh thưởng xáo chạy cùng 500 bước nhưng quay về mức S1.'],
 ['2','Không chỉ một lượt huấn luyện','Hai lượt GRPO cùng cao hơn S1; trên ACU cả hai tăng khoảng 4 điểm.'],
 ['3','Bốn công cụ đánh giá','Chiều tăng giữ dưới 4 công cụ và nhiều luật đánh giá.'],
 ['4','Giữ trên tác vụ mới','ACU: +4,58 điểm trên các tác vụ không có trong tập dạy S1.']
];
ev.forEach((c,i)=>{const x=i%2===0?M:5.05,y=1.32+Math.floor(i/2)*2.15;rect(x,y,4.40,1.78,LIGHT,{radius:0.05,line:i<2?FOOTC:FOOTD});addText(c[0],{x:x+0.16,y:y+0.16,w:0.48,h:0.48,fontSize:22,bold:true,color:FOOTB,align:'center'});addText(c[1],{x:x+0.72,y:y+0.18,w:3.45,h:0.38,fontSize:14.4,bold:true,color:FOOTB});addText(c[2],{x:x+0.72,y:y+0.68,w:3.40,h:0.85,fontSize:13.2,fit:'shrink'});});
addText('Chuỗi kết quả này bổ sung bằng chứng rằng mức tăng trên AndroidControl gắn với tín hiệu SPICE và được giữ khi thay điều kiện đánh giá.',{x:M,y:5.82,w:8.9,h:0.50,fontSize:13.6,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn Chương 6'); foot();

// 21 · scope
newSlide('21. Phạm vi kết luận và hướng mở rộng');
addText('Phạm vi hiện tại',{x:M,y:0.95,w:2.0,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Kết luận chính về executability tập trung vào các bước có thao tác chạm.','Thực nghiệm chính dùng AndroidControl tiếng Anh và backbone Qwen2.5-VL-3B.','Đa số nhánh được chạy một lượt; S1 và GRPO-SPICE có hai lượt để kiểm tra độ ổn định về hướng.','AitZ cho thấy lợi ích bổ sung của SPICE phụ thuộc vào phân phối câu chuẩn.'],M,1.36,8.9,{gap:0.56,fs:12.9,h:0.50});
addText('Hướng mở rộng',{x:M,y:3.75,w:2.0,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Mở rộng sang nhiều miền giao diện, câu chuẩn do người viết và giao diện tiếng Việt.','Tăng độ bao phủ cho thao tác ngoài thao tác chạm và chuỗi nhiều màn hình.','Lặp thêm lượt huấn luyện để ước lượng chính xác hơn độ biến thiên của mức tăng.'],M,4.20,8.9,{gap:0.72,fs:13.8,h:0.60});
source('Luận văn §7.2–§7.4'); foot();

// 22 · contributions recap
newSlide('22. Ba đóng góp chính');
rect(M,1.20,2.72,3.62,LIGHT,{radius:0.05,line:FOOTB});
addText('Phương pháp',{x:M+0.15,y:1.50,w:2.42,h:0.40,fontSize:17,bold:true,color:FOOTB,align:'center'});
addText('GRPO-SPICE tạo phần lớn mức tăng; ACE nâng chất lượng câu mà giữ executability.',{x:M+0.25,y:2.20,w:2.22,h:1.35,fontSize:14.2,align:'center',valign:'mid',fit:'shrink'});
rect(3.64,1.20,2.72,3.62,LIGHT,{radius:0.05,line:FOOTC});
addText('Độ đo',{x:3.79,y:1.50,w:2.42,h:0.40,fontSize:17,bold:true,color:FOOTB,align:'center'});
addText('Executability đánh giá trực tiếp khả năng xác định đúng phần tử và thao tác, có các kiểm tra độ tin cậy đi kèm.',{x:3.89,y:2.15,w:2.22,h:1.50,fontSize:14.0,align:'center',valign:'mid',fit:'shrink'});
rect(6.72,1.20,2.72,3.62,LIGHT,{radius:0.05,line:FOOTD});
addText('Bằng chứng',{x:6.87,y:1.50,w:2.42,h:0.40,fontSize:17,bold:true,color:FOOTB,align:'center'});
addText('Nhánh thưởng xáo, 2 lượt GRPO, 4 công cụ đánh giá, ACU, lịch sử tự sinh và AitZ cùng làm rõ phạm vi tác dụng.',{x:6.97,y:2.15,w:2.22,h:1.50,fontSize:14.0,align:'center',valign:'mid',fit:'shrink'});
addText('Các thí nghiệm bổ sung giúp làm rõ mức tăng giữ được ở đâu và giới hạn xuất hiện khi nào.',{x:M,y:5.42,w:8.9,h:0.65,fontSize:15.5,bold:true,color:FOOTB,align:'center',fit:'shrink'});
source('Luận văn Chương 7'); foot();

// 23 · Conclusion
newSlide('23. Kết luận');
metricBadge(0.65,1.05,2.60,'+1,55','tập kiểm chính',FOOTB);
metricBadge(3.70,1.05,2.60,'+4,58','tác vụ chưa có trong tập dạy S1',FOOTC);
metricBadge(6.75,1.05,2.60,'+9,14','so với 7B prompting',FOOTD);
line(M,2.72,8.9,0,RULE,1);
bullets(['Nhánh thưởng xáo chạy cùng 500 bước nhưng quay về mức S1.','GRPO-SPICE tăng +1,55 điểm trên tập kiểm chính và +4,58 điểm trên ACU; chiều tăng giữ qua bốn công cụ đánh giá.','ACE đạt 60,68% executability và tăng cả 7 metric chữ; 6/6 metric có KTC nằm trên 0.','Trên AitZ, S1 vẫn cao hơn Base còn GRPO-SPICE tương đương S1 về executability.'],M,3.15,8.9,{gap:0.72,fs:13.8,h:0.60});
rect(1.10,6.10,7.80,0.58,LIGHT,{radius:0.05,line:FOOTD});
addText('Kết luận chính: trong thiết lập AndroidControl, GRPO-SPICE làm tăng đồng thời chất lượng câu và executability.',{x:1.28,y:6.10,w:7.44,h:0.58,fontSize:13.2,bold:true,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
source('Luận văn Chương 7'); foot();

// 24 · Cảm ơn — chỉ giữ đúng một câu theo yêu cầu
newSlide();
addText('Trân trọng cảm ơn Quý thầy cô đã lắng nghe.',{x:0.85,y:2.75,w:8.30,h:1.15,fontSize:27,bold:true,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
PAGE++;

// Slide bổ sung 1 · Định nghĩa executability
newSlide('Định nghĩa executability'); slide.hidden = true;
addText('Một bước đúng khi đồng thời:',{x:M,y:0.98,w:3.6,h:0.55,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Đúng loại thao tác.','Không mô tả thao tác theo nghĩa ngược.','|px−gx| ≤ 0,14W; |py−gy| ≤ 0,14H.','Điểm p nằm trong ô Voronoi của phần tử cần chạm.'],M,1.5,8.9,{gap:0.82,fs:15.5,h:0.67});
addText('Executability = số bước đúng / tổng số bước chạm.',{x:M,y:5.25,w:8.9,h:0.5,fontSize:17,bold:true,color:FOOTB,align:'center'}); footB();

// Slide bổ sung 2 · Toàn bộ metric
newSlide('Toàn bộ thước đo'); slide.hidden = true;
table(M,0.88,[2.35,1.2,1.2,1.35,1.35,1.25],[{cells:['Metric','Base','S1','GRPO','Đề xuất','Δ ACE'],fill:FOOTB,color:WHITE,bold:true,h:0.42,fs:12},{cells:['Executability','47,59','59,11','60,65','60,68','+0,02'],h:0.42,rule:true},{cells:['Hộp phần tử','53,60','65,49','67,02','67,11','+0,09'],h:0.42,rule:true},{cells:['AitW đầy đủ','63,39','74,37','76,25','76,32','+0,07'],h:0.42,rule:true},{cells:['BLEU-4','15,30','51,56','52,36','53,47','+1,11'],h:0.42,rule:true},{cells:['METEOR','24,60','36,79','37,92','38,37','+0,45'],h:0.42,rule:true},{cells:['ROUGE-L','42,30','67,35','68,36','69,11','+0,74'],h:0.42,rule:true},{cells:['CIDEr-D','88,00','416,12','430,05','442,02','+11,97'],h:0.42,rule:true},{cells:['SPICE','18,50','44,37','45,79','47,13','+1,33'],h:0.42,rule:true},{cells:['chrF','40,20','61,26','62,87','63,44','+0,58'],h:0.42,rule:true},{cells:['BERTScore','40,10','66,33','67,07','67,73','+0,66'],h:0.42}],{align:['left','center','center','center','center','center'],fs:11.7}); footB();

// Slide bổ sung 3 · Cross-listener
newSlide('Đối chiếu bằng bốn công cụ đánh giá'); slide.hidden = true;
addText('GRPO-SPICE − S1 trên cùng 4.463 bước',{x:M,y:0.95,w:8.9,h:0.45,fontSize:16.5,bold:true,color:FOOTB,align:'center'});
table(1.05,1.65,[2.20,1.55,3.80],[
  {cells:['Công cụ','Δ','KTC 95%'],fill:FOOTB,color:WHITE,bold:true,h:0.46},
  {cells:['UGround','+1,55','[+0,80; +2,33]'],h:0.58,rule:true},
  {cells:['UI-Venus','+1,55','[+0,82; +2,30]'],h:0.58,rule:true},
  {cells:['Phi-Ground','+0,78','[+0,05; +1,51]'],h:0.58,rule:true},
  {cells:['Phi-4','+0,69','[+0,02; +1,40]'],h:0.58}
],{align:['left','center','center'],fs:13});
addText('Cả bốn khoảng tin cậy đều nằm trên 0. Phi-Ground và Phi-4 nằm ngoài họ Qwen.',{x:M,y:4.75,w:8.9,h:0.65,fontSize:14.5,bold:true,color:FOOTB,align:'center',fit:'shrink'}); footB();

// Slide bổ sung 4 · Cấu hình huấn luyện
newSlide('Cấu hình huấn luyện'); slide.hidden = true;
table(M,1.0,[3.0,5.8],[{cells:['Hạng mục','Giá trị'],fill:FOOTB,color:WHITE,bold:true,h:0.44},{cells:['Backbone','Qwen2.5-VL-3B-Instruct'],h:0.48,rule:true},{cells:['Fine-tuning','QLoRA NF4 4-bit, rank 8, alpha 16, dropout 0,05'],h:0.48,rule:true},{cells:['SFT','2 epochs = 8.072 steps, batch hiệu dụng 16, LR 1e−4'],h:0.48,rule:true},{cells:['GRPO','8 samples/prompt, 500 updates, LR 1e−5, KL β 0,04'],h:0.48,rule:true},{cells:['Phần cứng','1 × A100, vision tower không cập nhật tham số'],h:0.48}],{align:['left','left'],fs:12.7}); footB();

newSlide('Các hướng đã khảo sát'); slide.hidden = true;
table(M,1.05,[2.75,1.20,4.95],[
  {cells:['Hướng','Exec.','Điều rút ra'],fill:FOOTB,color:WHITE,bold:true,h:0.46,fs:12.3},
  {cells:['Mô tả phần tử trước câu','57,2','Khi biểu diễn trung gian sai, câu cuối bị ảnh hưởng mạnh.'],h:0.64,rule:true},
  {cells:['MIN-DESC','60,0','Mục tiêu ưu tiên có đóng góp riêng +0,63 điểm so với học thêm có giám sát.'],h:0.64,rule:true},
  {cells:['Phần thưởng tọa độ','60,1','Biểu diễn tọa độ tốt hơn nhưng thay đổi ở câu cuối nhỏ hơn.'],h:0.64,rule:true},
  {cells:['Chọn ứng viên','56,1','Khi thực sự chọn, chất lượng khá tốt; vấn đề nằm ở quyết định từ chối chọn.'],h:0.64,rule:true},
  {cells:['TAGE','60,2','Bộ biên tập có ích khi vùng cắt đúng; khâu chọn vùng còn là điểm cần cải thiện.'],h:0.64}
],{align:['left','center','left'],fs:12.1});
rect(M,5.35,8.9,0.78,LIGHT,{radius:0.05,line:FOOTD});
addText('Các hướng trung gian giúp xác định rằng tối ưu trực tiếp câu cuối phù hợp hơn với mục tiêu chính.',{x:M+0.20,y:5.35,w:8.50,h:0.78,fontSize:14.0,bold:true,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
footB();

pptx.writeFile({ fileName:path.join(__dirname, '..', 'LUAN_VAN_SLIDE_BAO_VE_CONCISE.pptx') });
