# -*- coding: utf-8 -*-
"""Sinh notebook Colab 2 cổng (grounder-gate + component-probe). Chạy local, xuất .ipynb hợp lệ.
   ~/.venvs/thesis/bin/python harness/make_colab_gates.py  ->  harness/colab_gates.ipynb"""
import json, os

def md(*lines): return {"cell_type": "markdown", "metadata": {}, "source": [l + "\n" for l in lines]}
def code(src): return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
                       "source": [l + "\n" for l in src.strip("\n").split("\n")]}

cells = []

cells.append(md(
    "# Luận văn — 2 CỔNG go/no-go trên Colab",
    "",
    "Chạy **trước khi train**. Hai cổng chỉ *suy luận* (không train) → rẻ, nhanh.",
    "",
    "- **Cổng A — bộ trỏ:** một grounder có định vị đúng nút từ CÂU GOLD không? Cần ~80%. Nếu rớt → trục executability chưa dùng được.",
    "- **Cổng B — room cho thành phần:** model nền (Qwen-3B, chưa fine-tune) yếu ở đâu — bịa nhiều hay trỏ kém? Chỗ yếu = chỗ gắn thành phần.",
    "",
    "**Cách dùng:** Runtime → Change runtime type → GPU (T4 đủ). Chạy từng cell từ trên xuống. Cuối mỗi cổng có dòng KẾT LUẬN — copy dán lại cho trợ lý.",
    "",
    "> ⚠️ Không chạy được trên máy không-GPU của bạn — đây là file để chạy trên Colab sau khi mua Pro.",
))

cells.append(md("## 0. Cài đặt + cấu hình"))
cells.append(code(
    "!pip -q install transformers==4.49.0 accelerate qwen-vl-utils bitsandbytes pillow huggingface_hub datasets\n"
    "import torch; print('CUDA:', torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else '')"
))
cells.append(code(
    "# ---- CẤU HÌNH ----\n"
    "REPO      = 'wangyuanlei/android_control_test'   # mirror AC-test có ảnh + step_instructions + toạ độ gold\n"
    "N_STEPS   = 60          # số bước lấy để thử (đủ tín hiệu, rẻ)\n"
    "GROUNDER  = 'Qwen/Qwen2.5-VL-3B-Instruct'  # bộ trỏ. 3B fit T4. Nếu <80% → thử 'Qwen/Qwen2.5-VL-7B-Instruct' hoặc 'OS-Copilot/OS-Atlas-Base-7B'\n"
    "BASE_GEN  = 'Qwen/Qwen2.5-VL-3B-Instruct'  # model nền sinh hướng dẫn (cùng model, prompt khác — tiết kiệm VRAM)\n"
    "TOL       = 0.14        # dung sai trúng (theo cạnh màn, chuẩn AITW ~14%)\n"
    "SEED      = 20260720"
))

cells.append(md("## 1. Tải dữ liệu — ảnh + câu gold + toạ độ gold (chỉ bước có toạ độ)"))
cells.append(code(
    "import re, json, random\n"
    "from huggingface_hub import HfApi, hf_hub_download\n"
    "api = HfApi(); files = api.list_repo_files(REPO, repo_type='dataset')\n"
    "id2json = {}; png_set = set(f for f in files if f.endswith('.png'))\n"
    "for f in files:\n"
    "    m = re.search(r'episode_(\\d+)\\.json', f)\n"
    "    if m: id2json[int(m.group(1))] = f\n"
    "rng = random.Random(SEED); eids = list(id2json); rng.shuffle(eids)\n"
    "items = []\n"
    "for eid in eids:\n"
    "    if len(items) >= N_STEPS: break\n"
    "    try: o = json.load(open(hf_hub_download(REPO, id2json[eid], repo_type='dataset'), encoding='utf-8'))\n"
    "    except Exception: continue\n"
    "    insts = o.get('step_instructions') or []; acts = o.get('actions') or []\n"
    "    for si,(ins,a) in enumerate(zip(insts, acts)):\n"
    "        if len(items) >= N_STEPS: break\n"
    "        if a.get('action_type') not in ('click','long_press') or 'x' not in a: continue\n"
    "        cand = [p for p in png_set if f'episode_{eid}_screenshot_{si}.png' in p]\n"
    "        if not cand: continue\n"
    "        png = hf_hub_download(REPO, cand[0], repo_type='dataset')\n"
    "        items.append({'eid':eid,'si':si,'instr':ins,'gx':float(a['x']),'gy':float(a['y']),'png':png,'goal':o.get('goal')})\n"
    "print(f'Lấy được {len(items)} bước có toạ độ gold + ảnh')"
))

