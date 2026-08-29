"""EXP1 §4: two-sided validation of the fresh verdict streams (23, 29, 31)
before any contender exposure.  On each stream: A10-class scans pass;
OracleFull certifies with the marker; OracleIdent certifies the marker
(honest reachability); cluster and every L3-2 control certify nothing, with
the STOP-era-certifier regression form intact."""
import json
import sys
import time

sys.path.insert(0, ".")
from crucible.engine import Engine
from crucible.gen import generate_corpus
from crucible import policies as PL
from crucible.audits import a10_scans
from l3_2 import contenders as X
from l3_2 import certify_p003 as CP
from l3_2.certify import certify_run as certify_old

TH = {"delta_e": 0.05, "theta_ev": 0.15}
STREAMS = (23, 29, 31)
CONTROLS = {"null_empty": PL.NullEmpty, "null_default": PL.NullDefault,
            "static": PL.StaticFeat, "ambient_corr": PL.AmbientCorr,
            "lookup": PL.Lookup, "cluster": PL.ClusterRelabel,
            "cluster_wild": X.ClusterWild, "cluster_greedy": X.ClusterGreedy}


def main():
    t0 = time.time()
    out = {"streams": {}, "pass": True}
    corpora = {s: generate_corpus(s) for s in STREAMS}
    scans = a10_scans(corpora)
    out["a10"] = {"holdout_violations_pre_ER":
                  scans["holdout_violations_pre_ER"],
                  "cracked_pre_EC": scans["cracked_pre_EC"],
                  "pass": scans["pass"]}
    if not scans["pass"]:
        out["pass"] = False
    for s in STREAMS:
        rec = {}
        ref = Engine(corpora[s], PL.OracleFull(seed=90001 + s))
        ref.run()
        rcert = CP.certify_run_p003(ref, ref, TH)
        rec["oracle_certified"] = rcert["n_certified"]
        rec["oracle_marker"] = rcert["marker_fired"]
        hon = Engine(corpora[s], PL.OracleIdent(seed=90001 + s))
        hon.run()
        hcert = CP.certify_run_p003(hon, ref, TH)
        rec["ident_certified"] = hcert["n_certified"]
        rec["ident_marker"] = hcert["marker_fired"]
        rec["controls"] = {}
        ok = rcert["marker_fired"] and hcert["marker_fired"]
        for name, cls in CONTROLS.items():
            eng = Engine(corpora[s], cls(seed=90001 + s))
            eng.policy.read_violations = eng.violations_for
            eng.run()
            cert = CP.certify_run_p003(eng, ref, TH)
            n = cert["n_certified"]
            rec["controls"][name] = n
            if n > 0:
                ok = False
            if name == "cluster":
                old = certify_old(eng)["certified"]
                flipped = all(cert["units"].get(c, {}).get("state")
                              == "uncertifiable-untested" for c in old)
                rec["cluster_regression_form"] = {"stop_era": old,
                                                  "flipped": flipped}
                if not flipped:
                    ok = False
        rec["pass"] = ok
        out["streams"][str(s)] = rec
        if not ok:
            out["pass"] = False
        print("stream %d: oracle marker=%s ident marker=%s controls=%s "
              "pass=%s (%.0fs)" % (s, rec["oracle_marker"],
                                   rec["ident_marker"],
                                   rec["controls"], ok, time.time() - t0))
    json.dump(out, open("l3_5/stream_validation.json", "w"), indent=1,
              default=repr)
    print("STREAM VALIDATION:", "PASS" if out["pass"] else "FAIL")
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
