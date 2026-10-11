# G2b (trang, dự phòng 11/10/2026 tối): G2 trên uyenle chạy >10 h không rõ lý do ⇒ chạy lại test shard 7,8,9/10
# dưới dạng 6 nửa shard k/20 + (k+10)/20 (rows[k::20] ∪ rows[k+10::20] = rows[k::10]); gộp lại ở máy nhà.
import importlib.util, os, sys
K = os.path.dirname(os.path.abspath(__file__))
src = open(f"{K}/dung_nb_chia.py").read().split("V1 = ")[0]
exec(src)
V = {0: [("test", 7, 20), ("test", 17, 20), ("test", 8, 20)], 1: [("test", 18, 20), ("test", 9, 20), ("test", 19, 20)]}
dung("cw-ra-g2b-309", V, False, {"id": "trangphngngc/cw-ra-g2b-309",
     "dataset_sources": ["trangphngngc/fgrb-p1-bundle", "trangphngngc/grpo-spice-ck500", "trangphngngc/ra-sft-script",
                         "trangphngngc/cw-ra-309", "trangphngngc/thesis-score"],
     "kernel_sources": ["trangphngngc/cw-ra-t-309"]})
