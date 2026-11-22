const pptxgen = require('pptxgenjs');
const path = require('path');

const pptx = new pptxgen();
pptx.defineLayout({ name: 'A43', width: 10, height: 7.5 });
pptx.layout = 'A43';
pptx.author = 'Le Doan Phuong Uyen';
pptx.subject = 'Bao cao tien do voi giao vien huong dan 11/2026';
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
  'Dữ liệu': { n: 2, label: 'Dữ liệu' },
  'Executability': { n: 3, label: 'Executability: chấm câu bằng việc làm theo' },
  'Phương pháp đề xuất': { n: 4, label: 'Phương pháp đề xuất' },
  'Kết quả chính': { n: 5, label: 'Kết quả chính' },
  'So sánh RL': { n: 6, label: 'So sánh các thuật toán RL và các phần thưởng' },
  'Kết luận': { n: 7, label: 'Việc tiếp theo và kết luận' }
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

// ===== Bổ sung cho deck trình thầy 15/11 =====
const fs = require('fs');
const FIG = path.join(__dirname, '..', '..', 'thesis', 'figures');
const HL = 'EDE7F6', OK = '2E7D4F', BAD = 'B23A3A';
const NOTES = [];
function note(t){ t=t.trim(); slide.addNotes(t); NOTES.push({page:PAGE+1, hidden:!!slide.hidden, t}); }
function img(file,x,y,w,h){ slide.addImage({path:file,x,y,w,h}); }
function imgFit(file,pw,ph,x,y,w,h){ const r=Math.min(w/pw,h/ph),ww=pw*r,hh=ph*r; img(file,x+(w-ww)/2,y+(h-hh)/2,ww,hh); }
function vn(v,sign=true){ const s=(Math.abs(v)<0.005?0:v).toFixed(2).replace('.',','); return (sign&&v>0.004?'+':'')+s.replace('-','−'); }
// Biểu đồ rừng: chấm = mức chênh, vạch ngang = KTC 95%
function forest(x,y,w,rows,o={}){
  const labelW=o.labelW||2.75, valW=o.valW||2.05, rowH=o.rowH||0.50;
  const px=x+labelW+0.10, pw=w-labelW-valW-0.20, min=o.min, max=o.max;
  const X=v=>px+pw*(v-min)/(max-min);
  const top=y, bottom=y+rows.length*rowH;
  for(let t=Math.ceil(min*2)/2;t<=max+1e-9;t+=0.5){
    line(X(t),top,0,bottom-top,t===0?FOOTB:'E4E1EA',t===0?1.5:0.75);
    addText(vn(t,true),{x:X(t)-0.3,y:bottom+0.04,w:0.6,h:0.24,fontSize:10.5,color:GREY,align:'center'});
  }
  addText(o.axis||'Δ exec so với S1 (điểm)',{x:px,y:bottom+0.28,w:pw,h:0.26,fontSize:11,color:GREY,align:'center'});
  addText('Δ [KTC 95%]',{x:x+w-valW,y:top-0.34,w:valW,h:0.28,fontSize:11,color:GREY,align:'right'});
  rows.forEach((r,i)=>{
    const yy=top+i*rowH, cy=yy+rowH/2, c=r.color||FOOTC;
    if(r.fill) rect(x,yy+0.03,w,rowH-0.06,r.fill);
    addText(r.label,{x:x+0.08,y:yy,w:labelW-0.08,h:rowH,fontSize:o.fs||13,bold:!!r.bold,italic:!!r.italic,color:r.italic?GREY:INK,valign:'mid',fit:'shrink'});
    line(X(r.lo),cy,X(r.hi)-X(r.lo),0,c,2.25);
    slide.addShape(pptx.ShapeType.ellipse,{x:X(r.d)-0.085,y:cy-0.085,w:0.17,h:0.17,fill:{color:c},line:{color:WHITE,width:1}});
    addText(`${vn(r.d)} [${vn(r.lo)}; ${vn(r.hi)}]`,{x:x+w-valW,y:yy,w:valW,h:rowH,fontSize:(o.fs||13)-1,bold:!!r.bold,color:r.italic?GREY:c,align:'right',valign:'mid'});
  });
}

// 1 · Bìa
newSlide();
rect(0,0,W,0.66,FOOTA);
addText('ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH  -  TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN',{x:0,y:0,w:W,h:0.66,fontSize:14,bold:true,color:WHITE,align:'center',valign:'mid'});
rect(0.8,1.18,W-1.6,2.5,FOOTB,{radius:0.08});
addText('BÁO CÁO TIẾN ĐỘ LUẬN VĂN THẠC SĨ',{x:0.8,y:1.45,w:W-1.6,h:0.35,fontSize:14,bold:true,color:WHITE,align:'center'});
addText('PHÁT SINH TỰ ĐỘNG HƯỚNG DẪN SỬ DỤNG PHẦN MỀM\nDỰA TRÊN LLM TỪ CÁC TRƯỜNG HỢP SỬ DỤNG\nVÀ GIAO DIỆN NGƯỜI DÙNG',{x:0.95,y:1.96,w:W-1.9,h:1.45,fontSize:21,bold:true,color:WHITE,align:'center',valign:'mid',fit:'shrink'});
addText('Học viên thực hiện: Lê Đoàn Phương Uyên',{x:0.8,y:4.55,w:W-1.6,h:0.4,fontSize:16,bold:true,align:'center'});
addText('Giáo viên hướng dẫn: TS. Nguyễn Hồng Bửu Long',{x:0.8,y:5.0,w:W-1.6,h:0.4,fontSize:16,bold:true,align:'center'});
addText('TP. Hồ Chí Minh - 11/2026',{x:0.8,y:5.88,w:W-1.6,h:0.35,fontSize:13,align:'center'});
note(`- Báo cáo hai phần.
- Phần một nhắc lại bài toán và cách chấm bằng executability, vì mọi phép so phía sau đều đọc bằng con số này.
- Phần hai là việc thầy giao ngày 1/11: so GRPO với các thuật toán RL khác, so SPICE với các độ đo thưởng khác, và giải thích vì sao.`);
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
addText('Đầu ra là câu hướng dẫn cho người dùng, không phải tọa độ để hệ thống tự thao tác.',{x:0.78,y:5.72,w:8.35,h:0.50,fontSize:14.2,color:GREY,fit:'shrink'});
note(`- Ví dụ đầu ra: "Tap Not now".
- Câu viết cho người đọc làm theo; mô hình không tự bấm thay người dùng.`);
foot();

