"""EXP2 §3: two-sided validation of the rule-drawn verdict streams
(1009, 1013, 1019) before any E.2 exposure, under the P004 machinery and
the frozen theta_comp.  On each stream: A10-class scans pass; OracleFull
certifies with the marker at composite level; OracleIdent certifies the
marker (reachability re-confirmed — a failure is an apparatus stop, not
a threshold adjustment); every control certifies nothing; the STOP-era
cluster regression form holds; no bare P4 is certifiable."""
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

STREAMS = (1009, 1013, 1019)
CONTROLS = {"null_empty": PL.NullEmpty, "null_default": PL.NullDefault,
            "static": PL.StaticFeat, "ambient_corr": PL.AmbientCorr,
            "lookup": PL.Lookup, "cluster": PL.ClusterRelabel,
            "cluster_wild": X.ClusterWild, "cluster_greedy": X.ClusterGreedy}


def main():
    t0 = time.time()
    TH = json.load(open("l3_5/FREEZE_P004.json"))["thresholds"]
    out = {"streams": {}, "pass": True, "thresholds": TH}
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
        rcert = C4.certify_run_p004(ref, ref, TH)
        rec["oracle_full"] = {"certified": rcert["n_certified"],
                              "marker": rcert["marker_fired"],
                              "marker_units": rcert["marker_units"]}
        hon = Engine(corpora[s], PL.OracleIdent(seed=90001 + s))
        hon.run()
        hcert = C4.certify_run_p004(hon, ref, TH)
        rec["oracle_ident"] = {"certified": hcert["n_certified"],
                               "marker": hcert["marker_fired"],
                               "composite_shares": {
                                   n: r["abstention"]["share"]
                                   for n, r in hcert["units"].items()
                                   if n.startswith("unit:")}}
        ok = rcert["marker_fired"] and hcert["marker_fired"]
        rec["controls"] = {}
        for name, cls in CONTROLS.items():
            eng = Engine(corpora[s], cls(seed=90001 + s))
            eng.policy.read_violations = eng.violations_for
            eng.run()
            cert = C4.certify_run_p004(eng, ref, TH)
            rec["controls"][name] = cert["n_certified"]
            if cert["n_certified"] > 0:
                ok = False
            if name == "cluster":
                old = certify_old(eng)["certified"]
                flipped = all(cert["units"].get(c, {}).get("state")
                              == "uncertifiable-untested" for c in old)
                rec["cluster_regression_form"] = {"stop_era": old,
                                                  "flipped": flipped}
                if not flipped:
                    ok = False
        for pc in (rcert, hcert):
            for n in pc["certified"]:
                if pc["units"][n]["productions"] == ["P4"]:
                    ok = False
                    rec.setdefault("bare_p4", []).append(n)
        rec["pass"] = ok
        out["streams"][str(s)] = rec
        if not ok:
            out["pass"] = False
        print("stream %d: full=%s ident=%s ident-shares=%s controls=%s "
              "pass=%s (%.0fs)"
              % (s, rcert["marker_fired"], hcert["marker_fired"],
                 rec["oracle_ident"]["composite_shares"],
                 rec["controls"], ok, time.time() - t0))
    json.dump(out, open("l3_5/exp2_stream_validation.json", "w"),
              indent=1, default=repr)
    print("EXP2 STREAM VALIDATION:", "PASS" if out["pass"] else "FAIL")
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
