"""P004 sequence step 3: reference measurement -> theta_comp by the
PREREGISTERED formula (P004 Amendment 2, committed 0a6735e BEFORE this
script existed) -> two-sided acceptance conditions (Amendment 3) ->
freeze (l3_5/FREEZE_P004.json).  Any apparatus-stop condition halts for
a Director ruling.

Formula: theta_comp = min(2*S_or, (S_or+S_cc)/2), S_or = max OracleIdent
composite share across verdict streams 23/29/31, S_cc = min control
composite share (leg vacuous if no control holds P4 content).
Stops: theta_comp/S_or < 1.5; theta_comp >= any control composite share;
OracleFull composites fail theta_comp; any acceptance condition fails."""
import hashlib
import json
import sys
import time

sys.path.insert(0, ".")
from crucible.engine import Engine
from crucible.gen import generate_corpus
from crucible import policies as PL
from l3_2 import certify_p003 as CP
from l3_2 import certify_p004 as C4
from l3_2 import contenders as X
from l3_2.certify import certify_run as certify_old

STREAMS = (23, 29, 31)
CONTROLS = {"null_empty": PL.NullEmpty, "null_default": PL.NullDefault,
            "static": PL.StaticFeat, "ambient_corr": PL.AmbientCorr,
            "lookup": PL.Lookup, "cluster": PL.ClusterRelabel,
            "cluster_wild": X.ClusterWild, "cluster_greedy": X.ClusterGreedy}


def composite_shares(cert):
    return {n: r["abstention"]["share"] for n, r in cert["units"].items()
            if n.startswith("unit:")
            and r["abstention"]["share"] is not None}


def main():
    t0 = time.time()
    out = {"streams": {}, "stops": [], "pass": True}
    provisional = {"delta_e": 0.05, "theta_ev": 0.15, "theta_comp": 1.0}
    engines = {}
    # ---- reference measurement (shares are threshold-independent)
    orid_shares, orfull_shares, ctrl_shares = [], [], []
    for s in STREAMS:
        corpus = generate_corpus(s)
        ref = Engine(corpus, PL.OracleFull(seed=90001 + s))
        ref.run()
        hon = Engine(corpus, PL.OracleIdent(seed=90001 + s))
        hon.run()
        engines[s] = {"corpus": corpus, "ref": ref, "hon": hon,
                      "controls": {}}
        cf = C4.certify_run_p004(ref, ref, provisional)
        ch = C4.certify_run_p004(hon, ref, provisional)
        orfull_shares += list(composite_shares(cf).values())
        orid_shares += list(composite_shares(ch).values())
        out["streams"][str(s)] = {
            "oracle_full_composite_shares": composite_shares(cf),
            "oracle_ident_composite_shares": composite_shares(ch)}
        for name, cls in CONTROLS.items():
            eng = Engine(corpus, cls(seed=90001 + s))
            eng.policy.read_violations = eng.violations_for
            eng.run()
            engines[s]["controls"][name] = eng
            cc = C4.certify_run_p004(eng, ref, provisional)
            sh = composite_shares(cc)
            ctrl_shares += list(sh.values())
            if sh:
                out["streams"][str(s)].setdefault(
                    "control_composite_shares", {})[name] = sh
        print("stream %d measured (%.0fs)" % (s, time.time() - t0))
    S_or = max(orid_shares)
    S_cc = min(ctrl_shares) if ctrl_shares else None
    theta_comp = 2 * S_or if S_cc is None \
        else min(2 * S_or, (S_or + S_cc) / 2)
    out["S_or"] = S_or
    out["S_cc"] = S_cc
    out["theta_comp"] = round(theta_comp, 4)
    # ---- apparatus stops
    if theta_comp / S_or < 1.5:
        out["stops"].append("oracle margin under 1.5x")
    if any(c <= theta_comp for c in ctrl_shares):
        out["stops"].append("theta_comp >= a control composite share")
    if any(sh > theta_comp for sh in orfull_shares):
        out["stops"].append("OracleFull composite fails theta_comp")
    # ---- two-sided acceptance under the derived theta_comp
    TH = {"delta_e": 0.05, "theta_ev": 0.15, "theta_comp": theta_comp}
    for s in STREAMS:
        e = engines[s]
        rec = out["streams"][str(s)]
        cf = C4.certify_run_p004(e["ref"], e["ref"], TH)
        ch = C4.certify_run_p004(e["hon"], e["ref"], TH)
        rec["oracle_full"] = {"certified": cf["n_certified"],
                              "marker": cf["marker_fired"],
                              "marker_units": cf["marker_units"]}
        rec["oracle_ident"] = {"certified": ch["n_certified"],
                               "marker": ch["marker_fired"],
                               "marker_units": ch["marker_units"]}
        ok = cf["marker_fired"] and ch["marker_fired"]
        bare_p4 = []
        rec["controls"] = {}
        for name, eng in e["controls"].items():
            cc = C4.certify_run_p004(eng, e["ref"], TH)
            rec["controls"][name] = cc["n_certified"]
            if cc["n_certified"] > 0:
                ok = False
            if name == "cluster":
                old = certify_old(eng)["certified"]
                flipped = all(cc["units"].get(c, {}).get("state")
                              == "uncertifiable-untested" for c in old)
                rec["cluster_regression_form"] = {"stop_era": old,
                                                  "flipped": flipped}
                if not flipped:
                    ok = False
        for pol_cert in (cf, ch):
            for n in pol_cert["certified"]:
                if pol_cert["units"][n]["productions"] == ["P4"]:
                    bare_p4.append(n)
        if bare_p4:
            ok = False
            out["stops"].append("bare P4 in certifiable set: %s" % bare_p4)
        rec["pass"] = ok
        if not ok:
            out["pass"] = False
        print("stream %d: full-marker=%s ident-marker=%s controls=%s "
              "pass=%s" % (s, cf["marker_fired"], ch["marker_fired"],
                           rec["controls"], ok))
    if out["stops"]:
        out["pass"] = False
    out["wall_seconds"] = round(time.time() - t0, 1)
    json.dump(out, open("l3_5/p004_validation.json", "w"), indent=1,
              default=repr)
    if out["pass"]:
        freeze = {
            "preregistration": "PREREGISTRATION_004 (commit 0a6735e)",
            "theta_comp": round(theta_comp, 4),
            "S_or": S_or, "S_cc": S_cc,
            "thresholds": TH,
            "certify_p004_sha256": hashlib.sha256(
                open("l3_2/certify_p004.py", "rb").read()).hexdigest(),
            "certify_p003_sha256_unchanged": hashlib.sha256(
                open("l3_2/certify_p003.py", "rb").read()).hexdigest(),
        }
        json.dump(freeze, open("l3_5/FREEZE_P004.json", "w"), indent=1)
    print("theta_comp=%.4f (S_or=%.4f, S_cc=%s) | stops: %s | %s"
          % (theta_comp, S_or, S_cc, out["stops"] or "none",
             "PASS" if out["pass"] else "FAIL/STOP"))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
