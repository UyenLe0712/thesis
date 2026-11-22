const pptxgen = require('pptxgenjs');
const path = require('path');

const pptx = new pptxgen();
pptx.defineLayout({ name: 'A43', width: 10, height: 7.5 });
pptx.layout = 'A43';
pptx.author = 'Le Doan Phuong Uyen';
pptx.subject = 'Thuyet trinh luan van 11/2026';
pptx.title = 'Phat sinh tu dong huong dan su dung phan mem dua tren LLM';
pptx.lang = 'vi-VN';

const W = 10, H = 7.5, M = 0.55;
const TF = 'Cambria', MONO = 'Consolas';
const FOOTA='191132', FOOTB='25194B', FOOTC='4F417A', FOOTD='7A7099';
const BAR=FOOTB, ACCENT=FOOTC, ACCENT2=FOOTD;
const WHITE='FFFFFF', INK='1A1A1A', GREY='5A5A66', LIGHT='F3F2F5', RULE='D9D6DF';
const TITLE_FS=20, SECTION_FS=17, BODY_FS=16, TABLE_FS=13.2, SMALL_FS=12.5;
let slide, PAGE=0, BPAGE=0; const TOTAL=26;
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
  'Executability': { n: 4, label: 'Executability: chấm câu bằng việc làm theo' },
  'Phương pháp đề xuất': { n: 3, label: 'Phương pháp đề xuất' },
  'Kết quả chính': { n: 5, label: 'Kết quả chính' },
  'So sánh RL': { n: 6, label: 'So sánh các thuật toán RL và các phần thưởng' },
  'Kết luận': { n: 7, label: 'Hạn chế và kết luận' }
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
function source(t){ addText(t,{x:M,y:6.92,w:W-2*M,h:0.15,fontSize:8.5,color:GREY,align:'left'}); }
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
function table(x,y,colW,rows,o={}){ let yy=y; rows.forEach(r=>{ const h=r.h||0.48; if(r.fill) rect(x,yy,colW.reduce((a,b)=>a+b,0),h,r.fill); let xx=x; r.cells.forEach((c,i)=>{ const cell=typeof c==='string'?{t:c}:c; if(cell.fill) rect(xx,yy,colW[i],h,cell.fill); addText(cell.t,{x:xx,y:yy,w:colW[i],h,fontSize:cell.fs||r.fs||o.fs||TABLE_FS,bold:cell.bold!=null?cell.bold:r.bold,color:cell.color||r.color||INK,align:cell.align||(o.align&&o.align[i])||'left',valign:'mid',fit:'shrink'}); xx += colW[i]; }); if(r.rule) line(x,yy+h,colW.reduce((a,b)=>a+b,0),0,r.rule===true?RULE:r.rule,1); yy += h; }); }

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
    addText(r.label,{x:x+0.08,y:yy,w:labelW-0.08,h:rowH,fontSize:o.fs||13,bold:!!r.bold,color:r.italic?GREY:INK,valign:'mid',fit:'shrink'});
    line(X(r.lo),cy,X(r.hi)-X(r.lo),0,c,2.25);
    slide.addShape(pptx.ShapeType.ellipse,{x:X(r.d)-0.085,y:cy-0.085,w:0.17,h:0.17,fill:{color:c},line:{color:WHITE,width:1}});
    addText(`${vn(r.d)} [${vn(r.lo)}; ${vn(r.hi)}]`,{x:x+w-valW,y:yy,w:valW,h:rowH,fontSize:(o.fs||13)-1,bold:!!r.bold,color:r.italic?GREY:c,align:'right',valign:'mid'});
  });
}


const SOFT = 'F4F2F8';
function card(x,y,w,h,title,body,o={}){
  rect(x,y,w,h,o.fill||SOFT,{radius:0.06,line:o.line||RULE});
  addText(title,{x:x+0.18,y:y+0.14,w:w-0.36,h:o.th||0.42,fontSize:o.tfs||15,bold:true,color:o.tc||FOOTB,valign:'top',fit:'shrink'});
  if(body) addText(body,{x:x+0.18,y:y+0.14+(o.th||0.42)+0.06,w:w-0.36,h:h-(o.th||0.42)-0.36,fontSize:o.fs||13,color:INK,valign:'top',fit:'shrink'});
}
function arrow(x,y,w){ line(x,y,w,0,FOOTC,2,true); }

// 1 · Bìa
newSlide();
rect(0,0,W,0.66,FOOTA);
addText('ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH  -  TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN',{x:0,y:0,w:W,h:0.66,fontSize:14,bold:true,color:WHITE,align:'center',valign:'mid'});
rect(0.8,1.18,W-1.6,2.5,FOOTB,{radius:0.08});
addText('Luận văn thạc sĩ  -  Ngành Trí tuệ nhân tạo',{x:0.8,y:1.45,w:W-1.6,h:0.35,fontSize:14,bold:true,color:WHITE,align:'center'});
addText('PHÁT SINH TỰ ĐỘNG HƯỚNG DẪN SỬ DỤNG PHẦN MỀM\nDỰA TRÊN LLM TỪ CÁC TRƯỜNG HỢP SỬ DỤNG\nVÀ GIAO DIỆN NGƯỜI DÙNG',{x:0.95,y:1.96,w:W-1.9,h:1.45,fontSize:21,bold:true,color:WHITE,align:'center',valign:'mid',fit:'shrink'});
addText('Học viên thực hiện: Lê Đoàn Phương Uyên',{x:0.8,y:4.55,w:W-1.6,h:0.4,fontSize:16,bold:true,align:'center'});
addText([{text:'Giáo viên hướng dẫn:',options:{bold:true}},{text:'   TS. Nguyễn Hồng Bửu Long'}],{x:0.8,y:5.0,w:W-1.6,h:0.4,fontSize:16,align:'center'});
addText('TP. Hồ Chí Minh - 11/2026',{x:0.8,y:5.88,w:W-1.6,h:0.35,fontSize:13,align:'center'});
note(`- Chào hội đồng, giới thiệu đề tài, học viên, giáo viên hướng dẫn.`);
foot();

// 2 · Mục lục
newSlide('Nội dung');
const ML=['Bài toán','Dữ liệu','Phương pháp đề xuất: GRPO-SPICE và ACE','Độ đo executability','Kết quả trên tập kiểm tra','So sánh các thuật toán học tăng cường và các phần thưởng','Hạn chế và kết luận'];
ML.forEach((t,i)=>{ const y=0.95+i*0.84; rect(1.1,y,0.62,0.62,FOOTB,{radius:0.08}); addText(String(i+1),{x:1.1,y,w:0.62,h:0.62,fontSize:20,bold:true,color:WHITE,align:'center',valign:'mid'}); addText(t,{x:2.0,y,w:7.0,h:0.62,fontSize:18,color:INK,valign:'mid'}); });
note(`- Bảy phần. Độ đo executability trình bày ngay trước kết quả, vì mọi con số kết quả đều đọc bằng nó.`);
foot();

