# -*- coding: utf-8 -*-
"""
FREE · offline — hồ sơ BƯỚC của AndroidControl test (mọi episode có sẵn trong cache HF).

Vá hai chỗ hở của report/98:
  · lỗ 2 "~53% bước là chạm" — con số cũ lấy từ pilot 188 bước, cần đếm trên toàn bộ
    dữ liệu local, tách rõ nhóm nào bộ trỏ chấm được, nhóm nào chấm bằng nội dung.
  · lỗ 1 "mù đảo nghĩa" — report hứa "báo % bước là toggle" nhưng chưa có số.
    Đếm bằng danh sách từ trạng thái ĐỘC LẬP với bảng của metric_exec.py, và tách
    riêng phần bảng thước hiện phủ được với phần nó bỏ lọt.

Chạy: python3 harness/ac_step_profile.py
"""
import os, re, json, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
HF = os.path.expanduser("~/.cache/huggingface/hub/datasets--wangyuanlei--android_control_test/snapshots")
OUT = os.path.join(HERE, "ac_step_profile_results.json")

# --- danh sách cặp trạng thái ĐỘC LẬP (soạn tay, KHÔNG import từ metric_exec) ---
STATE_PAIRS = [
    ("on", "off"), ("enable", "disable"), ("enabled", "disabled"), ("show", "hide"),
    ("mute", "unmute"), ("up", "down"), ("add", "remove"), ("expand", "collapse"),
    ("start", "stop"), ("open", "close"), ("check", "uncheck"), ("select", "deselect"),
    ("increase", "decrease"), ("next", "previous"), ("more", "less"), ("forward", "backward"),
    ("allow", "block"), ("public", "private"), ("light", "dark"), ("day", "night"),
    ("follow", "unfollow"), ("like", "unlike"), ("subscribe", "unsubscribe"),
    ("play", "pause"), ("accept", "decline"), ("in", "out"), ("first", "last"),
    ("ascending", "descending"), ("max", "min"), ("plus", "minus"),
]
# bảng mà metric_exec.py HIỆN có (chép tay để so phủ, không import)
METRIC_COVERS = {"on", "off", "enable", "disable", "enabled", "disabled", "show", "hide",
                 "mute", "unmute", "up", "down", "add", "remove", "expand", "collapse",
                 "start", "stop", "open", "close", "check", "uncheck", "select", "deselect"}

STATE_WORDS = {}
for a, b in STATE_PAIRS:
    STATE_WORDS[a] = b
    STATE_WORDS[b] = a


def words(t):
    return set(re.findall(r"[a-z]+", (t or "").lower()))


def main():
    eps = glob.glob(os.path.join(HF, "*", "test_output_json", "*", "episode_*.json"))
    n_ep = 0
    act_count = collections.Counter()
    n_step = 0
    n_state, n_state_covered, n_state_missed = 0, 0, 0
    missed_words = collections.Counter()
    state_by_action = collections.Counter()
    for p in eps:
        try:
            o = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        acts = o.get("actions") or []
        insts = o.get("step_instructions") or []
        if not acts:
            continue
        n_ep += 1
        for i, a in enumerate(acts):
            t = a.get("action_type", "?")
            has_xy = "x" in a and "y" in a
            key = t + ("+xy" if has_xy else "")
            act_count[key] += 1
            n_step += 1
            instr = insts[i] if i < len(insts) else ""
            ws = words(instr)
            hit = [w for w in ws if w in STATE_WORDS and STATE_WORDS[w] in STATE_WORDS]
            # chỉ tính là "bước có từ trạng thái" khi câu chứa một từ thuộc cặp đảo được
            if hit:
                n_state += 1
                state_by_action[key] += 1
                if any(w in METRIC_COVERS for w in hit):
                    n_state_covered += 1
                else:
                    n_state_missed += 1
                    for w in hit:
                        if w not in METRIC_COVERS:
                            missed_words[w] += 1

    # nhóm theo cách chấm
    grounder = sum(v for k, v in act_count.items() if k.startswith(("click", "long_press")) and "+xy" in k)
    content = sum(v for k, v in act_count.items() if k.startswith(("input_text", "scroll", "open_app")))
    other = n_step - grounder - content

    res = {
        "n_episode": n_ep, "n_step": n_step,
        "action_breakdown": dict(act_count.most_common()),
        "cham_co_toa_do": grounder, "ti_le_cham": grounder / max(n_step, 1),
        "go_cuon_moapp": content, "ti_le_noi_dung": content / max(n_step, 1),
        "khac": other,
        "buoc_co_tu_trang_thai": n_state, "ti_le_trang_thai": n_state / max(n_step, 1),
        "thuoc_phu_duoc": n_state_covered, "thuoc_bo_lot": n_state_missed,
        "tu_bi_bo_lot": dict(missed_words.most_common(15)),
        "trang_thai_theo_loai_thao_tac": dict(state_by_action.most_common()),
    }
    json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("=" * 70)
    print(f"AndroidControl test (cache local): {n_ep} episode · {n_step} bước")
    print("=" * 70)
    for k, v in act_count.most_common():
        print(f"  {k:22} {v:5}  {v/n_step:6.1%}")
    print("-" * 70)
    print(f"  Chạm CÓ toạ độ gold (bộ trỏ chấm được) : {grounder:5} = {grounder/n_step:.1%}")
    print(f"  Gõ / cuộn / mở app (chấm nội dung)      : {content:5} = {content/n_step:.1%}")
    print(f"  Còn lại (back, wait, ...)               : {other:5} = {other/n_step:.1%}")
    print("-" * 70)
    print(f"  Bước có từ trạng thái đảo được          : {n_state:5} = {n_state/n_step:.1%}")
    print(f"     bảng của metric_exec.py phủ          : {n_state_covered:5}")
    print(f"     bảng bỏ lọt                          : {n_state_missed:5}")
    if missed_words:
        print("     từ bị bỏ lọt nhiều nhất: " + ", ".join(f"{w}({c})" for w, c in missed_words.most_common(10)))
    print("=" * 70)
    print("Đã lưu", OUT)


if __name__ == "__main__":
    main()