cells.append(md("## 2. Load bộ trỏ (Qwen2.5-VL)"))
cells.append(code(
    "from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor\n"
    "from qwen_vl_utils import process_vision_info\n"
    "from PIL import Image\n"
    "gm = Qwen2_5_VLForConditionalGeneration.from_pretrained(GROUNDER, torch_dtype='auto', device_map='auto')\n"
    "gp = AutoProcessor.from_pretrained(GROUNDER)\n"
    "\n"
    "def ask_point(png, instruction):\n"
    "    '''Trả (x,y) pixel trên ảnh gốc, hoặc None.'''\n"
    "    im = Image.open(png).convert('RGB'); W,H = im.size\n"
    "    prompt = (f'This screenshot is {W}x{H} pixels. A user is told: \"{instruction}\". '\n"
    "              f'Output ONLY the pixel coordinate to tap as two integers: x,y')\n"
    "    msgs = [{'role':'user','content':[{'type':'image','image':png},{'type':'text','text':prompt}]}]\n"
    "    text = gp.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)\n"
    "    imgs, vids = process_vision_info(msgs)\n"
    "    inp = gp(text=[text], images=imgs, videos=vids, padding=True, return_tensors='pt').to(gm.device)\n"
    "    out = gm.generate(**inp, max_new_tokens=32, do_sample=False)\n"
    "    dec = gp.batch_decode([o[len(i):] for i,o in zip(inp.input_ids, out)], skip_special_tokens=True)[0]\n"
    "    nums = re.findall(r'\\d+\\.?\\d*', dec)\n"
    "    if len(nums) >= 2: return float(nums[0]), float(nums[1]), dec\n"
    "    return None, None, dec\n"
    "\n"
    "# SANITY: in thô 3 câu đầu — KIỂM định dạng toạ độ có hợp lý (trong khoảng ảnh) không.\n"
    "for it in items[:3]:\n"
    "    x,y,raw = ask_point(it['png'], it['instr'])\n"
    "    print(f\"gold=({it['gx']:.0f},{it['gy']:.0f}) pred=({x},{y}) raw={raw!r}  | {it['instr']}\")"
))
cells.append(md(
    "> **KIỂM 3 dòng trên:** `pred` phải là số pixel nằm trong kích thước ảnh (vd ảnh 1080×2400 thì x<1080, y<2400). "
    "Nếu model trả 0-1000 (chuẩn hoá) hay định dạng lạ → sửa prompt/parse trong hàm `ask_point` trước khi chạy tiếp."
))

cells.append(md("## 3. CỔNG A — bộ trỏ trên CÂU GOLD (cần ~80%)"))
cells.append(code(
    "hits = {0.05:0, 0.10:0, 0.14:0}; scored=0; unparsed=0\n"
    "for it in items:\n"
    "    im = Image.open(it['png']); W,H = im.size\n"
    "    x,y,_ = ask_point(it['png'], it['instr'])\n"
    "    if x is None: unparsed+=1; continue\n"
    "    scored+=1\n"
    "    for t in hits:\n"
    "        if abs(x-it['gx'])<=t*W and abs(y-it['gy'])<=t*H: hits[t]+=1\n"
    "print('='*56)\n"
    "for t in (0.05,0.10,0.14):\n"
    "    print(f'  trúng ±{int(t*100)}%: {hits[t]}/{scored} = {hits[t]/max(scored,1):.1%}')\n"
    "print(f'  (bỏ {unparsed} không đọc được toạ độ)')\n"
    "ok = hits[0.14]/max(scored,1) >= 0.80\n"
    "print('='*56)\n"
    "print('KẾT LUẬN CỔNG A:', 'GO — bộ trỏ đủ tin' if ok else 'NO-GO — thử grounder mạnh hơn (7B/OS-Atlas) hoặc rẽ đường thu-hẹp')"
))