// 3 · Bài toán
newSlide('Giới thiệu','Bài toán');
addText('Sinh một câu hướng dẫn cho bước tiếp theo trên màn hình di động.',{x:M,y:0.88,w:6.2,h:0.7,fontSize:17,bold:true,color:FOOTB,fit:'shrink'});
addText([{text:'Đầu vào. ',options:{bold:true,color:FOOTB}},{text:'Mục tiêu của tác vụ, các bước đã làm, ảnh chụp màn hình hiện tại và văn bản hiển thị trên giao diện.'}],{x:M,y:1.75,w:6.0,h:1.1,fontSize:15,valign:'top'});
addText([{text:'Kết quả. ',options:{bold:true,color:FOOTB}},{text:'Một câu nêu thao tác cần làm và phần tử cần tương tác, ví dụ “Click on the Not now button”.'}],{x:M,y:2.95,w:6.0,h:0.9,fontSize:15,valign:'top'});
rect(M,4.15,6.0,1.25,SOFT,{radius:0.06});
addText('Tác tử giao diện đọc câu rồi tự bấm. Bài toán này đi theo chiều ngược lại: mô hình viết câu để người dùng đọc và tự làm.',{x:M+0.2,y:4.2,w:5.6,h:1.15,fontSize:14.5,color:INK,valign:'mid'});
addText('Ảnh: một bước thật trong tập kiểm tra. Vòng vàng là phần tử người dùng đã chạm (nút Bin).',{x:M,y:5.7,w:6.0,h:0.5,fontSize:12,color:GREY});
imgFit(path.join(FIG,'fig_bai_toan_anh.png'),1080,2160,6.85,0.82,2.7,6.2);
note(`- Mô hình nhìn màn hình, biết mục tiêu và các bước đã làm, viết câu cho bước kế tiếp.
- Ảnh: một bước thật trong tập kiểm tra, người dùng chạm nút Bin.`);
foot();

// 4 · Vấn đề
newSlide('Giới thiệu','BLEU và SPICE không kiểm được câu có chỉ đúng phần tử');
rect(1.0,1.2,8.0,1.6,FOOTB,{radius:0.08});
addText('“Tap the button.”',{x:1.0,y:1.2,w:8.0,h:1.6,fontSize:34,bold:true,color:WHITE,align:'center',valign:'mid'});
addText('Câu đúng ngữ pháp, nghe tự nhiên, nhưng màn hình có nhiều nút thì người đọc không biết bấm nút nào.',{x:1.0,y:3.2,w:8.0,h:0.9,fontSize:16,valign:'mid'});
addText('BLEU hay SPICE chỉ so câu chữ với câu chuẩn. Muốn biết câu có dẫn tới đúng phần tử thì phải chấm bằng cách làm theo câu.',{x:1.0,y:4.35,w:8.0,h:0.9,fontSize:16,bold:true,color:FOOTC,valign:'mid'});
note(`- Câu không chỉ ra phần tử nào vẫn có thể được BLEU/SPICE cho điểm khá.
- Từ đây dẫn sang executability.`);
foot();

// 5 · Dữ liệu
newSlide('Dữ liệu');
addText('AndroidControl (Li và cộng sự, NeurIPS 2024), dùng theo chiều ngược lại: câu hướng dẫn từ đầu vào trở thành đích cần sinh.',{x:M,y:0.88,w:8.9,h:0.75,fontSize:15.5,color:FOOTB,fit:'shrink'});
[['64.567','bước huấn luyện','12.895 tác vụ, dựng tự động, không gán nhãn thêm',FOOTC],
 ['4.463','bước chạm ở tập kiểm tra','1.432 tác vụ, không trùng tác vụ với tập huấn luyện',FOOTC],
 ['2.495','bước không chạm','cuộn, quay lại, nhập chữ; đánh giá riêng',FOOTD]].forEach((d,i)=>{
  const x=M+i*3.0; rect(x,1.9,2.8,3.1,SOFT,{radius:0.06});
  addText(d[0],{x,y:2.05,w:2.8,h:0.9,fontSize:32,bold:true,color:d[3],align:'center',valign:'mid'});
  addText(d[1],{x:x+0.15,y:3.0,w:2.5,h:0.55,fontSize:15,bold:true,align:'center',valign:'mid'});
  addText(d[2],{x:x+0.15,y:3.6,w:2.5,h:1.2,fontSize:12.5,color:GREY,align:'center',valign:'top'});
});
addText('Ghép hai bản phát hành công khai trên HuggingFace theo (episode_id, step_id): một bản có câu hướng dẫn của người chú thích, một bản có ảnh màn hình.',{x:M,y:5.35,w:8.9,h:0.8,fontSize:13.5,color:GREY});
note(`- Bộ gốc dùng câu hướng dẫn làm đầu vào để dự đoán thao tác; đề tài dùng câu làm đích sinh.
- Mọi số executability tính trên 4.463 bước chạm.
- Bước không chạm báo riêng vì không có điểm chạm để chấm.`);
foot();

// 10 · Phương pháp
newSlide('Phương pháp đề xuất');
const PP=[['S1\nQwen2.5-VL-3B\ntinh chỉnh có giám sát',WHITE,INK],['GRPO-SPICE\nhọc tăng cường,\nthưởng SPICE',FOOTC,WHITE],['ACE\nthay câu có chọn lọc\nbằng câu ví dụ',FOOTC,WHITE],['Câu\nhướng dẫn',WHITE,INK]];
PP.forEach((f,i)=>{ const x=0.45+i*2.42; box(x,1.2,1.9,1.7,f[0],{fill:f[1],color:f[2],line:FOOTB,fs:13.5,bold:true,radius:0.06}); if(i<3) arrow(x+1.94,2.05,0.44); });
rect(M,3.5,8.9,1.2,SOFT,{radius:0.06});
addText('Phần thưởng không dùng UGround, mô hình định vị chấm điểm ở phần sau. Vì vậy mô hình sinh không được tối ưu thẳng theo dụng cụ dùng để đánh giá nó.',{x:M+0.2,y:3.5,w:8.5,h:1.2,fontSize:14.5,valign:'mid'});
note(`- S1 là nền chung của mọi nhánh, huấn luyện bằng QLoRA.
- GRPO-SPICE sinh câu ban đầu; ACE chỉ thay câu ở một phần nhỏ số bước.`);
foot();

