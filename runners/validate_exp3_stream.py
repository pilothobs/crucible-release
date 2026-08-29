"""EXP3 fresh-stream (1021) two-sided validation.  RECORD REPAIR like
l3_5/run_exp3.py: the validation at EXP3 time ran from an uncommitted
inline driver; this file reconstructs it and was verified on the
original host to reproduce the committed l3_5/exp3_stream_validation.json
byte-identically before being committed."""
import json
import sys
import time

sys.path.insert(0, ".")
from crucible.engine import Engine
from crucible.gen import generate_corpus
from crucible import policies as PL
from crucible.audits import a10_scans
from l3_2 import contenders as X
from l3_2 import certify_p004 as C4
from l3_2.certify import certify_run as certify_old


def main():
    t0 = time.time()
    TH = json.load(open("l3_5/FREEZE_P004.json"))["thresholds"]
    s = 1021
    corpus = generate_corpus(s)
    scans = a10_scans({s: corpus})
    out = {"stream": s, "a10": {"pass": scans["pass"]}}
    ref = Engine(corpus, PL.OracleFull(seed=90001 + s))
    ref.run()
    cf = C4.certify_run_p004(ref, ref, TH)
    hon = Engine(corpus, PL.OracleIdent(seed=90001 + s))
    hon.run()
    ch = C4.certify_run_p004(hon, ref, TH)
    ok = scans["pass"] and cf["marker_fired"] and ch["marker_fired"]
    out["oracle_full_marker"] = cf["marker_fired"]
    out["oracle_ident_marker"] = ch["marker_fired"]
    out["ident_composite_shares"] = {n: r["abstention"]["share"]
                                     for n, r in ch["units"].items()
                                     if n.startswith("unit:")}
    CONTROLS = {"null_empty": PL.NullEmpty, "null_default": PL.NullDefault,
                "static": PL.StaticFeat, "ambient_corr": PL.AmbientCorr,
                "lookup": PL.Lookup, "cluster": PL.ClusterRelabel,
                "cluster_wild": X.ClusterWild,
                "cluster_greedy": X.ClusterGreedy}
    out["controls"] = {}
    for name, cls in CONTROLS.items():
        eng = Engine(corpus, cls(seed=90001 + s))
        eng.policy.read_violations = eng.violations_for
        eng.run()
        cc = C4.certify_run_p004(eng, ref, TH)
        out["controls"][name] = cc["n_certified"]
        if cc["n_certified"]:
            ok = False
        if name == "cluster":
            old = certify_old(eng)["certified"]
            flipped = all(cc["units"].get(c, {}).get("state")
                          == "uncertifiable-untested" for c in old)
            out["cluster_regression_form"] = flipped
            if not flipped:
                ok = False
    for pc in (cf, ch):
        for n in pc["certified"]:
            if pc["units"][n]["productions"] == ["P4"]:
                ok = False
    out["pass"] = ok
    json.dump(out, open("l3_5/exp3_stream_validation.json", "w"),
              indent=1, default=repr)
    print("stream 1021 validation:", "PASS" if ok else "FAIL",
          "(%.0fs)" % (time.time() - t0))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
