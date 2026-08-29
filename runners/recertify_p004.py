"""P004 Amendment 4: deterministic replay re-certification of the 15 EXP1
scored runs (frozen Candidate E, digest asserted) under the P004
machinery and the frozen theta_comp.  No new runs, no new streams.
Run twice back-to-back for the determinism check; the cross-scope
consistency check compares this replay's composite-scope shares against
the H2 attributed-classes shares (different scopes, both must
reproduce)."""
import hashlib
import json
import sys
import time

sys.path.insert(0, ".")
from crucible.engine import Engine
from crucible.gen import generate_corpus
from crucible import policies as PL
from l3_2 import certify_p004 as C4
from l3_5.candidate_e import CandidateE

STREAMS = (23, 29, 31)
SEEDS = (201, 202, 203, 204, 205)


def main():
    t0 = time.time()
    freeze = json.load(open("l3_5/FREEZE.json"))
    cur = hashlib.sha256(
        open("l3_5/candidate_e.py", "rb").read()).hexdigest()
    assert cur == freeze["digests_sha256"]["l3_5/candidate_e.py"], \
        "contender digest does not match freeze"
    p004 = json.load(open("l3_5/FREEZE_P004.json"))
    assert hashlib.sha256(open("l3_2/certify_p004.py", "rb").read()
                          ).hexdigest() == p004["certify_p004_sha256"]
    TH = p004["thresholds"]
    out = {"theta_comp": TH["theta_comp"], "runs": {},
           "per_seed_marker": {}, "endpoint": None}
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
            pol = CandidateE(seed=seed)
            eng = Engine(corpus, pol)
            pol.read_violations = eng.violations_for
            eng.run()
            cert = C4.certify_run_p004(eng, ref, TH)
            comp = {n: {"share": r["abstention"]["share"],
                        "state": r["state"],
                        "b": r["b"]["margin"],
                        "e": r["e"]["margin_shift"]}
                    for n, r in cert["units"].items()
                    if n.startswith("unit:")}
            out["runs"]["%d/%d" % (seed, s)] = {
                "marker": cert["marker_fired"],
                "marker_units": cert["marker_units"],
                "certified": cert["certified"],
                "composites": comp}
            fired += bool(cert["marker_fired"])
            print("seed %d stream %d: marker=%s certified=%s comps=%s"
                  " (%.0fs)"
                  % (seed, s, cert["marker_fired"], cert["certified"],
                     {n: c["share"] for n, c in comp.items()},
                     time.time() - t0))
        out["per_seed_marker"][str(seed)] = fired
    passing = sum(1 for v in out["per_seed_marker"].values() if v >= 2)
    out["seeds_passing"] = passing
    out["endpoint"] = ("PRIMARY-MET-UNDER-P004" if passing >= 3
                       else "PRIMARY-NOT-MET-UNDER-P004")
    json.dump(out, open("l3_5/scored_runs_p004.json", "w"), indent=1,
              default=repr)
    print("per-seed:", out["per_seed_marker"], "| ENDPOINT:",
          out["endpoint"])


if __name__ == "__main__":
    main()