// 10b · SPICE là gì
newSlide('Phương pháp đề xuất','SPICE so nội dung câu với câu chuẩn');
addText('SPICE (Anderson và cộng sự, ECCV 2016) chấm một câu bằng cách so nội dung của nó với câu chuẩn: câu nhắc tới những đối tượng nào, đối tượng có đặc điểm gì, và liên hệ với nhau ra sao.',{x:M,y:0.85,w:8.9,h:0.95,fontSize:14.5,color:FOOTB});
const SP=[['1. Tách câu','thành các bộ: đối tượng, thuộc tính, quan hệ'],['2. Làm như vậy','với câu chuẩn của người chú thích'],['3. Đếm số bộ khớp','giữa hai câu, rồi tính điểm F1']];
SP.forEach((f,i)=>{ const x=0.45+i*3.12; box(x,2.0,2.6,1.25,f[0]+'\n'+f[1],{fill:i===2?FOOTC:WHITE,color:i===2?WHITE:INK,line:FOOTB,fs:13,bold:true,radius:0.06}); if(i<2) arrow(x+2.64,2.62,0.44); });
addText('Độ chính xác P = số bộ khớp / số bộ của câu sinh     Độ phủ R = số bộ khớp / số bộ của câu chuẩn     SPICE = 2PR / (P + R)',{x:M,y:3.5,w:8.9,h:0.5,fontSize:12.5,color:GREY,align:'center',fit:'shrink'});
card(M,4.2,4.35,2.3,'Hợp với bài toán','Câu gọi sai tên phần tử thì mất ngay các bộ quan trọng, nên điểm giảm rõ. Đổi động từ đồng nghĩa (“tap” hay “click”) hầu như không ảnh hưởng.',{tfs:14.5,fs:12.5,fill:HL});
card(5.1,4.2,4.35,2.3,'Điểm yếu đã đo','Gần như không phân biệt loại thao tác: đổi “Click” thành “Swipe up” vẫn được điểm cao. Câu quá ngắn như “Scroll down” không có bộ nào nên được 0, kể cả khi đúng nguyên văn.',{tfs:14.5,fs:12.5});
note(`- BLEU đếm chữ trùng; SPICE so các đối tượng, thuộc tính và quan hệ mà câu nhắc tới.
- Điểm yếu đã đo trên câu chuẩn của tập kiểm định: đổi "Click" thành "Swipe up" SPICE vẫn cho khoảng 0,92, các độ đo khác chỉ 0,45 đến 0,79.
- Hai điểm yếu này là lý do thử thêm phần thưởng SA-SPICE-v3 ở phần so sánh.`);
foot();

// 10c · Ví dụ SPICE
newSlide('Phương pháp đề xuất','Ví dụ: SPICE thưởng câu gọi đúng phần tử');
imgFit(path.join(FIG,'fig_vidu_spice.png'),1500,1732,M,0.8,4.2,4.85);
addText('Câu chuẩn: “Click on the Not now button to remove this pop up notification”',{x:4.95,y:0.9,w:4.5,h:0.75,fontSize:13,bold:true,color:FOOTB});
table(4.95,1.8,[2.0,1.25,1.25],[
  {cells:['Bộ của câu chuẩn','S1','GRPO-SPICE'],fill:FOOTB,color:WHITE,bold:true,h:0.45,fs:12},
  {cells:['button','có','có'],h:0.42,rule:true,fs:12.5},
  {cells:['button – Not now',{t:'không',color:BAD,bold:true},{t:'có',color:OK,bold:true}],h:0.42,rule:true,fs:12.5},
  {cells:['notification','không','không'],h:0.42,rule:true,fs:12.5},
  {cells:['notification – pop up','không','không'],h:0.42,fs:12.5}
],{align:['left','center','center']});
addText('S1 viết “Allow button”: chỉ khớp bộ “button”. GRPO-SPICE viết “Not Now button”: khớp thêm đúng bộ quan trọng nhất là tên phần tử, nên được điểm cao hơn. UGround đọc câu GRPO-SPICE và chạm đúng nút.',{x:4.95,y:4.0,w:4.5,h:1.65,fontSize:12.5,valign:'top'});
source('Bảng bộ là minh hoạ rút gọn để dễ theo dõi, không phải đầu ra đầy đủ của bộ phân tích SPICE.');
note(`- Ví dụ thật từ tập kiểm tra.
- Trong GRPO, tám câu của cùng một bước được chấm như vậy; câu gọi đúng "Not now" có điểm cao hơn trung bình nhóm nên được khuyến khích.`);
foot();

// 11 · GRPO-SPICE
newSlide('Phương pháp đề xuất','GRPO-SPICE');
bullets(['Với mỗi câu nhắc, mô hình viết tám câu.','Mỗi câu được chấm SPICE so với câu chuẩn, trừ một khoản phạt độ dài.','Câu có điểm cao hơn trung bình nhóm được tăng xác suất, câu thấp hơn bị giảm.','Phạt KL giữ mô hình không đi quá xa S1.'],M,1.0,4.6,{gap:0.95,fs:14.5,h:0.85});
rect(5.4,0.95,4.05,2.75,SOFT,{radius:0.06});
addText('Thiết lập',{x:5.6,y:1.05,w:3.7,h:0.4,fontSize:15,bold:true,color:FOOTB});
addText('r = SPICE(câu, câu chuẩn) − 0,02 × phạt độ dài',{x:5.6,y:1.55,w:3.7,h:0.7,fontSize:13,bold:true,color:FOOTC});
addText('500 bước cập nhật, 1.000 câu nhắc\n8 câu mỗi nhóm, hệ số KL 0,04\ntốc độ học 1e-5',{x:5.6,y:2.3,w:3.7,h:1.1,fontSize:12.5});
addText('Tiền lệ dùng độ đo làm phần thưởng: SCST (Rennie và cộng sự, CVPR 2017) và SPIDEr (Liu và cộng sự, ICCV 2017).',{x:M,y:5.35,w:8.9,h:0.7,fontSize:13,color:GREY});
note(`- GRPO không cần mô hình giá trị: mốc so là trung bình của chính nhóm tám câu.
- Không nhận điểm mới ở thuật toán hay ở việc chọn SPICE; điểm mới là áp vào bài toán này và đánh giá bằng executability.`);
foot();

