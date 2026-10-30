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

function addText(t,o={}){ slide.addText(t,Object.assign({fontFace:TF,fontSize:BODY_FS,color:INK,margin:0,lineSpacingMultiple:1.25},o)); }
function rect(x,y,w,h,fill,o={}){ slide.addShape(o.radius?pptx.ShapeType.roundRect:pptx.ShapeType.rect,{x,y,w,h,fill:{color:fill},line:o.line?{color:o.line,width:o.lw||1}:{color:fill,transparency:100},radius:o.radius||0}); }
function line(x,y,w,h,c=RULE,lw=1,end=false){ slide.addShape(pptx.ShapeType.line,{x,y,w,h,line:{color:c,width:lw,endArrowType:end?'triangle':'none'}}); }
function bar(section){
  rect(0,0,W,0.58,BAR);
  addText(section,{x:0.30,y:0,w:9.40,h:0.58,fontSize:18.2,bold:true,color:WHITE,valign:'mid',fit:'shrink'});
}
function footRow(label){ const y=H-0.26,h=0.26; rect(0,y,3,h,FOOTA);rect(3,y,3.7,h,FOOTB);rect(6.7,y,1.9,h,FOOTC);rect(8.6,y,1.4,h,FOOTD); addText('Luận văn thạc sĩ',{x:0,y,w:3,h,fontFace:MONO,fontSize:8,bold:true,color:WHITE,align:'center',valign:'mid'}); addText('Phát sinh tự động hướng dẫn sử dụng phần mềm dựa trên LLM',{x:3,y,w:3.7,h,fontSize:8,color:WHITE,align:'center',valign:'mid'}); addText('Lê Đoàn Phương Uyên',{x:6.7,y,w:1.9,h,fontSize:8,color:WHITE,align:'center',valign:'mid'}); addText(label,{x:8.6,y,w:1.4,h,fontSize:8,color:WHITE,align:'center',valign:'mid'}); }
function foot(){ PAGE++; footRow(`${PAGE}/${TOTAL}`); }
function footB(){ BPAGE++; footRow(''); }
const SECTION_META = {
  'Giới thiệu': { n: 1, label: 'Tổng quan' },
  'Dữ liệu và đánh giá': { n: 2, label: 'Dữ liệu và đánh giá' },
  'Phương pháp đề xuất': { n: 3, label: 'Phương pháp đề xuất' },
  'Thực nghiệm và kết quả': { n: 4, label: 'Thực nghiệm và kết quả' },
  'Kết luận': { n: 5, label: 'Kết luận' }
};
const sectionSlideCount = {};
function newSlide(section,topic=''){
  slide=pptx.addSlide();
  slide.background={color:WHITE};
  if(!section) return;
  const meta=SECTION_META[section];
  if(!meta){ bar(section); return; }
  const count=(sectionSlideCount[section]||0)+1;
  sectionSlideCount[section]=count;
  const heading=count===1
    ? `${meta.n}. ${meta.label}`
    : `${meta.n}.${count-1}. ${topic}`;
  bar(heading);
}
function bullets(items,x,y,w,o={}){ const gap=o.gap||0.88; items.forEach((it,i)=>{ const yy=y+i*gap; slide.addShape(pptx.ShapeType.ellipse,{x:x+0.02,y:yy+0.15,w:0.07,h:0.07,fill:{color:o.dot||ACCENT},line:{color:o.dot||ACCENT,transparency:100}}); addText(it,{x:x+0.23,y:yy,w:w-0.23,h:o.h||0.72,fontSize:o.fs||BODY_FS,color:o.color||INK,fit:'shrink',valign:'top',lineSpacingMultiple:1.25}); }); }
function box(x,y,w,h,t,o={}){ rect(x,y,w,h,o.fill||WHITE,{radius:o.radius||0,line:o.line||ACCENT2,lw:o.lw||1}); addText(t,{x,y,w,h,fontSize:o.fs||BODY_FS,bold:o.bold,color:o.color||INK,align:'center',valign:'mid',fit:'shrink'}); }
function source(t){ addText(t,{x:M,y:6.92,w:W-2*M,h:0.15,fontSize:8,italic:true,color:GREY,align:'right'}); }
function metricBadge(x,y,w,value,label,color=ACCENT){ addText(value,{x,y,w,h:0.55,fontSize:24,bold:true,color,align:'center',valign:'mid'}); addText(label,{x,y:y+0.58,w,h:0.52,fontSize:SMALL_FS,color:INK,align:'center',valign:'mid',fit:'shrink'}); }
function hbarChart(x,y,w,items,o={}){
  const labelW=o.labelW||2.15, valueW=o.valueW||0.92, gap=o.gap||0.16;
  const rowH=o.rowH||0.68, max=o.max||Math.max(...items.map(d=>d.value));
  const barX=x+labelW, barW=w-labelW-valueW-gap;
  items.forEach((d,i)=>{
    const yy=y+i*rowH;
    addText(d.label,{x,y:yy-0.01,w:labelW-0.12,h:0.40,fontSize:o.fs||13.6,bold:d.bold||false,color:d.labelColor||INK,valign:'mid',fit:'shrink'});
    rect(barX,yy+0.07,barW,0.28,o.track||'ECEAF0',{radius:0.04});
    rect(barX,yy+0.07,Math.max(0.06,barW*d.value/max),0.28,d.color||ACCENT,{radius:0.04});
    addText(d.text||String(d.value),{x:barX+barW+gap,y:yy-0.02,w:valueW,h:0.42,fontSize:o.fs||13.6,bold:d.bold||false,color:d.color||ACCENT,align:'right',valign:'mid',fit:'shrink'});
  });
}
function table(x,y,colW,rows,o={}){ let yy=y; rows.forEach(r=>{ const h=r.h||0.48; if(r.fill) rect(x,yy,colW.reduce((a,b)=>a+b,0),h,r.fill); let xx=x; r.cells.forEach((c,i)=>{ const cell=typeof c==='string'?{t:c}:c; if(cell.fill) rect(xx,yy,colW[i],h,cell.fill); addText(cell.t,{x:xx,y:yy,w:colW[i],h,fontSize:cell.fs||r.fs||o.fs||TABLE_FS,bold:cell.bold!=null?cell.bold:r.bold,color:cell.color||r.color||INK,align:cell.align||(o.align&&o.align[i])||'left',valign:'mid',fit:'shrink',italic:cell.italic}); xx += colW[i]; }); if(r.rule) line(x,yy+h,colW.reduce((a,b)=>a+b,0),0,r.rule===true?RULE:r.rule,1); yy += h; }); }

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

