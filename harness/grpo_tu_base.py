# -*- coding: utf-8 -*-
"""GRPO của lưới nhưng XUẤT PHÁT TỪ BASE (report/326 danh sách B, report/329 đợt 4 độ nhạy):
điểm xuất phát là Qwen2.5-VL-3B-Instruct gốc thay cho S1/101 hoà. KHÔNG sửa grpo_luoi.py /
grpo_spice.py: tệp này chỉ bọc GS.nap rồi gọi đúng GL.main().

Về mặt mã, `grpo_luoi.py --merged Qwen/Qwen2.5-VL-3B-Instruct` đã đủ (nap nạp thẳng từ a.merged,
LoRA mới chỉ lấy r/alpha/target từ adapter_config của S1 nên phép so số tham số vẫn đúng, LoRA mới
B = 0 nên tham chiếu KL = mô hình nạp = Base). Tệp bọc này thêm hai thứ để log kiểm được:
  · ép a.merged = GS.BASE bất kể --merged truyền vào (notebook luôn truyền s1_merged) và in
    dòng `[xuất phát] Base …` kèm giá trị --merged bị bỏ;
  · sau khi nạp, assert config._name_or_path == GS.BASE.
dtype giữ nguyên đường cũ: GS._dtype() ⇒ fp16 trên T4 (S1 hoà cũng được dựng ở fp16 trên T4).

  python grpo_tu_base.py --selftest-base                       # CPU, nạp giả, không tải mô hình
  python grpo_tu_base.py --train --algo grpo --reward spice --bundle B --out O --resume auto --no-q4 ...
  (mọi cờ y như grpo_luoi.py; --merged có truyền cũng bị bỏ)
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grpo_luoi as GL          # noqa: E402
import grpo_spice as GS         # noqa: E402

_goc_nap = GS.nap


def nap_base(a):
    bo = a.merged
    a.merged = GS.BASE
    print(f"[xuất phát] Base {GS.BASE} · KHÔNG hoà S1 · tham chiếu KL = Base (LoRA mới B=0)"
          f" · bỏ --merged {bo!r}", flush=True)
    proc, model, dt = _goc_nap(a)
    ten = getattr(model.config, "_name_or_path", None)
    assert ten == GS.BASE, f"⛔ mô hình nạp là {ten!r}, không phải {GS.BASE}"
    print(f"[xuất phát] đã nạp {ten} · dtype {dt}", flush=True)
    return proc, model, dt


def cai():
    GS.nap = nap_base


def selftest_base():
    import types, torch, transformers
    goi = {}

    class Gia:
        def __init__(self, p):
            self.config = types.SimpleNamespace(_name_or_path=p)

    def fp(path, **kw):
        goi["path"], goi["kw"] = path, kw
        return Gia(path)

    GS._dtype = lambda: torch.float16                        # giả T4
    transformers.AutoProcessor.from_pretrained = lambda *x, **k: "proc"
    transformers.Qwen2_5_VLForConditionalGeneration.from_pretrained = fp
    torch.cuda.get_device_name = lambda i=0: "T4 giả"
    cai()
    a = types.SimpleNamespace(merged="/kaggle/working/s1_merged", q4=False)
    _, m, dt = GS.nap(a)                                     # đúng đường GL.train gọi
    assert goi["path"] == GS.BASE and a.merged == GS.BASE, goi
    assert dt == torch.float16 and goi["kw"].get("dtype", goi["kw"].get("torch_dtype")) == torch.float16, goi
    assert "quantization_config" not in goi["kw"], goi
    # mô hình nạp không phải Base thì phải dừng
    transformers.Qwen2_5_VLForConditionalGeneration.from_pretrained = lambda p, **k: Gia("/kaggle/working/s1_merged")
    try:
        GS.nap(types.SimpleNamespace(merged="x", q4=False))
        raise SystemExit("⛔ không chặn được mô hình sai")
    except AssertionError as e:
        print("  chặn đúng:", e, flush=True)
    print("✅ selftest xuất phát từ Base ĐẠT (nạp giả, chưa nạp mô hình thật)", flush=True)


if __name__ == "__main__":
    if "--selftest-base" in sys.argv:
        selftest_base()
    else:
        cai()
        GL.main()