// 12 · ACE
newSlide('Phương pháp đề xuất','ACE');
addText('Nhiều tác vụ lặp lại với thay đổi nhỏ, nên câu chuẩn của một bước cũ đôi khi dùng được nguyên văn.',{x:M,y:0.9,w:8.9,h:0.7,fontSize:15,color:FOOTB});
box(0.45,1.95,2.3,1.5,'Truy hồi bốn bước\ngiống nhất trong\ntập huấn luyện',{fill:WHITE,line:FOOTB,fs:13,bold:true,radius:0.06});
arrow(2.8,2.7,0.4);
box(3.25,1.95,2.3,1.5,'Bộ sinh xem\nbốn câu ví dụ,\nviết câu ứng viên',{fill:WHITE,line:FOOTB,fs:13,bold:true,radius:0.06});
arrow(5.6,2.7,0.4);
box(6.05,1.95,3.5,1.5,'Chỉ thay câu khi ứng viên\ntrùng nguyên văn một câu ví dụ\nvà cùng loại thao tác\nvới câu GRPO-SPICE',{fill:FOOTC,color:WHITE,line:FOOTC,fs:13,bold:true,radius:0.06});
rect(M,4.0,8.9,1.3,SOFT,{radius:0.06});
addText('Ở phần lớn các bước, câu GRPO-SPICE được giữ. Dùng câu ứng viên cho mọi bước thì executability giảm 1,25 điểm, nên không bỏ được hai điều kiện này.',{x:M+0.2,y:4.0,w:8.5,h:1.3,fontSize:14.5,valign:'mid'});
note(`- ACE: Action-Consistent Exemplar copying.
- Quy tắc chọn trên tập kiểm định, áp lên tập kiểm tra một lần.`);
foot();

// 6 · Executability
newSlide('Executability');
addText('Đưa câu cho một “người lạ” chỉ nhìn màn hình và làm theo, rồi xem người đó bấm vào đâu.',{x:M,y:0.9,w:8.9,h:0.6,fontSize:16,bold:true,color:FOOTB,fit:'shrink'});
const FL=[['Câu mô hình viết\n+ ảnh màn hình',WHITE,INK],['UGround\nmô hình định vị,\nkhông biết đáp án',FOOTC,WHITE],['Một điểm chạm\ntrên màn hình',WHITE,INK],['So với điểm\nngười dùng\nchạm thật',WHITE,INK]];
FL.forEach((f,i)=>{ const x=0.45+i*2.42; box(x,2.0,1.9,1.5,f[0],{fill:f[1],color:f[2],line:FOOTB,fs:13.5,bold:true,radius:0.06}); if(i<3) arrow(x+1.94,2.75,0.44); });
rect(M,4.1,8.9,0.95,SOFT,{radius:0.06});
addText('Executability = tỉ lệ bước mà câu dẫn người làm theo tới đúng phần tử, với đúng loại thao tác.',{x:M+0.2,y:4.1,w:8.5,h:0.95,fontSize:15.5,bold:true,color:FOOTB,valign:'mid'});
addText('UGround không tham gia huấn luyện và không nằm trong phần thưởng, nên độ đo tách khỏi mục tiêu huấn luyện.',{x:M,y:5.35,w:8.9,h:0.7,fontSize:14,color:GREY});
note(`- BLEU/SPICE so chữ với câu chuẩn; executability xem người làm theo câu có bấm đúng chỗ không.
- UGround là mô hình định vị giao diện có sẵn: nhận ảnh và câu, trả về một điểm.`);
foot();

// 7 · Ba điều kiện
newSlide('Executability','Một bước đạt khi thoả cả ba điều kiện');
[['1. Đúng loại thao tác','Bước cần chạm mà câu bảo vuốt hay quay lại thì không đạt.'],
 ['2. Lệch không quá 14% mỗi chiều','Ngưỡng của bộ AndroidInTheWild.'],
 ['3. Nằm trong ô Voronoi của điểm thật','Gần điểm thật hơn mọi phần tử bấm được khác, để loại câu gọi nhầm nút bên cạnh.']].forEach((c,i)=>{
  card(M,0.9+i*1.45,4.0,1.3,c[0],c[1],{tfs:14.5,fs:12.5,th:0.36});
});
imgFit(path.join(FIG,'fig_voronoi.png'),1080,740,4.75,0.9,4.75,3.3);
addText('Ví dụ thật: câu của S1 “Click on the Birthday option” chạm đúng ô Birthday; câu của mô hình gốc gọi ô Gender ngay hàng trên nên không đạt.',{x:4.75,y:4.3,w:4.75,h:0.8,fontSize:12,color:GREY});
rect(M,5.4,8.9,0.95,SOFT,{radius:0.06});
addText('Khi điểm chạm bị dời sang phần tử bên cạnh, chỉ dùng dung sai 14% vẫn chấp nhận 84,3% số ca; thêm điều kiện ô Voronoi thì còn 2,8%. Chạm lệch nhẹ trong cùng phần tử vẫn được giữ 99,7%.',{x:M+0.2,y:5.4,w:8.5,h:0.95,fontSize:13,valign:'mid'});
note(`- Hai ô Birthday và Gender chỉ cách nhau một hàng: chỉ đo khoảng cách thì câu sai vẫn có thể được tính đúng.`);
foot();

// 8 · Trần và sàn
newSlide('Executability','Câu chuẩn đạt 75,7, câu của màn hình khác chỉ 6,1');
hbarChart(M,1.05,8.9,[
  {label:'Câu chuẩn (trần)',value:75.7,text:'75,7',color:FOOTB,bold:true},
  {label:'GRPO-SPICE từ SFT tiếp',value:60.88,text:'60,9',color:FOOTC,bold:true},
  {label:'GRPO-SPICE (đề xuất)',value:60.65,text:'60,7',color:FOOTC,bold:true},
  {label:'S1 (tinh chỉnh có giám sát)',value:59.11,text:'59,1',color:FOOTD},
  {label:'Mô hình gốc',value:47.59,text:'47,6',color:FOOTD},
  {label:'“Tap the button.” mọi bước *',value:12.0,text:'12,0',color:'A9A4B8'},
  {label:'Câu thật của màn hình khác *',value:6.1,text:'6,1',color:'A9A4B8'}
],{labelW:2.9,valueW:0.8,rowH:0.56,max:80,fs:13.5});
addText('Ngay câu chuẩn cũng chỉ đạt 75,7% vì bộ định vị đôi khi chạm lệch. Câu đúng văn phong mà sai nội dung chỉ đạt 6,1%, thấp hơn cả câu chung chung: bộ định vị thật sự đọc nội dung câu.',{x:M,y:5.0,w:8.9,h:0.95,fontSize:13.5});
source('Executability (%) trên 4.463 bước chạm. * Đo trên mẫu 800 bước, trần trên mẫu này 74,9%.');
note(`- Trần 75,7 là giới hạn của dụng cụ, không phải của ngôn ngữ.
- Sau tinh chỉnh, các mức chênh chỉ 1 đến 2 điểm nên luôn kèm khoảng tin cậy.`);
foot();

