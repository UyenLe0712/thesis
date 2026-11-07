# -*- coding: utf-8 -*-
"""Máy chủ người nghe (B.7 của 288) — tiến trình riêng, nạp Phi-4 MỘT lần, phục vụ mọi nhánh qua TCP.

    /content/vphi/bin/python nghe_server.py --backend phi4 --bang bang_nghe.json --img-root <gói> --cong 47288

Vì sao tách tiến trình: Phi-4 cần transformers 4.48.2, môi trường train dùng bản khác.
Giao thức: client gửi MỘT dòng JSON {"viec": [{"key", "sent"}, …]} + "\n"; máy chủ trả một dòng
{"chon": [...], "raw": [...], "dt": giây}. "viec" rỗng = ping → {"ok": true, "ten": …}. Lỗi một kết nối
không làm dừng máy chủ. Tuần tự (một GPU). Câu hỏi + vẽ ô = giao thức 14/9 (som_listener, som_build.ve).
Backend `gia` (tự kiểm): câu có "TREO" ngủ 30 giây; có "TRUNG" và màn có đáp án → ô đáp án đầu, ngược lại "0".
Viết lại 6/10/2026 từ bản mô tả B.7 (mã gốc ở máy Mac) ⇒ md5 khác bản gốc.
"""
import sys
sys.modules.setdefault("torchao", None)       # transformers 4.48.2 vấp torchao mới của môi trường train
import argparse, functools, json, os, re, socket, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import som_listener as SL
from som_build import ve


class Gia:
    ten = "gia (tự kiểm)"

    def __init__(self, bang):
        self.bang = bang

    def tra_loi(self, key, s):
        if "TREO" in s:
            time.sleep(30)
        dap = self.bang[key]["dap_an"]
        return str(dap[0]) if "TRUNG" in s and dap else "0"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=["phi4", "gia"], required=True)
    ap.add_argument("--bang", required=True)
    ap.add_argument("--img-root", required=True)
    ap.add_argument("--cong", type=int, default=47288)
    a = ap.parse_args()
    bang = json.load(open(a.bang, encoding="utf-8"))["bang"]
    from PIL import Image

    @functools.lru_cache(maxsize=128)
    def anh(key):
        b = bang[key]
        return ve(Image.open(os.path.join(a.img_root, b["image"])), [tuple(x) for x in b["boxes"]])

    mo = SL.Phi4() if a.backend == "phi4" else Gia(bang)
    print(f"[máy chủ] {mo.ten} · {len(bang)} màn · cổng {a.cong} · crops {os.environ.get('SOM_PHI4_CROPS', 'mặc định')}", flush=True)
    sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sv.bind(("127.0.0.1", a.cong)); sv.listen(8)
    print("SẴN SÀNG", flush=True)
    n_lan, n_cau, t_tong, n_oom = 0, 0, 0.0, 0
    while True:
        conn, _ = sv.accept()
        try:
            buf = b""
            while not buf.endswith(b"\n"):
                x = conn.recv(65536)
                if not x:
                    break
                buf += x
            q = json.loads(buf.decode("utf-8") or "{}") if buf.strip() else {}
            viec = q.get("viec") or []
            if not viec:
                conn.sendall((json.dumps({"ok": True, "ten": mo.ten}, ensure_ascii=False) + "\n").encode("utf-8"))
                continue
            t0, chon, raw = time.time(), [], []
            for v in viec:
                k, s = v["key"], v["sent"]
                img = anh(k)                       # backend giả cũng vẽ để kiểm đường dẫn ảnh
                if a.backend == "gia":
                    r = mo.tra_loi(k, s)
                else:
                    try:
                        r = mo.hoi(img, SL.CAU_HOI.format(s=s))
                    except Exception as e:
                        if "out of memory" not in str(e).lower():
                            raise
                        import torch; torch.cuda.empty_cache()
                        r, n_oom = "__OOM__", n_oom + 1
                m = re.search(r"\d+", r) if r != "__OOM__" else None
                chon.append(int(m.group()) if m else None); raw.append(r)
            dt = time.time() - t0
            n_lan += 1; n_cau += len(viec); t_tong += dt
            conn.sendall((json.dumps({"chon": chon, "raw": raw, "dt": dt}, ensure_ascii=False) + "\n").encode("utf-8"))
            if n_lan % 50 == 0:
                print(f"[máy chủ] {n_lan} lần · {n_cau} câu · {t_tong / max(n_cau, 1):.2f} s/câu · OOM {n_oom}", flush=True)
        except Exception as e:
            print(f"⚠️ [máy chủ] lỗi kết nối: {e!r}", flush=True)
            try:
                conn.sendall((json.dumps({"loi": repr(e)}) + "\n").encode("utf-8"))
            except Exception:
                pass
        finally:
            try:
                conn.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()
