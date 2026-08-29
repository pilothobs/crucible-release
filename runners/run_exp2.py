"""EXP2 scored runs: Candidate E.2 (frozen, l3_5/FREEZE_EXP2.json) on
the rule-drawn fresh verdict streams 1009/1013/1019 x training seeds
301-305.  First contender exposure of these streams.  Certification:
frozen P004 machinery, theta_comp 0.4022.  Endpoint: marker >= 3/5
seeds, a seed counting iff the marker fires on >= 2/3 streams.  Also
records each run's exploration-action distribution (EXP2 section 2
standing check)."""
import hashlib
import json
import sys
import time
from collections import Counter

sys.path.insert(0, ".")
from crucible.engine import Engine
from crucible.gen import generate_corpus
from crucible import policies as PL
from l3_2 import certify_p004 as C4
from l3_5.candidate_e2 import CandidateE2

STREAMS = (1009, 1013, 1019)
SEEDS = (301, 302, 303, 304, 305)


class _Counting(CandidateE2):
    def begin_run(self):
        super().begin_run()
        self.action_counts = Counter()

    def learner_action(self, obs):
        act = super().learner_action(obs)
        self.action_counts[act[0]] += 1
        return act


def main():
    t0 = time.time()
    freeze = json.load(open("l3_5/FREEZE_EXP2.json"))
    cur = hashlib.sha256(
        open("l3_5/candidate_e2.py", "rb").read()).hexdigest()
    assert cur == freeze["digests_sha256"]["l3_5/candidate_e2.py"], \
        "contender digest does not match freeze"
    TH = freeze["thresholds"]
    out = {"freeze_digest": cur, "theta_comp": TH["theta_comp"],
           "runs": {}, "per_seed_marker": {}, "endpoint": None}
    refs = {}
    for s in STREAMS:
        corpus = generate_corpus(s)
        ref = Engine(corpus, PL.OracleFull(seed=90001 + s))
        ref.run()
        refs[s] = (corpus, ref)
    for seed in SEEDS:
        fired = 0
        for s in STREAMS:
            corpus, ref = refs[s]
            pol = _Counting(seed=seed)
            eng = Engine(corpus, pol)
            pol.read_violations = eng.violations_for
            res = eng.run()
            cert = C4.certify_run_p004(eng, ref, TH)
            rec = {
                "marker": cert["marker_fired"],
                "marker_units": cert["marker_units"],
                "certified": cert["certified"],
                "certified_units": {
                    u: {"productions": cert["units"][u]["productions"],
                        "b": cert["units"][u]["b"],
                        "c": cert["units"][u]["c"],
                        "d_state": cert["units"][u]["d_state"],
                        "e": cert["units"][u]["e"],
                        "abstention": cert["units"][u]["abstention"]}
                    for u in cert["certified"]},
                "composites": {
                    n: {"share": r["abstention"]["share"],
                        "state": r["state"], "b": r["b"]["margin"],
                        "e": r["e"]["margin_shift"]}
                    for n, r in cert["units"].items()
                    if n.startswith("unit:")},
                "accuracy": {k: v for k, v in res["accuracy"].items()},
                "counts": {"classes": len(pol.classes),
                           "attrs": len(pol.attrs),
                           "arules": len(pol.arules),
                           "aprules": len(pol.aprules),
                           "guard": pol._guard_cid},
                "action_distribution": dict(pol.action_counts),
                "total_bits": res["total_bits"],
                "stats": dict(pol.stats),
            }
            out["runs"]["%d/%d" % (seed, s)] = rec
            fired += bool(cert["marker_fired"])
            print("seed %d stream %d: marker=%s certified=%s comps=%s "
                  "(%.0fs)"
                  % (seed, s, cert["marker_fired"], cert["certified"],
                     {n: round(c["share"], 3) if c["share"] is not None
                      else None for n, c in rec["composites"].items()},
                     time.time() - t0))
        out["per_seed_marker"][str(seed)] = fired
    passing = sum(1 for v in out["per_seed_marker"].values() if v >= 2)
    out["seeds_passing"] = passing
    out["endpoint"] = "PRIMARY-MET" if passing >= 3 else "PRIMARY-NOT-MET"
    json.dump(out, open("l3_5/scored_runs_exp2.json", "w"), indent=1,
              default=repr)
    print("per-seed marker streams:", out["per_seed_marker"])
    print("ENDPOINT:", out["endpoint"], "(%d/5 seeds)" % passing)


if __name__ == "__main__":
    main()