// 9 · Kiểm tra thước
newSlide('Executability','Điểm giảm khi câu thiếu tên, chiều tăng giữ khi đổi bộ định vị');
card(M,0.9,2.85,3.6,'Bỏ tên phần tử khỏi câu chuẩn',null,{tfs:14});
addText('−28,5',{x:M,y:1.55,w:2.85,h:0.8,fontSize:30,bold:true,color:FOOTC,align:'center'});
addText('điểm trên các bước bị tác động. Bỏ mô tả vị trí chỉ mất 3,5 điểm: gọi đúng tên quan trọng hơn chỉ chỗ.',{x:M+0.18,y:2.45,w:2.5,h:1.9,fontSize:12.5,valign:'top'});
card(3.57,0.9,2.85,3.6,'Đổi bộ định vị chấm điểm',null,{tfs:14});
table(3.72,1.45,[1.45,1.1],[
  {cells:['bộ định vị','GRPO-SPICE − S1'],bold:true,color:FOOTB,h:0.42,rule:true,fs:11},
  {cells:['UGround','+1,55'],h:0.4,fs:12.5},{cells:['UI-Venus','+1,55'],h:0.4,fs:12.5},
  {cells:['Phi-Ground','+0,78'],h:0.4,fs:12.5},{cells:['Phi-4','+0,69'],h:0.4,fs:12.5}
],{align:['left','right']});
addText('Phi-Ground và Phi-4 không thuộc họ Qwen.',{x:3.72,y:3.6,w:2.55,h:0.7,fontSize:12,color:GREY,valign:'top'});
card(6.6,0.9,2.85,3.6,'Chấm lại nhiều lần',null,{tfs:14});
addText('0',{x:6.6,y:1.55,w:2.85,h:0.8,fontSize:30,bold:true,color:FOOTC,align:'center'});
addText('bất đồng trên 1.625 phép so, qua bốn lượt chấm khác thứ tự và cách gom lô.',{x:6.78,y:2.45,w:2.5,h:1.9,fontSize:12.5,valign:'top'});
note(`- Mức số tuyệt đối khác nhau theo bộ định vị, nhưng phương pháp luôn cao hơn S1.
- Độ đo tất định: cùng câu, cùng ảnh cho cùng toạ độ.`);
foot();

// 13 · Kết quả chính
newSlide('Kết quả chính');
table(0.6,0.95,[3.3,1.85,1.95,1.7],[
  {cells:['Mô hình','Executability','Hộp phần tử (D.3)','AitW đầy đủ'],fill:FOOTB,color:WHITE,bold:true,h:0.5,fs:13},
  {cells:['Câu chuẩn (trần)','75,73','83,82','92,14'],h:0.46,rule:true,color:GREY},
  {cells:['Mô hình gốc','47,59','53,60','63,39'],h:0.46,rule:true},
  {cells:['S1','59,11','65,49','74,37'],h:0.42,rule:true},
  {cells:['SFT tiếp (S1 học thêm, không RL)','60,16','66,64','75,71'],h:0.42,rule:true},
  {cells:['GRPO-SPICE (từ S1)','60,65','67,02','76,25'],h:0.42,rule:true,fill:HL,bold:true,color:FOOTB},
  {cells:['GRPO-SPICE + ACE','60,68','67,11','76,32'],h:0.42,rule:true,fill:HL,bold:true,color:FOOTB},
  {cells:['GRPO-SPICE (từ SFT tiếp)','60,88','67,38','76,92'],h:0.42,fill:HL,bold:true,color:FOOTC}
],{align:['left','center','center','center'],fs:13});
card(M,4.55,2.85,2.15,'GRPO-SPICE − S1: +1,55','KTC 95% [+0,80; +2,33], không chứa 0. Hai tiêu chí vị trí còn lại tăng cùng cỡ.',{tfs:14,fs:12,fill:HL});
card(3.57,4.55,2.85,2.15,'Từ SFT tiếp − S1: +1,77','KTC [+1,13; +2,44]. So với chính điểm xuất phát SFT tiếp: +0,72 [+0,24; +1,20].',{tfs:14,fs:12,fill:HL});
card(6.6,4.55,2.85,2.15,'ACE giữ executability','Cả bảy độ đo văn bản tăng thêm, ví dụ CIDEr-D 430,0 lên 442,0.',{tfs:14,fs:12});
source('% trên 4.463 bước chạm của tập kiểm tra, một hạt giống.');
note(`- D.3: tiêu chí gốc của AndroidControl, điểm chạm nằm trong hộp phần tử đúng.
- AitW đầy đủ: khoảng cách 14% hoặc cùng nằm trong hộp nới 1,4 lần.
- Lượt mới 17/11: cùng thưởng SPICE nhưng xuất phát từ SFT tiếp và tập câu nhắc mới, nên so công bằng là so với SFT tiếp (+0,72, có ý nghĩa).
- Lượt mới so với GRPO-SPICE từ S1: +0,22 [−0,35; +0,81], chưa tách được.`);
foot();

// 14 · Kiểm soát
newSlide('Kết quả chính','Nguồn gốc và độ bền của mức tăng');
[['0,00','SPICE ghép ngẫu nhiên','Cùng 500 bước GRPO, điểm SPICE ghép ngẫu nhiên giữa các mẫu: bằng đúng S1.',FOOTD],
 ['+4,58','Tác vụ S1 chưa thấy','1.484 bước, [+3,17; +6,05]. Lượt GRPO thứ hai: +4,04.',FOOTC],
 ['+1,48','Lịch sử do mô hình tự viết','Các bước trước không dùng câu chuẩn, [+0,54; +2,43].',FOOTC],
 ['≈ 0','Bộ dữ liệu AitZ','S1 vẫn hơn mô hình gốc 3,29 điểm, nhưng GRPO-SPICE ngang S1.',FOOTD]].forEach((d,i)=>{
  const x=M+(i%2)*4.55, y=0.95+Math.floor(i/2)*2.55;
  rect(x,y,4.35,2.35,SOFT,{radius:0.06});
  addText(d[0],{x:x+0.2,y:y+0.15,w:1.6,h:0.8,fontSize:28,bold:true,color:d[3],valign:'mid'});
  addText(d[1],{x:x+1.85,y:y+0.15,w:2.35,h:0.8,fontSize:14.5,bold:true,color:FOOTB,valign:'mid',fit:'shrink'});
  addText(d[2],{x:x+0.2,y:y+1.05,w:3.95,h:1.15,fontSize:13,valign:'top'});
});
source('Mức chênh executability so với S1, đơn vị điểm phần trăm.');
note(`- Nhánh ghép ngẫu nhiên loại khả năng mức tăng chỉ do chạy thêm vòng lặp học tăng cường.
- Trên tác vụ mới mức tăng còn lớn hơn.
- AitZ: lợi ích riêng của SPICE phụ thuộc phân phối câu chuẩn.`);
foot();

