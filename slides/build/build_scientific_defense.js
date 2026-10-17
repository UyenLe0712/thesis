// Scientific thesis-defense deck, generated from the current thesis (Oct 2026).
// Keeps the user's existing 4:3 template: navy title bar, Cambria, gray rounded blocks, 4-cell footer.
// Scientific-slide principles: one claim per slide, visual-first, evidence chain, minimal prose, backup slides.
// Output: ../LUAN_VAN_SLIDE_BAO_VE_SCIENTIFIC.pptx
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

const pres = new pptxgen();
pres.defineLayout({ name: 'A43', width: 10, height: 7.5 });
pres.layout = 'A43';
pres.author = 'Le Doan Phuong Uyen';
pres.subject = 'Master thesis defense';
pres.title = 'Phat sinh tu dong huong dan su dung phan mem dua tren LLM - scientific defense';
pres.company = 'VNU-HCM University of Science';
pres.lang = 'vi-VN';

const TF='Cambria', MONO='Consolas';
const NAVY='322164', INK='1A1A1A', WHITE='FFFFFF';
const FOOTA='191132', FOOTB='25194B', FOOTC='4F417A', FOOTD='7A7099';
const BLOCK='E9E8EC', TEAL='006666', BLUE='1414BE', RED='B22222', MAROON='990000';
const GREY='5A5A66', LIGHT='F5F4F7', GREEN='1B7F5B', ORANGE='C75C24', PALE_GREEN='E5F1EC', PALE_RED='F6E7E7';
const W=10, H=7.5, M=0.5, PX=96;
const FIG = path.resolve(__dirname, '../../thesis/figures');
const FMAP={Cambria:"'DejaVu Serif',Georgia,serif",Consolas:"'DejaVu Sans Mono',monospace"};
let s, PAGE=0, BPAGE=0, TOTAL=21, htmlSlides=[], cur='';