// 2 · Bài toán
newSlide('Giới thiệu','Bài toán');
addText('Mô hình nhận trạng thái tác vụ và giao diện hiện tại, rồi sinh một câu hướng dẫn cho bước tiếp theo.',{x:M,y:0.92,w:8.9,h:0.56,fontSize:16.8,color:FOOTB,align:'center',fit:'shrink'});
addText('Mô hình nhận vào',{x:0.78,y:1.74,w:2.65,h:0.36,fontSize:16.4,bold:true,color:FOOTB});
line(0.78,2.16,2.65,0,FOOTD,1.2);
bullets(['Ảnh màn hình hiện tại','Mục tiêu người dùng','Các bước đã thực hiện trước đó','Văn bản hiển thị trên giao diện'],0.78,2.43,2.86,{gap:0.69,fs:14.4,h:0.54});
line(3.78,1.72,0,3.70,RULE,1);
box(4.18,2.62,1.68,1.28,'Mô hình\nsinh câu',{bold:true,fill:WHITE,line:FOOTB,fs:16});
line(5.98,3.26,0.55,0,FOOTC,2,true);
addText('Mô hình sinh ra',{x:6.78,y:1.74,w:2.35,h:0.36,fontSize:16.4,bold:true,color:FOOTB});
line(6.78,2.16,2.35,0,FOOTD,1.2);
addText('Một câu hướng dẫn\ncho bước tiếp theo',{x:6.78,y:2.63,w:2.35,h:1.12,fontSize:19,bold:true,color:INK,align:'left',valign:'mid',fit:'shrink'});
addText('Đầu ra của luận văn là câu hướng dẫn cho người dùng, không phải tọa độ để hệ thống tự thao tác.',{x:0.78,y:5.72,w:8.35,h:0.50,fontSize:14.2,color:GREY,fit:'shrink'}); foot();

// 3 · Yêu cầu câu hướng dẫn
newSlide('Giới thiệu','Yêu cầu của câu hướng dẫn');
addText('Một câu tự nhiên vẫn có thể chưa đủ rõ để người dùng chọn đúng phần tử.',{x:M,y:0.96,w:8.9,h:0.50,fontSize:16.8,color:FOOTB,align:'center',fit:'shrink'});
table(0.92,1.68,[4.10,4.10],[
  {cells:['Câu mơ hồ','Câu đủ rõ'],fill:FOOTB,color:WHITE,bold:true,h:0.56,fs:14.0},
  {cells:[{t:'“Tap the button.”',italic:true,color:FOOTD},{t:'“Tap Not now.”',italic:true,color:FOOTC}],h:0.92,rule:true,fs:18.0},
  {cells:['Không biết cần chạm nút nào khi màn hình có nhiều nút.','Xác định được phần tử cần thao tác.'],h:1.06,fs:14.6}
],{align:['center','center'],fs:14.6});
line(0.92,4.76,8.20,0,RULE,1);
addText('Yêu cầu của bài toán không chỉ là sinh câu đúng nội dung, mà còn phải giúp phân biệt đúng phần tử cần thao tác.',{x:1.08,y:5.12,w:7.84,h:0.78,fontSize:15.4,color:FOOTB,align:'center',valign:'mid',fit:'shrink'}); foot();

