"""P004 certification machinery (PREREGISTRATION_004): composite-mandatory
certification for attribute content.  A thin versioned wrapper over the
FROZEN certify_p003 module — every evaluation function is reused
unchanged; certify_p003.py is not edited.  Changes, per P004 Amendment 1
and 2 only:

  - unit set: all non-P4 singletons, plus the declared composite for each
    P4 (attr + referencing P5/P6 rules, the existing standard_units
    construction).  Bare P4 singletons are NOT certifiable units.  A P4
    with no referencing rule has no composite and no certifiable form
    (SPEC 5.7: the marker instance requires at least one AURule/APRule).
  - thresholds: composite units are evaluated with theta_comp (fixed by
    the P004 Amendment-2 formula from reference measurement, frozen in
    l3_5/FREEZE_P004.json); singleton units keep theta_ev unchanged.
"""
import sys

sys.path.insert(0, ".")
from l3_2 import certify_p003 as CP


def standard_units_p004(engine):
    p4 = {cid for cid in engine.lib.order
          if engine.lib.concepts[cid]["term"]["p"] == "P4"}
    units = []
    for name, members in CP.standard_units(engine):
        if len(members) == 1 and next(iter(members)) in p4:
            continue
        units.append((name, members))
    return units


def certify_run_p004(engine, ref_engine, thresholds):
    """thresholds: delta_e, theta_ev (singletons), theta_comp
    (composites).  Everything else identical to certify_run_p003."""
    CP.check_alignment(engine, ref_engine)
    surface = CP.shift_surface(engine)
    refmap = CP.ref_resolved_map(ref_engine)
    scored_index = {e: i for i, e in enumerate(engine.scored)}
    n_scored = len(engine.scored)
    n_pre = sum(1 for e in engine.scored
                if engine.archive[e]["strata"]["window"] == "pre")
    results = {}
    for name, members in standard_units_p004(engine):
        th = dict(thresholds)
        if name.startswith("unit:"):
            th["theta_ev"] = thresholds["theta_comp"]
        results[name] = CP.evaluate_unit(engine, name, members, surface,
                                         refmap, scored_index, n_scored,
                                         n_pre, th)
    certified = [n for n, r in results.items() if r["certified"]]
    marker = [n for n in certified if not results[n]["initial_kind"]]
    unc = [n for n, r in results.items()
           if r.get("state") == "uncertifiable-untested"]
    return {"units": results, "n_units": len(results),
            "certified": certified, "n_certified": len(certified),
            "uncertifiable_untested": unc,
            "marker_fired": bool(marker), "marker_units": marker,
            "surface_n": len(surface)}