// 15 · Cách so sánh
newSlide('So sánh RL','Cách so sánh');
card(M,0.95,4.35,1.9,'Phép so 1: đổi thuật toán','Giữ nguyên phần thưởng SPICE, lần lượt thay GRPO bằng SCST, PPO, REINFORCE, RLOO.',{tfs:16,fs:14});
card(5.1,0.95,4.35,1.9,'Phép so 2: đổi phần thưởng','Giữ nguyên GRPO, lần lượt thay SPICE bằng ROUGE-L, METEOR, CIDEr-D, SA-SPICE-v3.',{tfs:16,fs:14});
card(M,3.1,8.9,1.75,'Hai mốc để đọc số','S1: mô hình trước khi học tăng cường (59,11).\nHọc thêm không RL: S1 học thêm có giám sát trên cùng câu nhắc, không có phần thưởng (60,16).',{tfs:16,fs:14,fill:WHITE});
addText('Mọi thứ khác giữ nguyên: cùng dữ liệu, cùng số câu nhắc, cùng hạt giống. Số là executability trên 4.463 bước chạm của tập kiểm tra.',{x:M,y:5.1,w:8.9,h:0.7,fontSize:13.5,color:GREY});
note(`- Hai phép so, mỗi phép chỉ đổi một yếu tố.
- Mốc "học thêm không RL" để tách công của học tăng cường với công của việc học thêm.`);
foot();

const DAGGER='Thanh đánh dấu † xuất phát từ mô hình học thêm không RL; các thanh còn lại xuất phát từ S1.';

// 16 · Thuật toán: biểu đồ
newSlide('So sánh RL','Đổi thuật toán, giữ phần thưởng SPICE');
addText('Executability, và số điểm hơn S1',{x:M,y:0.8,w:8.9,h:0.35,fontSize:13,color:GREY});
hbarChart(M,1.25,8.9,[
  {label:'GRPO †',value:1.77,text:'60,88   +1,77',color:FOOTC,bold:true},
  {label:'SCST',value:1.43,text:'60,54   +1,43',color:FOOTD},
  {label:'PPO, λ = 1',value:0.96,text:'60,07   +0,96',color:FOOTD},
  {label:'REINFORCE',value:0.90,text:'60,00   +0,90',color:FOOTD},
  {label:'PPO, λ = 0,95',value:0.87,text:'59,98   +0,87',color:FOOTD},
  {label:'RLOO',value:0.34,text:'59,44   +0,34',color:FOOTD},
  {label:'Học thêm không RL',value:1.05,text:'60,16   +1,05',color:'A9A4B8'}
],{labelW:2.3,valueW:1.75,rowH:0.56,max:2.0,fs:13.5});
rect(M,5.3,8.9,0.95,SOFT,{radius:0.06});
addText('Mọi thuật toán đều cao hơn S1. GRPO từ S1 (60,65) hơn REINFORCE 0,65 điểm và RLOO 1,21 điểm, cả hai có ý nghĩa; với SCST và PPO thì chưa tách được.',{x:M+0.2,y:5.3,w:8.5,h:0.95,fontSize:13.5,bold:true,color:FOOTB,valign:'mid'});
source(DAGGER+' S1 = 59,11.');
note(`- Đọc: cột số đầu là executability, số sau là hơn S1 bao nhiêu điểm.
- GRPO ở đây xuất phát từ mô hình học thêm, nên phần hơn S1 gồm cả công học thêm (+1,05); so với chính điểm xuất phát, GRPO hơn +0,72 [+0,24; +1,20].
- SCST hơn S1 +1,43 [+0,79; +2,10]; RLOO +0,34, khoảng tin cậy chứa 0.
- So trực tiếp với GRPO-SPICE từ S1 (60,65, không có trên hình): REINFORCE −0,65 (p=0,009), RLOO −1,21 (p=4e−6); SCST, PPO ngang.`);
foot();

// Bảng số đầy đủ: in đậm giá trị cao nhất mỗi cột trong các hàng RL (không tính hàng mốc)
function numTable(y,head,colW,rows,o={}){
  const nC=head.length, best=[];
  for(let j=1;j<nC;j++){ const v=rows.filter(r=>!r.base).map(r=>parseFloat(String(r.c[j]).replace('−','-').replace(',','.'))).filter(v=>!isNaN(v)); best[j]=Math.max(...v); }
  const tr=[{cells:head,fill:FOOTB,color:WHITE,bold:true,h:o.hh||0.62,fs:o.hfs||11.5}];
  rows.forEach((r,i)=>{
    tr.push({cells:r.c.map((c,j)=>{ const v=parseFloat(String(c).replace('−','-').replace(',','.')); const b=j>0&&!r.base&&v===best[j]; return {t:c,bold:b||(j===0&&r.hl),color:r.base?GREY:(b?FOOTC:INK)}; }),
      h:o.rh||0.46,rule:i<rows.length-1,fill:r.hl?HL:(r.base?LIGHT:undefined),fs:o.fs||12.5});
  });
  table(o.x||M,y,colW,tr,{align:['left'].concat(Array(nC-1).fill('center'))});
}
const POS_HEAD=['','Executability','Hộp phần tử (D.3)','AitW đầy đủ','Đúng loại thao tác','Hơn S1'];
const TXT_HEAD=['','BLEU-4','METEOR','ROUGE-L','CIDEr-D','SPICE','chrF','BERTScore'];
const ALG_POS=[
  {c:['GRPO †','60,88','67,38','76,92','95,94','+1,77'],hl:true},
  {c:['SCST','60,54','66,88','76,14','95,99','+1,43']},
  {c:['PPO, λ = 1','60,07','66,77','76,09','96,35','+0,96']},
  {c:['REINFORCE','60,00','66,41','75,51','95,74','+0,90']},
  {c:['PPO, λ = 0,95','59,98','66,26','75,69','95,38','+0,87']},
  {c:['RLOO','59,44','65,81','75,02','94,91','+0,34']},
  {c:['Học thêm không RL','60,16','66,64','75,71','96,06','+1,05'],base:true},
  {c:['S1','59,11','65,49','74,37','94,26','-'],base:true}];
const ALG_TXT=[
  {c:['GRPO †','52,59','38,74','69,51','436,26','46,41','64,07','67,96'],hl:true},
  {c:['SCST','51,97','38,15','68,70','430,89','45,93','63,31','67,25']},
  {c:['PPO, λ = 1','50,70','37,86','68,25','420,72','44,98','63,00','66,78']},
  {c:['REINFORCE','52,52','37,37','67,97','426,11','45,27','62,06','66,76']},
  {c:['PPO, λ = 0,95','50,67','37,89','67,96','419,53','44,81','62,85','66,54']},
  {c:['RLOO','52,00','37,00','67,33','422,10','45,26','61,65','66,31']},
  {c:['Học thêm không RL','52,07','37,75','68,55','425,79','45,33','62,64','67,05'],base:true},
  {c:['S1','51,56','36,79','67,35','416,12','44,37','61,26','66,33'],base:true}];

