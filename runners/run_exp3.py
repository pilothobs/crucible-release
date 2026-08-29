"""EXP3 scored runner (PREREGISTRATION_L35_EXP3).  RECORD REPAIR, noted
in the replication report: the EXP3 scoring at verdict time (commit
0af3a88's scored_runs_exp3.json) was executed from an uncommitted
driver; this file reconstructs that driver verbatim-in-logic and was
verified on the original host to reproduce the committed artifact
exactly before being committed.  It touches no frozen artifact."""
import hashlib
import json
import sys
import time

sys.path.insert(0, ".")
from crucible.engine import Engine
from crucible.gen import generate_corpus
from crucible import policies as PL
from l3_2 import certify_p004 as C4
from l3_5.candidate_e3 import CandidateE3


def main():
    t0 = time.time()
    freeze = json.load(open("l3_5/FREEZE_EXP3.json"))
    assert hashlib.sha256(open("l3_5/candidate_e3.py", "rb").read()
                          ).hexdigest() \
        == freeze["digests_sha256"]["l3_5/candidate_e3.py"]
    TH = freeze["thresholds"]
    e2 = json.load(open("l3_5/scored_runs_exp2.json"))
    out = {"runs": {}, "prediction": {}}
    refs = {}
    for s in (1009, 1013, 1019, 1021):
        corpus = generate_corpus(s)
        ref = Engine(corpus, PL.OracleFull(seed=90001 + s))
        ref.run()
        refs[s] = (corpus, ref)
    p1_guard = p1_marker = 0
    p2_ok = True
    p3_marker = 0
    for seed in (301, 302, 303, 304, 305):
        for s in (1009, 1013, 1019, 1021):
            corpus, ref = refs[s]
            pol = CandidateE3(seed=seed)
            eng = Engine(corpus, pol)
            pol.read_violations = eng.violations_for
            eng.run()
            cert = C4.certify_run_p004(eng, ref, TH)
            best = min((r["abstention"]["share"]
                        for n, r in cert["units"].items()
                        if n.startswith("unit:")
                        and r["abstention"]["share"] is not None),
                       default=None)
            key = "%d/%d" % (seed, s)
            out["runs"][key] = {"marker": cert["marker_fired"],
                                "certified": cert["certified"],
                                "guard": pol._guard_cid,
                                "best_composite_share": best,
                                "deferrals": pol.truncations_prevented}
            if s == 1013:
                p1_guard += pol._guard_cid is not None
                p1_marker += cert["marker_fired"]
            elif s == 1021:
                p3_marker += cert["marker_fired"]
            else:
                e2best = min((c["share"] for c in
                              e2["runs"][key]["composites"].values()
                              if c["share"] is not None), default=None)
                if not cert["marker_fired"] or best > e2best + 0.02:
                    p2_ok = False
                out["runs"][key]["e2_best"] = e2best
            print(key, "marker", cert["marker_fired"], "guard",
                  pol._guard_cid,
                  "best %.3f" % best if best else None,
                  "(%.0fs)" % (time.time() - t0))
    out["prediction"] = {
        "P1_guard_admitted_1013": "%d/5" % p1_guard,
        "P1_marker_1013": "%d/5" % p1_marker,
        "P1_met": p1_guard == 5 and p1_marker >= 4,
        "P2_no_harm_met": p2_ok,
        "P3_marker_1021": "%d/5" % p3_marker,
        "P3_met": p3_marker >= 4,
    }
    out["verdict"] = ("E3-CONFIRMED" if out["prediction"]["P1_met"]
                      and p2_ok and out["prediction"]["P3_met"] else
                      ("E3-REFUTED" if not out["prediction"]["P1_met"]
                       else "E3-MIXED"))
    json.dump(out, open("l3_5/scored_runs_exp3.json", "w"), indent=1,
              default=repr)
    print("PREDICTION:", out["prediction"])
    print("VERDICT:", out["verdict"])


if __name__ == "__main__":
    main()
