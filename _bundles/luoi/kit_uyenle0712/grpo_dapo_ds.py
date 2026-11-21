"""DAPO dynamic sampling THẬT (Yu và cộng sự 2025, arXiv 2503.14476) trên cùng vòng lặp ck500 — `--algo dapo_ds`.

Thi hành slides/ACTION_4_THUAT_TOAN_RL_2025_SO_VOI_GRPO_20_11_2026.md mục 12.4.A (mục 12 thắng mục 5.3: bản cũ chỉ che
nhóm hoà, KHÔNG phải DAPO). Không sửa grpo_luoi.py · grpo_codien.py · grpo_moi_b*.py: tệp này import grpo_codien rồi gọi
main() của nó, nên điểm xuất phát (S1 hoà + LoRA mới), 1.000 câu nhắc của ck500, G = 8, lr, β, số bước, phần thưởng,
điểm lưu và dòng log `[nạp default]` giữ nguyên.

Cơ chế (mỗi optimizer step = MỘT lô sinh 16 câu = 2 câu nhắc × G = 8, vì steps_per_generation = accum = 4, μ = 1):
  1. Sinh + chấm 2 nhóm của lô như GRPO (câu nhắc lấy từ dataloader, đúng dòng câu nhắc của ck500).
  2. Nhóm có thưởng HOÀ hoàn toàn (max − min < 1e-9) bị loại khỏi lô cập nhật.
  3. Thiếu bao nhiêu nhóm thì lấy câu nhắc khác từ CÙNG pool 1.000 câu nhắc (train_dataset của trainer; bộ lặp riêng,
     xáo theo seed, hết vòng thì xáo lại, bỏ qua câu nhắc đang có trong lô của bước này), sinh + chấm theo khúc 2 câu
     nhắc (cùng cỡ lô sinh như bước thường ⇒ cùng đỉnh VRAM sinh), cho tới khi đủ đúng 2 nhóm hữu hiệu. Khúc cho thừa
     nhóm hữu hiệu thì nhóm thừa bị bỏ (vẫn tính vào ngân sách rollout).
  4. Trần --dapo-max-bu lần bù mỗi bước (mặc định 8 ⇒ tối đa 16 câu nhắc bù). Chạm trần: giữ nhóm hoà của lượt đầu với
     A = 0 (không đóng góp gradient chính sách, chỉ còn KL) và in cảnh báo `⚠️ [dapo] chạm trần`.
  Policy giữ nguyên trong suốt lúc bù: TRL gọi _generate_and_score_completions trong _prepare_inputs ở micro-step đầu
  của bước (self._step % steps_per_generation == 0), TRƯỚC mọi backward/optimizer.step của bước đó; mã còn tự khẳng
  định (assert) tổng tham số học được và global_step không đổi giữa đầu và cuối vòng bù.
  Lợi thế của nhóm giữ lại = lợi thế TRL tính lúc sinh nhóm đó, scale_rewards = "group" ⇒ (r − TB nhóm)/(std nhóm + 1e-4),
  độc lập giữa các nhóm nên ghép nhóm từ nhiều lần gọi không đổi giá trị (mã assert lại từng nhóm).

Phần còn lại của DAPO: loss theo token (loss_type "dapo", lưới đã có) · lọc câu bị cắt (mask_truncated_completions,
lưới đã có trên GPU) · μ = 1 · ε_high = 0,28 (--eps-high của grpo_codien; KHÔNG tác dụng khi μ = 1 vì tỉ số luôn bằng 1,
đặt cho đúng công thức). KHÁC bài gốc, phải khai: giữ β = 0,04 (KL về S1) để so với GRPO A/A, bài gốc β = 0.
Không nói DAPO và GRPO "cùng compute": chỉ cùng số nhóm cập nhật; tổng rollout báo riêng trong dapo_ngan_sach.json.

num_items_in_batch (mẫu số của loss "dapo") tính lại theo ĐÚNG định nghĩa TRL 0.29.1 (grpo_trainer.py:1616, tổng độ dài
câu sinh TRƯỚC khi che câu bị cắt) trên các hàng giữ lại — không phải tổng completion_mask — để bước không có nhóm hoà
cho lô cập nhật trùng từng bit với GRPO A/A (hàm trả nguyên dict TRL khi không phải bù).

Metric TRL (reward, reward_std, frac_reward_zero_std, completions/*, rewards/*) bị append một lần mỗi lần gọi sinh;
các lần gọi BÙ bị cắt khỏi danh sách, nên các trường đó vẫn là của 2 câu nhắc đầu từ dataloader (so thẳng với GRPO A/A).
num_tokens giữ số token đã thấy GỒM cả rollout bù. Metric riêng mỗi bước (`dapo/…`):
  n_nhom_sinh · n_nhom_hoa · n_lan_bu · n_nhom_du · cham_tran · reward_update (thưởng TB 16 câu cập nhật) ·
  reward_rollout (thưởng TB mọi câu đã sinh) · cộng dồn cd_buoc · cd_nhom_sinh · cd_nhom_hoa · cd_lan_bu · cd_nhom_du ·
  cd_cham_tran · cd_nhom_hoa_giu · cd_bo_qua · con_tro (vị trí bộ lặp bù).
Cộng dồn sống qua resume: dựng lại từ log_history của điểm lưu (như b_tu_log của grpo_luoi) và ghi `dapo_ngan_sach.json`
trong --out sau mỗi bước. _logs của TRL (chỉ dùng khi log_completions, tức --probe) giữ 16 hàng của lần gọi CUỐI.

Cờ MỚI so với grpo_codien: --dapo-max-bu (8) · --selftest-algo · --selftest-cpu [--vl] [--out D].

  python grpo_dapo_ds.py --selftest-algo               # CPU, không mạng: chọn/ghép dict TRL, vòng bù, lợi thế
  python grpo_dapo_ds.py --selftest-cpu [--vl]         # CPU: 3 bước + resume + chạm trần trên mô hình tí hon
  python grpo_dapo_ds.py --train --no-q4 --bs 4 --accum 4 --gen-chunk 8 --algo dapo_ds --reward spice --seed 101 \
      --bundle B --merged M --out O --resume auto --keys-ck500 K --eps-high 0.28
"""
import os, sys, json, math, copy, random, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grpo_codien as CD                                  # noqa: E402
GL = CD.GL