// 4 · Cách đánh giá
newSlide('Giới thiệu','Cách đánh giá câu hướng dẫn');
addText('Luận văn dùng hai góc nhìn bổ sung nhau: chất lượng câu và khả năng làm theo câu hướng dẫn.',{x:M,y:0.94,w:8.9,h:0.52,fontSize:16.4,color:FOOTB,align:'center',fit:'shrink'});
table(0.72,1.62,[2.25,3.20,3.10],[
  {cells:['Nhóm chỉ số','Đo gì','Vai trò'],fill:FOOTB,color:WHITE,bold:true,h:0.58,fs:13.4},
  {cells:['BLEU / ROUGE','Mức độ giống cách diễn đạt với câu chuẩn','Đánh giá cách viết'],h:0.90,rule:true,fs:13.8},
  {cells:['SPICE / CIDEr','Mức độ giống về nội dung','Đánh giá nội dung câu'],h:0.90,rule:true,fs:13.8},
  {cells:[{t:'Executability',bold:true,color:FOOTB,fill:'EDE7F6'},{t:'Đúng phần tử và đúng loại thao tác',bold:true,color:FOOTB,fill:'EDE7F6'},{t:'Đánh giá khả năng làm theo',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.94,fs:13.8}
],{align:['left','left','left'],fs:13.8});
addText('Hai nhóm chỉ số được báo cùng nhau vì một câu có thể giống câu chuẩn nhưng vẫn chưa đủ rõ để thực hiện.',{x:0.92,y:5.36,w:8.16,h:0.60,fontSize:14.5,color:GREY,align:'center',fit:'shrink'}); foot();

// 5 · Đóng góp
newSlide('Giới thiệu','Đóng góp chính');
addText('Ba đóng góp của luận văn được tóm tắt dưới đây.',{x:M,y:0.94,w:8.9,h:0.42,fontSize:16.0,color:FOOTB,align:'center'});
table(0.70,1.50,[2.05,4.75,2.05],[
  {cells:['Đóng góp','Nội dung','Kết quả tiêu biểu'],fill:FOOTB,color:WHITE,bold:true,h:0.58,fs:13.0},
  {cells:[{t:'1 · Phương pháp',bold:true},'GRPO-SPICE tối ưu trực tiếp câu hướng dẫn. ACE hiệu chỉnh có chọn lọc.',{t:'+1,55',bold:true,color:FOOTB,fill:'EDE7F6'}],h:1.10,rule:true,fs:13.6},
  {cells:[{t:'2 · Executability',bold:true},'Đề xuất executability để đánh giá khả năng làm theo câu hướng dẫn.',{t:'60,65%',bold:true,color:FOOTB,fill:'EDE7F6'}],h:1.10,rule:true,fs:13.6},
  {cells:[{t:'3 · Bằng chứng thực nghiệm',bold:true},'Kiểm tra trên tác vụ mới, nhiều mô hình định vị, các bước trước do mô hình tạo và AitZ.',{t:'+4,58',bold:true,color:FOOTB,fill:'EDE7F6'}],h:1.18,fs:13.3}
],{align:['left','left','center'],fs:13.5});
addText('Sau ACE, cả 7 chỉ số chất lượng câu đều tăng so với GRPO-SPICE.',{x:0.92,y:5.70,w:8.16,h:0.46,fontSize:14.0,color:GREY,align:'center',fit:'shrink'}); foot();

// 6 · Dữ liệu nguồn
newSlide('Dữ liệu và đánh giá','AndroidControl');
addText('AndroidControl là bộ dữ liệu thao tác trên giao diện Android do Google DeepMind công bố.',{x:M,y:0.92,w:8.9,h:0.50,fontSize:16.2,color:FOOTB,align:'center',fit:'shrink'});
table(0.84,1.54,[2.72,2.72,2.72],[
  {cells:[{t:'15.283',bold:true,color:FOOTB},{t:'Người thật',bold:true,color:FOOTB},{t:'0',bold:true,color:FOOTB}],h:0.62,fs:20.0},
  {cells:['chuỗi thao tác','thực hiện các chuỗi thao tác','nhãn thủ công bổ sung'],h:0.55,fs:12.8}
],{align:['center','center','center']});
line(0.84,2.86,8.16,0,RULE,1);
addText('Thông tin có ở mỗi bước',{x:0.84,y:3.15,w:2.40,h:0.36,fontSize:15.4,bold:true,color:FOOTB});
table(0.84,3.62,[2.00,2.00,2.00,2.16],[
  {cells:['Màn hình','Thao tác','Tọa độ chạm','Câu hướng dẫn'],fill:LIGHT,bold:true,h:0.62,fs:13.4},
  {cells:['Trạng thái giao diện','Loại thao tác thực hiện','Vị trí tương tác nếu có','Do người thực hiện viết'],h:0.90,fs:12.8}
],{align:['center','center','center','center']});
addText('AndroidControl dùng câu hướng dẫn để dự đoán thao tác. Luận văn dùng dữ liệu theo chiều ngược lại để sinh câu hướng dẫn cho bước tiếp theo.',{x:0.84,y:5.40,w:8.16,h:0.72,fontSize:14.2,color:FOOTB,align:'center',fit:'shrink'}); foot();

// 7 · Cách chia dữ liệu
newSlide('Dữ liệu và đánh giá','Cách chia dữ liệu');
addText('Huấn luyện và kiểm tra chính được tách theo tác vụ.',{x:M,y:0.92,w:8.9,h:0.46,fontSize:16.2,color:FOOTB,align:'center',fit:'shrink'});
table(1.12,1.48,[3.50,2.20,2.20],[
  {cells:['Chỉ số','Huấn luyện','Kiểm tra chính'],fill:FOOTB,color:WHITE,bold:true,h:0.58,fs:13.4},
  {cells:['Số bước','64.567','6.958'],h:0.68,rule:true,fs:14.0},
  {cells:['Bước có thao tác chạm','41.191','4.463'],h:0.68,rule:true,fs:14.0},
  {cells:['Số tác vụ','12.895','1.432'],h:0.68,fs:14.0}
],{align:['left','center','center'],fs:14.0});
addText('Không có tác vụ nào xuất hiện ở cả tập huấn luyện và tập kiểm tra chính.',{x:1.12,y:3.96,w:7.90,h:0.42,fontSize:13.8,color:GREY,align:'center',fit:'shrink'});
addText('Hai tập bổ sung để kiểm tra khả năng khái quát',{x:1.12,y:4.56,w:7.90,h:0.38,fontSize:15.0,bold:true,color:FOOTB});
table(1.12,5.02,[2.45,5.45],[
  {cells:[{t:'Tác vụ mới (ACU)',bold:true,color:FOOTB,fill:'EDE7F6'},'1.484 bước từ các tác vụ không xuất hiện trong tập huấn luyện có giám sát'],h:0.68,rule:true,fs:13.2},
  {cells:[{t:'Bộ dữ liệu khác (AitZ)',bold:true},'Bộ dữ liệu giao diện khác để kiểm tra khả năng áp dụng ngoài AndroidControl'],h:0.68,fs:13.2}
],{align:['left','left'],fs:13.2}); foot();

// 7 · Baseline và scale
newSlide('Dữ liệu và đánh giá','Executability');
box(0.65,1.72,1.90,0.92,'Câu hướng dẫn',{bold:true,fill:WHITE,line:FOOTD});
line(2.67,2.18,0.40,0,FOOTC,2,true);
box(3.18,1.58,2.25,1.20,'Mô hình định vị\ntách biệt',{bold:true,fill:LIGHT,line:FOOTB,fs:15});
line(5.55,2.18,0.40,0,FOOTC,2,true);
box(6.06,1.72,1.30,0.92,'Điểm (x,y)',{bold:true,fill:WHITE,line:FOOTD,fs:14});
line(7.48,2.18,0.40,0,FOOTC,2,true);
box(7.98,1.50,1.38,1.36,'Kiểm tra\nphần tử + thao tác',{bold:true,fill:LIGHT,line:FOOTC,fs:13.2});
addText('Một bước được tính đúng khi đồng thời:',{x:M,y:3.48,w:4.75,h:0.55,fontSize:15.5,bold:true,color:FOOTB,valign:'mid',fit:'shrink'});
bullets(['đúng loại thao tác','không diễn đạt ngược thao tác cần làm','điểm định vị thuộc vùng của phần tử cần chạm'],M,4.02,8.9,{gap:0.62,fs:15.0,h:0.52});
addText('Mô hình định vị không tham gia huấn luyện phương pháp và không biết tọa độ đáp án.',{x:M,y:5.98,w:8.9,h:0.45,fontSize:14.0,color:FOOTB,align:'center'}); foot();

// 9 · Độ tin cậy metric
newSlide('Dữ liệu và đánh giá','Kiểm tra độ tin cậy của executability');
addText('Trên cùng một nhóm bước, câu càng thiếu thông tin để xác định đúng phần tử thì executability càng thấp.',{x:M,y:0.91,w:8.9,h:0.62,fontSize:16.0,color:FOOTB,align:'center',fit:'shrink'});
hbarChart(1.05,1.78,7.90,[
  {label:'Câu chuẩn (đầy đủ thông tin)',value:74.9,text:'74,9%',color:FOOTB,bold:true},
  {label:'Câu mơ hồ: “Tap the button.”',value:12.0,text:'12,0%',color:FOOTC},
  {label:'Câu sai màn hình',value:6.1,text:'6,1%',color:FOOTD}
],{max:80,rowH:0.90,labelW:2.35,valueW:0.92,fs:14.2});
rect(1.15,4.92,7.70,0.94,LIGHT,{line:FOOTC});
addText('Kết quả đúng kỳ vọng: 74,9% → 12,0% → 6,1%. Khi câu mơ hồ hoặc sai ngữ cảnh, executability giảm mạnh.',{x:1.38,y:4.92,w:7.24,h:0.94,fontSize:15.4,bold:true,color:FOOTB,align:'center',valign:'mid',fit:'shrink'}); foot();

// 10 · Tổng quan phương pháp
newSlide('Phương pháp đề xuất','Quy trình tổng thể');
box(0.45,1.18,1.72,1.28,'Baseline S1\n3B sau tinh chỉnh\ncó giám sát',{bold:true,line:FOOTD,fs:12.9});
line(2.05,1.80,0.20,0,FOOTC,2,true);
box(2.32,1.25,2.08,1.10,'GRPO-SPICE\nsinh câu ban đầu',{bold:true,fill:LIGHT,line:FOOTB,fs:15});
line(4.52,1.80,0.28,0,FOOTC,2,true);
box(4.90,1.25,2.08,1.10,'ACE\nhiệu chỉnh có chọn lọc',{bold:true,fill:LIGHT,line:FOOTC,fs:15});
line(7.10,1.80,0.28,0,FOOTC,2,true);
box(7.48,1.25,1.98,1.10,'Câu hướng dẫn\ncuối',{bold:true,fill:WHITE,line:FOOTD,fs:14});
addText('GRPO-SPICE',{x:M,y:3.42,w:2.15,h:0.40,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Sinh 8 câu cho cùng đầu vào.','Dùng SPICE + phạt độ dài để cập nhật mô hình.'],M,3.92,4.15,{gap:0.76,fs:15.2,h:0.62});
addText('ACE',{x:5.05,y:3.42,w:1.2,h:0.40,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Tìm 4 câu ví dụ phù hợp trong tập huấn luyện.','Chỉ thay câu ban đầu khi qua 2 điều kiện chọn lọc.'],5.05,3.92,4.35,{gap:0.76,fs:15.2,h:0.62});
addText('Mô hình định vị chỉ được dùng để đánh giá câu hướng dẫn. Mô hình này không tham gia sinh câu hay cập nhật mô hình.',{x:M,y:5.82,w:8.9,h:0.48,fontSize:14.2,color:FOOTB,align:'center',fit:'shrink'}); foot();

// 11 · GRPO
newSlide('Phương pháp đề xuất','Thành phần thứ nhất: GRPO-SPICE');
box(0.60,1.85,1.55,0.92,'Một mẫu huấn luyện',{bold:true,fill:LIGHT,line:FOOTD});
line(2.28,2.31,0.42,0,FOOTC,2,true);
box(2.82,1.66,1.75,1.30,'8 câu\nhướng dẫn',{bold:true,fill:LIGHT,line:FOOTB});
line(4.70,2.31,0.42,0,FOOTC,2,true);
box(5.24,1.66,1.80,1.30,'SPICE\n− phạt độ dài',{bold:true,fill:LIGHT,line:FOOTC,fs:15});
line(7.17,2.31,0.42,0,FOOTC,2,true);
box(7.71,1.60,1.70,1.42,'Cập nhật\nGRPO',{bold:true,fill:LIGHT,line:FOOTD,fs:15});
rect(M,3.65,8.9,1.72,LIGHT,{line:FOOTD});
addText('Vai trò của SPICE',{x:M+0.22,y:3.90,w:2.15,h:0.35,fontSize:15.5,bold:true,color:FOOTB});
addText('SPICE ưu tiên đúng nội dung hơn mức độ giống câu chữ.\nTín hiệu huấn luyện tập trung vào đối tượng và quan hệ cần mô tả.',{x:M+2.12,y:3.72,w:6.50,h:0.96,fontSize:15.6,valign:'mid',fit:'shrink'});
addText('GRPO-SPICE tối ưu trực tiếp câu hướng dẫn bằng tín hiệu SPICE.',{x:M,y:5.80,w:8.9,h:0.45,fontSize:14.6,bold:true,color:FOOTB,align:'center'}); foot();

// 12 · shuffled control
newSlide('Phương pháp đề xuất','Thành phần thứ hai: ACE');
box(0.45,1.25,1.65,0.95,'Câu ban đầu',{bold:true,fill:WHITE,line:FOOTD,fs:14.5});
line(2.20,1.73,0.38,0,FOOTC,2,true);
box(2.68,1.15,1.90,1.15,'Tìm 4 câu ví dụ phù hợp\ntừ tập huấn luyện',{bold:true,fill:LIGHT,line:FOOTB,fs:13.2});
line(4.68,1.73,0.38,0,FOOTC,2,true);
box(5.16,1.15,1.55,1.15,'Sinh câu\nứng viên',{bold:true,fill:LIGHT,line:FOOTC,fs:14});
line(6.81,1.73,0.38,0,FOOTC,2,true);
box(7.29,1.05,2.20,1.35,'Kiểm tra\n2 điều kiện chọn lọc',{bold:true,fill:LIGHT,line:FOOTD,fs:14});
rect(M,3.42,4.20,1.18,LIGHT,{line:FOOTC});
addText('1 · Câu ứng viên phải trùng với một trong bốn câu ví dụ đã tìm.',{x:M+0.18,y:3.42,w:3.84,h:1.18,fontSize:14.0,align:'center',valign:'mid',fit:'shrink'});
rect(5.25,3.42,4.20,1.18,LIGHT,{line:FOOTC});
addText('2 · Động từ đầu câu phải cùng lớp thao tác với câu ban đầu.',{x:5.43,y:3.42,w:3.84,h:1.18,fontSize:14.0,align:'center',valign:'mid',fit:'shrink'});
box(1.80,5.10,2.80,0.82,'Đủ điều kiện → dùng câu mới',{bold:true,fill:LIGHT,line:FOOTC,fs:14});
box(5.40,5.10,2.80,0.82,'Không đủ → giữ câu ban đầu',{bold:true,fill:WHITE,line:FOOTD,fs:14}); foot();

// 16 · ACE result
newSlide('Thực nghiệm và kết quả','So sánh 3B đã tinh chỉnh với 7B Base');
addText('Cùng một prompt, tinh chỉnh 3B cho mức tăng lớn hơn việc chỉ tăng kích chỉ số mô hình lên 7B.',{x:M,y:0.92,w:8.9,h:0.58,fontSize:15.6,color:FOOTB,align:'center',fit:'shrink'});
table(0.95,1.65,[3.30,2.15,2.35],[
  {cells:['Mô hình','Executability','Δ so với 7B Base'],fill:FOOTB,color:WHITE,bold:true,h:0.58,fs:13.0},
  {cells:['3B · Base','47,59','−3,92'],h:0.72,rule:true,fs:13.8},
  {cells:['7B · Base','51,51','—'],h:0.72,rule:true,fs:13.8},
  {cells:['3B · Baseline S1','59,11','+7,60'],h:0.72,rule:true,fs:13.8},
  {cells:['3B · GRPO-SPICE',{t:'60,65',bold:true,color:FOOTB,fill:'EDE7F6'},{t:'+9,14',bold:true,color:FOOTC}],h:0.78,fs:13.8}
],{align:['left','center','center'],fs:13.5});
addText('7B Base dùng cùng prompt của 3B Base và không được tối ưu prompt riêng.',{x:M,y:5.62,w:8.9,h:0.42,fontSize:12.8,color:GREY,align:'center',fit:'shrink'}); foot();

// 8 · Executability
newSlide('Thực nghiệm và kết quả','Vai trò của tín hiệu SPICE');
addText('Giữ nguyên số bước cập nhật GRPO, chỉ cấu hình dùng đúng điểm SPICE cho câu được sinh mới làm executability tăng.',{x:M,y:0.88,w:8.9,h:0.54,fontSize:16.1,color:FOOTB,align:'center',fit:'shrink'});
table(1.05,1.62,[3.55,2.05,2.35],[
  {cells:['Thiết lập','Executability','Thay đổi so với S1'],fill:FOOTB,color:WHITE,bold:true,h:0.58,fs:12.8},
  {cells:['Baseline S1','59,11%','—'],h:0.76,rule:true,fs:14.0},
  {cells:['GRPO với SPICE không đúng câu','59,11%','0,00'],h:0.82,rule:true,fs:13.5},
  {cells:['GRPO-SPICE',{t:'60,65%',bold:true,color:FOOTB,fill:'EDE7F6'},{t:'+1,55',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.86,fs:14.0}
],{align:['left','center','center'],fs:13.5});
rect(1.15,4.72,7.70,1.02,LIGHT,{line:FOOTC});
addText('Kết quả cho thấy mức tăng gắn với tín hiệu SPICE, không chỉ với việc chạy thêm GRPO.',{x:1.40,y:4.72,w:7.20,h:1.02,fontSize:15.2,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
addText('GRPO-SPICE cao hơn cấu hình kiểm tra +1,55 điểm · KTC 95% từ +0,81 đến +2,30.',{x:M,y:5.96,w:8.9,h:0.42,fontSize:13.2,color:GREY,align:'center',fit:'shrink'}); foot();

// 13 · main benchmark
newSlide('Thực nghiệm và kết quả','Kết quả trên tập kiểm chính');
addText('GRPO-SPICE cao hơn baseline S1 trên các độ đo chính.',{x:M,y:0.93,w:8.9,h:0.48,fontSize:16.7,color:FOOTB,align:'center'});
rect(0.64,3.40,8.72,0.72,'F0EEF5');
table(0.64,1.52,[2.02,1.55,1.38,1.38,1.05,1.34],[
  {cells:['Mô hình','Executability','Hộp phần tử','AitW đầy đủ','SPICE','CIDEr-D'],fill:FOOTB,color:WHITE,bold:true,h:0.62,fs:11.8},
  {cells:['Base','47,59','53,60','63,39','18,50','88,00'],h:0.66,rule:true},
  {cells:['Baseline S1','59,11','65,49','74,37','44,37','416,12'],h:0.66,rule:true},
  {cells:['GRPO-SPICE',{t:'60,65',bold:true,color:FOOTB,fill:'EDE7F6'},{t:'67,02',bold:true,color:FOOTB,fill:'EDE7F6'},{t:'76,25',bold:true,color:FOOTB,fill:'EDE7F6'},{t:'45,79',bold:true,color:FOOTB,fill:'EDE7F6'},{t:'430,05',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.72}
] ,{align:['left','center','center','center','center','center'],fs:13.4});
metricBadge(1.08,4.48,2.30,'+1,55','Executability',FOOTC);
metricBadge(3.85,4.48,2.30,'+1,52','Hộp phần tử',FOOTC);
metricBadge(6.62,4.48,2.30,'+1,88','AitW đầy đủ',FOOTC);
addText('12/12 độ đo có KTC nằm trên 0. METEOR tăng nhưng chưa có KTC.',{x:M,y:6.00,w:8.9,h:0.42,fontSize:13.6,color:FOOTB,align:'center',fit:'shrink'}); foot();

// 14 · ACU
newSlide('Thực nghiệm và kết quả','Kết quả trên tác vụ mới (ACU)');
addText('ACU gồm 1.484 bước từ các tác vụ không xuất hiện trong huấn luyện S1.',{x:M,y:0.92,w:8.9,h:0.50,fontSize:15.4,color:FOOTB,align:'center',fit:'shrink'});
table(0.72,1.72,[2.65,1.55,1.85,2.70],[
  {cells:['Mô hình','Executability','Δ so với S1','KTC 95%'],fill:FOOTB,color:WHITE,bold:true,h:0.58,fs:12.7},
  {cells:['Base','49,80','—','—'],h:0.72,rule:true,fs:13.2},
  {cells:['Baseline S1','52,16','—','—'],h:0.72,rule:true,fs:13.2},
  {cells:['GRPO-SPICE','56,74',{t:'+4,58',bold:true,color:FOOTC},'+3,17 đến +6,05'],h:0.72,rule:true,fs:13.2},
  {cells:['ACE',{t:'57,01',bold:true,color:FOOTB,fill:'EDE7F6'},{t:'+4,85',bold:true,color:FOOTC},'+3,43 đến +6,32'],h:0.76,fs:13.2}
],{align:['left','center','center','center'],fs:13.0});
addText('Trên tập gộp 5.947 bước, GRPO-SPICE cao hơn S1 +2,30 điểm với KTC 95% từ +1,62 đến +2,99.',{x:0.95,y:5.60,w:8.10,h:0.55,fontSize:13.6,color:FOOTB,align:'center',fit:'shrink'}); foot();

// 15 · ACE process
newSlide('Thực nghiệm và kết quả','Kết quả sau ACE');
metricBadge(0.92,0.96,2.35,'60,68%','Executability',FOOTB);
metricBadge(3.82,0.96,2.35,'+0,02','so với GRPO-SPICE',FOOTD);
metricBadge(6.72,0.96,2.35,'7/7','chỉ số chất lượng câu tăng',FOOTC);
addText('ACE giữ executability ở mức tương đương GRPO-SPICE và tiếp tục tăng các độ đo dựa trên câu chuẩn.',{x:M,y:1.98,w:8.9,h:0.42,fontSize:14.0,color:FOOTB,align:'center',fit:'shrink'});
rect(6.34,2.53,2.05,3.84,'F0EEF5');
table(0.56,2.53,[1.70,1.30,1.56,1.76,1.76],[
  {cells:['Chỉ số','Base','Baseline S1','GRPO-SPICE',{t:'ACE',bold:true}],fill:FOOTB,color:WHITE,bold:true,h:0.48,fs:11.6},
  {cells:['BLEU-4','15,34','51,56','52,36',{t:'53,47',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.48,rule:true},
  {cells:['METEOR','24,58','36,79','37,92',{t:'38,37',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.48,rule:true},
  {cells:['ROUGE-L','42,31','67,35','68,36',{t:'69,11',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.48,rule:true},
  {cells:['CIDEr-D','88,01','416,12','430,05',{t:'442,02',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.48,rule:true},
  {cells:['SPICE','18,48','44,37','45,79',{t:'47,13',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.48,rule:true},
  {cells:['chrF','40,18','61,26','62,87',{t:'63,45',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.48,rule:true},
  {cells:['BERTScore','40,10','66,33','67,07',{t:'67,73',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.48}
],{align:['left','center','center','center','center'],fs:11.9});
addText('6/6 độ đo có KTC nằm trên 0. METEOR chưa có KTC.',{x:M,y:6.43,w:8.9,h:0.32,fontSize:12.8,color:FOOTB,align:'center',fit:'shrink'}); foot();

// Full evaluation table
newSlide('Thực nghiệm và kết quả','Toàn bộ chỉ số đánh giá');
addText('Kết quả trên 4.463 bước có thao tác chạm. Giá trị cao nhất trong bốn cấu hình được in đậm.',{x:M,y:0.86,w:8.9,h:0.42,fontSize:13.4,color:FOOTB,align:'center',fit:'shrink'});
table(0.60,1.38,[2.42,1.36,1.60,1.64,1.64],[
  {cells:['Chỉ số','Base','Baseline S1','GRPO-SPICE','ACE'],fill:FOOTB,color:WHITE,bold:true,h:0.46,fs:11.6},
  {cells:['Executability','47,59','59,11','60,65',{t:'60,68',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.40,rule:true,fs:11.5},
  {cells:['Hộp phần tử','53,60','65,49','67,02',{t:'67,11',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.40,rule:true,fs:11.5},
  {cells:['Hộp phần tử + 14%','49,76','61,73','63,25',{t:'63,28',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.40,rule:true,fs:11.5},
  {cells:['AitW đầy đủ','63,39','74,37','76,25',{t:'76,32',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.40,rule:true,fs:11.5},
  {cells:['Đúng loại thao tác',{t:'96,5',bold:true,color:FOOTB,fill:'EDE7F6'},'94,35','95,97','95,97'],h:0.40,rule:true,fs:11.5},
  {cells:['BLEU-4','15,34','51,56','52,36',{t:'53,47',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.40,rule:true,fs:11.5},
  {cells:['METEOR','24,58','36,79','37,92',{t:'38,37',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.40,rule:true,fs:11.5},
  {cells:['ROUGE-L','42,31','67,35','68,36',{t:'69,11',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.40,rule:true,fs:11.5},
  {cells:['CIDEr-D','88,01','416,12','430,05',{t:'442,02',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.40,rule:true,fs:11.5},
  {cells:['SPICE','18,48','44,37','45,79',{t:'47,13',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.40,rule:true,fs:11.5},
  {cells:['chrF','40,18','61,26','62,87',{t:'63,45',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.40,rule:true,fs:11.5},
  {cells:['BERTScore','40,10','66,33','67,07',{t:'67,73',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.40,fs:11.5}
],{align:['left','center','center','center','center'],fs:11.5});
foot();

// 17 · multi-tool
newSlide('Thực nghiệm và kết quả','Đối chiếu với bốn mô hình định vị');
addText('Executability được tính lại bằng bốn mô hình định vị để kiểm tra độ ổn định của kết quả.',{x:M,y:0.90,w:8.9,h:0.52,fontSize:15.2,color:FOOTB,align:'center',fit:'shrink'});
table(0.58,1.48,[2.18,1.55,1.55,1.55,1.55],[
  {cells:['Mô hình','UGround','UI-Venus','Phi-Ground','Phi-4'],fill:FOOTB,color:WHITE,bold:true,h:0.54,fs:12.3},
  {cells:['Base','47,59','—','40,80','38,23'],h:0.60,rule:true,fs:12.8},
  {cells:['Baseline S1','59,11','54,51','46,96','44,63'],h:0.60,rule:true,fs:12.8},
  {cells:['GRPO-SPICE','60,65','56,06',{t:'47,75',bold:true,color:FOOTB,fill:'EDE7F6'},{t:'45,33',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.62,rule:true,fs:12.8},
  {cells:['ACE',{t:'60,68',bold:true,color:FOOTB,fill:'EDE7F6'},{t:'56,20',bold:true,color:FOOTB,fill:'EDE7F6'},'47,73',{t:'45,33',bold:true,color:FOOTB,fill:'EDE7F6'}],h:0.62,rule:true,fs:12.8},
  {cells:['Δ GRPO-SPICE − S1',{t:'+1,55',bold:true,color:FOOTC},{t:'+1,55',bold:true,color:FOOTC},{t:'+0,78',bold:true,color:FOOTC},{t:'+0,69',bold:true,color:FOOTC}],h:0.64,fs:12.6}
],{align:['left','center','center','center','center'],fs:12.7});
foot();

// 18 · history + AitZ
newSlide('Thực nghiệm và kết quả','Khi các bước trước do mô hình tạo ra');
addText('Khi các bước trước cũng do chính mô hình tạo ra, GRPO-SPICE vẫn cao hơn Baseline S1.',{x:M,y:0.94,w:8.9,h:0.52,fontSize:15.4,color:FOOTB,align:'center',fit:'shrink'});
table(1.05,1.72,[3.10,2.20,2.20],[
  {cells:['Mô hình','Các bước trước từ dữ liệu gốc','Các bước trước do mô hình tạo'],fill:FOOTB,color:WHITE,bold:true,h:0.58,fs:12.4},
  {cells:['Baseline S1','59,11','54,96'],h:0.78,rule:true,fs:14.0},
  {cells:['GRPO-SPICE',{t:'60,65',bold:true,color:FOOTB,fill:'EDE7F6'},{t:'56,44',bold:true,color:FOOTC}],h:0.78,rule:true,fs:14.0},
  {cells:['Δ GRPO-SPICE − S1',{t:'+1,55',bold:true,color:FOOTC},{t:'+1,48',bold:true,color:FOOTC}],h:0.82,fs:14.0}
],{align:['left','center','center'],fs:13.6});
addText('KTC 95% khi các bước trước do mô hình tạo: +0,54 đến +2,43.',{x:M,y:5.16,w:8.9,h:0.44,fontSize:13.2,color:FOOTB,align:'center'});
addText('Cả hai mô hình đều giảm khoảng 4 điểm khi không dùng các bước trước từ dữ liệu gốc.',{x:M,y:5.72,w:8.9,h:0.46,fontSize:13.2,color:GREY,align:'center',fit:'shrink'}); foot();

newSlide('Thực nghiệm và kết quả','Kết quả trên AitZ');
addText('AitZ là bộ dữ liệu giao diện khác, dùng để kiểm tra khả năng áp dụng ngoài AndroidControl.',{x:M,y:0.92,w:8.9,h:0.50,fontSize:15.4,color:FOOTB,align:'center',fit:'shrink'});
table(0.92,1.58,[2.75,1.65,1.95,2.35],[
  {cells:['Mô hình','Executability','Δ so với S1','KTC 95%'],fill:FOOTB,color:WHITE,bold:true,h:0.56,fs:12.7},
  {cells:['Base','34,50','−3,29','−5,03 đến −1,51'],h:0.68,rule:true,fs:13.0},
  {cells:['Baseline S1',{t:'37,79',bold:true,color:FOOTB,fill:'EDE7F6'},'—','—'],h:0.68,rule:true,fs:13.0},
  {cells:['GRPO-SPICE','37,28','−0,51','−1,39 đến +0,36'],h:0.68,rule:true,fs:13.0},
  {cells:['ACE','37,28','−0,51','−1,39 đến +0,36'],h:0.68,fs:13.0}
],{align:['left','center','center','center'],fs:12.9});
addText('S1 vẫn cao hơn Base. GRPO-SPICE và ACE không khác rõ S1 về executability.',{x:M,y:5.54,w:8.9,h:0.50,fontSize:13.5,color:FOOTB,align:'center',fit:'shrink'}); foot();

newSlide('Thực nghiệm và kết quả','Độ ổn định giữa hai lần chạy GRPO-SPICE');
addText('Hai lần chạy GRPO-SPICE dùng cùng điểm khởi tạo và cùng cấu hình. Chỉ seed của giai đoạn GRPO thay đổi.',{x:M,y:0.94,w:8.9,h:0.54,fontSize:15.2,color:FOOTB,align:'center',fit:'shrink'});
table(0.92,1.82,[3.20,2.55,2.55],[
  {cells:['Mô hình','Executability','Δ giữa hai lần chạy'],fill:FOOTB,color:WHITE,bold:true,h:0.60,fs:13.0},
  {cells:['Baseline S1','59,11','—'],h:0.78,rule:true,fs:14.0},
  {cells:['GRPO-SPICE',{t:'60,65 / 59,94',bold:true,color:FOOTC},{t:'−0,72',bold:true,color:FOOTD}],h:0.84,fs:14.0}
],{align:['left','center','center'],fs:13.6});
addText('Cả hai lần chạy đều cao hơn Baseline S1. Kết quả thứ hai thấp hơn kết quả chính 0,72 điểm.',{x:1.18,y:4.38,w:7.64,h:0.68,fontSize:14.3,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
addText('KTC 95% cho Δ giữa hai lần chạy: −1,27 đến −0,16.',{x:M,y:5.48,w:8.9,h:0.44,fontSize:13.0,color:GREY,align:'center'}); foot();

// 21 · scope
newSlide('Kết luận','Phạm vi và hướng phát triển');
addText('Phạm vi hiện tại',{x:M,y:0.95,w:2.0,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Executability hiện tập trung vào các bước có thao tác chạm.','Thực nghiệm chính dùng AndroidControl tiếng Anh và Qwen2.5-VL-3B.','Trên AitZ, lợi ích bổ sung của GRPO-SPICE không còn rõ như trên AndroidControl.'],M,1.36,8.9,{gap:0.78,fs:15.0,h:0.64});
addText('Hướng mở rộng',{x:M,y:4.00,w:2.0,h:0.35,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Mở rộng sang nhiều miền giao diện và dữ liệu tiếng Việt.','Mở rộng executability cho thao tác ngoài chạm và chuỗi nhiều màn hình.'],M,4.50,8.9,{gap:1.02,fs:15.2,h:0.76}); foot();

// 23 · Conclusion
newSlide('Kết luận','Kết luận chung');
addText('Kết quả chính',{x:0.82,y:0.96,w:2.0,h:0.36,fontSize:16.4,bold:true,color:FOOTB});
table(0.82,1.42,[3.10,2.20,3.30],[
  {cells:['So sánh','Mức tăng','Ý nghĩa'],fill:FOOTB,color:WHITE,bold:true,h:0.56,fs:13.0},
  {cells:['GRPO-SPICE vs Baseline S1',{t:'+1,55',bold:true,color:FOOTB,fill:'EDE7F6'},'Tập kiểm chính'],h:0.70,rule:true,fs:13.5},
  {cells:['GRPO-SPICE vs Baseline S1',{t:'+4,58',bold:true,color:FOOTB,fill:'EDE7F6'},'Tác vụ mới (ACU)'],h:0.70,rule:true,fs:13.5},
  {cells:['GRPO-SPICE vs 7B Base',{t:'+9,14',bold:true,color:FOOTB,fill:'EDE7F6'},'Cùng prompt'],h:0.70,fs:13.5}
],{align:['left','center','left'],fs:13.5});
addText('Kết luận',{x:0.82,y:4.20,w:1.6,h:0.36,fontSize:16.4,bold:true,color:FOOTB});
bullets(['ACE giữ executability ở 60,68% và tăng cả 7 chỉ số chất lượng câu.','Trên AitZ, lợi ích bổ sung của GRPO-SPICE không còn rõ như trên AndroidControl.','Trong thiết lập AndroidControl, GRPO-SPICE làm tăng đồng thời chất lượng câu và executability.'],0.82,4.66,8.36,{gap:0.66,fs:14.6,h:0.54}); foot();

// 24 · Cảm ơn — chỉ giữ đúng một câu theo yêu cầu
newSlide();
addText('Trân trọng cảm ơn Quý thầy cô đã lắng nghe.',{x:0.85,y:2.75,w:8.30,h:1.15,fontSize:27,bold:true,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
PAGE++;

// Slide bổ sung 1 · Định nghĩa executability
newSlide('Định nghĩa executability'); slide.hidden = true;
addText('Một bước đúng khi đồng thời:',{x:M,y:0.98,w:3.6,h:0.55,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Đúng loại thao tác.','Không mô tả thao tác theo nghĩa ngược.','|px−gx| ≤ 0,14W và |py−gy| ≤ 0,14H.','Điểm p nằm trong ô Voronoi của phần tử cần chạm.'],M,1.5,8.9,{gap:0.82,fs:15.5,h:0.67});
addText('Executability = số bước đúng / tổng số bước chạm.',{x:M,y:5.25,w:8.9,h:0.5,fontSize:17,bold:true,color:FOOTB,align:'center'}); footB();

// Slide bổ sung 3 · Cross-listener
newSlide('Đối chiếu bằng bốn công cụ đánh giá'); slide.hidden = true;
addText('GRPO-SPICE − S1 trên cùng 4.463 bước',{x:M,y:0.95,w:8.9,h:0.45,fontSize:16.5,bold:true,color:FOOTB,align:'center'});
table(1.05,1.65,[2.20,1.55,3.80],[
  {cells:['Công cụ','Δ','KTC 95%'],fill:FOOTB,color:WHITE,bold:true,h:0.46},
  {cells:['UGround','+1,55','+0,80 đến +2,33'],h:0.58,rule:true},
  {cells:['UI-Venus','+1,55','+0,82 đến +2,30'],h:0.58,rule:true},
  {cells:['Phi-Ground','+0,78','+0,05 đến +1,51'],h:0.58,rule:true},
  {cells:['Phi-4','+0,69','+0,02 đến +1,40'],h:0.58}
],{align:['left','center','center'],fs:13});
addText('Cả bốn khoảng tin cậy đều nằm trên 0. Phi-Ground và Phi-4 nằm ngoài họ Qwen.',{x:M,y:4.75,w:8.9,h:0.65,fontSize:14.5,bold:true,color:FOOTB,align:'center',fit:'shrink'}); footB();

// Slide bổ sung 4 · Cấu hình huấn luyện
newSlide('Cấu hình huấn luyện'); slide.hidden = true;
table(M,1.0,[3.0,5.8],[{cells:['Hạng mục','Giá trị'],fill:FOOTB,color:WHITE,bold:true,h:0.44},{cells:['Backbone','Qwen2.5-VL-3B-Instruct'],h:0.48,rule:true},{cells:['Fine-tuning','QLoRA NF4 4-bit, rank 8, alpha 16, dropout 0,05'],h:0.48,rule:true},{cells:['SFT','2 epochs = 8.072 steps, batch hiệu dụng 16, LR 1e−4'],h:0.48,rule:true},{cells:['GRPO','8 câu/prompt, 500 bước cập nhật, LR 1e−5, KL β 0,04'],h:0.48,rule:true},{cells:['Phần cứng','1 × A100, vision tower không cập nhật tham số'],h:0.48}],{align:['left','left'],fs:12.7}); footB();

newSlide('Các hướng đã khảo sát'); slide.hidden = true;
table(M,1.05,[2.75,1.20,4.95],[
  {cells:['Hướng','Exec.','Điều rút ra'],fill:FOOTB,color:WHITE,bold:true,h:0.46,fs:12.3},
  {cells:['Mô tả phần tử trước câu','57,2','Khi biểu diễn trung gian sai, câu cuối bị ảnh hưởng mạnh.'],h:0.64,rule:true},
  {cells:['MIN-DESC','60,0','Mục tiêu ưu tiên có đóng góp riêng +0,63 điểm so với học thêm có giám sát.'],h:0.64,rule:true},
  {cells:['Phần thưởng tọa độ','60,1','Biểu diễn tọa độ tốt hơn nhưng thay đổi ở câu cuối nhỏ hơn.'],h:0.64,rule:true},
  {cells:['Chọn ứng viên','56,1','Khi thực sự chọn, chất lượng khá tốt. Vấn đề nằm ở quyết định từ chối chọn.'],h:0.64,rule:true},
  {cells:['TAGE','60,2','Bộ biên tập có ích khi vùng cắt đúng. Khâu chọn vùng còn là điểm cần cải thiện.'],h:0.64}
],{align:['left','center','left'],fs:12.1});
rect(M,5.35,8.9,0.78,LIGHT,{radius:0.05,line:FOOTD});
addText('Các hướng trung gian giúp xác định rằng tối ưu trực tiếp câu cuối phù hợp hơn với mục tiêu chính.',{x:M+0.20,y:5.35,w:8.50,h:0.78,fontSize:14.0,bold:true,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
footB();

pptx.writeFile({ fileName:path.join(__dirname, '..', 'LUAN_VAN_SLIDE_BAO_VE_CONCISE.pptx') });
