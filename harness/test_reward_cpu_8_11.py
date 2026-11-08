#!/usr/bin/env python3
"""Full C1 pipeline smoke, using FAKE scorers. NO research conclusions."""
import importlib.util
import json
import pathlib
import sys
import tempfile
import types

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("screen_cpu", ROOT/"harness/reward_cpu_8_11.py")
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

class FakeCHRF:
    def sentence_score(self, s, refs):
        a=set(s.lower().split())
        b=set(refs[0].lower().split())
        sc = 100.0 if s == refs[0] else (100 * len(a&b)/len(a|b) if (a|b) else 0)
        return types.SimpleNamespace(score=sc)

sys.modules["sacrebleu"] = types.ModuleType("sacrebleu")
sm = types.ModuleType("sacrebleu.metrics")
sm.CHRF=FakeCHRF
sys.modules["sacrebleu.metrics"]=sm
def fake_spice(pairs, batch_size):
    return {pair: (0.0 if pair[1].strip().lower() in ("scroll down","go back")
                   else (1.0 if pair[0] == pair[1] else 0.5))
            for pair in dict.fromkeys(pairs)}
m.spice_scores=fake_spice
with tempfile.TemporaryDirectory() as d:
    sys.argv=["reward_cpu_8_11.py","--data",str(ROOT/"_bundles/reward_cpu_8_11/ds"),
              "--out",d]
    m.main()
    r=json.loads((pathlib.Path(d)/"reward_cpu_c1.json").read_text())
    assert r["metadata"]["n_prompts"] == 400
    assert r["rewards"]["R4_sparse_action"]["tap"]["n"] == 249
    assert r["rewards"]["R4_sparse_action"]["non_tap"]["n"] == 151
    assert all(len(r["rewards"][z]) >= 3 for z in m.REWARDS)
    assert len(r["stress"]) == len(m.STRESS)
print("FULL_PIPELINE_MOCK_OK (fake SPICE and chrF; no real research result)")