// 17 · Thuật toán: bảng vị trí
newSlide('So sánh RL','Đổi thuật toán: số theo tiêu chí vị trí');
numTable(0.95,POS_HEAD,[2.4,1.3,1.4,1.25,1.3,1.25],ALG_POS);
addText('GRPO dẫn ba cột vị trí, SCST đứng thứ hai. PPO λ = 1 viết đúng loại thao tác nhiều nhất nhưng executability thấp hơn.',{x:M,y:5.45,w:8.9,h:0.75,fontSize:13.5,bold:true,color:FOOTB});
source('% trên 4.463 bước chạm. '+DAGGER+' Đậm: cao nhất trong các lượt RL.');
note(`- Executability, D.3 và AitW là ba cách xác định câu có dẫn tới đúng phần tử; đúng loại thao tác chỉ xét động từ.
- PPO chạy 1.000 bước cập nhật để đi hết cùng 1.000 câu nhắc.
- Dr.GRPO đầy đủ (22/11): executability 60,00, thấp hơn GRPO-SPICE từ S1 0,65 điểm; chưa chấm D.3, AitW và độ đo văn bản nên chưa đưa vào bảng. A2C mới thăm dò.`);
foot();

// 18 · Thuật toán: bảng văn bản
newSlide('So sánh RL','Đổi thuật toán: số theo độ đo văn bản');
numTable(0.95,TXT_HEAD,[2.3,0.95,0.95,0.95,1.0,0.9,0.9,0.95],ALG_TXT,{fs:12});
addText('GRPO cao nhất ở cả bảy độ đo văn bản; SCST đứng thứ hai ở phần lớn các cột. Mọi lượt RL đều cao hơn S1 ở gần như mọi cột.',{x:M,y:5.45,w:8.9,h:0.75,fontSize:13.5,bold:true,color:FOOTB});
source('Bộ chấm COCO, mức kho trên 4.463 bước chạm; BERTScore đã chuẩn hoá. '+DAGGER);
note(`- Các độ đo này so câu sinh với câu chuẩn của người chú thích.
- Thứ hạng theo độ đo văn bản không trùng hẳn thứ hạng theo executability.`);
foot();

const RW_POS=[
  {c:['SA-SPICE-v3 †','61,21','67,56','77,12','95,79','+2,11']},
  {c:['SPICE †','60,88','67,38','76,92','95,94','+1,77'],hl:true},
  {c:['ROUGE-L','60,63','67,04','76,79','96,75','+1,52']},
  {c:['METEOR','60,27','66,75','76,27','96,17','+1,17']},
  {c:['CIDEr-D','60,27','66,44','76,00','95,99','+1,17']},
  {c:['SPICE ghép ngẫu nhiên','59,11','65,58','74,59','94,06','0,00'],base:true},
  {c:['Học thêm không RL','60,16','66,64','75,71','96,06','+1,05'],base:true},
  {c:['S1','59,11','65,49','74,37','94,26','-'],base:true}];
const RW_TXT=[
  {c:['SA-SPICE-v3 †','51,24','38,90','69,31','429,12','45,76','64,40','67,59']},
  {c:['SPICE †','52,59','38,74','69,51','436,26','46,41','64,07','67,96'],hl:true},
  {c:['ROUGE-L','52,59','38,20','69,27','432,81','45,57','63,42','67,57']},
  {c:['METEOR','50,76','38,63','69,14','426,61','45,13','64,19','67,35']},
  {c:['CIDEr-D','51,59','37,78','68,47','424,52','44,43','62,90','67,03']},
  {c:['SPICE ghép ngẫu nhiên','51,32','36,95','67,36','418,13','44,40','61,52','66,40'],base:true},
  {c:['Học thêm không RL','52,07','37,75','68,55','425,79','45,33','62,64','67,05'],base:true},
  {c:['S1','51,56','36,79','67,35','416,12','44,37','61,26','66,33'],base:true}];

// 19 · Phần thưởng: biểu đồ
newSlide('So sánh RL','Đổi phần thưởng, giữ thuật toán GRPO');
addText('Executability, và số điểm hơn S1',{x:M,y:0.8,w:8.9,h:0.35,fontSize:13,color:GREY});
hbarChart(M,1.25,8.9,[
  {label:'SA-SPICE-v3 †',value:2.11,text:'61,21   +2,11',color:FOOTD},
  {label:'SPICE †',value:1.77,text:'60,88   +1,77',color:FOOTC,bold:true},
  {label:'ROUGE-L',value:1.52,text:'60,63   +1,52',color:FOOTD},
  {label:'METEOR',value:1.17,text:'60,27   +1,17',color:FOOTD},
  {label:'CIDEr-D',value:1.17,text:'60,27   +1,17',color:FOOTD},
  {label:'SPICE ghép ngẫu nhiên',value:0.0,text:'59,11   +0,00',color:'A9A4B8'},
  {label:'Học thêm không RL',value:1.05,text:'60,16   +1,05',color:'A9A4B8'}
],{labelW:2.3,valueW:1.75,rowH:0.56,max:2.3,fs:13.5});
rect(M,5.3,8.9,0.95,SOFT,{radius:0.06});
addText('Ghép ngẫu nhiên điểm SPICE giữa các câu thì mô hình bằng đúng S1 (59,11): mức tăng đến từ nội dung phần thưởng.',{x:M+0.2,y:5.3,w:8.5,h:0.95,fontSize:13.5,bold:true,color:FOOTB,valign:'mid'});
source(DAGGER+' S1 = 59,11.');
note(`- Hàng ghép ngẫu nhiên là phép kiểm quan trọng nhất: cùng vòng lặp GRPO, chỉ khác là phần thưởng không mang thông tin.
- SPICE, ROUGE-L, METEOR, CIDEr-D có khoảng tin cậy chồng nhau; không viết SPICE là tốt nhất.`);
foot();

// 20 · Phần thưởng: bảng vị trí
newSlide('So sánh RL','Đổi phần thưởng: số theo tiêu chí vị trí');
numTable(0.95,POS_HEAD,[2.4,1.3,1.4,1.25,1.3,1.25],RW_POS);
addText('SA-SPICE-v3 dẫn ba cột vị trí, SPICE đứng thứ hai; ROUGE-L viết đúng loại thao tác nhiều nhất.',{x:M,y:5.45,w:8.9,h:0.75,fontSize:13.5,bold:true,color:FOOTB});
source('% trên 4.463 bước chạm. '+DAGGER+' Đậm: cao nhất trong các lượt RL.');
note(`- SA-SPICE-v3 và SPICE cùng xuất phát nên so trực tiếp được: chênh 0,34 điểm, chưa có ý nghĩa.`);
foot();