TEN = "dapo_ds"
HS = dict(max_bu=8)
NGAN_SACH = "dapo_ngan_sach.json"
NGUONG_HOA = 1e-9
_lop = GL.lop_trainer

# ============================ chọn hàng + ghép dict TRL (tensor thuần) ============================
# Mọi khoá dict đầu ra của GRPOTrainer._generate_and_score_completions (TRL 0.29.1, grpo_trainer.py:1994–2026).
K_PROMPT = {"prompt_ids": "pad", "prompt_mask": 0}                       # (B, P), đệm TRÁI (dòng 1721–1722)
K_COMP = {"completion_ids": "pad", "completion_mask": 0,                 # (B, C), đệm PHẢI (dòng 1725–1726)
          "old_per_token_logps": 0.0, "ref_per_token_logps": 0.0,        # (B, C) hoặc vắng khi None (1858, 1922)
          "sampling_per_token_logps": 0.0,                               # (B, C) chỉ khi có logprobs lúc sinh (1729)
          "tool_mask": 1}                                                # (B, C) đệm 1 (1736)
K_PC = ("token_type_ids", "mm_token_type_ids")                           # (B, P+C): phần prompt đệm trái, phần câu đệm phải (1786–1797)
K_HANG = ("advantages", "pixel_attention_mask", "image_sizes")           # theo hàng (một ảnh/hàng), đuôi phải cùng cỡ
K_ANH = ("pixel_values", "image_grid_thw", "num_images")                 # patch nối phẳng theo ảnh (Qwen2.5-VL)
K_SO = ("num_items_in_batch",)                                           # tensor 0 chiều = tổng token câu sinh (1616)
K_CAM = ("importance_sampling_ratio",)                                   # chỉ có với vLLM: không hỗ trợ
K_BIET = set(K_PROMPT) | set(K_COMP) | set(K_PC) | set(K_HANG) | set(K_ANH) | set(K_SO)


def kiem_khoa(d):
    cam = [k for k in d if k in K_CAM]
    assert not cam, f"⛔ dapo_ds không hỗ trợ khoá {cam} (vLLM)"
    la = sorted(set(d) - K_BIET)
    assert not la, f"⛔ dict TRL có khoá lạ {la}: phải viết cách ghép trước khi chạy (không ghép im lặng)"
    for k in ("prompt_ids", "prompt_mask", "completion_ids", "completion_mask", "advantages", "num_items_in_batch"):
        assert k in d, f"⛔ dict TRL thiếu khoá {k}"


def _dem(t, n, v, trai):
    """Đệm chiều 1 của t (B, L, ...) tới n bằng v, bên trái hoặc phải."""
    import torch
    L = t.size(1)
    if L == n:
        return t
    p = torch.full((t.size(0), n - L) + tuple(t.shape[2:]), v, dtype=t.dtype, device=t.device)
    return torch.cat([p, t] if trai else [t, p], 1)


def _anh_theo_hang(d):
    """Cắt pixel_values / image_grid_thw thành từng hàng (theo num_images), như split_pixel_values_by_grid của TRL."""
    import torch
    from itertools import accumulate
    ni = list(d["num_images"])
    dai = d["image_grid_thw"].prod(-1).tolist()
    assert sum(dai) == d["pixel_values"].size(0), f"⛔ tổng patch {sum(dai)} ≠ {d['pixel_values'].size(0)}"
    assert len(dai) == sum(ni) and len(ni) == d["prompt_ids"].size(0), (len(dai), ni)
    b = [0, *accumulate(ni)]
    sec = [sum(dai[b[i]:b[i + 1]]) for i in range(len(ni))]
    return list(torch.split(d["pixel_values"], sec, 0)), list(torch.split(d["image_grid_thw"], ni, 0)), ni


def ghep_hang(nguon, pad_id, so_tok):
    """nguon: danh sách (dict TRL, [chỉ số hàng]) theo đúng thứ tự muốn ghép. Trả dict mới gồm đúng các hàng đó.

    prompt đệm trái tới P lớn nhất, câu sinh đệm phải tới C lớn nhất, *_type_ids tách tại P của từng nguồn rồi đệm hai
    phía, ảnh ghép theo hàng. so_tok: num_items_in_batch mới (int). Khoá lạ / thiếu ⇒ AssertionError.
    """
    import torch
    assert nguon, "⛔ không có hàng nào để ghép"
    for d, _ in nguon:
        kiem_khoa(d)
    khoa = set(nguon[0][0])
    for d, _ in nguon:
        assert set(d) == khoa, f"⛔ hai dict khác khoá: {sorted(set(d) ^ khoa)}"
    Pm = max(d["prompt_ids"].size(1) for d, _ in nguon)
    Cm = max(d["completion_ids"].size(1) for d, _ in nguon)
    out = {}
    for k in khoa:
        if k in K_SO:
            continue
        if k in ("pixel_values", "image_grid_thw", "num_images"):
            continue
        manh = []
        for d, ix in nguon:
            t = d[k]
            if t is None:
                manh.append(None)
                continue
            it = torch.as_tensor(ix, dtype=torch.long, device=t.device)
            P, C = d["prompt_ids"].size(1), d["completion_ids"].size(1)
            if k in K_PROMPT:
                v = pad_id if K_PROMPT[k] == "pad" else K_PROMPT[k]
                manh.append(_dem(t[it], Pm, v, True))
            elif k in K_COMP:
                v = pad_id if K_COMP[k] == "pad" else K_COMP[k]
                assert t.size(1) == C, f"⛔ {k} rộng {t.size(1)} ≠ C {C}"
                manh.append(_dem(t[it], Cm, v, False))
            elif k in K_PC:
                assert t.size(1) == P + C, f"⛔ {k} rộng {t.size(1)} ≠ P+C {P}+{C}"
                s = t[it]
                manh.append(torch.cat([_dem(s[:, :P], Pm, 0, True), _dem(s[:, P:], Cm, 0, False)], 1))
            else:                                         # K_HANG
                manh.append(t[it])
        if all(m is None for m in manh):
            out[k] = None
            continue
        assert all(m is not None for m in manh), f"⛔ {k} là None ở một nguồn mà không ở nguồn khác"
        if k in K_HANG and k != "advantages":
            assert len({tuple(m.shape[1:]) for m in manh}) == 1, f"⛔ {k} khác cỡ đuôi giữa hai nguồn"
        out[k] = torch.cat(manh, 0)
    if "pixel_values" in khoa or "image_grid_thw" in khoa or "num_images" in khoa:
        assert {"pixel_values", "image_grid_thw", "num_images"} <= khoa, "⛔ thiếu một trong ba khoá ảnh"
        pv, gt, ni = [], [], []
        for d, ix in nguon:
            p_, g_, n_ = _anh_theo_hang(d)
            for i in ix:
                pv.append(p_[i])
                gt.append(g_[i])
                ni.append(n_[i])
        out["pixel_values"], out["image_grid_thw"], out["num_images"] = torch.cat(pv, 0), torch.cat(gt, 0), ni
    n0 = nguon[0][0]["num_items_in_batch"]
    out["num_items_in_batch"] = torch.as_tensor(so_tok, dtype=n0.dtype, device=n0.device) \
        if isinstance(n0, torch.Tensor) else so_tok
    B = sum(len(ix) for _, ix in nguon)
    for k, v in out.items():
        if v is None or k in K_SO:
            continue
        n = len(v) if isinstance(v, list) else v.size(0)
        if k in ("pixel_values", "image_grid_thw"):
            continue
        assert n == B, f"⛔ {k} có {n} hàng ≠ {B}"
    return out