cells.append(md(
    "## 4. CỔNG B — room cho thành phần: model NỀN yếu ở đâu?",
    "Cho Qwen-3B (chưa fine-tune) tự sinh hướng dẫn từ ẢNH+MỤC TIÊU (không xem đáp án), rồi:",
    "- **đo TRỎ KÉM:** ground câu nó sinh, xem executability thấp hơn câu gold bao nhiêu → room cho *vòng kiểm-sửa*.",
    "- **(bịa nút: đo riêng trên MobileViews vì cần View Hierarchy — chạy ở notebook khác.)**"
))
cells.append(code(
    "def gen_instruction(png, goal):\n"
    "    prompt = (f'Screenshot of a mobile app. Goal: \"{goal}\". '\n"
    "              f'Write ONE short next-step instruction for a human to tap on THIS screen. Output only the sentence.')\n"
    "    msgs = [{'role':'user','content':[{'type':'image','image':png},{'type':'text','text':prompt}]}]\n"
    "    text = gp.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)\n"
    "    imgs,vids = process_vision_info(msgs)\n"
    "    inp = gp(text=[text], images=imgs, videos=vids, padding=True, return_tensors='pt').to(gm.device)\n"
    "    out = gm.generate(**inp, max_new_tokens=48, do_sample=False)\n"
    "    return gp.batch_decode([o[len(i):] for i,o in zip(inp.input_ids,out)], skip_special_tokens=True)[0].strip()\n"
    "\n"
    "base_hit=0; gold_hit=0; n=0\n"
    "for it in items:\n"
    "    im=Image.open(it['png']); W,H=im.size\n"
    "    gen = gen_instruction(it['png'], it['goal'])\n"
    "    bx,by,_ = ask_point(it['png'], gen)          # ground câu MODEL NỀN sinh\n"
    "    gx,gy,_ = ask_point(it['png'], it['instr'])  # ground câu GOLD (mốc trần)\n"
    "    n+=1\n"
    "    if bx is not None and abs(bx-it['gx'])<=TOL*W and abs(by-it['gy'])<=TOL*H: base_hit+=1\n"
    "    if gx is not None and abs(gx-it['gx'])<=TOL*W and abs(gy-it['gy'])<=TOL*H: gold_hit+=1\n"
    "print('='*56)\n"
    "print(f'  executability câu MODEL NỀN = {base_hit/n:.1%}')\n"
    "print(f'  executability câu GOLD (trần) = {gold_hit/n:.1%}')\n"
    "print(f'  KHOẢNG CÁCH (room) = {(gold_hit-base_hit)/n:.1%}')\n"
    "print('='*56)\n"
    "print('ĐỌC: room LỚN → câu model nền trỏ kém hơn gold nhiều → thành phần VÒNG-KIỂM-SỬA có đất.')\n"
    "print('     room NHỎ → model nền đã trỏ tốt → chuyển sang đo bịa-nút (faithfulness) để tìm room khác.')"
))

cells.append(md(
    "## 5. Copy về cho trợ lý",
    "Dán lại: (a) 3 dòng SANITY ở mục 2, (b) KẾT LUẬN CỔNG A, (c) ba số CỔNG B. "
    "Từ đó chốt: đường executability sống không, và gắn thành phần gì."
))

nb = {"cells": cells,
      "metadata": {"accelerator": "GPU",
                   "colab": {"provenance": []},
                   "kernelspec": {"display_name": "Python 3", "name": "python3"},
                   "language_info": {"name": "python"}},
      "nbformat": 4, "nbformat_minor": 0}

out = os.path.join(os.path.dirname(__file__), "colab_gates.ipynb")
json.dump(nb, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("WROTE", out, "-", len(cells), "cells")
