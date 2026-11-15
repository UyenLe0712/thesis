# -*- coding: utf-8 -*-
"""Người nghe trắc nghiệm: đọc câu + ảnh có đánh số, trả lời số của phần tử cần chạm. Chạy trên GPU.

    python harness/som_listener.py --backend phi4 --img-root <thư mục chứa images/> \
        --som som.jsonl --cau cau_chuan.jsonl --out chon_phi4_chuan.jsonl [--mau 200] [--shard 0/2]

Giao thức khoá 14/9/2026 (xem `som_build.py`): người nghe KHÔNG thấy mục tiêu, KHÔNG thấy lịch sử, chỉ
thấy ảnh đã vẽ số và câu cần chấm ⇒ chỉ giải được bước nếu câu đủ thông tin. Giải mã tham lam, tối đa
8 token, lấy số nguyên đầu tiên trong câu trả lời. Câu rỗng không gọi mô hình, tính trượt.
Ghi dần + nối tiếp được (bỏ qua bước đã có trong --out). In dòng `[cấu hình] …` để kiểm máy kia đang
chạy đúng mô hình, đúng tệp câu.

--backend:
  phi4     microsoft/Phi-4-multimodal-instruct  (transformers 4.48.2, trust_remote_code, eager, fp16)
  pixtral  mistral-community/pixtral-12b        (LlavaForConditionalGeneration, fp16, device_map auto)
  gia      không nạp mô hình, trả lời ngẫu nhiên — chỉ để thử đường ống trên CPU
"""
import argparse, json, os, random, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from som_build import ve

CAU_HOI = ("This is a phone screenshot. Colored boxes with numbers mark the elements that can be tapped.\n"
           "A user was given this instruction:\n\"{s}\"\n"
           "Which numbered box is the element the instruction tells the user to tap? "
           "Answer with the number only.")


def mau_co_dinh(n_tong, k, seed=20260914):
    """Lát thử cố định, chọn theo chỉ số — không phụ thuộc đáp án hay nhánh nào."""
    idx = list(range(n_tong)); random.Random(seed).shuffle(idx)
    return set(sorted(idx[:k]))


class Phi4:
    ten = "microsoft/Phi-4-multimodal-instruct"

    def __init__(self):
        import torch
        from transformers import AutoModelForCausalLM, AutoProcessor
        self.torch = torch
        self.proc = AutoProcessor.from_pretrained(self.ten, trust_remote_code=True)
        self.m = AutoModelForCausalLM.from_pretrained(self.ten, trust_remote_code=True, torch_dtype=torch.float16,
                                                      _attn_implementation="eager").cuda().eval()
        crops = os.environ.get("SOM_PHI4_CROPS")      # mặc định của mô hình là 36 mảnh; chỉ hạ khi tràn bộ nhớ
        if crops:
            self.proc.image_processor.dynamic_hd = int(crops)
        print(f"[phi4] dynamic_hd = {getattr(self.proc.image_processor, 'dynamic_hd', '?')}", flush=True)

    def hoi(self, img, text):
        p = f"<|user|><|image_1|>{text}<|end|><|assistant|>"
        x = self.proc(text=p, images=img, return_tensors="pt").to("cuda", self.torch.float16)
        with self.torch.no_grad():
            y = self.m.generate(**x, max_new_tokens=8, do_sample=False)
        return self.proc.batch_decode(y[:, x["input_ids"].shape[1]:], skip_special_tokens=True)[0]


class Pixtral:
    ten = "mistral-community/pixtral-12b"

    def __init__(self):
        import torch
        from transformers import AutoProcessor, LlavaForConditionalGeneration
        self.torch = torch
        self.proc = AutoProcessor.from_pretrained(self.ten)
        self.m = LlavaForConditionalGeneration.from_pretrained(self.ten, torch_dtype=torch.float16,
                                                               device_map="auto").eval()

    def hoi(self, img, text):
        p = f"<s>[INST]{text}\n[IMG][/INST]"
        x = self.proc(text=p, images=[img], return_tensors="pt").to(self.m.device, self.torch.float16)
        with self.torch.no_grad():
            y = self.m.generate(**x, max_new_tokens=8, do_sample=False)
        return self.proc.batch_decode(y[:, x["input_ids"].shape[1]:], skip_special_tokens=True)[0]


class Gia:
    ten = "gia (ngẫu nhiên, thử đường ống)"

    def hoi(self, img, text):
        return str(random.randint(1, 20))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=["phi4", "pixtral", "gia"], required=True)
    ap.add_argument("--img-root", required=True, help="thư mục mà <img-root>/<image_goc> là ảnh gốc")
    ap.add_argument("--som", required=True)
    ap.add_argument("--cau", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--mau", type=int, default=0, help="chỉ chấm lát thử cố định k bước")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--shard", default="0/1", help="i/n: chỉ chấm bước có chỉ số % n == i (chạy 2 GPU)")
    a = ap.parse_args()

    som = [json.loads(l) for l in open(a.som, encoding="utf-8")]
    cau = {(str(o["episode_id"]), str(o["step_id"])): o for o in map(json.loads, open(a.cau, encoding="utf-8"))}
    assert len(som) == 4463 and len(cau) == 4463, (len(som), len(cau))
    chon = mau_co_dinh(len(som), a.mau) if a.mau else set(range(len(som)))
    si, sn = map(int, a.shard.split("/"))
    viec = [i for i in sorted(chon) if i % sn == si]
    if a.limit:
        viec = viec[:a.limit]
    xong = set()
    if os.path.exists(a.out):
        for l in open(a.out, encoding="utf-8"):
            try:
                o = json.loads(l); xong.add((o["episode_id"], o["step_id"]))
            except json.JSONDecodeError:
                pass
    print(f"[cấu hình] backend={a.backend} · câu={os.path.basename(a.cau)} · ra={a.out} · "
          f"bước cần={len(viec)} · đã xong={len(xong)} · shard={a.shard} · mẫu={a.mau or 'đủ'}", flush=True)

    mo = {"phi4": Phi4, "pixtral": Pixtral, "gia": Gia}[a.backend]()
    print(f"[mô hình] {mo.ten}", flush=True)
    t0, n = time.time(), 0
    with open(a.out, "a", encoding="utf-8") as f:
        for i in viec:
            r = som[i]; k = (str(r["episode_id"]), str(r["step_id"]))
            if k in xong:
                continue
            c = cau[k]; s = c["sent"]
            if not s or not r["boxes"]:
                raw, so = "", None
            else:
                from PIL import Image
                img = ve(Image.open(os.path.join(a.img_root, r["image_goc"])), r["boxes"])
                raw = mo.hoi(img, CAU_HOI.format(s=s))
                m = re.search(r"\d+", raw or "")
                so = int(m.group()) if m else None
            dung = int(so is not None and so in r["dap_an"])
            f.write(json.dumps({"episode_id": k[0], "step_id": k[1], "raw": raw, "chon": so, "dung": dung,
                                "dung_thaotac": int(dung and c["action_ok"] and c["toggle_ok"]),
                                "n_o": len(r["boxes"])}, ensure_ascii=False) + "\n")
            f.flush(); n += 1
            if n % 25 == 0:
                dt = (time.time() - t0) / n
                print(f"  {n}/{len(viec) - len(xong)} · {dt:.2f} s/bước · còn ~{dt*(len(viec)-len(xong)-n)/60:.0f} phút",
                      flush=True)
    print(f"xong {n} bước mới → {a.out}", flush=True)


if __name__ == "__main__":
    main()