function esc(t){return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function plain(c){return typeof c==='string'?c:c.map(r=>r.text+(r.options&&r.options.breakLine?'\n':'')).join('');}
function hpush(h){cur+=h;}
function slide(bg=WHITE){if(cur) htmlSlides.push(cur+'</div>'); s=pres.addSlide(); s.background={color:bg}; cur=`<div class="slide" style="background:#${bg}">`;}
function done(){if(cur){htmlSlides.push(cur+'</div>');cur='';}}
function text(content,o={}){
  const opt=Object.assign({x:0,y:0,w:4,h:1,fontSize:13,color:INK,fontFace:TF,align:'left',valign:'top',margin:o.margin!=null?o.margin:4},o);
  if(o.lh) opt.lineSpacingMultiple=o.lh;
  s.addText(content,opt);
  const jc=opt.align==='center'?'center':opt.align==='right'?'flex-end':'flex-start';
  const ai=opt.valign==='middle'?'center':opt.valign==='bottom'?'flex-end':'flex-start';
  const st=`position:absolute;left:${opt.x*PX}px;top:${opt.y*PX}px;width:${opt.w*PX}px;height:${opt.h*PX}px;display:flex;justify-content:${jc};align-items:${ai};padding:${(opt.margin||0)/72}in;box-sizing:border-box;font-family:${FMAP[opt.fontFace]||FMAP[TF]};font-size:${(opt.fontSize*1.333).toFixed(1)}px;color:#${opt.color};text-align:${opt.align};line-height:${o.lh||1.2};${opt.bold?'font-weight:700;':''}${opt.italic?'font-style:italic;':''}`;
  hpush(`<div style="${st}"><div style="white-space:pre-line;width:100%">${esc(plain(content))}</div></div>`);
}
function rect(x,y,w,h,fill,o={}){
  const shp=o.radius?pres.shapes.ROUNDED_RECTANGLE:pres.shapes.RECTANGLE;
  const p={x,y,w,h,fill:fill==='none'?{type:'none'}:{color:fill},line:o.line?{color:o.line,width:o.lw||1}:{type:'none'}};
  if(o.shadow) p.shadow={type:'outer',color:'8C8C99',blur:5,offset:2.5,angle:45,opacity:0.35};
  s.addShape(shp,p);
  hpush(`<div style="position:absolute;left:${x*PX}px;top:${y*PX}px;width:${w*PX}px;height:${h*PX}px;${fill==='none'?'':`background:#${fill};`}${o.radius?`border-radius:${o.radius*PX}px;`:''}${o.line?`border:${o.lw||1}px solid #${o.line};box-sizing:border-box;`:''}"></div>`);
}
function line(x,y,w,h,c='9A94AE',lw=1,dash=false,endArrow=false){
  s.addShape(pres.shapes.LINE,{x,y,w,h,line:{color:c,width:lw,dashType:dash?'dash':'solid',endArrowType:endArrow?'triangle':'none'}});
  hpush(`<div style="position:absolute;left:${x*PX}px;top:${y*PX}px;width:${w*PX}px;height:${h*PX}px;border-top:${lw}px ${dash?'dashed':'solid'} #${c}"></div>`);
}
function arrow(x,y,w,c=FOOTC,lw=2){line(x,y,w,0,c,lw,false,true);}
function img(file,x,y,w,h){s.addImage({path:file,x,y,w,h});hpush(`<img src="file://${file}" style="position:absolute;left:${x*PX}px;top:${y*PX}px;width:${w*PX}px;height:${h*PX}px">`);}
function imgFit(file,pw,ph,x,y,w,h){const r=Math.min(w/pw,h/ph),ww=pw*r,hh=ph*r;img(file,x+(w-ww)/2,y+(h-hh)/2,ww,hh);}
function note(t){s.addNotes(t.trim());}
function bar(t){rect(0,0,W,0.6,NAVY);text(t,{x:0.22,y:0,w:W-0.44,h:0.6,fontSize:19,bold:true,color:WHITE,valign:'middle',margin:0});}
function footRow(label){const yy=H-0.26,hh=0.26;rect(0,yy,3.0,hh,FOOTA);rect(3.0,yy,3.7,hh,FOOTB);rect(6.7,yy,1.9,hh,FOOTC);rect(8.6,yy,1.4,hh,FOOTD);text('Luận văn thạc sĩ',{x:0,y:yy,w:3,h:hh,fontSize:8,bold:true,color:WHITE,align:'center',valign:'middle',margin:0,fontFace:MONO});text('Phát sinh tự động hướng dẫn sử dụng phần mềm dựa trên LLM',{x:3,y:yy,w:3.7,h:hh,fontSize:8,color:WHITE,align:'center',valign:'middle',margin:0});text('Lê Đoàn Phương Uyên',{x:6.7,y:yy,w:1.9,h:hh,fontSize:8,color:WHITE,align:'center',valign:'middle',margin:0});text(label,{x:8.6,y:yy,w:1.4,h:hh,fontSize:8,color:WHITE,align:'center',valign:'middle',margin:0});}
function foot(){PAGE++;footRow(`${PAGE}/${TOTAL}`);} function footB(){BPAGE++;footRow(`dự phòng ${BPAGE}`);}
function block(x,y,w,h,fill=BLOCK){rect(x,y,w,h,fill,{radius:0.06,shadow:true});}
function box(x,y,w,h,t,o={}){rect(x,y,w,h,o.fill||WHITE,{radius:0.06,line:o.line||'6E6890',lw:o.lw||1.2});text(t,{x,y,w,h,fontSize:o.fs||11.5,align:'center',valign:'middle',bold:o.bold,color:o.color||INK,margin:3,lh:o.lh||1.15});}
function bullet(t,x,y,w,o={}){text('•',{x,y,w:0.22,h:o.h||0.5,fontSize:o.fs||13,color:o.dot||TEAL,bold:true,margin:0});text(t,{x:x+0.25,y,w:w-0.25,h:o.h||0.5,fontSize:o.fs||13,color:o.color||INK,margin:0,lh:o.lh||1.2});}
function bullets(items,x,y,w,o={}){const gap=o.gap||0.62;items.forEach((it,i)=>bullet(it,x,y+i*gap,w,{fs:o.fs||13,h:o.itemH||gap,lh:o.lh||1.2,dot:o.dot}));}
function cite(t){text(t,{x:M,y:6.90,w:W-2*M,h:0.18,fontSize:8.2,italic:true,color:GREY,align:'right',margin:0});}
function sectionTag(t){text(t.toUpperCase(),{x:M,y:0.72,w:2.2,h:0.24,fontSize:9.5,bold:true,color:TEAL,margin:0});}
function claim(t,sub=''){text(t,{x:M,y:0.92,w:W-2*M,h:0.72,fontSize:22,bold:true,color:NAVY,margin:0,lh:1.1}); if(sub) text(sub,{x:M,y:1.64,w:W-2*M,h:0.45,fontSize:12.5,color:GREY,margin:0,lh:1.2});}
function tile(x,y,w,h,big,small,o={}){block(x,y,w,h,o.fill||BLOCK);text(big,{x:x+0.14,y:y+0.08,w:w-0.28,h:0.5,fontSize:o.bf||19,bold:true,color:o.color||NAVY,align:o.align||'left',margin:0});text(small,{x:x+0.14,y:y+0.6,w:w-0.28,h:h-0.68,fontSize:o.sf||11.5,color:o.smallColor||INK,align:o.align||'left',margin:0,lh:1.18});}
function labelPill(x,y,w,t,fill=TEAL){rect(x,y,w,0.28,fill,{radius:0.08});text(t,{x,y,w,h:0.28,fontSize:9,bold:true,color:WHITE,align:'center',valign:'middle',margin:0});}
function hbar(x,y,w,val,max,label,value,color=NAVY){text(label,{x,y:y-0.02,w:2.75,h:0.32,fontSize:11.7,margin:0,valign:'middle'});rect(x+2.85,y,w,0.27,'DDDBE4');rect(x+2.85,y,w*(val/max),0.27,color);text(value,{x:x+2.85+w+0.12,y:y-0.04,w:0.8,h:0.34,fontSize:12.5,bold:true,color,margin:0,valign:'middle'});}
function ciRow(y,label,mid,lo,hi,color=NAVY){const x0=4.25,scale=1.0; text(label,{x:M,y:y-0.09,w:3.25,h:0.3,fontSize:11.8,margin:0}); const map=v=>x0+(v+1)*scale; line(map(lo),y,map(hi)-map(lo),0,color,3); rect(map(mid)-0.05,y-0.05,0.1,0.1,color,{radius:0.04});}
function table(x,y,colW,rows,o={}){let yy=y;const fs=o.fs||11.5;rows.forEach(r=>{const h=r.h||0.38; if(r.fill)rect(x,yy,colW.reduce((a,b)=>a+b,0),h,r.fill);let xx=x;r.cells.forEach((c,i)=>{const cell=typeof c==='string'?{t:c}:c;text(cell.t,{x:xx,y:yy,w:colW[i],h,fontSize:cell.fs||r.fs||fs,bold:cell.bold!=null?cell.bold:r.bold,color:cell.color||r.color||INK,align:cell.align||(o.align&&o.align[i])||'left',valign:'middle',margin:3,italic:cell.italic});xx+=colW[i];});if(r.rule)line(x,yy+h,colW.reduce((a,b)=>a+b,0),0,r.rule===true?'9A94AE':r.rule,r.ruleW||1);yy+=h;});return yy;}

// 1. COVER
slide();rect(0,0,W,0.66,NAVY);text('ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH  -  TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN',{x:0,y:0,w:W,h:0.66,fontSize:14,bold:true,color:WHITE,align:'center',valign:'middle',margin:0});rect(0.8,1.18,W-1.6,2.5,NAVY,{radius:0.09,shadow:true});text('LUẬN VĂN THẠC SĨ  ·  NGÀNH TRÍ TUỆ NHÂN TẠO',{x:0.8,y:1.46,w:W-1.6,h:0.35,fontSize:14,bold:true,color:WHITE,align:'center',margin:0});text('PHÁT SINH TỰ ĐỘNG HƯỚNG DẪN SỬ DỤNG PHẦN MỀM\nDỰA TRÊN LLM TỪ CÁC TRƯỜNG HỢP SỬ DỤNG\nVÀ GIAO DIỆN NGƯỜI DÙNG',{x:0.9,y:1.95,w:W-1.8,h:1.45,fontSize:21,bold:true,color:WHITE,align:'center',margin:0,lh:1.2});text('LLM-Based Automatic Generation of Software User Guides from Use Cases and Front-End Structures',{x:0.8,y:3.82,w:W-1.6,h:0.4,fontSize:11.5,italic:true,color:GREY,align:'center',margin:0});text('Học viên:  Lê Đoàn Phương Uyên',{x:0.8,y:4.55,w:W-1.6,h:0.4,fontSize:15,bold:true,align:'center',margin:0});text('GVHD:  TS. Nguyễn Hồng Bửu Long',{x:0.8,y:5.0,w:W-1.6,h:0.4,fontSize:15,bold:true,align:'center',margin:0});text('TP. Hồ Chí Minh  ·  2026',{x:0.8,y:5.75,w:W-1.6,h:0.35,fontSize:12,align:'center',margin:0});note('Em xin trình bày luận văn theo mạch: bài toán, cách đo, phương pháp, bằng chứng thực nghiệm và giới hạn.');foot();

// 2. PROBLEM
slide();bar('Bài toán: đầu ra là câu hướng dẫn cho người dùng');sectionTag('Problem');claim('Cùng một màn hình, GUI agent và luận văn giải hai đầu ra khác nhau.','Đề tài đánh giá chất lượng của câu hướng dẫn, không đánh giá tọa độ do chính mô hình sinh ra.');
box(M,2.28,4.18,1.2,'GUI agent\n→ click(872, 141)',{fs:17,bold:true,fill:LIGHT,line:FOOTC});box(5.32,2.28,4.18,1.2,'Luận văn\n→ “Tap the share icon at the top right.”',{fs:14,bold:true,fill:'EEEAF6',line:NAVY,lw:1.7});
text('Máy tự thao tác',{x:M,y:3.62,w:4.18,h:0.35,fontSize:12.5,bold:true,color:GREY,align:'center',margin:0});text('Con người đọc và thao tác',{x:5.32,y:3.62,w:4.18,h:0.35,fontSize:12.5,bold:true,color:TEAL,align:'center',margin:0});
block(M,4.25,W-2*M,1.45);text('Thách thức khoa học',{x:M+0.2,y:4.4,w:2.0,h:0.32,fontSize:13.5,bold:true,color:NAVY,margin:0});bullets(['Một nút có nhiều cách gọi đều đúng → không thể chấm bằng một câu chuẩn duy nhất.','Lỗi chính không phải “bịa nút”, mà là câu mơ hồ giữa các phần tử giống nhau.'],M+2.15,4.34,W-2*M-2.35,{fs:12.5,gap:0.62,itemH:0.58});cite('SeeClick; OS-Atlas; Aguvis · Luận văn Ch.1');note('Điểm khác biệt của đề tài là đầu ra cuối cùng chính là câu hướng dẫn. Khi đó hai câu khác chữ vẫn có thể cùng đúng nếu cùng dẫn tới đúng phần tử.');foot();

// 3. WHY TEXT METRICS FAIL
slide();bar('Không thể chỉ dùng độ giống câu để chấm hướng dẫn');sectionTag('Problem');claim('“Đúng nghĩa chung” không đồng nghĩa với “chỉ đúng phần tử”.','Các thước dựa trên chuỗi hoặc embedding dễ thưởng/phạt sai điều quan trọng nhất: phần tử mà câu đang nói tới.');
tile(M,2.25,2.75,1.55,'97,5%','câu diễn đạt khác nhưng cùng chỉ đúng phần tử bị phép so chuỗi loại nhầm',{color:RED,bf:22});tile(3.63,2.25,2.75,1.55,'AUC 0,336','so vector ngữ nghĩa trên 51 trường hợp viết tay — thấp hơn ngẫu nhiên',{color:RED,bf:22});tile(6.76,2.25,2.74,1.55,'0,76 > 0,55','inbox/outbox gần embedding hơn search/magnifying glass dù chỉ cặp sau cùng một nút',{color:MAROON,bf:20});
block(M,4.15,W-2*M,1.35,'EEEAF6');text('Research gap',{x:M+0.2,y:4.32,w:1.5,h:0.3,fontSize:13.5,bold:true,color:NAVY,margin:0});text('Cần một thước đo hỏi trực tiếp: “Câu này có khiến một người nghe độc lập tìm đúng phần tử cần chạm không?”',{x:M+1.65,y:4.25,w:W-2*M-1.85,h:0.65,fontSize:15,bold:true,color:NAVY,margin:0,lh:1.25});cite('Luận văn Ch.1–2 · Zhao et al., EACL 2021');note('Đây là lý do thesis không lấy BLEU/ROUGE làm số chính. Chúng vẫn được báo kèm, nhưng quyết định mô hình tốt hơn dựa trên executability.');foot();

// 4. QUESTIONS + CONTRIBUTIONS
slide();bar('Ba đóng góp xoay quanh một câu hỏi trung tâm');sectionTag('Research questions');claim('Làm sao viết câu ngắn nhưng đủ phân biệt để người nghe tìm đúng phần tử?');
const cards=[['1','Phương pháp','GRPO thưởng SPICE + ACE tác động trực tiếp vào câu cuối.'],['2','Độ đo','Executability: listener độc lập → tọa độ → đúng/sai.'],['3','Phân tích','Các hướng thất bại cho biết nút thắt nằm ở đâu và vì sao phải đổi hướng.']];cards.forEach((c,i)=>{const x=M+i*3.0;block(x,2.45,2.8,2.45,i===0?'EEEAF6':BLOCK);text(c[0],{x:x+0.12,y:2.58,w:0.48,h:0.48,fontSize:24,bold:true,color:i===0?NAVY:TEAL,align:'center',margin:0});text(c[1],{x:x+0.65,y:2.62,w:1.95,h:0.35,fontSize:14.5,bold:true,color:NAVY,margin:0});text(c[2],{x:x+0.2,y:3.25,w:2.4,h:1.2,fontSize:12.5,margin:0,lh:1.3});});
block(M,5.25,W-2*M,0.9);text('Scientific story',{x:M+0.2,y:5.38,w:1.4,h:0.3,fontSize:12.5,bold:true,color:TEAL,margin:0});text('Đo đúng → cải thiện trực tiếp câu → kiểm bằng nhiều listener/rule → công khai giới hạn. ',{x:M+1.55,y:5.32,w:W-2*M-1.75,h:0.42,fontSize:13.5,bold:true,color:NAVY,margin:0});cite('Luận văn §1.6');foot();

// 5. DATA
slide();bar('Dữ liệu được dựng tự động, không bổ sung nhãn thủ công');sectionTag('Data');claim('64.567 bước huấn luyện được tạo từ nhãn có sẵn của AndroidControl.','Tập kiểm tra giữ riêng theo tác vụ; mọi mô hình được chấm trên cùng một tập.');
tile(M,2.28,2.0,1.35,'64.567','bước huấn luyện',{color:NAVY});tile(2.66,2.28,2.0,1.35,'6.958','bước kiểm tra',{color:NAVY});tile(4.82,2.28,2.0,1.35,'4.463','bước chạm dùng cho executability',{color:TEAL});tile(6.98,2.28,2.0,1.35,'1.432','tác vụ kiểm tra',{color:TEAL});
box(M,4.1,2.0,0.82,'AndroidControl\nlabels',{fs:11.5});arrow(2.55,4.5,0.55);box(3.15,4.1,2.0,0.82,'ghép ảnh + OCR\n+ cây trợ năng',{fs:11.5,fill:LIGHT});arrow(5.2,4.5,0.55);box(5.8,4.1,1.65,0.82,'kiểm cấu trúc\n+ rò rỉ',{fs:11.5});arrow(7.5,4.5,0.55);box(8.1,4.1,1.4,0.82,'train / test',{fs:11.5,bold:true,line:NAVY});
text('Không tác vụ nào trùng giữa train và test.',{x:M,y:5.35,w:W-2*M,h:0.45,fontSize:14,bold:true,color:TEAL,align:'center',margin:0});cite('AndroidControl · Luận văn Ch.3');foot();

// 6. BASELINE
slide();bar('Tinh chỉnh có giám sát tạo mốc mạnh nhưng vẫn còn khoảng cách lớn');sectionTag('Baseline');claim('S1 tăng +11,5 pp so với mô hình gốc, nhưng còn cách câu chuẩn 16,6 pp.','Qwen2.5-VL-3B + QLoRA, hai hạt giống 101/202; mọi so sánh sau đều ghép cặp trên cùng 4.463 bước.');
hbar(M,2.45,4.55,47.6,80,'Base','47,6%',FOOTC);hbar(M,3.15,4.55,59.1,80,'S1 / seed 101','59,1%',NAVY);hbar(M,3.85,4.55,59.6,80,'S1 / seed 202','59,6%',TEAL);hbar(M,4.55,4.55,75.7,80,'Câu chuẩn (ceiling)','75,7%',GREEN);
block(M,5.4,W-2*M,0.72);text('Seed variance: +0,52 pp  [−0,22; +1,26]  ·  S1 − Base: +11,5 pp  [ +10,0; +13,1 ]',{x:M+0.18,y:5.4,w:W-2*M-0.36,h:0.72,fontSize:12.5,bold:true,color:NAVY,align:'center',valign:'middle',margin:0});cite('Qwen2.5-VL-3B · QLoRA · Luận văn §4.3, §6.7');foot();

// 7. EXECUTABILITY
slide();bar('Executability hỏi trực tiếp câu có dẫn tới đúng phần tử hay không');sectionTag('Metric');claim('Sentence → independent listener → point → correctness.');
box(M,2.0,1.7,0.9,'câu sinh ra',{fs:13,bold:true});arrow(2.25,2.45,0.45);box(2.75,2.0,2.05,0.9,'UGround-V1-2B\n(listener độc lập)',{fs:11.5,bold:true,fill:'EEEAF6',line:NAVY,lw:1.5});arrow(4.85,2.45,0.45);box(5.35,2.0,1.45,0.9,'điểm (x,y)',{fs:13,bold:true});arrow(6.85,2.45,0.45);box(7.35,2.0,2.15,0.9,'đúng phần tử?\nđúng thao tác?\nkhông đảo nghĩa?',{fs:11,bold:true,fill:LIGHT});
block(M,3.45,W-2*M,1.75);text('Một bước = đúng khi đồng thời',{x:M+0.2,y:3.62,w:2.5,h:0.3,fontSize:13.5,bold:true,color:NAVY,margin:0});bullets(['đúng loại thao tác (tap / type / scroll / back / …)','không đảo nghĩa (on/off, show/hide, …)','điểm nằm trong dung sai 14% và trong ô Voronoi của phần tử cần chạm'],M+2.55,3.55,W-2*M-2.75,{fs:12.5,gap:0.48,itemH:0.45});
text('Listener không biết tọa độ đáp án và không tham gia huấn luyện phương pháp.',{x:M,y:5.55,w:W-2*M,h:0.42,fontSize:13.5,bold:true,color:TEAL,align:'center',margin:0});cite('Mao et al. 2016; UGround · Luận văn Ch.5');foot();

// 8. VORONOI
slide();bar('Luật Voronoi loại được lỗi “chỉ sang nút bên cạnh”');sectionTag('Metric design');claim('Dung sai ±14% quá rộng: 84,3% câu chỉ sai nút vẫn có thể được tính đúng.');
imgFit(path.join(FIG,'fig_voronoi.png'),1080,740,M,2.05,5.1,3.5);block(5.95,2.05,3.55,3.5);
text('Sai nút gần nhất',{x:6.18,y:2.28,w:3.1,h:0.35,fontSize:14,bold:true,color:RED,margin:0});tile(6.18,2.82,1.35,1.05,'84,3%','±14% vẫn chấp nhận',{bf:19,sf:10.5,color:RED});tile(7.78,2.82,1.35,1.05,'2,8%','Voronoi chấp nhận',{bf:19,sf:10.5,color:TEAL});text('Ngưỡng tối đa của Voronoi khi điểm chỉ lệch 3% vẫn đạt 99,7%.',{x:6.18,y:4.23,w:3.1,h:0.65,fontSize:12.5,bold:true,color:NAVY,margin:0,lh:1.25});cite('Luận văn §5.2 · AndroidInTheWild tolerance rule');foot();

// 9. VALIDATION
slide();bar('Trước khi dùng executability, luận văn kiểm chính dụng cụ đo');sectionTag('Metric validation');claim('Ceiling cao, floor thấp, và thứ tự mô hình bền qua listener/rule khác.');
const vcards=[['75,7%','câu chuẩn'],['12,0%','“Tap the button.”'],['6,1%','câu đúng văn phong nhưng sai màn'],['94%','độ lớn S1−Base còn giữ khi đổi sang UI-Venus']];vcards.forEach((c,i)=>tile(M+i*2.25,2.2,2.05,1.3,c[0],c[1],{color:i===0?GREEN:(i===3?TEAL:RED),bf:20,sf:10.8,align:'center'}));
block(M,3.85,W-2*M,1.7);bullets(['10 kiểu lỗi chèn có kiểm soát: metric giảm đúng chiều.','1.139 câu viết lại giữ nghĩa: Δ = +0,35 pp, KTC [−0,59; +1,29].','Phi-4 listener ngoài họ Qwen vẫn giữ thứ tự giữa các mô hình.'],M+0.25,4.0,W-2*M-0.5,{fs:12.7,gap:0.48,itemH:0.46});
text('Kết luận sử dụng: đọc điểm mô hình so với ceiling 75,7%, không so với 100%.',{x:M,y:5.9,w:W-2*M,h:0.38,fontSize:13.5,bold:true,color:NAVY,align:'center',margin:0});cite('Luận văn §5.5–§5.10');foot();

// 10. METHOD OVERVIEW
slide();bar('Phương pháp đề xuất: cải thiện trực tiếp câu ở đầu ra');sectionTag('Method');claim('Hai thành phần nối tiếp: GRPO + SPICE tạo câu nháp, ACE chỉ chép exemplar khi đủ an toàn.');
box(M,2.0,1.65,0.95,'S1\n59,1%',{fs:14,bold:true});arrow(2.2,2.48,0.45);box(2.72,1.8,2.2,1.35,'1 · GRPO\nreward = SPICE\n→ draft sentence',{fs:12.5,bold:true,fill:'EEEAF6',line:NAVY,lw:1.7});arrow(4.98,2.48,0.45);box(5.5,1.8,2.2,1.35,'2 · ACE\nretrieve 4 exemplars\n+ consensus rule',{fs:12.2,bold:true,fill:PALE_GREEN,line:TEAL,lw:1.7});arrow(7.77,2.48,0.45);box(8.28,2.0,1.22,0.95,'final\nsentence',{fs:12.5,bold:true,line:NAVY,lw:1.5});
block(M,3.7,W-2*M,1.8);text('Thiết kế độc lập với metric',{x:M+0.2,y:3.88,w:2.1,h:0.3,fontSize:13.5,bold:true,color:NAVY,margin:0});bullets(['Phần thưởng chỉ dùng SPICE + phạt độ dài; UGround không xuất hiện trong reward.','ACE không thấy câu chuẩn của bước test; chỉ truy hồi câu chuẩn từ train.','Nếu consensus không đạt, giữ nguyên câu nháp.'],M+2.0,3.82,W-2*M-2.2,{fs:12.5,gap:0.5,itemH:0.46});cite('GRPO: Shao et al. 2024 · SPICE: Anderson et al. 2016 · Luận văn Ch.4');foot();

// 11. GRPO
slide();bar('Thành phần 1: GRPO thưởng câu nào “nói đúng nội dung hơn”');sectionTag('Method · component 1');claim('Mỗi prompt sinh 8 câu; câu có SPICE cao hơn trung bình nhóm được tăng xác suất.');
const steps=[['1','Sample','8 câu / prompt, temperature = 1.0'],['2','Reward','SPICE(sentence, reference) − length penalty'],['3','Advantage','so với trung bình 8 câu cùng prompt'],['4','Update','GRPO + KL β = 0,04 để không lệch xa S1']];steps.forEach((c,i)=>{const y=2.05+i*0.82;labelPill(M,y,0.45,c[0],i===1?TEAL:NAVY);text(c[1],{x:M+0.62,y:y-0.01,w:1.2,h:0.3,fontSize:13,bold:true,color:NAVY,margin:0});text(c[2],{x:M+1.72,y:y-0.01,w:4.2,h:0.42,fontSize:12.4,margin:0});if(i<3)line(M+0.22,y+0.31,0,0.48,FOOTC,1.5,true,false);});
block(6.55,2.05,2.95,3.35,'EEEAF6');text('Reward',{x:6.8,y:2.25,w:2.45,h:0.32,fontSize:14,bold:true,color:NAVY,align:'center',margin:0});text('r(s) = SPICE(s,g)\n− 0,02 · max(0, |s|−|g|−3)',{x:6.75,y:2.9,w:2.55,h:1.0,fontSize:15,bold:true,color:BLUE,align:'center',valign:'middle',margin:0,fontFace:MONO});text('500 updates · 1.000 prompts\nLR = 1e−5 · starting from S1/101',{x:6.8,y:4.35,w:2.45,h:0.72,fontSize:11.5,align:'center',margin:0,lh:1.3});cite('Luận văn §4.5');foot();

// 12. SPICE EXAMPLE
slide();bar('Một thay đổi nhỏ trong câu có thể sửa đúng phần tử');sectionTag('Evidence · component 1');claim('GRPO thưởng SPICE sửa cả lỗi loại thao tác lẫn lỗi gọi sai phần tử.');
imgFit(path.join(FIG,'fig_vidu_spice.png'),1500,1660,M,1.9,4.05,4.55);block(4.85,1.9,4.65,4.55);
text('Cần chạm',{x:5.1,y:2.12,w:1.1,h:0.3,fontSize:12,bold:true,color:GREY,margin:0});text('Not now',{x:6.22,y:2.12,w:2.6,h:0.3,fontSize:14,bold:true,color:TEAL,margin:0});
text('S1',{x:5.1,y:2.85,w:0.75,h:0.32,fontSize:13,bold:true,color:RED,margin:0});text('“Click on the Allow button …”',{x:5.9,y:2.78,w:3.1,h:0.55,fontSize:13,color:RED,italic:true,margin:0});
line(5.1,3.45,3.95,0,'B7B3C1',1);
text('GRPO + SPICE',{x:5.1,y:3.72,w:1.45,h:0.32,fontSize:13,bold:true,color:TEAL,margin:0});text('“Click on Not now at the bottom …”',{x:6.55,y:3.65,w:2.7,h:0.65,fontSize:13,color:TEAL,italic:true,margin:0});
block(5.1,4.7,3.95,1.05,PALE_GREEN);text('Net effect on test set',{x:5.3,y:4.84,w:3.55,h:0.3,fontSize:12.5,bold:true,color:NAVY,align:'center',margin:0});text('159 rescued  ·  90 broken  →  +69 steps',{x:5.3,y:5.28,w:3.55,h:0.3,fontSize:13,bold:true,color:TEAL,align:'center',margin:0});cite('Luận văn §6.3 · Fig. 6.1');foot();

// 13. ACE
slide();bar('Thành phần 2: ACE chỉ chép exemplar khi hai tín hiệu đồng thuận');sectionTag('Method · component 2');claim('Retrieval hữu ích, nhưng “luôn dùng generator” làm executability giảm.');
box(M,2.0,1.55,0.85,'current step',{fs:12.5,bold:true});arrow(2.1,2.43,0.4);box(2.55,1.83,1.95,1.2,'retrieve 4 similar\ntraining steps\n(TF-IDF)',{fs:11.5,fill:LIGHT});arrow(4.55,2.43,0.35);box(4.95,1.83,1.85,1.2,'generator sees\n4 reference\nsentences',{fs:11.5,fill:'EEEAF6',line:NAVY});arrow(6.85,2.43,0.35);box(7.25,1.83,2.25,1.2,'accept only if\n① exact exemplar copy\n② same action type',{fs:11.2,bold:true,fill:PALE_GREEN,line:TEAL});
block(M,3.55,4.25,2.15,PALE_GREEN);text('ACE accepts',{x:M+0.2,y:3.72,w:1.2,h:0.3,fontSize:13,bold:true,color:GREEN,margin:0});text('Draft: “Click on the first image.”\nCopied exemplar: “Select the second photo.”\n→ both are TAP → replace draft',{x:M+0.2,y:4.12,w:3.85,h:1.2,fontSize:11.8,margin:0,lh:1.25});
block(5.25,3.55,4.25,2.15,PALE_RED);text('ACE rejects',{x:5.45,y:3.72,w:1.2,h:0.3,fontSize:13,bold:true,color:RED,margin:0});text('Draft: “Click on the close icon.”\nCopied exemplar: “Swipe up.”\n→ TAP ≠ SCROLL → keep draft',{x:5.45,y:4.12,w:3.85,h:1.2,fontSize:11.8,margin:0,lh:1.25});cite('Luận văn §4.6');foot();

// 14. MAIN RESULT
slide();bar('Phương pháp đề xuất đạt 60,7% executability');sectionTag('Main result');claim('+1,57 pp so với S1, khoảng tin cậy 95% [+0,86; +2,31], p < 0,001.');
hbar(M,2.45,4.55,47.6,80,'Base','47,6%',FOOTC);hbar(M,3.12,4.55,59.1,80,'S1','59,1%',NAVY);hbar(M,3.79,4.55,60.65,80,'GRPO + SPICE','60,6%',TEAL);hbar(M,4.46,4.55,60.68,80,'Proposed = SPICE + ACE','60,7%',GREEN);hbar(M,5.13,4.55,75.7,80,'Reference ceiling','75,7%',MAROON);
labelPill(7.65,3.73,1.45,'+1,55 pp',TEAL);labelPill(7.65,4.4,1.45,'+1,57 pp',GREEN);text('ACE giữ gần nguyên phần tăng về vị trí; phần lớn cải thiện đến từ GRPO + SPICE.',{x:M,y:5.95,w:W-2*M,h:0.42,fontSize:13.5,bold:true,color:NAVY,align:'center',margin:0});cite('4.463 touch steps · Luận văn §6.2, §6.6');foot();

// 15. STATISTICAL EVIDENCE
slide();bar('Mức tăng vượt seed noise và khoảng tin cậy không chạm 0');sectionTag('Evidence');claim('Bằng chứng chính là phép so ghép cặp theo từng bước, không phải chênh điểm độc lập.');
text('Δ executability (percentage points)',{x:4.0,y:1.9,w:3.5,h:0.3,fontSize:11.5,bold:true,color:GREY,align:'center',margin:0});line(4.25,2.38,4.0,0,'A7A3B2',1);for(let v=-1;v<=3;v++){const xx=4.25+(v+1);line(xx,2.32,0,0.12,'A7A3B2',1);text(String(v),{x:xx-0.12,y:2.48,w:0.24,h:0.2,fontSize:9,color:GREY,align:'center',margin:0});}line(5.25,2.15,0,2.85,'9A94AE',1.2,true,false);
ciRow(3.0,'Proposed − S1',1.57,0.86,2.31,GREEN);ciRow(3.75,'GRPO+SPICE − S1',1.55,0.80,2.33,TEAL);ciRow(4.5,'S1 seed 202 − seed 101',0.52,-0.22,1.26,FOOTC);
block(M,5.35,W-2*M,0.82);text('Interpretation: proposed gain ≈ 3× seed difference, and CI excludes 0; seed difference itself is not significant.',{x:M+0.18,y:5.35,w:W-2*M-0.36,h:0.82,fontSize:12.8,bold:true,color:NAVY,align:'center',valign:'middle',margin:0});cite('Bootstrap clustered by application · McNemar paired test · Luận văn §5.13, §6.6');foot();

// 16. ACE EFFECT
slide();bar('ACE cải thiện câu chữ mà không hy sinh khả năng định vị');sectionTag('Evidence · ACE');claim('ACE thay 402/4.463 câu (9,0%): 15 bước được cứu, 14 bước bị phá.');
tile(M,2.25,2.2,1.45,'+0,02 pp','Executability vs draft\nCI [−0,21; +0,26]',{color:TEAL,bf:20,align:'center'});tile(2.92,2.25,2.2,1.45,'+11,98','CIDEr-D',{color:GREEN,bf:20,align:'center'});tile(5.34,2.25,2.2,1.45,'+1,34','SPICE',{color:GREEN,bf:20,align:'center'});tile(7.76,2.25,1.74,1.45,'7/7','text metrics increase',{color:GREEN,bf:20,align:'center'});
block(M,4.15,W-2*M,1.4);text('Why consensus matters',{x:M+0.2,y:4.32,w:1.9,h:0.3,fontSize:13.5,bold:true,color:NAVY,margin:0});text('Dùng generator ở mọi bước làm executability giảm 1,25 pp (p = 0,002). ACE giữ phần chép exemplar hữu ích và loại phần generator tự viết kém hơn draft.',{x:M+2.0,y:4.2,w:W-2*M-2.2,h:0.82,fontSize:12.8,margin:0,lh:1.3});cite('Luận văn §6.4');foot();

// 17. ROBUSTNESS
slide();bar('Kết luận không phụ thuộc vào một listener hay một rule duy nhất');sectionTag('Robustness');claim('Đổi công cụ đo làm đổi điểm tuyệt đối, nhưng không đổi thứ tự hệ thống.');
tile(M,2.2,2.6,1.45,'+10,35 pp','S1 − Base dưới UGround',{color:NAVY,bf:20,align:'center'});tile(3.34,2.2,2.6,1.45,'+9,68 pp','S1 − Base dưới UI-Venus\n= 94% độ lớn',{color:TEAL,bf:20,align:'center'});tile(6.18,2.2,3.32,1.45,'same ranking','Phi-4 listener ngoài họ Qwen\nReference > S1 > Base > generic',{color:GREEN,bf:19,align:'center'});
block(M,4.1,W-2*M,1.35);text('Năm luật điểm khác nhau',{x:M+0.2,y:4.28,w:2.0,h:0.3,fontSize:13.5,bold:true,color:NAVY,margin:0});text('Ceiling thay đổi 56,6 → 82,2%, nhưng S1 luôn hơn Base 9,5 → 13,0 pp. Điều này giúp tách “conclusion stability” khỏi “absolute score”.',{x:M+2.1,y:4.15,w:W-2*M-2.3,h:0.8,fontSize:12.8,margin:0,lh:1.3});cite('UI-Venus-Ground-7B; Phi-4 multimodal · Luận văn §5.9–§5.12');foot();

// 18. WHAT FAILED
slide();bar('Các hướng thất bại giải thích vì sao phương pháp cuối tác động thẳng vào câu');sectionTag('Negative results');claim('Sửa bước trung gian chưa đủ: tín hiệu tốt thường không truyền thành câu tốt.');
const rows=[['S2: mô tả phần tử trước câu','57,2%','trỏ đúng → câu tốt; trỏ sai → câu tệ'],['MIN-DESC','60,0%','78% mức tăng đến từ học thêm giám sát'],['Reward tọa độ','60,1%','tọa độ tốt hơn, câu gần như không đổi'],['Candidate selection','56,1%','khi chọn thì tốt, nhưng từ chối quá nhiều'],['TAGE crop editor','60,2%','thấp hơn draft 0,43 pp']];table(M,2.15,[3.2,1.25,4.05],[{cells:['Hướng','Exec.','Điều rút ra'],fill:NAVY,color:WHITE,bold:true,h:0.42,fs:12},...rows.map((r,i)=>({cells:[r[0],{t:r[1],bold:true,color:i===2?TEAL:INK},r[2]],h:0.56,fs:11.7,rule:i<rows.length-1}))],{align:['left','center','left']});
block(M,5.55,W-2*M,0.75,'EEEAF6');text('Design pivot: đặt reward trực tiếp lên câu + chỉ tái sử dụng exemplar khi consensus an toàn.',{x:M+0.2,y:5.55,w:W-2*M-0.4,h:0.75,fontSize:13.5,bold:true,color:NAVY,align:'center',valign:'middle',margin:0});cite('Luận văn §6.10 + Appendix A');foot();

// 19. LIMITATIONS
slide();bar('Kết quả có ý nghĩa, nhưng còn bốn giới hạn cần giữ nguyên khi kết luận');sectionTag('Limitations');claim('Deck bảo vệ nên nói rõ giới hạn trước khi hội đồng phải hỏi.');
const lims=[['1','RL control','Chưa có đối chứng “học giám sát thêm cùng số bước” để tách reward khỏi việc học thêm.'],['2','ACE attribution','Chưa tách riêng lợi ích của retrieval; text-metric deltas nhỏ chưa có CI.'],['3','Metric ≠ human','Executability đo listener model; chưa có đánh giá tay 100 câu để nối metric với người thật.'],['4','Scope','Một dataset, UI tiếng Anh, một backbone 3B, single-screen; test không phải app-unseen.']];lims.forEach((c,i)=>{const x=i%2===0?M:5.05,y=2.1+Math.floor(i/2)*1.65;block(x,y,4.45,1.42,i===2?'F6E7E7':BLOCK);labelPill(x+0.16,y+0.16,0.42,c[0],i===2?RED:TEAL);text(c[1],{x:x+0.7,y:y+0.14,w:3.45,h:0.3,fontSize:13.2,bold:true,color:NAVY,margin:0});text(c[2],{x:x+0.18,y:y+0.58,w:4.05,h:0.72,fontSize:11.5,margin:0,lh:1.25});});cite('Luận văn §6.3.2, §6.4, §7.2');foot();

// 20. CONCLUSION
slide();bar('Kết luận: một cải thiện nhỏ nhưng có bằng chứng chặt và diễn giải rõ');sectionTag('Conclusion');claim('Phương pháp cuối cải thiện S1 có ý nghĩa theo thước chặt nhất, và metric được kiểm độc lập trước khi dùng.');
tile(M,2.15,2.75,1.45,'60,7%','proposed executability',{color:GREEN,bf:23,align:'center'});tile(3.63,2.15,2.75,1.45,'+1,57 pp','vs S1 · CI [+0,86; +2,31]',{color:GREEN,bf:23,align:'center'});tile(6.76,2.15,2.74,1.45,'13/13','metrics improved by GRPO+SPICE',{color:TEAL,bf:22,align:'center'});
block(M,4.05,W-2*M,1.75);bullets(['Đóng góp chính: GRPO thưởng SPICE + ACE, tác động trực tiếp vào câu cuối.','Đóng góp đo lường: executability có ceiling/floor, stress tests và cross-listener validation.','Đóng góp phân tích: negative results chỉ ra vì sao các bước trung gian không truyền đủ tín hiệu sang câu.'],M+0.25,4.2,W-2*M-0.5,{fs:12.8,gap:0.48,itemH:0.46});cite('Luận văn Ch.7');foot();

// 21. Q&A
slide(NAVY);text('Trân trọng cảm ơn',{x:0.8,y:2.35,w:W-1.6,h:0.65,fontSize:27,bold:true,color:WHITE,align:'center',margin:0});text('Hỏi đáp và thảo luận',{x:0.8,y:3.25,w:W-1.6,h:0.5,fontSize:17,color:'D8D4E6',align:'center',margin:0});line(3.55,4.0,2.9,0,'7A7099',1.5);text('Lê Đoàn Phương Uyên   ·   TS. Nguyễn Hồng Bửu Long\nTrường Đại học Khoa học Tự nhiên, ĐHQG-HCM',{x:0.8,y:4.35,w:W-1.6,h:0.9,fontSize:13,color:'D8D4E6',align:'center',margin:0,lh:1.4});foot();

// BACKUP 1
slide();bar('Dự phòng · Định nghĩa executability chính xác');
text('Executable(s) = ActionMatch ∧ NotOpposite ∧ Grounded',{x:M,y:1.05,w:W-2*M,h:0.48,fontSize:19,bold:true,color:NAVY,align:'center',margin:0,fontFace:MONO});
block(M,1.85,W-2*M,2.0);bullets(['Grounded: |px−gx| ≤ 0,14W và |py−gy| ≤ 0,14H.','Voronoi: ||p−g|| < ||p−c(e)|| với mọi phần tử e khác trên màn.','Điểm hệ thống = tỷ lệ bước chạm thỏa cả ba điều kiện.'],M+0.3,2.05,W-2*M-0.6,{fs:13,gap:0.5,itemH:0.46});
text('Điểm chính chỉ đo khả năng xác định phần tử; không đo độ trôi chảy hay “helpfulness” đầy đủ.',{x:M,y:4.35,w:W-2*M,h:0.52,fontSize:13.5,bold:true,color:RED,align:'center',margin:0});footB();

// BACKUP 2
slide();bar('Dự phòng · Bảng nhiều thước của phương pháp đề xuất');
table(M,1.0,[2.4,1.4,1.4,1.55,1.55],[{cells:['Metric','Base','S1','GRPO+SPICE','Proposed'],fill:NAVY,color:WHITE,bold:true,h:0.42,fs:11.8},{cells:['Executability','47,6','59,11','60,65',{t:'60,68',bold:true,color:TEAL}],h:0.4,rule:true},{cells:['AndroidControl box','53,6','65,49','67,02',{t:'67,11',bold:true}],h:0.4,rule:true},{cells:['AitW Euclid','63,4','74,37','76,25',{t:'76,32',bold:true}],h:0.4,rule:true},{cells:['BLEU-4','15,3','51,56','52,36',{t:'53,47',bold:true}],h:0.4,rule:true},{cells:['METEOR','24,6','36,79','37,92',{t:'38,37',bold:true}],h:0.4,rule:true},{cells:['ROUGE-L','42,3','67,35','68,36',{t:'69,08',bold:true}],h:0.4,rule:true},{cells:['CIDEr-D','88,0','416,1','430,0',{t:'442,0',bold:true}],h:0.4,rule:true},{cells:['SPICE','18,5','44,37','45,79',{t:'47,13',bold:true}],h:0.4,rule:true},{cells:['chrF','40,2','61,26','62,87',{t:'63,44',bold:true}],h:0.4,rule:true},{cells:['BERTScore','40,1','66,33','67,07',{t:'67,73',bold:true}],h:0.4}],{align:['left','center','center','center','center'],fs:11.5});text('Với các mô hình chênh <2 pp executability, text metrics có thể xếp hạng khác; kết luận chính vẫn đọc trên executability.',{x:M,y:5.72,w:W-2*M,h:0.55,fontSize:11.5,italic:true,color:GREY,align:'center',margin:0});footB();

// BACKUP 3
slide();bar('Dự phòng · Cross-listener validation');
table(M,1.15,[3.4,2.55,2.55],[{cells:['Comparison','UGround','UI-Venus'],fill:NAVY,color:WHITE,bold:true,h:0.44,fs:12.3},{cells:['S1 − Base',{t:'+10,35',bold:true,color:TEAL},{t:'+9,68',bold:true,color:TEAL}],h:0.55,rule:true},{cells:['S2 − S1',{t:'−1,93',color:RED},{t:'−1,21',color:RED}],h:0.55,rule:true},{cells:['Reference ceiling','70,0','69,3'],h:0.5}],{align:['left','center','center']});
block(M,3.65,W-2*M,1.55);text('Phi-4 listener ngoài họ Qwen',{x:M+0.2,y:3.82,w:2.25,h:0.3,fontSize:13.5,bold:true,color:NAVY,margin:0});text('Reference 54,9  >  S1 44,6  >  Base 38,6  >  generic 15,9',{x:M+2.35,y:3.8,w:W-2*M-2.55,h:0.36,fontSize:14,bold:true,color:TEAL,margin:0});text('Các listener sai ở nhiều bước khác nhau nhưng vẫn giữ thứ tự hệ thống.',{x:M+2.35,y:4.32,w:W-2*M-2.55,h:0.38,fontSize:12,margin:0});footB();

// BACKUP 4
slide();bar('Dự phòng · Các hướng đã thử trước phương pháp cuối');
table(M,0.95,[2.6,1.1,5.0],[{cells:['Hướng','Exec.','Điều rút ra'],fill:NAVY,color:WHITE,bold:true,h:0.42,fs:11.8},{cells:['S2 descriptor','57,2','Bước trung gian đúng thì giúp, sai thì gây hại mạnh.'],h:0.5,rule:true},{cells:['CE2-S2','59,4','Học thêm giám sát giải thích phần lớn mức tăng.'],h:0.5,rule:true},{cells:['MIN-DESC','60,0','Ưu tiên descriptor chỉ thêm +0,63 pp so CE2-S2.'],h:0.5,rule:true},{cells:['Reward tọa độ','60,1','Tọa độ descriptor tăng, câu gần như đứng yên.'],h:0.5,rule:true},{cells:['Candidate','56,1','Mô hình từ chối chọn quá nhiều.'],h:0.5,rule:true},{cells:['TAGE','60,2','Crop editor thấp hơn draft; selector nhận cả crop sai.'],h:0.5}],{align:['left','center','left'],fs:11.7});
block(M,4.75,W-2*M,1.25,'EEEAF6');text('Takeaway: can thiệp ở biểu diễn trung gian có thể tốt cục bộ nhưng không truyền ổn định tới câu cuối → chuyển sang tối ưu trực tiếp câu.',{x:M+0.25,y:4.75,w:W-2*M-0.5,h:1.25,fontSize:13,bold:true,color:NAVY,align:'center',valign:'middle',margin:0,lh:1.3});footB();

// BACKUP 5
slide();bar('Dự phòng · Cấu hình huấn luyện');
table(M,1.0,[3.2,5.55],[{cells:['Item','Configuration'],fill:NAVY,color:WHITE,bold:true,h:0.42,fs:12},{cells:['Backbone','Qwen2.5-VL-3B-Instruct'],h:0.42,rule:true},{cells:['Fine-tuning','QLoRA NF4 4-bit; rank 8; α 16; dropout 0,05'],h:0.42,rule:true},{cells:['Trainable params','14.966.784 (~0,48% language side)'],h:0.42,rule:true},{cells:['Context / effective batch','2.560 tokens / 16'],h:0.42,rule:true},{cells:['SFT','2 epochs = 8.072 steps; LR 1e−4; seed 101 & 202'],h:0.42,rule:true},{cells:['GRPO','G=8; 500 updates; 1.000 prompts; LR 1e−5; βKL=0,04'],h:0.42,rule:true},{cells:['Hardware','1 × A100; vision tower frozen'],h:0.42}],{align:['left','left'],fs:11.8});footB();

// BACKUP 6
slide();bar('Dự phòng · Hướng phát triển ưu tiên');
const fw=[['1','Human validation','Hai người chấm 100 câu; đo agreement với executability.'],['2','Fair RL control','SFT thêm cùng số bước + cùng generation pipeline với S1.'],['3','ACE confidence','Bootstrap CI cho text metrics và ablation retrieval/no-retrieval.'],['4','Stronger paraphrase','Viết lại cả tên và cách mô tả phần tử, không chỉ động từ/trật tự.'],['5','Broader scope','Official AndroidControl test, multi-screen, Vietnamese UI, second dataset.']];fw.forEach((c,i)=>{const y=0.95+i*1.05;labelPill(M,y+0.07,0.42,c[0],i<2?RED:TEAL);text(c[1],{x:M+0.65,y,w:2.2,h:0.32,fontSize:13.2,bold:true,color:NAVY,margin:0});text(c[2],{x:M+2.8,y,w:6.1,h:0.52,fontSize:12,margin:0,lh:1.25});if(i<fw.length-1)line(M+0.65,y+0.72,8.35,0,'D0CDD7',1);});footB();

// EXPORT
done();
const OUT='../LUAN_VAN_SLIDE_BAO_VE_SCIENTIFIC.pptx';
pres.writeFile({fileName:OUT}).then(()=>{
  const html='<!doctype html><meta charset="utf-8"><title>Scientific thesis defense preview</title><style>body{background:#555;margin:0;padding:24px;font-family:sans-serif}.slide{position:relative;width:960px;height:720px;margin:0 auto 24px;box-shadow:0 3px 14px rgba(0,0,0,.5);overflow:hidden}</style>'+htmlSlides.join('\n');
  fs.mkdirSync('_preview',{recursive:true});
  fs.writeFileSync('_preview/preview_scientific_defense.html',html);
  console.log(`Xong: ${OUT} | main=${PAGE} | backup=${BPAGE}`);
});