// 3 · Yêu cầu
newSlide('Giới thiệu','Yêu cầu của câu hướng dẫn');
addText('Một câu tự nhiên vẫn có thể chưa đủ rõ để người dùng chọn đúng phần tử.',{x:M,y:0.96,w:8.9,h:0.50,fontSize:16.8,color:FOOTB,align:'center',fit:'shrink'});
table(0.92,1.68,[4.10,4.10],[
  {cells:['Câu mơ hồ','Câu đủ rõ'],fill:FOOTB,color:WHITE,bold:true,h:0.56,fs:14.0},
  {cells:[{t:'“Tap the button.”',italic:true,color:FOOTD},{t:'“Tap Not now.”',italic:true,color:FOOTC}],h:0.92,rule:true,fs:18.0},
  {cells:['Không biết cần chạm nút nào khi màn hình có nhiều nút.','Biết ngay phải chạm nút nào.'],h:1.06,fs:14.6}
],{align:['center','center'],fs:14.6});
line(0.92,4.76,8.20,0,RULE,1);
addText('Nghe tự nhiên thôi chưa đủ: câu phải giúp người đọc chọn đúng phần tử cần thao tác.',{x:1.08,y:5.12,w:7.84,h:0.78,fontSize:15.4,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
note(`- Màn hình có mười nút thì "Tap the button" đúng ngữ pháp mà không dùng được.
- Vì vậy cần một cách chấm kiểm được câu có giúp chọn đúng phần tử hay không. Đó là executability ở phần sau.`);
foot();

// 4 · AndroidControl
newSlide('Dữ liệu','AndroidControl');
addText('AndroidControl (Google DeepMind, NeurIPS 2024): người thật thao tác trên ứng dụng Android, mỗi bước kèm câu hướng dẫn do chính người thao tác viết.',{x:M,y:0.92,w:8.9,h:0.62,fontSize:15.4,color:FOOTB,align:'center',fit:'shrink'});
table(0.84,1.72,[2.00,2.00,2.00,2.16],[
  {cells:['Màn hình','Thao tác','Tọa độ chạm','Câu hướng dẫn'],fill:LIGHT,bold:true,h:0.58,fs:13.4},
  {cells:['Trạng thái giao diện','Loại thao tác thực hiện','Vị trí người dùng chạm','Do người thực hiện viết'],h:0.80,fs:12.8}
],{align:['center','center','center','center']});
table(1.12,3.40,[3.50,2.20,2.20],[
  {cells:['','Huấn luyện','Kiểm tra'],fill:FOOTB,color:WHITE,bold:true,h:0.50,fs:13.4},
  {cells:['Số bước','64.567','6.958'],h:0.50,rule:true,fs:14.0},
  {cells:['Bước có thao tác chạm','41.191',{t:'4.463',bold:true,color:FOOTB,fill:HL}],h:0.50,rule:true,fs:14.0},
  {cells:['Số tác vụ','12.895','1.432'],h:0.50,fs:14.0}
],{align:['left','center','center'],fs:14.0});
addText('Tách theo tác vụ: không tác vụ nào có mặt ở cả hai tập. Mọi số exec trong báo cáo tính trên 4.463 bước chạm của tập kiểm tra.',{x:1.12,y:5.62,w:7.90,h:0.62,fontSize:13.8,color:GREY,align:'center',fit:'shrink'});
note(`- Bộ gốc dùng câu hướng dẫn làm đầu vào để dự đoán thao tác; đề tài đi chiều ngược lại, câu là thứ cần sinh.
- Mỗi bước có toạ độ người dùng đã chạm thật, và executability chấm dựa trên toạ độ này.
- Mọi số exec hôm nay tính trên 4.463 bước chạm của tập kiểm tra.`);
foot();

// 5 · Executability: ý tưởng
newSlide('Executability','Ý tưởng');
addText('Thay vì hỏi “câu có giống câu chuẩn không”, executability hỏi “đọc câu xong, có bấm đúng nút không”.',{x:M,y:0.92,w:8.9,h:0.60,fontSize:16.6,bold:true,color:FOOTB,align:'center',fit:'shrink'});
box(0.45,1.92,1.95,1.25,'Câu do mô hình viết\n“Click on the\nBirthday option”',{fill:WHITE,line:FOOTD,fs:13});
line(2.48,2.55,0.42,0,FOOTC,2,true);
box(2.98,1.80,2.10,1.50,'Người làm theo\n(mô hình định vị UGround)',{bold:true,fill:LIGHT,line:FOOTB,fs:14});
line(5.16,2.55,0.42,0,FOOTC,2,true);
box(5.66,1.92,1.55,1.25,'Chạm vào\nmột điểm',{bold:true,fill:WHITE,line:FOOTD,fs:14});
line(7.29,2.55,0.42,0,FOOTC,2,true);
box(7.79,1.80,1.75,1.50,'So với chỗ người\ndùng thật đã chạm',{bold:true,fill:LIGHT,line:FOOTC,fs:13.4});
addText('Người làm theo chỉ nhận ảnh màn hình và câu. Không biết đáp án, không tham gia huấn luyện.',{x:2.80,y:3.36,w:4.6,h:0.5,fontSize:12,italic:true,color:GREY,align:'center',fit:'shrink'});
rect(0.95,4.20,8.10,1.35,HL,{radius:0.08});
addText([{text:'Executability',options:{bold:true,color:FOOTB}},{text:' = tỉ lệ số bước mà người làm theo chạm đúng phần tử, chỉ dựa vào câu do mô hình viết.',options:{color:INK}}],{x:1.20,y:4.20,w:7.60,h:1.35,fontSize:17,align:'center',valign:'mid',fit:'shrink'});
addText('BLEU, SPICE so chữ với câu chuẩn. Executability xem câu có đưa người đọc tới đúng chỗ hay không.',{x:M,y:5.85,w:8.9,h:0.50,fontSize:13.8,color:GREY,align:'center',fit:'shrink'});
note(`- Hình dung: đưa câu cho một người lạ không biết đáp án, chỉ nhìn màn hình và đọc câu, rồi xem họ bấm vào đâu. Bấm trúng chỗ người dùng thật đã bấm thì câu dùng được.
- Người lạ ở đây là UGround, một mô hình định vị giao diện có sẵn: nhận ảnh và câu, trả về một điểm trên màn hình.
- UGround không được huấn luyện cùng mô hình của đề tài và không biết đáp án.
- BLEU, SPICE so chữ với câu chuẩn; executability xem câu có đưa người đọc tới đúng chỗ không.`);
foot();

// 6 · Ví dụ thật
newSlide('Executability','Một ví dụ thật trong tập kiểm tra');
imgFit(path.join(FIG,'fig_voronoi.png'),1080,740,0.40,0.95,4.85,3.40);
addText('Câu chuẩn: “Click on the Birthday”',{x:5.45,y:1.00,w:4.15,h:0.42,fontSize:14,italic:true,color:GREY});
rect(5.45,1.55,4.15,1.45,'E8F3EC',{radius:0.06});
addText([{text:'S1 (sau tinh chỉnh)',options:{bold:true,color:OK,breakLine:true}},{text:'“Click on the Birthday option”',options:{italic:true,breakLine:true}},{text:'→ UGround chạm vào ô Birthday: ĐÚNG',options:{bold:true,color:OK}}],{x:5.62,y:1.55,w:3.85,h:1.45,fontSize:13.4,valign:'mid',fit:'shrink'});
rect(5.45,3.15,4.15,1.45,'F8E9E9',{radius:0.06});
addText([{text:'Mô hình gốc (chưa tinh chỉnh)',options:{bold:true,color:BAD,breakLine:true}},{text:'“Click on the "Gender" section to change it to "Male".”',options:{italic:true,breakLine:true}},{text:'→ UGround chạm vào ô Gender: SAI',options:{bold:true,color:BAD}}],{x:5.62,y:3.15,w:3.85,h:1.45,fontSize:13.4,valign:'mid',fit:'shrink'});
rect(0.55,4.90,8.90,1.25,LIGHT,{radius:0.06});
addText('Câu của mô hình gốc dài và đúng ngữ pháp nhưng gọi sai ô. Điểm chạm chỉ lệch một hàng (Gender nằm ngay trên Birthday) và bước này vẫn bị tính sai.',{x:0.80,y:4.90,w:8.40,h:1.25,fontSize:14.4,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
note(`- Màn hình thật trong tập kiểm tra. Người dùng chạm ô Birthday (vòng vàng).
- S1 viết "Click on the Birthday option"; UGround chạm đúng ô Birthday (vòng xanh), bước này đạt.
- Mô hình gốc viết "Click on the Gender section to change it to Male": câu dài, đúng ngữ pháp, nhưng gọi sai ô. UGround chạm ô Gender (dấu X đỏ), bước này không đạt.
- Hai ô chỉ cách nhau một hàng. Nếu chỉ đo khoảng cách, câu sai này vẫn có thể được tính đúng; slide sau nói cách loại.`);
foot();

// 7 · Ba điều kiện
newSlide('Executability','Một bước được tính đúng khi nào');
const cond=[
  ['1','Đúng loại thao tác','Bước cần chạm mà câu viết “Swipe up” hay “Go back” thì sai ngay, không cần xem điểm chạm.'],
  ['2','Chạm gần chỗ người dùng đã chạm','Điểm UGround chạm lệch không quá 14% bề ngang và 14% bề dọc màn hình so với điểm thật.'],
  ['3','Gần phần tử đúng hơn mọi phần tử khác','Điểm chạm phải gần điểm thật hơn mọi phần tử bấm được khác trên màn hình (vùng tô vàng trong ví dụ). Điều kiện này loại câu gọi nhầm nút bên cạnh.']
];
cond.forEach((c,i)=>{ const yy=1.00+i*1.32;
  slide.addShape(pptx.ShapeType.ellipse,{x:0.62,y:yy+0.22,w:0.62,h:0.62,fill:{color:FOOTB},line:{color:FOOTB}});
  addText(c[0],{x:0.62,y:yy+0.22,w:0.62,h:0.62,fontSize:20,bold:true,color:WHITE,align:'center',valign:'mid'});
  addText(c[1],{x:1.48,y:yy+0.05,w:7.9,h:0.42,fontSize:16.4,bold:true,color:FOOTB});
  addText(c[2],{x:1.48,y:yy+0.48,w:7.9,h:0.72,fontSize:14,color:INK,valign:'top',fit:'shrink'});
});
rect(0.95,5.12,8.10,1.10,HL,{radius:0.08});
addText([{text:'Executability = ',options:{bold:true,color:FOOTB}},{text:'số bước đạt cả 3 điều kiện  /  4.463 bước chạm',options:{color:INK}}],{x:1.1,y:5.12,w:7.8,h:1.10,fontSize:17,align:'center',valign:'mid',fit:'shrink'});
note(`- Ba điều kiện phải đạt cùng lúc.
- Một: đúng loại thao tác. Bước cần chạm mà câu bảo vuốt lên hay quay lại thì sai ngay.
- Hai: điểm chạm lệch không quá 14% chiều ngang và 14% chiều dọc màn hình so với điểm thật. Ngưỡng này lấy từ bộ AndroidInTheWild.
- Ba: điểm chạm gần điểm thật hơn mọi phần tử bấm được khác, tức nằm trong ô Voronoi (vùng tô vàng ở ví dụ trước). Điều kiện này loại câu gọi nhầm nút bên cạnh.`);
foot();

// 8 · Vì sao cần điều kiện 3
newSlide('Executability','Vì sao cần điều kiện thứ ba');
addText('Thử trên các điểm chạm giả lập: dịch điểm chạm sang phần tử bên cạnh, hoặc chỉ lệch nhẹ trong cùng phần tử.',{x:M,y:0.92,w:8.9,h:0.60,fontSize:15.2,color:FOOTB,align:'center',fit:'shrink'});
table(0.85,1.78,[3.70,2.20,2.40],[
  {cells:['Cách chấm','Lệch nhẹ, cùng phần tử\n(nên chấp nhận)','Sang phần tử bên cạnh\n(nên loại)'],fill:FOOTB,color:WHITE,bold:true,h:0.82,fs:12.6},
  {cells:['Chỉ điều kiện 2 (dung sai 14%)','100,0%',{t:'84,3% vẫn được chấp nhận',bold:true,color:BAD}],h:0.78,rule:true,fs:13.8},
  {cells:['Điều kiện 2 + 3 (executability)','99,7%',{t:'chỉ còn 2,8%',bold:true,color:OK,fill:HL}],h:0.78,fs:13.8}
],{align:['left','center','center'],fs:13.8});
rect(0.95,4.55,8.10,1.25,LIGHT,{radius:0.06});
addText('Chỉ đo khoảng cách thì câu gọi nhầm nút bên cạnh vẫn được điểm. Thêm điều kiện 3 loại gần hết các ca này mà vẫn giữ các ca chạm lệch nhẹ.',{x:1.15,y:4.55,w:7.70,h:1.25,fontSize:15,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
note(`- Phép thử: cố ý dịch điểm chạm, hoặc sang phần tử bên cạnh, hoặc lệch nhẹ trong cùng phần tử.
- Chỉ dùng dung sai 14% thì 84,3% ca dịch sang nút bên cạnh vẫn được chấp nhận, gần như không phân biệt nút đúng với nút kế bên.
- Thêm điều kiện ô Voronoi thì chỉ còn 2,8%, trong khi ca lệch nhẹ trong cùng phần tử vẫn giữ 99,7%.`);
foot();

// 9 · Đọc số exec: thang đo
newSlide('Executability','Đọc con số executability thế nào');
addText('Thang thực tế không phải 0 đến 100: đưa chính câu chuẩn cho UGround cũng chỉ đạt 75,7%, vì UGround đôi khi chạm lệch.',{x:M,y:0.90,w:8.9,h:0.62,fontSize:15.2,color:FOOTB,align:'center',fit:'shrink'});
const RX=0.75, RW=8.5, RY=3.30, X100=v=>RX+RW*v/80;
rect(RX,RY-0.07,RW,0.14,'E4E1EA',{radius:0.04});
rect(X100(12),RY-0.07,X100(75.7)-X100(12),0.14,'C9C0DD');
[0,20,40,60,80].forEach(t=>{ line(X100(t),RY+0.10,0,0.10,GREY,0.75); addText(String(t),{x:X100(t)-0.3,y:RY+0.22,w:0.6,h:0.25,fontSize:10.5,color:GREY,align:'center'}); });
const marks=[
  {v:6.1,t:'6,1\ncâu thật nhưng\nsai màn hình',up:false,c:FOOTD},
  {v:12.0,t:'12,0\n“Tap the button.”\ncho mọi bước',up:true,c:FOOTD},
  {v:47.6,t:'47,6\nmô hình gốc 3B',up:true,c:FOOTC},
  {v:59.1,t:'59,1\nS1',up:false,c:FOOTC},
  {v:60.7,t:'60,7\nGRPO-SPICE',up:true,c:FOOTB},
  {v:61.2,t:'61,2\nSA-SPICE-v3',up:false,c:FOOTB,dx:0.55},
  {v:75.7,t:'75,7\ncâu chuẩn',up:true,c:OK}
];
marks.forEach(m=>{ const x=X100(m.v);
  slide.addShape(pptx.ShapeType.ellipse,{x:x-0.08,y:RY-0.08,w:0.16,h:0.16,fill:{color:m.c},line:{color:WHITE,width:1}});
  const dx=m.dx||0;
  if(m.up){ line(x,RY-0.62,0,0.52,m.c,1); addText(m.t,{x:x-0.85+dx,y:RY-1.48,w:1.7,h:0.86,fontSize:11.5,bold:true,color:m.c,align:'center',valign:'bottom'}); }
  else { line(x,RY+0.48,0,0.30,m.c,1); addText(m.t,{x:x-0.85+dx,y:RY+0.80,w:1.7,h:0.86,fontSize:11.5,bold:true,color:m.c,align:'center',valign:'top'}); }
});
rect(0.95,5.10,8.10,1.12,HL,{radius:0.08});
addText('Khoảng dùng được là từ khoảng 12 (câu không chỉ ra phần tử nào) tới 75,7 (câu chuẩn). Tinh chỉnh đưa mô hình từ 47,6 lên 59,1; học tăng cường đưa tiếp lên 60,7 và 61,2.',{x:1.15,y:5.10,w:7.70,h:1.12,fontSize:14.2,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
addText('Hai mốc thấp (6,1 và 12,0) đo trên 800 bước của tập kiểm tra, các mốc còn lại trên đủ 4.463 bước.',{x:M,y:6.42,w:8.9,h:0.32,fontSize:10.5,italic:true,color:GREY,align:'center'});
note(`- Trần không phải 100: đưa câu chuẩn cho UGround cũng chỉ đạt 75,7%, vì UGround đôi khi chạm lệch. Đây là giới hạn của dụng cụ đo.
- Sàn không phải 0: "Tap the button" cho mọi bước vẫn đạt 12%. Câu thật nhưng lấy từ màn hình khác chỉ đạt 6,1%, thấp hơn cả sàn, nghĩa là UGround đọc nội dung câu chứ không chấm văn phong.
- Mô hình gốc 47,6, S1 59,1, GRPO-SPICE 60,7, SA-SPICE-v3 61,2. Sau tinh chỉnh các mức chênh chỉ 1 đến 2 điểm nên phép so nào cũng kèm khoảng tin cậy.`);
foot();

// 10 · Độ tin cậy
newSlide('Executability','Executability có đáng tin không');
table(0.62,0.98,[3.30,5.46],[
  {cells:['Phép kiểm','Kết quả'],fill:FOOTB,color:WHITE,bold:true,h:0.50,fs:13.4},
  {cells:[{t:'Câu càng thiếu thông tin, điểm càng thấp',bold:true},'Trên cùng 800 bước: câu chuẩn 74,9, “Tap the button.” 12,0, câu lấy từ màn hình khác 6,1'],h:0.86,rule:true,fs:13.2},
  {cells:[{t:'Bỏ tên phần tử khỏi câu chuẩn',bold:true},'Mất 28,5 điểm trên các bước bị tác động; bỏ mô tả vị trí chỉ mất 3,5 điểm'],h:0.86,rule:true,fs:13.2},
  {cells:[{t:'Đổi người làm theo',bold:true},'GRPO-SPICE vẫn cao hơn S1 dưới cả bốn mô hình định vị: UGround, UI-Venus, Phi-Ground, Phi-4'],h:0.86,rule:true,fs:13.2},
  {cells:[{t:'Chấm lại cùng câu',bold:true},'Kết quả tất định: 0 bất đồng trên 1.625 lần chấm lại'],h:0.70,fs:13.2}
],{align:['left','left'],fs:13.2});
addText('Điểm đi theo nội dung câu, nhất là tên phần tử, và thứ tự các mô hình giữ nguyên khi đổi mô hình định vị.',{x:0.85,y:5.18,w:8.30,h:0.80,fontSize:14.6,bold:true,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
note(`- Bỏ tên phần tử khỏi câu chuẩn thì mất 28,5 điểm trên các bước bị tác động, bỏ mô tả vị trí chỉ mất 3,5: thước thưởng việc gọi đúng tên phần tử.
- Đổi người làm theo sang ba mô hình định vị khác, phương pháp vẫn cao hơn S1. Phi-Ground và Phi-4 không thuộc họ Qwen.
- Chấm lại cùng câu cho đúng cùng kết quả.`);
foot();

// 11 · Quy trình
newSlide('Phương pháp đề xuất','Quy trình tổng thể');
box(0.45,1.18,1.72,1.28,'Baseline S1\n3B sau tinh chỉnh\ncó giám sát',{bold:true,line:FOOTD,fs:12.9});
line(2.17,1.80,0.12,0,FOOTC,2,true);
box(2.32,1.25,2.08,1.10,'GRPO-SPICE\nsinh câu ban đầu',{bold:true,fill:LIGHT,line:FOOTB,fs:15});
line(4.42,1.80,0.42,0,FOOTC,2,true);
box(4.90,1.25,2.08,1.10,'ACE\nhiệu chỉnh có chọn lọc',{bold:true,fill:LIGHT,line:FOOTC,fs:15});
line(7.00,1.80,0.42,0,FOOTC,2,true);
box(7.48,1.25,1.98,1.10,'Câu hướng dẫn\ncuối',{bold:true,fill:WHITE,line:FOOTD,fs:14});
addText('GRPO-SPICE',{x:M,y:3.42,w:2.15,h:0.40,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Sinh 8 câu cho cùng đầu vào.','Thưởng = SPICE so với câu chuẩn, trừ phạt độ dài.'],M,3.92,4.15,{gap:0.76,fs:15.2,h:0.62});
addText('ACE',{x:5.05,y:3.42,w:1.2,h:0.40,fontSize:SECTION_FS,bold:true,color:FOOTB});
bullets(['Tìm 4 câu ví dụ giống nhất trong tập huấn luyện.','Chỉ thay câu ban đầu khi qua 2 điều kiện chọn lọc.'],5.05,3.92,4.35,{gap:0.76,fs:15.2,h:0.62});
addText('Mô hình định vị chỉ dùng để chấm: không tham gia sinh câu và không nằm trong phần thưởng.',{x:M,y:5.82,w:8.9,h:0.48,fontSize:14.2,color:FOOTB,align:'center',fit:'shrink'});
note(`- Xuất phát từ S1: Qwen2.5-VL-3B đã tinh chỉnh có giám sát.
- Thành phần một: học tăng cường bằng GRPO, thưởng SPICE.
- Thành phần hai: ACE tra bốn câu ví dụ giống nhất trong tập huấn luyện và chỉ thay câu khi đạt hai điều kiện.
- UGround không nằm trong phần thưởng, nên thước chấm độc lập với mục tiêu huấn luyện.`);
foot();

// 12 · GRPO-SPICE
newSlide('Phương pháp đề xuất','Thành phần thứ nhất: GRPO-SPICE');
box(0.60,1.85,1.55,0.92,'Một mẫu huấn luyện',{bold:true,fill:LIGHT,line:FOOTD});
line(2.28,2.31,0.42,0,FOOTC,2,true);
box(2.82,1.66,1.75,1.30,'8 câu\nhướng dẫn',{bold:true,fill:LIGHT,line:FOOTB});
line(4.70,2.31,0.42,0,FOOTC,2,true);
box(5.24,1.66,1.80,1.30,'SPICE\n− phạt độ dài',{bold:true,fill:LIGHT,line:FOOTC,fs:15});
line(7.17,2.31,0.42,0,FOOTC,2,true);
box(7.71,1.60,1.70,1.42,'Câu hơn trung bình\nnhóm thì được\nkhuyến khích',{bold:true,fill:LIGHT,line:FOOTD,fs:12.6});
rect(M,3.65,8.9,1.72,LIGHT,{line:FOOTD});
addText('Vì sao SPICE',{x:M+0.22,y:3.90,w:2.15,h:0.35,fontSize:15.5,bold:true,color:FOOTB});
addText('SPICE so câu theo đối tượng, thuộc tính, quan hệ thay vì từng chữ. Hai câu cùng nói về một nút vẫn được điểm cao dù khác cách viết.',{x:M+2.12,y:3.72,w:6.50,h:1.48,fontSize:15.2,valign:'mid',fit:'shrink'});
addText('Tiền lệ: SCST (CVPR 2017) và SPIDEr (ICCV 2017) trong sinh chú thích ảnh.',{x:M,y:5.80,w:8.9,h:0.45,fontSize:14,color:GREY,align:'center'});
note(`- Mỗi mẫu, mô hình viết tám câu; mỗi câu được chấm SPICE so với câu chuẩn, trừ phạt độ dài.
- Câu có điểm cao hơn trung bình nhóm thì được tăng xác suất, thấp hơn thì bị giảm. Mốc so là trung bình của chính nhóm, nên không cần mô hình giá trị riêng.
- Phạt KL giữ mô hình không đi quá xa S1.
- SPICE chấm theo đối tượng và quan hệ, hợp với việc gọi đúng phần tử. Dùng độ đo làm phần thưởng đã có từ SCST và SPIDEr.`);
foot();

// 13 · ACE
newSlide('Phương pháp đề xuất','Thành phần thứ hai: ACE');
box(0.45,1.25,1.65,0.95,'Câu ban đầu',{bold:true,fill:WHITE,line:FOOTD,fs:14.5});
line(2.20,1.73,0.38,0,FOOTC,2,true);
box(2.68,1.15,1.90,1.15,'Tìm 4 câu ví dụ\ntừ tập huấn luyện',{bold:true,fill:LIGHT,line:FOOTB,fs:13.2});
line(4.68,1.73,0.38,0,FOOTC,2,true);
box(5.16,1.15,1.55,1.15,'Sinh câu\nứng viên',{bold:true,fill:LIGHT,line:FOOTC,fs:14});
line(6.81,1.73,0.38,0,FOOTC,2,true);
box(7.29,1.05,2.20,1.35,'Kiểm tra\n2 điều kiện chọn lọc',{bold:true,fill:LIGHT,line:FOOTD,fs:14});
rect(M,3.42,4.20,1.18,LIGHT,{line:FOOTC});
addText('1 · Câu ứng viên trùng nguyên văn một trong bốn câu ví dụ.',{x:M+0.18,y:3.42,w:3.84,h:1.18,fontSize:14.0,align:'center',valign:'mid',fit:'shrink'});
rect(5.25,3.42,4.20,1.18,LIGHT,{line:FOOTC});
addText('2 · Cùng loại thao tác với câu ban đầu.',{x:5.43,y:3.42,w:3.84,h:1.18,fontSize:14.0,align:'center',valign:'mid',fit:'shrink'});
box(1.80,5.10,2.80,0.82,'Đủ điều kiện → dùng câu mới',{bold:true,fill:LIGHT,line:FOOTC,fs:14});
box(5.40,5.10,2.80,0.82,'Không đủ → giữ câu ban đầu',{bold:true,fill:WHITE,line:FOOTD,fs:14});
note(`- Nhiều tác vụ lặp lại với khác biệt nhỏ, nên câu chuẩn của một bước cũ đôi khi dùng lại được nguyên văn.
- ACE cho bộ sinh xem câu của bốn bước giống nhất, và chỉ thay câu ban đầu khi câu mới trùng nguyên văn một câu ví dụ và cùng loại thao tác.
- Phần lớn các bước giữ câu ban đầu.`);
foot();

// 14 · Kết quả chính
newSlide('Kết quả chính','Kết quả trên tập kiểm tra');
addText('GRPO-SPICE cao hơn S1 trên cả ba tiêu chí vị trí và các độ đo văn bản.',{x:M,y:0.93,w:8.9,h:0.48,fontSize:16.2,color:FOOTB,align:'center'});
table(0.64,1.52,[2.02,1.55,1.38,1.38,1.05,1.34],[
  {cells:['Mô hình','Executability','Hộp phần tử','AitW đầy đủ','SPICE','CIDEr-D'],fill:FOOTB,color:WHITE,bold:true,h:0.62,fs:11.8},
  {cells:['Mô hình gốc 3B','47,59','53,60','63,39','18,48','88,01'],h:0.60,rule:true},
  {cells:['Baseline S1','59,11','65,49','74,37','44,37','416,12'],h:0.60,rule:true},
  {cells:['GRPO-SPICE',{t:'60,65',bold:true,color:FOOTB,fill:HL},{t:'67,02',bold:true,color:FOOTB,fill:HL},{t:'76,25',bold:true,color:FOOTB,fill:HL},{t:'45,79',bold:true,color:FOOTB,fill:HL},{t:'430,05',bold:true,color:FOOTB,fill:HL}],h:0.60,rule:true},
  {cells:['GRPO-SPICE + ACE','60,68','67,11','76,32','47,13','442,02'],h:0.60}
],{align:['left','center','center','center','center','center'],fs:13.4});
metricBadge(1.08,4.72,2.30,'+1,55','exec so với S1\nKTC 95% [+0,80; +2,33]',FOOTC);
metricBadge(3.85,4.72,2.30,'+1,52','hộp phần tử so với S1',FOOTC);
metricBadge(6.62,4.72,2.30,'+1,88','AitW đầy đủ so với S1',FOOTC);
addText('Hộp phần tử: điểm chạm nằm trong khung của phần tử đúng (tiêu chí gốc của AndroidControl). AitW đầy đủ: tiêu chí của bộ AndroidInTheWild.',{x:M,y:6.18,w:8.9,h:0.42,fontSize:11,italic:true,color:GREY,align:'center',fit:'shrink'});
note(`- GRPO-SPICE đạt 60,65, hơn S1 1,55 điểm; khoảng tin cậy 95% từ 0,80 đến 2,33, không chứa 0.
- Hai tiêu chí vị trí khác (hộp phần tử của AndroidControl, AitW đầy đủ) cũng tăng cỡ đó.
- Thêm ACE thì exec giữ nguyên, các độ đo văn bản tăng thêm.`);
foot();

// 15 · Bốn người làm theo
newSlide('Kết quả chính','Đổi người làm theo, kết quả giữ chiều');
addText('Chấm lại cùng câu bằng bốn mô hình định vị khác nhau.',{x:M,y:0.90,w:8.9,h:0.52,fontSize:15.6,color:FOOTB,align:'center',fit:'shrink'});
table(0.58,1.48,[2.18,1.55,1.55,1.55,1.55],[
  {cells:['Mô hình','UGround','UI-Venus','Phi-Ground','Phi-4'],fill:FOOTB,color:WHITE,bold:true,h:0.54,fs:12.3},
  {cells:['Baseline S1','59,11','54,51','46,96','44,63'],h:0.60,rule:true,fs:12.8},
  {cells:['GRPO-SPICE','60,65','56,06','47,75','45,33'],h:0.60,rule:true,fs:12.8},
  {cells:['Δ GRPO-SPICE − S1',{t:'+1,55',bold:true,color:FOOTC,fill:HL},{t:'+1,55',bold:true,color:FOOTC,fill:HL},{t:'+0,78',bold:true,color:FOOTC,fill:HL},{t:'+0,69',bold:true,color:FOOTC,fill:HL}],h:0.64,fs:12.6}
],{align:['left','center','center','center','center'],fs:12.7});
addText('Cả bốn khoảng tin cậy đều nằm trên 0. Phi-Ground và Phi-4 không thuộc họ Qwen, và mức tăng vẫn giữ chiều khi người làm theo khác họ với mô hình được chấm.',{x:0.85,y:4.20,w:8.30,h:0.90,fontSize:14.4,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
note(`- Chấm lại cùng các câu bằng ba mô hình định vị khác.
- Mức tuyệt đối khác nhau vì mỗi mô hình định vị mạnh yếu khác nhau.
- GRPO-SPICE luôn cao hơn S1 và cả bốn khoảng tin cậy đều trên 0.`);
foot();

// 16 · Thiết kế lưới
newSlide('So sánh RL','Thiết kế phép so');
addText('Yêu cầu ngày 1/11: so với các thuật toán RL khác và so SPICE với các độ đo thưởng khác, kèm giải thích.',{x:M,y:0.92,w:8.9,h:0.56,fontSize:15.2,color:FOOTB,align:'center',fit:'shrink'});
rect(M,1.70,4.30,2.55,LIGHT,{radius:0.08});
addText('Lưới 1 · đổi thuật toán',{x:M+0.2,y:1.80,w:3.9,h:0.40,fontSize:15.6,bold:true,color:FOOTB});
addText('Giữ thưởng SPICE, chỉ đổi thuật toán: GRPO, Dr.GRPO, SCST, REINFORCE, RLOO và PPO (hai mức λ của GAE).',{x:M+0.2,y:2.25,w:3.9,h:1.85,fontSize:14,valign:'top',fit:'shrink'});
rect(5.15,1.70,4.30,2.55,LIGHT,{radius:0.08});
addText('Lưới 2 · đổi phần thưởng',{x:5.35,y:1.80,w:3.9,h:0.40,fontSize:15.6,bold:true,color:FOOTB});
addText('Giữ GRPO, chỉ đổi phần thưởng: SPICE, ROUGE-L, METEOR, CIDEr-D. Từ SFT tiếp thêm SPICE thuần và SA-SPICE-v3 (SPICE trộn chrF, cộng điểm khi đúng loại thao tác).',{x:5.35,y:2.25,w:3.9,h:1.85,fontSize:14,valign:'top',fit:'shrink'});
addText('Giữ cố định',{x:M,y:4.45,w:3,h:0.36,fontSize:15,bold:true,color:FOOTB});
addText('Cùng điểm xuất phát S1, cùng 1.000 câu nhắc, 8 câu cho mỗi câu nhắc, cùng tốc độ học, phạt KL và seed.',{x:M,y:4.82,w:8.9,h:0.40,fontSize:13.6,fit:'shrink'});
addText('Ba mốc để đọc',{x:M,y:5.32,w:3,h:0.36,fontSize:15,bold:true,color:FOOTB});
addText('SFT tiếp: học thêm có giám sát trên cùng câu nhắc, không dùng RL.\nSPICE ghép ngẫu nhiên: phần thưởng không mang thông tin.\nGRPO chạy lại (A/A): cùng cấu hình, cho biết hai lần chạy lệch nhau bao nhiêu.',{x:M,y:5.69,w:8.9,h:0.80,fontSize:13.2,fit:'shrink'});
note(`- Hai lưới, mỗi lưới chỉ đổi một yếu tố.
- Lưới 1 giữ thưởng SPICE, đổi thuật toán. SCST là mốc kinh điển của bài toán chú thích ảnh.
- Lưới 2 giữ GRPO, đổi phần thưởng.
- Ba mốc đọc kèm: SFT tiếp tách công của RL khỏi công của việc học thêm; SPICE ghép ngẫu nhiên là thưởng không mang thông tin; GRPO chạy lại cho biết hai lần chạy cùng cấu hình lệch nhau bao nhiêu.`);
foot();

// 17 · Lưới thuật toán
newSlide('So sánh RL','Lưới 1: các thuật toán RL (cùng thưởng SPICE)');
addText('Chấm là mức chênh exec so với S1, vạch ngang là khoảng tin cậy 95%. Vạch nằm hẳn bên phải 0 là hơn S1 có ý nghĩa.',{x:0.55,y:0.68,w:6.6,h:0.30,fontSize:11,italic:true,color:GREY,fit:'shrink'});
forest(0.50,1.32,9.0,[
  {label:'GRPO (lượt chính)',d:1.55,lo:0.80,hi:2.33,color:FOOTB,bold:true},
  {label:'SCST',d:1.43,lo:0.79,hi:2.10},
  {label:'PPO, λ = 1',d:0.96,lo:0.19,hi:1.73},
  {label:'REINFORCE',d:0.90,lo:0.20,hi:1.60},
  {label:'Dr.GRPO',d:0.90,lo:0.26,hi:1.54},
  {label:'PPO, λ = 0,95',d:0.87,lo:0.02,hi:1.73},
  {label:'GRPO chạy lại (A/A)',d:0.63,lo:-0.11,hi:1.38},
  {label:'RLOO',d:0.34,lo:-0.33,hi:1.00},
  {label:'SFT tiếp (không RL)',d:1.05,lo:0.47,hi:1.64,color:FOOTD,italic:true,fill:'F6F5F8'}
],{min:-0.5,max:2.5,rowH:0.42,labelW:2.45,valW:2.10});
rect(0.70,5.85,8.60,0.88,HL,{radius:0.08});
addText('Mọi thuật toán đều hơn S1 từ 0,3 đến 1,6 điểm và các khoảng tin cậy chồng lên nhau. Hai lần chạy GRPO cùng cấu hình đã lệch nhau 0,92 điểm, bằng cỡ khoảng cách giữa các thuật toán.',{x:0.90,y:5.85,w:8.20,h:0.88,fontSize:13.4,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
note(`- Mỗi chấm là mức chênh exec so với S1, vạch ngang là khoảng tin cậy 95%. Chấm bên phải vạch 0 là hơn S1.
- Mọi thuật toán hơn S1 từ 0,3 đến 1,6 điểm; sáu trong tám lượt có khoảng tin cậy nằm hẳn trên 0.
- Các khoảng chồng lên nhau nhiều nên chưa kết luận được thuật toán nào hơn hẳn. GRPO và SCST nhỉnh nhất, RLOO thấp nhất.
- Chạy lại GRPO đúng cấu hình cũ chỉ được 0,63, lệch lượt chính 0,92: dao động giữa hai lần chạy đã cỡ khoảng cách giữa các thuật toán.
- Dr.GRPO (bỏ chia độ lệch chuẩn và bỏ chuẩn hoá theo độ dài) đạt 60,00: thấp hơn GRPO lượt chính 0,65 [0,19; 1,12], p = 0,009, ngang GRPO chạy lại cùng mã (+0,27, chưa có ý nghĩa). Bỏ hai phép chuẩn hoá không giúp gì ở bài này.
- SFT tiếp, không có RL, cũng hơn S1 1,05. Một phần mức tăng đến từ việc học thêm trên các câu nhắc này.`);
foot();

// 18 · Lưới thưởng
newSlide('So sánh RL','Lưới 2: các phần thưởng (cùng thuật toán GRPO)');
addText('Chấm là mức chênh exec so với S1, vạch ngang là khoảng tin cậy 95%. Vạch nằm hẳn bên phải 0 là hơn S1 có ý nghĩa.',{x:0.55,y:0.68,w:6.6,h:0.30,fontSize:11,italic:true,color:GREY,fit:'shrink'});
forest(0.50,1.32,9.0,[
  {label:'SA-SPICE-v3 *',d:2.11,lo:1.33,hi:2.89,color:FOOTB,bold:true},
  {label:'SPICE thuần *',d:1.77,lo:1.13,hi:2.44},
  {label:'SPICE (lượt chính)',d:1.55,lo:0.80,hi:2.33,color:FOOTB},
  {label:'ROUGE-L',d:1.52,lo:0.75,hi:2.29},
  {label:'METEOR',d:1.17,lo:0.39,hi:1.96},
  {label:'CIDEr-D',d:1.17,lo:0.41,hi:1.92},
  {label:'SPICE chạy lại (A/A)',d:0.63,lo:-0.11,hi:1.38},
  {label:'SPICE ghép ngẫu nhiên',d:0.00,lo:-0.41,hi:0.42,color:BAD,italic:true,fill:'F6F5F8'}
],{min:-0.5,max:3.0,rowH:0.44,labelW:2.45,valW:2.10});
addText('* xuất phát từ SFT tiếp thay vì S1. So với SFT tiếp: SA-SPICE-v3 +1,05 [+0,46; +1,65], SPICE thuần +0,72 [+0,24; +1,20].',{x:0.60,y:5.50,w:8.8,h:0.30,fontSize:11,italic:true,color:GREY});
rect(0.70,5.88,8.60,0.86,HL,{radius:0.08});
addText('Thưởng ngẫu nhiên cho đúng 0, thưởng thật cho từ +0,6 đến +2,1, nên mức tăng đến từ nội dung phần thưởng. Giữa SPICE, ROUGE-L, METEOR và CIDEr-D chưa tách được bên nào hơn.',{x:0.90,y:5.88,w:8.20,h:0.86,fontSize:13.2,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
note(`- Hàng quan trọng nhất là hàng cuối: ghép điểm SPICE ngẫu nhiên giữa các câu thì kết quả đúng bằng S1, chênh 0,00. Mức tăng đến từ nội dung phần thưởng, không phải từ việc chạy vòng lặp RL.
- SPICE, ROUGE-L, METEOR, CIDEr-D có khoảng tin cậy chồng nhau, chưa tách được bên nào hơn. Không viết "SPICE tốt nhất".
- SA-SPICE-v3 cao nhất, +2,11 so với S1, nhưng xuất phát từ SFT tiếp. So công bằng với SFT tiếp thì hơn 1,05, có ý nghĩa; slide 21 nói kỹ.
- SPICE thuần từ cùng điểm xuất phát: +1,77 so với S1, +0,72 so với SFT tiếp, cũng có ý nghĩa.`);
foot();

// Chờ số (ẩn) · điền khi có số test đợt B5, rồi chép vào slide 17/18 và bỏ ẩn hoặc xoá
function choSo(title, intro, head, rows, ghichu){
  newSlide(title); slide.hidden = true;
  addText(intro,{x:M,y:0.80,w:8.9,h:0.56,fontSize:14,color:FOOTB,align:'center',fit:'shrink'});
  const R=[{cells:head,fill:FOOTB,color:WHITE,bold:true,h:0.52,fs:12.8}];
  rows.forEach((r,i)=>R.push({cells:[{t:r[0],bold:true},r[1],{t:'[chờ số]',color:GREY,italic:true},{t:'[chờ số]',color:GREY,italic:true}],h:0.56,rule:i<rows.length-1,fs:13.2}));
  table(0.60,1.55,[3.60,1.60,1.40,2.20],R,{align:['left','center','center','center'],fs:13.2});
  addText(ghichu,{x:M,y:5.70,w:8.9,h:0.70,fontSize:12.5,italic:true,color:GREY,align:'center',valign:'mid',fit:'shrink'});
}
choSo('Chờ số · Lưới 1: các thuật toán RL thêm ở đợt B5',
  'Cùng cấu hình lưới: từ S1, thưởng SPICE, 1.000 câu nhắc, 8 câu mỗi câu nhắc, seed 101.',
  ['Thuật toán','Đã train','exec','Δ so với S1 [KTC 95%]'],
  [['DPO trực tuyến (câu tốt nhất và kém nhất trong nhóm 8)','500/500'],['DAPO','400/500'],['GSPO','750/1.000'],['GRPO μ=2','750/1.000'],['REINFORCE++ (lô 64)','70/125']],
  'Test chạy sau 28/11. Có số thì thêm hàng vào biểu đồ slide 17.');
note(`- Slide chờ số, đang ẩn. Điền exec và Δ so với S1 khi có số test, rồi chép vào biểu đồ slide 17.`);
footB();
choSo('Chờ số · Lưới 2: các phần thưởng thêm ở đợt B5',
  'Cùng cấu hình lưới: GRPO từ S1, 1.000 câu nhắc, 8 câu mỗi câu nhắc, seed 101; chỉ đổi phần thưởng.',
  ['Phần thưởng','Đã train','exec','Δ so với S1 [KTC 95%]'],
  [['chrF','500/500'],['BLEU-4','500/500'],['SPIDEr','500/500'],['BERTScore','500/500']],
  'Test chạy sau 28/11. Có số thì thêm hàng vào biểu đồ slide 18 và bảng độ đo văn bản ở slide 20; đọc kèm bước không chạm.');
note(`- Slide chờ số, đang ẩn. Điền exec và Δ so với S1 khi có số test, rồi chép vào biểu đồ slide 18 và bảng slide 20.
- Lượt chrF có KL lúc train cao hơn hẳn các lượt khác, nên đọc kèm bước không chạm.`);
footB();

// 19 · Phân rã
newSlide('So sánh RL','Vì sao các phần thưởng cho exec gần nhau');
addText('Số bước sửa được so với S1 (bước cứu được trừ bước làm hỏng), tách theo loại lỗi được sửa.',{x:M,y:0.90,w:8.9,h:0.46,fontSize:15,color:FOOTB,align:'center',fit:'shrink'});
const pr=[['SPICE (lượt chính)',28,41],['SCST + SPICE',33,31],['ROUGE-L',48,20],['METEOR',31,21],['CIDEr-D',34,18],['SPICE ghép ngẫu nhiên',-3,3]];
const BX=2.95, BS=0.050, B2=3.45;
addText('sửa loại thao tác',{x:BX,y:1.46,w:3.0,h:0.30,fontSize:12.5,bold:true,color:FOOTC});
addText('sửa phần tử được chọn',{x:BX+B2,y:1.46,w:3.2,h:0.30,fontSize:12.5,bold:true,color:FOOTB});
pr.forEach((r,i)=>{ const yy=1.86+i*0.56;
  addText(r[0],{x:0.55,y:yy,w:2.35,h:0.44,fontSize:13.4,bold:i===0,valign:'mid',color:i===5?GREY:INK,italic:i===5});
  const a=r[1], b=r[2];
  rect(BX,yy+0.08,Math.max(0.04,Math.abs(a)*BS),0.30,i===5?'C9C4D4':FOOTC);
  addText((a>0?'+':'−')+Math.abs(a),{x:BX+Math.abs(a)*BS+0.06,y:yy,w:0.6,h:0.44,fontSize:12.5,bold:true,color:FOOTC,valign:'mid'});
  rect(BX+B2,yy+0.08,Math.max(0.04,b*BS),0.30,i===5?'C9C4D4':FOOTB);
  addText('+'+b,{x:BX+B2+b*BS+0.06,y:yy,w:0.6,h:0.44,fontSize:12.5,bold:true,color:FOOTB,valign:'mid'});
});
rect(0.70,5.38,8.60,1.30,HL,{radius:0.08});
addText('Các phần thưởng tới mức exec gần nhau theo hai đường: ROUGE-L chủ yếu sửa loại thao tác, SPICE sửa phần tử nhiều hơn. Đây mới là dấu hiệu, vì so từng cặp không còn ý nghĩa sau hiệu chỉnh Holm và mới có một seed.',{x:0.90,y:5.38,w:8.20,h:1.30,fontSize:13.4,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
note(`- Tách số bước sửa được so với S1 làm hai phần: bước S1 sai loại thao tác mà lượt mới sửa đúng, và bước đúng loại thao tác mà lượt mới chọn đúng phần tử hơn.
- Thưởng thật đều sửa được loại thao tác; thưởng ngẫu nhiên gần như không sửa gì.
- ROUGE-L sửa loại thao tác nhiều nhất (48 bước) nhưng phần tử chỉ 20. SPICE sửa phần tử 41 bước, nhiều nhất. Hai phần bù nhau nên tổng exec gần bằng.
- Mới là dấu hiệu: so từng cặp không còn ý nghĩa sau hiệu chỉnh Holm, và mới một seed. Không viết "SPICE giúp định vị tốt hơn".`);
foot();

// 20 · Độ đo văn bản
newSlide('So sánh RL','Độ đo văn bản: không phần thưởng nào thắng mọi cột');
const T=(t,b)=>b?{t,bold:true,color:FOOTB,fill:HL}:t;
table(0.45,1.00,[2.40,1.12,1.12,1.12,1.12,1.10,1.12],[
  {cells:['Phần thưởng','BLEU-4','METEOR','ROUGE-L','CIDEr-D','SPICE','chrF'],fill:FOOTB,color:WHITE,bold:true,h:0.46,fs:12.4},
  {cells:['SPICE (lượt chính)','52,36','37,92','68,36','430,05','45,79','62,87'],h:0.41,rule:true},
  {cells:['SPICE chạy lại (A/A)',T('52,97',1),'37,55','68,44','430,92','46,00','62,39'],h:0.41,rule:true},
  {cells:['Dr.GRPO + SPICE','52,10','37,66','68,24','428,84','45,60','62,56'],h:0.41,rule:true},
  {cells:['ROUGE-L','52,59','38,20','69,27','432,81','45,57','63,42'],h:0.41,rule:true},
  {cells:['METEOR','50,76','38,63','69,14','426,61','45,13','64,19'],h:0.41,rule:true},
  {cells:['CIDEr-D','51,59','37,78','68,47','424,52','44,43','62,90'],h:0.41,rule:true},
  {cells:['SA-SPICE-v3 *','51,24',T('38,90',1),'69,31','429,12','45,76',T('64,40',1)],h:0.41,rule:true},
  {cells:['SPICE thuần *','52,59','38,74',T('69,51',1),T('436,26',1),T('46,41',1),'64,07'],h:0.41,rule:true},
  {cells:[{t:'SFT tiếp (không RL)',italic:true,color:GREY},'52,07','37,75','68,55','425,79','45,33','62,64'],h:0.40,rule:true,color:GREY},
  {cells:[{t:'S1',italic:true,color:GREY},'51,56','36,79','67,35','416,12','44,37','61,26'],h:0.40,color:GREY}
],{align:['left','center','center','center','center','center','center'],fs:12.6});
addText('Mọi lượt RL đều cao hơn S1 ở hầu hết các cột, và mỗi phần thưởng chỉ nhỉnh ở vài cột. Riêng lượt thưởng bằng CIDEr-D lại thấp ở chính CIDEr-D, hiện chưa giải thích được. (* xuất phát từ SFT tiếp)',{x:0.70,y:5.66,w:8.60,h:0.80,fontSize:13.4,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
note(`- Ô tô màu là cao nhất mỗi cột. Không phần thưởng nào thắng mọi cột, các chênh lệch đều nhỏ.
- SPICE thuần từ SFT tiếp cao nhất ở ROUGE-L, CIDEr-D và SPICE; SA-SPICE-v3 ở METEOR và chrF; GRPO chạy lại ở BLEU-4.
- Dr.GRPO ngang GRPO lượt chính ở mọi cột.
- Điểm lạ cần khai: thưởng bằng CIDEr-D mà lại thấp ở chính CIDEr-D. Đã kiểm cách tính IDF và cách tách từ, chưa giải thích được.`);
foot();

// 21 · SA-SPICE-v3
newSlide('So sánh RL','Phần thưởng mới: SA-SPICE-v3');
addText('Phần thưởng trộn SPICE với chrF (chrF đỡ các câu ngắn như “Scroll down” mà SPICE cho 0 điểm), cộng điểm khi đúng loại thao tác và trừ phạt độ dài.',{x:M,y:0.90,w:8.9,h:0.66,fontSize:14.6,color:FOOTB,align:'center',fit:'shrink'});
metricBadge(0.70,1.78,2.70,'61,21','exec, cao nhất\nmọi lượt đã huấn luyện',FOOTB);
metricBadge(3.65,1.78,2.70,'+1,05','so với điểm xuất phát\nSFT tiếp, p = 0,0007',FOOTC);
metricBadge(6.60,1.78,2.70,'+0,56','so với GRPO-SPICE\np = 0,069 (chưa ý nghĩa)',FOOTD);
table(0.80,3.30,[3.80,1.45,1.45,1.70],[
  {cells:['Bước không chạm (đúng loại thao tác, %)','SFT tiếp','SA-SPICE-v3','SPICE thuần'],fill:LIGHT,bold:true,h:0.50,fs:12.8},
  {cells:['Cuộn (755 bước)','76,82',{t:'80,00',bold:true,color:OK},'78,94'],h:0.46,rule:true,fs:13.2},
  {cells:['Quay lại (270 bước)','71,11',{t:'58,52',bold:true,color:BAD},{t:'56,30',bold:true,color:BAD}],h:0.46,rule:true,fs:13.2},
  {cells:['Toàn bộ (2.495 bước)','84,61','84,05','83,57'],h:0.46,fs:13.2}
],{align:['left','center','center','center'],fs:13.2});
rect(0.70,5.38,8.60,1.30,HL,{radius:0.08});
addText('Mới có một seed nên chưa viết là hơn GRPO-SPICE. SPICE thuần từ cùng điểm xuất phát đạt 60,88, ngang SA-SPICE-v3 (chênh 0,37, p = 0,46): phần trộn chrF chưa cho thấy lợi ích rõ ở exec. Cả hai cùng giảm ở bước quay lại.',{x:0.90,y:5.38,w:8.20,h:1.30,fontSize:13.4,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
note(`- Với câu ngắn như "Scroll down" hay "Go back", SPICE cho 0 điểm kể cả khi câu đúng nguyên văn; chrF đỡ chỗ này. Cộng thêm điểm khi câu đúng loại thao tác.
- 61,21 là exec cao nhất trong mọi lượt đã huấn luyện, hơn điểm xuất phát 1,05 và có ý nghĩa.
- Hơn GRPO-SPICE 0,56 nhưng p = 0,069, nên chưa viết là hơn.
- Điểm yếu: bước cuộn tăng, bước quay lại giảm từ 71,1 xuống 58,5.
- SPICE thuần (cùng điểm xuất phát, bỏ chrF và điểm loại thao tác) đạt 60,88, chênh SA-SPICE-v3 0,37, p = 0,46. Ở độ đo văn bản SPICE thuần còn nhỉnh hơn, trừ chrF. Bước quay lại của nó cũng giảm, xuống 56,3.
- Vậy phần trộn thưởng chưa mua được gì rõ; vấn đề bước quay lại cần chữa ngoài phần thưởng.`);
foot();

// 22 · Kết luận lưới
newSlide('So sánh RL','Trả lời câu hỏi “vì sao chọn GRPO và SPICE”');
table(0.60,1.00,[3.10,5.70],[
  {cells:['Câu hỏi','Câu trả lời từ số đo'],fill:FOOTB,color:WHITE,bold:true,h:0.50,fs:13.4},
  {cells:[{t:'RL có giúp không?',bold:true},'Có. Thưởng thật +0,6 đến +2,1 so với S1; thưởng ngẫu nhiên 0,00.'],h:0.80,rule:true,fs:13.4},
  {cells:[{t:'Thuật toán nào tốt nhất?',bold:true},'Không tách được. GRPO và SCST nhỉnh nhất, Dr.GRPO thấp hơn GRPO (−0,65). Độ lệch giữa hai lần chạy GRPO (0,92) cỡ khoảng cách giữa các thuật toán.'],h:0.98,rule:true,fs:13.4},
  {cells:[{t:'Phần thưởng nào tốt nhất?',bold:true},'SPICE và ROUGE-L ngang nhau ở exec, nhưng theo hai đường: SPICE sửa phần tử nhiều hơn, ROUGE-L sửa loại thao tác nhiều hơn. Trộn thêm chrF chưa hơn SPICE thuần.'],h:0.98,rule:true,fs:13.4},
  {cells:[{t:'Vì sao giữ GRPO-SPICE?',bold:true},'Thuộc nhóm dẫn đầu ở cả hai lưới, có tiền lệ (SCST, SPIDEr), và thưởng không chứa mô hình định vị nên thước chấm độc lập.'],h:0.98,fs:13.4}
],{align:['left','left'],fs:13.4});
note(`- RL có giúp, và giúp nhờ nội dung phần thưởng.
- Giữa các thuật toán chưa tách được bên nào tốt nhất. GRPO và SCST nhỉnh nhất, nhưng dao động giữa hai lần chạy cỡ khoảng cách đó.
- Giữa các phần thưởng, SPICE và ROUGE-L ngang nhau ở exec nhưng đi hai đường khác nhau.
- Giữ GRPO-SPICE vì nó thuộc nhóm dẫn đầu ở cả hai lưới, có tiền lệ rõ, và phần thưởng không dùng mô hình định vị.`);
foot();

// 23 · Đang làm
newSlide('Kết luận','Đang chạy và việc tiếp theo');
table(0.60,1.00,[5.50,3.30],[
  {cells:['Việc','Mục đích'],fill:FOOTB,color:WHITE,bold:true,h:0.50,fs:13.4},
  {cells:[{t:'Test 5 lượt đã train xong: DPO trực tuyến; GRPO + chrF, BLEU-4, SPIDEr, BERTScore',bold:true},'chạy sau 28/11; bản chạy thử đã đạt'],h:0.80,rule:true,fs:13.2},
  {cells:['Train nốt GSPO và GRPO μ=2 (750/1.000 bước), DAPO, REINFORCE++','đủ các thuật toán RL năm 2025 trong lưới'],h:0.76,rule:true,fs:13.2},
  {cells:['SA-SPICE-v3 thêm hai seed','biết kết quả có ổn định không'],h:0.62,rule:true,fs:13.2},
  {cells:['Chữa bước quay lại (câu nhắc phân tầng theo loại thao tác)','gỡ điểm yếu ở bước quay lại'],h:0.70,rule:true,fs:13.2},
  {cells:['Đưa hai lưới và phần giải thích vào luận văn','theo yêu cầu 1/11'],h:0.62,fs:13.2}
],{align:['left','left'],fs:13.2});
note(`- Năm lượt đã train xong. Bản chạy thử test 20 bước đạt cả năm lượt: nạp đúng adapter, câu sinh khác nhau giữa các lượt. Test đầy đủ chạy khi hạn mức máy làm mới sau 28/11.
- DPO trực tuyến là phương pháp học theo cặp ưu tiên phổ biến nhất còn thiếu trong lưới thuật toán.
- Kết quả từng lượt sẽ điền vào hai slide chờ số đang ẩn sau slide 18.
- Xin ý kiến thầy về thứ tự ưu tiên các việc này.`);
foot();

// 24 · Kết luận
newSlide('Kết luận','Kết luận');
table(0.82,1.00,[3.90,1.90,2.80],[
  {cells:['So sánh','Δ exec','KTC 95%'],fill:FOOTB,color:WHITE,bold:true,h:0.52,fs:13.0},
  {cells:['GRPO-SPICE − S1',{t:'+1,55',bold:true,color:FOOTB,fill:HL},'+0,80 đến +2,33'],h:0.62,rule:true,fs:13.5},
  {cells:['SA-SPICE-v3 − SFT tiếp',{t:'+1,05',bold:true,color:FOOTB,fill:HL},'+0,46 đến +1,65'],h:0.62,rule:true,fs:13.5},
  {cells:['Thưởng ngẫu nhiên − S1','0,00','−0,41 đến +0,42'],h:0.62,fs:13.5}
],{align:['left','center','center'],fs:13.5});
bullets(['Executability chấm câu bằng việc làm theo: đọc câu, chạm, xem có đúng phần tử không. Điểm phụ thuộc vào nội dung câu và giữ chiều khi đổi người làm theo.','Học tăng cường cải thiện câu nhờ nội dung phần thưởng. Các thuật toán và các độ đo thưởng phổ biến cho mức tăng gần nhau.','GRPO-SPICE thuộc nhóm dẫn đầu ở cả hai lưới; mọi kết quả hiện là một seed.'],0.82,3.70,8.36,{gap:0.92,fs:14.4,h:0.84});
note(`- Executability chấm câu bằng việc làm theo, và đã kiểm là nó phản ứng đúng với nội dung câu.
- RL giúp nhờ nội dung phần thưởng; các thuật toán và độ đo thưởng phổ biến cho mức tăng gần nhau.
- GRPO-SPICE thuộc nhóm dẫn đầu ở cả hai lưới. Mọi kết quả hiện là một seed, đang chạy thêm để chắc hơn.`);
foot();

// 25 · Cảm ơn
newSlide();
addText('Xin cảm ơn.',{x:0.85,y:2.75,w:8.30,h:1.15,fontSize:27,bold:true,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
PAGE++;

// ===== Dự phòng (ẩn) =====
newSlide('Dự phòng · Toàn bộ chỉ số đánh giá'); slide.hidden = true;
table(0.60,0.90,[2.42,1.36,1.60,1.64,1.64],[
  {cells:['Chỉ số','Mô hình gốc','Baseline S1','GRPO-SPICE','+ ACE'],fill:FOOTB,color:WHITE,bold:true,h:0.46,fs:11.6},
  {cells:['Executability','47,59','59,11','60,65','60,68'],h:0.40,rule:true,fs:11.5},
  {cells:['Hộp phần tử','53,60','65,49','67,02','67,11'],h:0.40,rule:true,fs:11.5},
  {cells:['AitW đầy đủ','63,39','74,37','76,25','76,32'],h:0.40,rule:true,fs:11.5},
  {cells:['Đúng loại thao tác','96,5','94,35','95,97','95,97'],h:0.40,rule:true,fs:11.5},
  {cells:['BLEU-4','15,34','51,56','52,36','53,47'],h:0.40,rule:true,fs:11.5},
  {cells:['METEOR','24,58','36,79','37,92','38,37'],h:0.40,rule:true,fs:11.5},
  {cells:['ROUGE-L','42,31','67,35','68,36','69,11'],h:0.40,rule:true,fs:11.5},
  {cells:['CIDEr-D','88,01','416,12','430,05','442,02'],h:0.40,rule:true,fs:11.5},
  {cells:['SPICE','18,48','44,37','45,79','47,13'],h:0.40,rule:true,fs:11.5},
  {cells:['chrF','40,18','61,26','62,87','63,45'],h:0.40,rule:true,fs:11.5},
  {cells:['BERTScore','40,10','66,33','67,07','67,73'],h:0.40,fs:11.5}
],{align:['left','center','center','center','center'],fs:11.5});
note(`- Bảng đủ các chỉ số cho bốn cấu hình, mở khi được hỏi chi tiết.`); footB();

newSlide('Dự phòng · Tác vụ mới, lịch sử tự sinh, AitZ, hai seed'); slide.hidden = true;
table(0.60,0.95,[4.30,2.00,2.50],[
  {cells:['Phép kiểm (GRPO-SPICE − S1)','Δ exec','KTC 95%'],fill:FOOTB,color:WHITE,bold:true,h:0.50,fs:12.6},
  {cells:['Tác vụ mới chưa thấy khi huấn luyện (ACU, 1.484 bước)','+4,58','+3,17 đến +6,05'],h:0.66,rule:true,fs:13},
  {cells:['Các bước trước do mô hình tự viết','+1,48','+0,54 đến +2,43'],h:0.62,rule:true,fs:13},
  {cells:['Bộ dữ liệu khác (AitZ, không huấn luyện thêm)','−0,51','−1,39 đến +0,36'],h:0.62,rule:true,fs:13},
  {cells:['GRPO-SPICE seed 202 so với seed 101','−0,72','−1,27 đến −0,16'],h:0.62,rule:true,fs:13},
  {cells:['Qwen2.5-VL-7B dùng prompt, không tinh chỉnh (so với GRPO-SPICE)','−9,14','−10,75 đến −7,54'],h:0.62,fs:13}
],{align:['left','center','center'],fs:13});
note(`- Tác vụ chưa thấy khi huấn luyện: mức tăng lớn hơn, +4,58.
- Các bước trước do mô hình tự viết: mức tăng giữ nguyên.
- AitZ, không huấn luyện thêm: không còn khác S1.
- Seed 202 thấp hơn seed 101 0,72 điểm nhưng vẫn hơn S1.`); footB();

newSlide('Dự phòng · Định nghĩa executability bằng ký hiệu'); slide.hidden = true;
bullets(['a(câu) = a(vàng): loại thao tác suy từ động từ đầu câu trùng loại thao tác thật.','|pₓ − gₓ| ≤ 0,14·W và |p_y − g_y| ≤ 0,14·H, với p là điểm UGround chạm, g là điểm người dùng chạm.','‖p − g‖ ≤ ‖p − cₖ‖ với mọi tâm phần tử bấm được khác cₖ (ô Voronoi của g).'],M,1.10,8.9,{gap:1.05,fs:15.2,h:0.90});
addText('Executability = (1/N) Σ 1[cả ba điều kiện],   N = 4.463 bước chạm',{x:M,y:4.6,w:8.9,h:0.6,fontSize:17,bold:true,color:FOOTB,align:'center'});
addText('Khoảng tin cậy: bootstrap theo cụm ứng dụng, 10.000 lần. Phép so ghép cặp: McNemar chính xác.',{x:M,y:5.4,w:8.9,h:0.5,fontSize:13,color:GREY,align:'center'});
note(`- Định nghĩa hình thức của executability, mở khi cần.`); footB();

pptx.writeFile({ fileName:path.join(__dirname, '..', 'LUAN_VAN_SLIDE_TRINH_THAY_15_11.pptx') }).then(()=>{
  const md=['# Kịch bản trình thầy (11/2026)','','Đi kèm `slides/LUAN_VAN_SLIDE_TRINH_THAY_15_11.pptx`. Sinh tự động từ ghi chú trong `slides/build/build_trinh_thay_15_11.js`; sửa lời ở script, không sửa tay file này.',''];
  NOTES.forEach(n=>{ md.push(`## ${n.hidden?'Dự phòng':'Slide '+n.page}`); md.push(n.t); md.push(''); });
  fs.writeFileSync(path.join(__dirname,'..','KICH_BAN_TRINH_THAY_15_11.md'),md.join('\n'));
  console.log('PAGE',PAGE,'notes',NOTES.length);
});