# ============================ chọn nhóm (thuần) ============================
def la_hoa(r):
    return (max(r) - min(r)) < NGUONG_HOA


def nhom_huu_hieu(r, G):
    assert len(r) % G == 0, (len(r), G)
    return [g for g in range(len(r) // G) if not la_hoa(r[g * G:(g + 1) * G])]


def vong_bu(r0, goi_bu, G, can, max_bu):
    """r0: thưởng của lượt đầu. goi_bu(): sinh + chấm thêm một khúc, trả thưởng. Trả (chọn, n_bu, chạm trần, hoà-giữ, thống kê).

    chọn: danh sách (lượt, nhóm) đúng `can` phần tử; lượt 0 là lượt đầu. hoà-giữ: các (0, nhóm) hoà bị buộc giữ khi chạm trần.
    """
    luot_r = [r0]
    chon = [(0, g) for g in nhom_huu_hieu(r0, G)][:can]
    n_bu = 0
    while len(chon) < can and n_bu < max_bu:
        r = goi_bu()
        luot_r.append(r)
        n_bu += 1
        for g in nhom_huu_hieu(r, G):
            if len(chon) < can:
                chon.append((len(luot_r) - 1, g))
    tran = len(chon) < can
    giu = []
    if tran:
        hoa0 = [(0, g) for g in range(len(r0) // G) if (0, g) not in chon]
        giu = hoa0[:can - len(chon)]
        chon = chon + giu
    assert len(chon) == can
    n_sinh = sum(len(r) // G for r in luot_r)
    n_hoa = sum(len(r) // G - len(nhom_huu_hieu(r, G)) for r in luot_r)
    n_du = (n_sinh - n_hoa) - (can - len(giu))
    return chon, n_bu, tran, giu, dict(n_nhom_sinh=n_sinh, n_nhom_hoa=n_hoa, n_nhom_du=n_du)


def a_grpo_nhom(r, G):
    """Lợi thế TRL với scale_rewards='group' (grpo_trainer.py:1886–1905): (r − TB nhóm)/(std nhóm + 1e-4)."""
    import torch
    t = torch.tensor(r, dtype=torch.float32).view(-1, G)
    return ((t - t.mean(1, keepdim=True)) / (t.std(1, keepdim=True) + 1e-4)).flatten()


# ============================ lớp trainer ============================
CD_KHOA = ("cd_buoc", "cd_nhom_sinh", "cd_nhom_hoa", "cd_lan_bu", "cd_nhom_du", "cd_cham_tran", "cd_nhom_hoa_giu",
           "cd_bo_qua", "con_tro")


def lop_trainer():
    import torch
    B = _lop()

    class DapoTrainer(B):
        _algo_that = "grpo"
        _dapo = None
        _dapo_lens = None
        _dapo_nk = None                                   # nhật ký từng bước (selftest đọc)
        _perm_cache = None

        # vòng lặp cha (LuoiTrainer) xử dapo_ds đúng như grpo: lợi thế TRL, không tính lại
        @property
        def algo(self):
            return "grpo" if self._algo_that == TEN else self._algo_that

        @algo.setter
        def algo(self, v):
            self._algo_that = v

        def _st(self):
            if self._dapo is None:
                self._dapo = {k: 0 for k in CD_KHOA}
                self._dapo_nk = []
            return self._dapo

        def train(self, resume_from_checkpoint=None, *args, **kw):
            if self._algo_that == TEN and isinstance(resume_from_checkpoint, str):
                self._dung_lai(resume_from_checkpoint)
            return super().train(resume_from_checkpoint, *args, **kw)

        def _dung_lai(self, ck):
            """Dựng lại bộ đếm cộng dồn + con trỏ bộ lặp bù từ log_history của điểm lưu."""
            st = json.load(open(os.path.join(ck, "trainer_state.json")))
            H = [h for h in st["log_history"] if "dapo/cd_buoc" in h]
            s = self._st()
            if H:
                for k in CD_KHOA:
                    s[k] = int(round(H[-1][f"dapo/{k}"]))
            assert s["cd_buoc"] == st["global_step"], \
                f"⛔ log dapo dừng ở bước {s['cd_buoc']} ≠ global_step {st['global_step']} (logging_steps phải = 1)"
            print(f"[dapo] dựng lại cộng dồn từ {ck}: {s}", flush=True)

        def _generate(self, prompts):
            out = super()._generate(prompts)
            self._dapo_lens = [len(x) for x in out[1]]    # độ dài câu sinh trước khi che câu bị cắt (định nghĩa TRL)
            return out

        def _perm(self, e):
            if self._perm_cache is None or self._perm_cache[0] != e:
                p = list(range(len(self.train_dataset)))
                random.Random(int(self.args.seed) * 100003 + 7919 + e).shuffle(p)
                self._perm_cache = (e, p)
            return self._perm_cache[1]

        def _lay_bu(self, k, dang_co):
            ds, s = self.train_dataset, self._st()
            if not hasattr(self, "_pool_keys"):
                self._pool_keys = list(ds["key"])
                assert len(set(self._pool_keys)) == len(self._pool_keys), "⛔ pool có key trùng"
            N = len(self._pool_keys)
            assert N - len(dang_co) >= k, f"⛔ pool {N} câu nhắc không đủ để bù {k} (đang có {len(dang_co)})"
            rows, chon = [], set()
            for _ in range(3 * N):
                e, p = divmod(s["con_tro"], N)
                i = self._perm(e)[p]
                s["con_tro"] += 1
                key = self._pool_keys[i]
                if key in dang_co or key in chon:
                    s["cd_bo_qua"] += 1
                    continue
                chon.add(key)
                rows.append(ds[int(i)])
                if len(rows) == k:
                    return rows
            raise RuntimeError("⛔ bộ lặp bù không lấy đủ câu nhắc")

        def _mot_luot(self, inputs):
            out = super()._generate_and_score_completions(inputs)
            r = [float(x) for x in GL.LAST["r"]]
            lens = list(self._dapo_lens)
            keys = [x["key"] for x in inputs]
            assert len(r) == len(lens) == len(inputs) == out["advantages"].numel(), \
                (len(r), len(lens), len(inputs), out["advantages"].shape)
            G = self.num_generations
            assert all(len(set(keys[i:i + G])) == 1 for i in range(0, len(keys), G)), "⛔ nhóm không cùng câu nhắc"
            return out, r, lens, keys

        def _tong_tham_so(self):
            with torch.no_grad():
                return sum(float(p.detach().float().sum()) for p in self.model.parameters() if p.requires_grad)

        def _generate_and_score_completions(self, inputs):
            if self._algo_that != TEN or not self.model.training:
                return super()._generate_and_score_completions(inputs)
            assert self.accelerator.num_processes == 1, "⛔ dapo_ds chỉ viết cho một tiến trình"
            assert not self.use_vllm, "⛔ dapo_ds không hỗ trợ vLLM"
            assert self.scale_rewards == "group" and self.multi_objective_aggregation == "sum_then_normalize", \
                "⛔ dapo_ds cần lợi thế chuẩn hoá theo nhóm (độc lập giữa các nhóm)"
            assert len(self.reward_funcs) == 1 and float(self.reward_weights[0]) == 1.0
            G = self.num_generations
            can = len(inputs) // G
            assert can * G == len(inputs) == self.args.generation_batch_size, (len(inputs), G)
            s = self._st()
            mt = self._metrics["train"]
            gs0, th0 = self.state.global_step, self._tong_tham_so()

            luot = [self._mot_luot(inputs)]
            snap = {k: len(v) for k, v in mt.items()}
            dang_co = set(luot[0][3])
            bu_keys = []

            def goi_bu():
                rows = self._lay_bu(can, dang_co)
                inp = [copy.deepcopy(x) for x in rows for _ in range(G)]
                o = self._mot_luot(inp)
                luot.append(o)
                dang_co.update(o[3])
                bu_keys.extend(o[3][::G])
                return o[1]

            chon, n_bu, tran, giu, tk = vong_bu(luot[0][1], goi_bu, G, can, HS["max_bu"])
            assert self.state.global_step == gs0 and self._tong_tham_so() == th0, \
                "⛔ chính sách đổi trong lúc lấy mẫu bù"
            for k in list(mt.keys()):                     # cắt metric TRL của các lần gọi bù (giữ num_tokens cộng dồn)
                if k.startswith("dapo/"):
                    continue
                if k in snap:
                    del mt[k][snap[k]:]
                else:
                    del mt[k]

            # lợi thế của nhóm giữ = lợi thế TRL lúc sinh, độc lập giữa nhóm (kiểm lại từng nhóm)
            for li, g in chon:
                o, r = luot[li][0], luot[li][1]
                a = o["advantages"][g * G:(g + 1) * G].float().cpu()
                ky = a_grpo_nhom(r[g * G:(g + 1) * G], G)
                assert torch.allclose(a, ky, atol=1e-3, rtol=1e-3), f"⛔ lợi thế nhóm ({li},{g}) khác GRPO theo nhóm"

            if n_bu == 0 and chon == [(0, g) for g in range(can)]:
                out = luot[0][0]                          # không bù: trả nguyên dict TRL (trùng GRPO A/A)
            else:
                seg = [(luot[li][0], list(range(g * G, (g + 1) * G))) for li, g in chon]
                so_tok = sum(sum(luot[li][2][g * G:(g + 1) * G]) for li, g in chon)
                out = ghep_hang(seg, self.pad_token_id, so_tok)
                if giu:                                   # nhóm hoà bị buộc giữ khi chạm trần: A = 0 đúng
                    for j, (li, g) in enumerate(chon):
                        if (li, g) in giu:
                            out["advantages"][j * G:(j + 1) * G] = 0.0
            r_up = [x for li, g in chon for x in luot[li][1][g * G:(g + 1) * G]]
            r_all = [x for o in luot for x in o[1]]
            GL.LAST["r"] = list(r_up)
            assert out["prompt_ids"].size(0) == len(inputs) == out["advantages"].numel()

            s["cd_buoc"] += 1
            s["cd_nhom_sinh"] += tk["n_nhom_sinh"]
            s["cd_nhom_hoa"] += tk["n_nhom_hoa"]
            s["cd_nhom_du"] += tk["n_nhom_du"]
            s["cd_lan_bu"] += n_bu
            s["cd_cham_tran"] += int(tran)
            s["cd_nhom_hoa_giu"] += len(giu)
            for k, v in tk.items():
                mt[f"dapo/{k}"].append(float(v))
            mt["dapo/n_lan_bu"].append(float(n_bu))
            mt["dapo/cham_tran"].append(float(tran))
            mt["dapo/reward_update"].append(sum(r_up) / len(r_up))
            mt["dapo/reward_rollout"].append(sum(r_all) / len(r_all))
            for k in CD_KHOA:
                mt[f"dapo/{k}"].append(float(s[k]))
            if tran:
                print(f"⚠️ [dapo] chạm trần {HS['max_bu']} lần bù ở bước {gs0 + 1}: giữ {len(giu)} nhóm hoà với A = 0",
                      flush=True)
            print(f"[dapo] bước {gs0 + 1} · sinh {tk['n_nhom_sinh']} nhóm · hoà {tk['n_nhom_hoa']} · bù {n_bu} lần · "
                  f"cộng dồn rollout {s['cd_nhom_sinh']} câu nhắc", flush=True)
            self._dapo_nk.append(dict(buoc=gs0 + 1, chon=chon, n_bu=n_bu, tran=tran, giu=giu, bu_keys=bu_keys,
                                      keys_dau=luot[0][3][::G], B=int(out["prompt_ids"].size(0)),
                                      hoa_trong_lo=[la_hoa(luot[li][1][g * G:(g + 1) * G]) for li, g in chon],
                                      so_tok=int(out["num_items_in_batch"]), khoa=sorted(out),
                                      n_anh=(int(out["image_grid_thw"].size(0)) if "image_grid_thw" in out else 0),
                                      n_patch=(int(out["pixel_values"].size(0)) if "pixel_values" in out else 0), **tk))
            self._ghi_ngan_sach()
            return out

        def _ghi_ngan_sach(self):
            s, G = self._st(), self.num_generations
            can = self.args.generation_batch_size // G
            ns = dict(
                thuat_toan=TEN, G=G, nhom_moi_buoc=can, max_bu=HS["max_bu"], seed=int(self.args.seed),
                beta=self.beta, loss_type=self.loss_type, epsilon_low=self.epsilon_low, epsilon_high=self.epsilon_high,
                num_iterations=self.num_iterations, mask_truncated_completions=self.mask_truncated_completions,
                buoc=s["cd_buoc"],
                cau_nhac_update=s["cd_buoc"] * can, cau_sinh_update=s["cd_buoc"] * can * G,
                cau_nhac_update_huu_hieu=s["cd_buoc"] * can - s["cd_nhom_hoa_giu"],
                cau_nhac_rollout=s["cd_nhom_sinh"], cau_sinh_rollout=s["cd_nhom_sinh"] * G,
                nhom_hoa_bi_loai=s["cd_nhom_hoa"] - s["cd_nhom_hoa_giu"], nhom_hoa_giu_khi_cham_tran=s["cd_nhom_hoa_giu"],
                nhom_huu_hieu_du_bo=s["cd_nhom_du"], lan_bu=s["cd_lan_bu"], buoc_cham_tran=s["cd_cham_tran"],
                cau_nhac_bo_qua_vi_dang_trong_lo=s["cd_bo_qua"], con_tro_bo_lap_bu=s["con_tro"],
                ti_le_rollout_tren_update=(s["cd_nhom_sinh"] / max(1, s["cd_buoc"] * can)),
            )
            os.makedirs(self.args.output_dir, exist_ok=True)
            p = os.path.join(self.args.output_dir, NGAN_SACH)
            json.dump(ns, open(p + ".tmp", "w"), ensure_ascii=False, indent=1)
            os.replace(p + ".tmp", p)

    return DapoTrainer


# ============================ tự kiểm ============================
def _dict_gia(tag, G, nhom, P, C, so_patch, pad_id, Fdim=3, ref=True, mm=True):
    """Dict giả cùng khuôn TRL: hàng i có prompt thật dài P-i%3 (đệm trái), câu thật dài C-i%2 (đệm phải)."""
    import torch
    B = G * nhom
    pi = torch.full((B, P), pad_id)
    pm = torch.zeros(B, P, dtype=torch.long)
    ci = torch.full((B, C), pad_id)
    cm = torch.zeros(B, C, dtype=torch.long)
    lens = []
    for i in range(B):
        lp, lc = P - i % 3, C - i % 2
        pi[i, P - lp:] = torch.arange(lp) + 1000 * tag + 10 * i
        pm[i, P - lp:] = 1
        ci[i, :lc] = torch.arange(lc) + 5000 + 1000 * tag + 10 * i
        cm[i, :lc] = 1
        lens.append(lc)
    d = dict(prompt_ids=pi, prompt_mask=pm, completion_ids=ci, completion_mask=cm,
             advantages=torch.arange(B, dtype=torch.float32) + 100 * tag,
             num_items_in_batch=torch.tensor(sum(lens)))
    if ref:
        d["ref_per_token_logps"] = (-torch.rand(B, C)) * cm
    if mm:
        d["mm_token_type_ids"] = torch.cat([pm * (tag + 1), torch.zeros(B, C, dtype=torch.long)], 1)
    grid = torch.tensor([[1, 2, so_patch[i % len(so_patch)] // 2] for i in range(B)])
    n = grid.prod(-1)
    d["image_grid_thw"] = grid
    d["pixel_values"] = torch.cat([torch.full((int(n[i]), Fdim), float(1000 * tag + i)) for i in range(B)], 0)
    d["num_images"] = [1] * B
    return d, lens


def selftest_algo(_):
    import torch
    pad = 7
    G = 4
    d1, l1 = _dict_gia(1, G, 2, P=5, C=6, so_patch=[4, 6, 8], pad_id=pad)
    d2, l2 = _dict_gia(2, G, 2, P=8, C=3, so_patch=[10, 2], pad_id=pad)
    # 1. ghép toàn bộ một nguồn = chính nó
    full = ghep_hang([(d1, list(range(8)))], pad, sum(l1))
    for k in d1:
        a, b = d1[k], full[k]
        assert (a == b) if isinstance(a, list) else torch.equal(torch.as_tensor(a), torch.as_tensor(b)), k
    # 2. ghép nhóm 1 của d1 + nhóm 0 của d2
    seg = [(d1, [4, 5, 6, 7]), (d2, [0, 1, 2, 3])]
    so = sum(l1[4:8]) + sum(l2[0:4])
    o = ghep_hang(seg, pad, so)
    assert o["prompt_ids"].shape == (8, 8) and o["completion_ids"].shape == (8, 6), (o["prompt_ids"].shape,
                                                                                       o["completion_ids"].shape)
    assert o["mm_token_type_ids"].shape == (8, 14) and o["ref_per_token_logps"].shape == (8, 6)
    assert int(o["num_items_in_batch"]) == so and o["num_items_in_batch"].dtype == d1["num_items_in_batch"].dtype
    assert int(o["completion_mask"].sum()) == so                       # (dict giả: không câu nào bị cắt)
    j = 0
    for d, ix in seg:
        P, C = d["prompt_ids"].size(1), d["completion_ids"].size(1)
        for i in ix:
            # token thật trùng nguồn, đệm đúng phía, mask khớp
            assert torch.equal(o["prompt_ids"][j][o["prompt_mask"][j].bool()], d["prompt_ids"][i][d["prompt_mask"][i].bool()])
            assert torch.equal(o["completion_ids"][j][o["completion_mask"][j].bool()],
                               d["completion_ids"][i][d["completion_mask"][i].bool()])
            pmj, cmj = o["prompt_mask"][j], o["completion_mask"][j]
            assert pmj[-1] == 1 and bool((pmj[1:] >= pmj[:-1]).all()), "⛔ prompt phải đệm TRÁI"
            assert cmj[0] == 1 and bool((cmj[1:] <= cmj[:-1]).all()), "⛔ câu sinh phải đệm PHẢI"
            assert int(pmj.sum()) == int(d["prompt_mask"][i].sum()) and int(cmj.sum()) == int(d["completion_mask"][i].sum())
            assert (o["prompt_ids"][j][~o["prompt_mask"][j].bool()] == pad).all()
            assert (o["completion_ids"][j][~o["completion_mask"][j].bool()] == pad).all()
            assert torch.equal(o["ref_per_token_logps"][j][:C], d["ref_per_token_logps"][i]) and \
                (o["ref_per_token_logps"][j][C:] == 0).all()
            mmj = o["mm_token_type_ids"][j]
            assert torch.equal(mmj[:8][o["prompt_mask"][j].bool()], d["mm_token_type_ids"][i][:P][d["prompt_mask"][i].bool()])
            assert (mmj[8:] == 0).all()
            assert torch.equal(o["advantages"][j], d["advantages"][i])
            assert torch.equal(o["image_grid_thw"][j], d["image_grid_thw"][i])
            j += 1
    # pixel_values: đúng thứ tự, đúng số patch mỗi ảnh (số patch khác nhau giữa các ảnh)
    n = o["image_grid_thw"].prod(-1).tolist()
    assert sum(n) == o["pixel_values"].size(0) and o["num_images"] == [1] * 8
    vals = []
    for (d, ix) in seg:
        tag = 1 if d is d1 else 2
        vals += [1000 * tag + i for i in ix]
    off = 0
    for v, k in zip(vals, n):
        assert (o["pixel_values"][off:off + k] == v).all(), "⛔ pixel_values lệch hàng"
        off += k
    # tách lại theo TRL (split_pixel_values_by_grid) phải đi qua
    try:
        from trl.trainer.utils import split_pixel_values_by_grid, unsplit_pixel_values_by_grid
        u = unsplit_pixel_values_by_grid(split_pixel_values_by_grid(dict(o)))
        assert torch.equal(u["pixel_values"], o["pixel_values"])
        print("  ghép ảnh tương thích split/unsplit_pixel_values_by_grid của TRL ✓")
    except ImportError:
        print("  (chưa có trl: bỏ phép đối chiếu split_pixel_values_by_grid)")
    # 3. khoá lạ / khoá cấm phải dừng
    for bad in ("khoa_la", "importance_sampling_ratio"):
        x = dict(d1)
        x[bad] = torch.zeros(8)
        try:
            ghep_hang([(x, [0])], pad, 1)
            raise SystemExit(f"⛔ khoá {bad} không bị chặn")
        except AssertionError:
            pass
    # 4. vòng bù: nhóm hoà bị loại, bù tới đủ, lợi thế giữ nguyên
    G8 = 8
    hoa, thuong = [0.5] * G8, [0.1 * i for i in range(G8)]
    luot = iter([hoa + hoa, hoa + thuong, thuong + thuong])
    chon, n_bu, tran, giu, tk = vong_bu(thuong + hoa, lambda: next(luot), G8, 2, 8)
    assert chon == [(0, 0), (2, 1)] and n_bu == 2 and not tran and not giu, (chon, n_bu)
    assert tk == dict(n_nhom_sinh=6, n_nhom_hoa=4, n_nhom_du=0), tk
    chon, n_bu, tran, giu, tk = vong_bu(hoa + thuong, lambda: thuong + thuong, G8, 2, 8)   # khúc bù thừa một nhóm
    assert chon == [(0, 1), (1, 0)] and n_bu == 1 and tk == dict(n_nhom_sinh=4, n_nhom_hoa=1, n_nhom_du=1), (chon, tk)
    chon, n_bu, tran, giu, tk = vong_bu(hoa + hoa, lambda: hoa + hoa, G8, 2, 3)
    assert tran and n_bu == 3 and chon == giu == [(0, 0), (0, 1)] and tk["n_nhom_hoa"] == 8, (chon, tk)
    chon, n_bu, tran, giu, _ = vong_bu(thuong + thuong, lambda: 1 / 0, G8, 2, 8)
    assert chon == [(0, 0), (0, 1)] and n_bu == 0
    # 5. lợi thế theo nhóm độc lập: chuẩn hoá cả lô ≠, từng nhóm =
    r = [0.1, 0.4, 0.2, 0.9, 3.0, 3.5, 2.0, 2.2]
    A = a_grpo_nhom(r, 4)
    assert torch.allclose(A[:4], a_grpo_nhom(r[:4], 4)) and torch.allclose(A[4:], a_grpo_nhom(r[4:], 4))
    assert torch.allclose(a_grpo_nhom(hoa, G8), torch.zeros(G8))
    assert torch.allclose(A, GL.loi_the("grpo", r, 4)[0], atol=1e-6)   # trùng công thức grpo của lưới
    print("✅ selftest dapo_ds ĐẠT: chọn/ghép dict TRL (đệm trái/phải, mm_token_type_ids, ref logps, ảnh nhiều patch, "
          "num_items_in_batch, khoá lạ) · vòng bù · chạm trần · lợi thế theo nhóm")


def selftest_cpu(a):
    """Mô hình tí hon CPU fp32: 3 bước dapo_ds với thưởng ép nhóm hoà, rồi resume từ điểm lưu bước 2, rồi chạm trần."""
    import re, time, shutil, torch, transformers, trl, peft
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model
    from trl import GRPOConfig
    from datasets import Dataset
    print(f"trl {trl.__version__} · transformers {transformers.__version__} · peft {peft.__version__} · "
          f"torch {torch.__version__}", flush=True)
    goc = a.out or "/tmp/dapo_ds_cpu"
    shutil.rmtree(goc, ignore_errors=True)
    golds = ["Click on the search bar", "Open the Clock app", "Swipe up to see more", "Type hello in the box"]
    W = re.compile(r"[a-z0-9]+")
    HANG = {f"k{i}" for i in range(16) if i % 4 != 0}       # 75% câu nhắc thưởng HẰNG ⇒ nhóm hoà
    mode = {"tat_ca_hang": False}

    def r_gia(completions, gold, key, **kw):
        out = []
        for c, g, k in zip(completions, gold, key):
            if mode["tat_ca_hang"] or k in HANG:
                out.append(0.5)
                continue
            a_, b_ = set(W.findall(GL.GS._text(c).lower())), set(W.findall(g.lower()))
            kk = len(a_ & b_)
            out.append((0.0 if not kk else 2 * kk / (len(a_) + len(b_))) + 0.01 * (len(GL.GS._text(c)) % 7))
        GL.LAST["r"] = list(out)
        return out

    if a.vl:
        from PIL import Image
        from transformers import AutoProcessor, AutoModelForImageTextToText
        Mten = "trl-internal-testing/tiny-Qwen2_5_VLForConditionalGeneration"
        kich = [(56, 56), (84, 56), (112, 84), (56, 112)]   # số patch khác nhau giữa các ảnh
        rows = [dict(key=f"k{i}", image=Image.new("RGB", kich[i % 4], (i * 15, 80, 160)),
                     prompt=[{"role": "user", "content": f"Describe step {i}"}], gold=golds[i % 4]) for i in range(16)]
    else:
        Mten = "trl-internal-testing/tiny-Qwen2ForCausalLM-2.5"
        rows = [dict(key=f"k{i}", prompt=[{"role": "user", "content": f"Describe step {i}"}], gold=golds[i % 4])
                for i in range(16)]
    pool = {r["key"] for r in rows}

    def dung(out, max_steps, save_steps, max_bu):
        HS["max_bu"] = max_bu
        transformers.set_seed(101)
        if a.vl:
            tk = AutoProcessor.from_pretrained(Mten)
            tk.tokenizer.padding_side = "left"
            m = AutoModelForImageTextToText.from_pretrained(Mten, dtype=torch.float32)
        else:
            tk = AutoTokenizer.from_pretrained(Mten)
            tk.padding_side = "left"
            m = AutoModelForCausalLM.from_pretrained(Mten, dtype=torch.float32)
        m = get_peft_model(m, LoraConfig(r=8, lora_alpha=16, lora_dropout=0.0, target_modules=["q_proj", "v_proj"],
                                         task_type="CAUSAL_LM"))
        args = GRPOConfig(output_dir=out, seed=101, num_generations=8, per_device_train_batch_size=4,
                          gradient_accumulation_steps=4, max_completion_length=12, temperature=1.0, top_p=1.0, top_k=0,
                          beta=0.04, learning_rate=1e-2, max_steps=max_steps, logging_steps=1, save_steps=save_steps,
                          report_to="none", remove_unused_columns=False, use_cpu=True, bf16=False, fp16=False,
                          lr_scheduler_type="constant", disable_tqdm=True, mask_truncated_completions=False,
                          scale_rewards="group", loss_type="dapo", num_iterations=1, epsilon_high=0.28)
        ds = Dataset.from_list(rows)
        T = lop_trainer()
        tr = T(model=m, reward_funcs=[r_gia], args=args, train_dataset=ds, processing_class=tk)
        tr.algo, tr.thuong = TEN, r_gia
        return tr

    # lượt chính: 3 bước, điểm lưu ở bước 2
    t0 = time.time()
    o1 = os.path.join(goc, "chinh")
    tr = dung(o1, 3, 2, 8)
    assert tr.algo == "grpo" and tr._algo_that == TEN
    nB = lambda t: sum(p.norm().item() for n_, p in t.model.named_parameters() if "lora_B" in n_)
    truoc = nB(tr)
    tr.train()
    sau = nB(tr)
    H = tr.state.log_history
    loss = [h["loss"] for h in H if "loss" in h]
    nk = tr._dapo_nk
    print("[nhật ký]", json.dumps([{k: v for k, v in x.items() if k not in ("hoa_trong_lo",)} for x in nk],
                                  ensure_ascii=False), flush=True)
    assert len(nk) == 3 and all(x["B"] == 16 for x in nk), [x["B"] for x in nk]
    if a.vl:                                              # lô ghép thật có ảnh: đủ khoá, 16 ảnh, số patch khác nhau
        for x in nk:
            assert {"pixel_values", "image_grid_thw", "num_images", "mm_token_type_ids"} <= set(x["khoa"]), x["khoa"]
            assert x["n_anh"] == 16 and x["n_patch"] > 0, x
        print(f"[ảnh] khoá dict ghép: {nk[0]['khoa']} · patch mỗi bước {[x['n_patch'] for x in nk]}", flush=True)
    assert all(not any(x["hoa_trong_lo"]) or x["tran"] for x in nk), "⛔ có nhóm hoà trong lô cập nhật"
    assert sum(x["n_bu"] for x in nk) > 0, "⛔ không có lần bù nào (thưởng giả phải ép nhóm hoà)"
    for x in nk:
        assert set(x["bu_keys"]) <= pool, "⛔ câu nhắc bù ngoài pool"
        assert not set(x["bu_keys"]) & set(x["keys_dau"]) and len(set(x["bu_keys"])) == len(x["bu_keys"]), \
            "⛔ câu nhắc bù trùng câu nhắc đang có trong lô"
    assert len(loss) == 3 and all(math.isfinite(v) for v in loss), loss
    assert sau > truoc, "⛔ lora_B không đổi"
    # metric: mỗi trường TRL một giá trị/bước (lần gọi bù đã cắt), metric dapo có mặt
    for h in [h for h in H if "loss" in h]:
        for k in ("dapo/n_nhom_sinh", "dapo/n_nhom_hoa", "dapo/n_lan_bu", "dapo/cd_nhom_sinh", "dapo/con_tro", "reward"):
            assert k in h, f"⛔ log thiếu {k}"
    # ngân sách ghi đúng
    ns = json.load(open(os.path.join(o1, NGAN_SACH)))
    s = tr._dapo
    assert ns["buoc"] == 3 and ns["cau_nhac_update"] == 6 and ns["cau_sinh_update"] == 48
    assert ns["cau_nhac_rollout"] == sum(x["n_nhom_sinh"] for x in nk) == 2 * 3 + 2 * sum(x["n_bu"] for x in nk)
    assert ns["lan_bu"] == sum(x["n_bu"] for x in nk) and ns["cau_sinh_rollout"] == 8 * ns["cau_nhac_rollout"]
    assert ns["nhom_hoa_bi_loai"] + ns["nhom_hoa_giu_khi_cham_tran"] == s["cd_nhom_hoa"]
    assert ns["cau_nhac_rollout"] == ns["cau_nhac_update"] + s["cd_nhom_hoa"] + ns["nhom_huu_hieu_du_bo"] - \
        ns["nhom_hoa_giu_khi_cham_tran"]
    assert abs(ns["epsilon_high"] - 0.28) < 1e-12 and ns["beta"] == 0.04 and ns["loss_type"] == "dapo"
    print(f"[lượt chính] ĐẠT · loss {[round(v, 4) for v in loss]} · lora_B {truoc:.4f} → {sau:.4f} · "
          f"ngân sách {json.dumps(ns, ensure_ascii=False)} · {time.time() - t0:.0f}s", flush=True)

    # resume: tiếp từ checkpoint-2, cộng dồn phải dựng lại đúng giá trị ở bước 2 rồi đi tiếp như lượt chính
    ck = os.path.join(o1, "checkpoint-2")
    assert os.path.exists(os.path.join(ck, "trainer_state.json")), "⛔ không có checkpoint-2"
    h2 = [h for h in json.load(open(os.path.join(ck, "trainer_state.json")))["log_history"] if "dapo/cd_buoc" in h][-1]
    o2 = os.path.join(goc, "tiep")
    shutil.copytree(ck, os.path.join(o2, "checkpoint-2"))
    tr2 = dung(o2, 3, 10 ** 6, 8)
    tr2._dung_lai(os.path.join(o2, "checkpoint-2"))
    for k in CD_KHOA:
        assert tr2._dapo[k] == int(h2[f"dapo/{k}"]), (k, tr2._dapo[k], h2)
    tr2._dapo = None                                       # để train(resume=...) tự dựng lại lần nữa qua đường thật
    tr2.train(resume_from_checkpoint=os.path.join(o2, "checkpoint-2"))
    ns2 = json.load(open(os.path.join(o2, NGAN_SACH)))
    assert ns2["buoc"] == 3 and ns2["cau_nhac_rollout"] == int(h2["dapo/cd_nhom_sinh"]) + tr2._dapo_nk[-1]["n_nhom_sinh"]
    assert ns2["con_tro_bo_lap_bu"] >= int(h2["dapo/con_tro"])
    print(f"[resume] ĐẠT · cộng dồn ở bước 2 {dict((k, int(h2['dapo/' + k])) for k in CD_KHOA)} · "
          f"sau bước 3 rollout {ns2['cau_nhac_rollout']} câu nhắc", flush=True)

    # chạm trần: mọi câu nhắc thưởng hằng, trần 1 lần bù ⇒ giữ 2 nhóm hoà với A = 0, vẫn B = 16, loss hữu hạn
    mode["tat_ca_hang"] = True
    o3 = os.path.join(goc, "tran")
    tr3 = dung(o3, 1, 10 ** 6, 1)
    tr3.train()
    x = tr3._dapo_nk[0]
    assert x["tran"] and x["n_bu"] == 1 and len(x["giu"]) == 2 and x["B"] == 16, x
    l3 = [h["loss"] for h in tr3.state.log_history if "loss" in h]
    assert l3 and all(math.isfinite(v) for v in l3), l3
    ns3 = json.load(open(os.path.join(o3, NGAN_SACH)))
    assert ns3["buoc_cham_tran"] == 1 and ns3["nhom_hoa_giu_khi_cham_tran"] == 2 and ns3["cau_nhac_rollout"] == 4
    print(f"[chạm trần] ĐẠT · {json.dumps(ns3, ensure_ascii=False)}", flush=True)
    print(f"✅ selftest CPU dapo_ds ĐẠT ({'Qwen2.5-VL tí hon, có ảnh' if a.vl else 'Qwen2 tí hon, chỉ văn bản'})",
          flush=True)


# ============================ chạy ============================
GL.ALGOS = GL.ALGOS + (TEN,)
GL.lop_trainer = lop_trainer


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--algo", default=TEN)
    ap.add_argument("--dapo-max-bu", type=int, default=HS["max_bu"])
    ap.add_argument("--selftest-algo", action="store_true")
    ap.add_argument("--selftest-cpu", action="store_true")
    ap.add_argument("--vl", action="store_true")
    a, rest = ap.parse_known_args()
    HS["max_bu"] = a.dapo_max_bu
    if a.selftest_algo:
        return selftest_algo(a)
    if a.selftest_cpu:
        a.out = rest[rest.index("--out") + 1] if "--out" in rest else ""
        return selftest_cpu(a)
    if a.algo != TEN:
        raise SystemExit(f"⛔ tệp này chỉ chạy --algo {TEN}; thuật toán khác dùng grpo_codien.py / grpo_moi_b*.py")
    if "--eps-high" not in rest:
        print("⚠️ thiếu --eps-high: DAPO dùng ε_high = 0,28 (không tác dụng khi μ = 1, đặt cho đúng công thức)", flush=True)
    print(f"[dapo_ds] lấy mẫu động thật · trần {HS['max_bu']} lần bù/bước · loss_type dapo · β giữ 0,04 "
          f"(KHÁC bài gốc β = 0) · cờ chuyển tiếp {rest}", flush=True)
    CD.main(rest + ["--algo", TEN])


if __name__ == "__main__":
    main()