// 21 · Phần thưởng: bảng văn bản
newSlide('So sánh RL','Đổi phần thưởng: số theo độ đo văn bản');
numTable(0.95,TXT_HEAD,[2.3,0.95,0.95,0.95,1.0,0.9,0.9,0.95],RW_TXT,{fs:12});
addText('Thưởng SPICE cao nhất ở ROUGE-L, CIDEr-D, SPICE, BERTScore, và bằng lượt thưởng ROUGE-L ở BLEU-4 (52,59). SA-SPICE-v3 cao nhất ở METEOR và chrF.',{x:M,y:5.45,w:8.9,h:0.75,fontSize:13.5,bold:true,color:FOOTB});
source('Bộ chấm COCO, mức kho trên 4.463 bước chạm; BERTScore đã chuẩn hoá. '+DAGGER);
note(`- Thưởng bằng CIDEr-D lại thấp ở chính CIDEr-D (424,52); đã kiểm cách tính IDF và tách từ, chưa giải thích được.`);
foot();

// 22 · SA-SPICE-v3
newSlide('So sánh RL','Phần thưởng trộn SA-SPICE-v3');
addText('SA-SPICE-v3 trộn SPICE với chrF và cộng thưởng khi câu đúng loại thao tác, vì với câu ngắn như “Scroll down” SPICE cho 0 dù câu đúng.',{x:M,y:0.9,w:8.9,h:0.9,fontSize:14});
[['61,21','SA-SPICE-v3','Executability cao nhất mọi lượt đã huấn luyện.',FOOTC,HL],
 ['60,88','SPICE','Cùng điểm xuất phát, thấp hơn SA-SPICE-v3 0,34 điểm (chưa có ý nghĩa) và cao hơn ở 5/7 độ đo văn bản.',FOOTB,SOFT],
 ['71,1 → 58,5','Bước quay lại','SA-SPICE-v3 làm giảm điểm ở bước quay lại (không chạm).',FOOTD,SOFT]].forEach((d,i)=>{
  const x=M+i*3.0; rect(x,2.0,2.8,3.3,d[4],{radius:0.06});
  addText(d[0],{x,y:2.15,w:2.8,h:0.75,fontSize:i===2?22:28,bold:true,color:d[3],align:'center',valign:'mid'});
  addText(d[1],{x:x+0.15,y:2.95,w:2.5,h:0.55,fontSize:14.5,bold:true,color:FOOTB,align:'center',valign:'mid',fit:'shrink'});
  addText(d[2],{x:x+0.15,y:3.6,w:2.5,h:1.6,fontSize:13,align:'center',valign:'top'});
});
addText('Trộn phần thưởng chưa cho lợi ích rõ so với SPICE.',{x:M,y:5.65,w:8.9,h:0.5,fontSize:15.5,bold:true,color:FOOTB});
note(`- SA-SPICE-v3 hơn mô hình học thêm không RL 1,05 điểm [+0,46; +1,65]; SPICE hơn 0,72 [+0,24; +1,20].
- Bước quay lại giảm nên phải khai; hướng chữa nằm ngoài phần thưởng.`);
foot();

// 18 · Hạn chế
newSlide('Kết luận','Hạn chế');
[['Mức tăng nhỏ, phần lớn một hạt giống','Khoảng 1,5 điểm, dưới mức phát hiện tối thiểu 2,1 điểm của thiết kế. Hạt giống thứ hai chỉ hơn S1 0,83.'],
 ['Bước không chạm bị ảnh hưởng','Bước cuộn giảm từ 83,97 xuống 77,75: mô hình dịch dần về câu chạm.'],
 ['Đánh giá qua mô hình','Chưa có người dùng thật làm theo. UGround và UI-Venus cùng họ Qwen; hai bộ ngoài họ cho cùng chiều nhưng mức nhỏ hơn.'],
 ['Lợi ích của SPICE phụ thuộc miền','Trên AitZ, GRPO-SPICE ngang S1.']].forEach((c,i)=>{
  card(M+(i%2)*4.55,0.95+Math.floor(i/2)*2.3,4.35,2.05,c[0],c[1],{tfs:15,fs:13.5,th:0.5});
});
note(`- Khai thẳng các hạn chế kèm số đo.
- Hướng tiếp: thêm hạt giống, chữa bước không chạm; DPO trực tuyến đã huấn luyện xong, đang chờ chấm.`);
foot();

// 19 · Kết luận
newSlide('Kết luận','Kết luận');
['Executability chấm câu bằng việc làm theo, và phản ứng đúng với nội dung câu: trần 75,7, sàn 12,0.',
 'GRPO-SPICE đạt 60,65%, hơn S1 1,55 điểm [+0,80; +2,33]; ACE giữ mức đó và cải thiện cả bảy độ đo văn bản. Lượt GRPO + SPICE mới từ SFT tiếp đạt 60,88%.',
 'Học tăng cường có ích nhờ nội dung phần thưởng: ghép điểm ngẫu nhiên thì không tăng. Các thuật toán và độ đo thưởng phổ biến cho mức tăng gần nhau; GRPO-SPICE thuộc nhóm dẫn đầu ở cả hai phép so.'].forEach((t,i)=>{
  const y=1.0+i*1.6; rect(M,y,0.75,0.75,FOOTC,{radius:0.08});
  addText(String(i+1),{x:M,y,w:0.75,h:0.75,fontSize:22,bold:true,color:WHITE,align:'center',valign:'mid'});
  addText(t,{x:M+1.0,y:y-0.1,w:7.9,h:1.3,fontSize:16,valign:'mid'});
});
addText('Xin cảm ơn.',{x:M,y:5.9,w:8.9,h:0.6,fontSize:20,bold:true,color:FOOTB,align:'center'});
note(`- Ba ý chính. Mời hội đồng đặt câu hỏi.`);
foot();

pptx.writeFile({ fileName:path.join(__dirname, '..', 'LUAN_VAN_SLIDE_THUYET_TRINH.pptx') }).then(()=>{
  const md=['# Kịch bản thuyết trình luận văn (18/11/2026)','','Đi kèm `slides/LUAN_VAN_SLIDE_THUYET_TRINH.pptx`. Sinh tự động từ ghi chú trong `slides/build/build_thuyet_trinh.js`; sửa lời ở script, không sửa tay file này.',''];
  NOTES.forEach(n=>{ md.push(`## Slide ${n.page}`); md.push(n.t); md.push(''); });
  fs.writeFileSync(path.join(__dirname,'..','KICH_BAN_THUYET_TRINH.md'),md.join('\n'));
  console.log('PAGE',PAGE,'notes',NOTES.length);
});
