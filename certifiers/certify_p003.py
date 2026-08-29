"""Certification under PREREGISTRATION_003 (the ruled amendments).

Changes from the STOP-era certify.py (preserved unchanged as evidence):

  A1  (e) is gated on the SHIFT-INTRODUCED surface (k_new-involving,
      weathered-involving, hypothetical transfer queries; windows mid/post);
      the whole-stream margin is computed and reported as description.
  A2  the abstention blade: over a unit's in-scope shift-surface queries that
      the REFERENCE structure resolves (reference = true-structure run on the
      byte-identical query stream; alignment asserted), the unit is
      (d)-passed, (d)-untested-correct (abstention share <= theta_ev), or
      UNCERTIFIABLE-UNTESTED (share > theta_ev).  Empty in-scope set =
      out-of-scope, follows the untested-correct path.
  A3  class contradictions may be answered by same-batch cited revisions to
      hosted rules; (d) runs over the class-plus-hosted-rules cluster.
  C1  certification may be evaluated at declared composite units: for each
      P4 attribute, the unit is the attribute concept plus every P5/P6 rule
      whose expression references it.  Thresholds re-derived on the new
      surface before certification and frozen in the re-freeze manifest.
"""
import math

from l3_2.certify import (_sign_test, _affected_eids, _scored_affected,
                          _lib_size_before, _contradictions, TH as TH_BASE)

TH = dict(TH_BASE)          # delta_b, tau_d, f_d, alpha carried forward
TH["delta_e"] = None        # set by derive_thresholds() before certification
TH["theta_ev"] = None

INITIAL = ("P1", "P2", "P3", "P8")


# ---------------------------------------------------------------- surfaces
def shift_surface(engine):
    out = []
    for eid in engine.scored:
        r = engine.archive[eid]
        s = r["strata"]
        if s["window"] == "pre":
            continue
        if s.get("k_new") or s.get("weathered") or s.get("hyp"):
            out.append(eid)
    return out


def check_alignment(engine, ref_engine):
    a = [(engine.archive[e]["ep"], engine.archive[e]["step"],
          engine.archive[e]["action"]) for e in engine.scored]
    b = [(ref_engine.archive[e]["ep"], ref_engine.archive[e]["step"],
          ref_engine.archive[e]["action"]) for e in ref_engine.scored]
    assert a == b, "scored streams misaligned with reference run"


def ref_resolved_map(ref_engine):
    return {i: ref_engine.archive[e]["resolved"]
            for i, e in enumerate(ref_engine.scored)}


# ---------------------------------------------------------------- units
def standard_units(engine):
    """Singletons plus per-attribute composites (P003 C1)."""
    units = [(cid, frozenset({cid})) for cid in engine.lib.order]
    for cid in engine.lib.order:
        if engine.lib.concepts[cid]["term"]["p"] != "P4":
            continue
        members = {cid}
        for rid in engine.lib.order:
            t = engine.lib.concepts[rid]["term"]
            if t["p"] not in ("P5", "P6"):
                continue
            expr = t.get("expr")
            lits = expr if isinstance(expr, list) else \
                ([expr] if expr else [])
            for lit in lits:
                if cid in lit:
                    members.add(rid)
        if len(members) > 1:
            units.append(("unit:" + cid, frozenset(members)))
    return units


def _unit_scope(engine, members, surface_eids):
    """Shift-surface queries targeting the unit's members (P003 A2):
    class-like members -> queries involving their member-objects;
    rules -> action-matching queries involving their host class's members;
    attrs -> via the rules in the unit."""
    class_like, rule_hosts = set(), []
    for cid in members:
        t = engine.lib.concepts[cid]["term"]
        p = t["p"]
        if p in ("P1", "P7", "P10"):
            class_like.add(cid)
        elif p in ("P2", "P3", "P9"):
            host = t.get("cls") or t.get("c1")
            rule_hosts.append((t.get("action", "grind"), host,
                               t.get("c2")))
        elif p in ("P5", "P6", "P8"):
            rule_hosts.append((t.get("action", "grind"), None, None))
    scope = []
    for eid in surface_eids:
        r = engine.archive[eid]
        mem = set().union(*(v["members"] for v in r["views"]))
        hit = bool(mem & class_like)
        if not hit:
            for (act, h1, h2) in rule_hosts:
                if r["action"] != act:
                    continue
                if h1 is None or h1 in mem or (h2 and h2 in mem):
                    hit = True
                    break
        if hit:
            scope.append(eid)
    return scope


# ---------------------------------------------------------------- measures
def _paired(engine, eids, excl):
    g = l = 0
    for eid in eids:
        r = engine.archive[eid]
        res_o, pred_o, _ = engine.lib.predict(r["action"], r["views"], excl)
        w = int(r["resolved"] and r["predicted"] == r["outcome"])
        wo = int(res_o and pred_o == r["outcome"])
        if w and not wo:
            g += 1
        elif wo and not w:
            l += 1
    return g, l


def _rent_unit(engine, members):
    from crucible import grammar as G
    excl = frozenset(members)
    start = min(engine.lib.concepts[c]["admitted_ep"] for c in members)
    affected = set()
    for c in members:
        affected |= _affected_eids(engine, c)
    saved = 0.0
    for eid in affected:
        r = engine.archive[eid]
        if r["ep"] < start or r["type"] == "scored_hyp":
            continue
        rw, pw, _ = engine.lib.predict(r["action"], r["views"])
        ro, po, _ = engine.lib.predict(r["action"], r["views"], excl)
        saved += (engine.lib.code_bits(ro, po, r["outcome"]) -
                  engine.lib.code_bits(rw, pw, r["outcome"]))
    n_cls, n_att, n_con = engine.lib.counts_for_costs()
    desc = sum(G.spelling_cost(engine.lib.concepts[c]["term"],
                               n_cls, n_att, n_con) for c in members)
    assertion = 0.0
    for op in engine.oplog:
        tag = op.get("op")
        if tag in ("member+", "member-") and op.get("cid") in members:
            assertion += op["bits"]
        elif tag == "attr" and (op.get("cls") in members
                                or op.get("attr") in members):
            assertion += op["bits"]
    return saved - desc - assertion


def _d_unit(engine, members, ab_pre_margin):
    """(d) with P003 A3: hosted-rule revisions citing the unit's
    contradictions answer the unit's contradictions."""
    vids, rev_pool = set(), []
    hosted = set(members)
    for cid in members:
        vids.update(_contradictions(engine, cid))
        t = engine.lib.concepts[cid]["term"]
        if t["p"] in ("P1", "P7", "P10"):
            for rid, r in engine.lib.concepts.items():
                if r["term"].get("cls") == cid or cid in (
                        r["term"].get("c1"), r["term"].get("c2")):
                    hosted.add(rid)
    if not vids:
        return {"tested": False}
    first_ep = min(engine.violations[v]["ep"] for v in vids)
    for cid in hosted:
        if cid not in engine.lib.concepts:
            continue
        for r in engine.lib.concepts[cid]["revisions"]:
            if r["ep"] >= first_ep and (set(r["cites"]) & vids):
                rev_pool.append((cid, r))
    # spec 5.4 split semantics: a batch whose meta declares revises=[host]
    # with citations answering the host's contradictions IS a revision of
    # the host (membership moves are not slot edits, so they leave no
    # concept-level revision record; the batch summary carries the
    # bookkeeping).  This is a certification-machinery change, so the
    # ClusterRelabel regression fixture is re-confirmed after it (P003 C2).
    for op in engine.oplog:
        if op.get("op") != "batch-summary" or not op.get("revises"):
            continue
        revs = set(op["revises"] if isinstance(op["revises"], list)
                   else [op["revises"]])
        if (revs & set(members)) and op["ep"] >= first_ep \
                and (set(op.get("cites", ())) & vids):
            rev_pool.append((sorted(revs & set(members))[0],
                             {"ep": op["ep"], "cites": op["cites"],
                              "batch": True}))
    out = {"tested": True, "n_contradictions": len(vids),
           "n_answering_revisions": len(rev_pool)}
    if not rev_pool:
        out.update({"pass": False, "why": "no cited revision answers the "
                    "contradictions"})
        return out
    frac = 0.0
    for op in engine.oplog:
        if op.get("op") == "batch-summary" and op.get("revises"):
            revs = set(op["revises"] if isinstance(op["revises"], list)
                       else [op["revises"]])
            if revs & {cid for cid, _ in rev_pool}:
                frac = max(frac, len(op["footprint"]) /
                           _lib_size_before(engine, op["ep"] + 1))
    last_ep = max(r["ep"] for _, r in rev_pool)
    later = [v for v in vids if engine.violations[v]["ep"] > last_ep]
    restored = (len(later) == 0
                and ab_pre_margin >= TH["delta_b"] - TH["tau_d"])
    ok = frac <= TH["f_d"] and restored
    out.update({"footprint_frac": round(frac, 3),
                "later_violations": len(later), "restored": restored,
                "pass": ok})
    return out


# ---------------------------------------------------------------- top level
def evaluate_unit(engine, name, members, surface, refmap, scored_index,
                  n_scored, n_pre, thresholds):
    excl = frozenset(members)
    eids_all = set()
    for c in members:
        eids_all |= set(_scored_affected(engine, c))
    if len(eids_all) < TH["delta_b"] * n_scored and len(members) == 1:
        return {"unit": name, "prefiltered": True, "certified": False,
                "state": "prefiltered",
                "affected_scored": len(eids_all)}
    g, l = _paired(engine, sorted(eids_all), excl)
    m_all = (g - l) / n_scored
    b_ok = m_all >= TH["delta_b"] and _sign_test(g, l) < TH["alpha"]
    pre_eids = [e for e in eids_all
                if engine.archive[e]["strata"]["window"] == "pre"]
    gp0, lp0 = _paired(engine, pre_eids, excl)
    m_pre = (gp0 - lp0) / max(1, n_pre)
    # (e): "carries its predictive advantage across a generator shift it
    # never trained on" — two textual consequences, both measured into place:
    # (i) evaluable only for units admitted BEFORE E_R (a unit formed from
    # post-shift data trained on the shifted distribution; also closes
    # (e)-farming by post-shift concept creation for every contender);
    # (ii) the advantage measured is the one CARRIED: both sides of the
    # ablation run under the library restricted to pre-E_R-admitted content,
    # so post-shift-learned rules cannot launder credit into a pre-shift
    # concept through the resolution path (measured leak: a cheap class rode
    # its post-shift pair rules to a 0.18 surface margin).
    from crucible import constants as C
    post_admitted = frozenset(
        c for c in engine.lib.concepts
        if engine.lib.concepts[c]["admitted_ep"] >= C.E_R)
    e_evaluable = min(engine.lib.concepts[c]["admitted_ep"]
                      for c in members) < C.E_R
    surf_set = [e for e in surface if e in eids_all]
    gs = ls = 0
    for eid in surf_set:
        r = engine.archive[eid]
        rw, pw, _ = engine.lib.predict(r["action"], r["views"],
                                       post_admitted)
        ro, po, _ = engine.lib.predict(r["action"], r["views"],
                                       post_admitted | excl)
        w = int(rw and pw == r["outcome"])
        wo = int(ro and po == r["outcome"])
        if w and not wo:
            gs += 1
        elif wo and not w:
            ls += 1
    m_shift = (gs - ls) / max(1, len(surface))
    e_ok = (e_evaluable and m_shift >= thresholds["delta_e"]
            and _sign_test(gs, ls) < TH["alpha"])
    rent = _rent_unit(engine, members)
    c_ok = rent > 0
    d = _d_unit(engine, members, m_pre)
    # abstention blade (A2).  The ruling's state 1 is "c's rules resolve
    # them CORRECTLY": credit = resolved AND correct.  Resolved-WRONG (e.g.
    # a grind default answering null on a fuse cell) earns no credit —
    # evasion with extra steps.  Unit participation (ablating c changes the
    # query) is measured and REPORTED but not required for credit: (b)/(e)
    # already enforce that the unit itself is load-bearing, and requiring
    # participation here penalizes a unit for queries the world routes
    # around it (the soaked-guard sends correct pair queries through the
    # default) — the wounds-the-wrong-target failure the ruling corrected.
    scope = _unit_scope(engine, members, surface)
    in_scope_ref = [e for e in scope if refmap.get(scored_index[e], False)]
    credit = participation = 0
    for e in in_scope_ref:
        r = engine.archive[e]
        if not (r["resolved"] and r["predicted"] == r["outcome"]):
            continue
        credit += 1
        res_o, pred_o, _ = engine.lib.predict(r["action"], r["views"], excl)
        if (res_o, pred_o) != (r["resolved"], r["predicted"]):
            participation += 1
    share = (1.0 - credit / len(in_scope_ref)) if in_scope_ref else None
    if d["tested"]:
        d_state = "d-passed" if d["pass"] else "d-failed"
    elif share is None:
        d_state = "out-of-scope"
    elif share > thresholds["theta_ev"]:
        d_state = "uncertifiable-untested"
    else:
        d_state = "d-untested-correct"
    certifiable_d = d_state in ("d-passed", "d-untested-correct",
                                "out-of-scope")
    certified = b_ok and c_ok and e_ok and certifiable_d
    prods = {engine.lib.concepts[c]["term"]["p"] for c in members}
    return {"unit": name, "members": sorted(members),
            "productions": sorted(prods),
            "initial_kind": prods <= set(INITIAL),
            "prefiltered": False,
            "b": {"margin": round(m_all, 4), "pass": b_ok},
            "c": {"rent_bits": round(rent, 1), "pass": c_ok},
            "d": d, "d_state": d_state,
            "abstention": {"scope": len(scope),
                           "ref_resolved": len(in_scope_ref),
                           "participation": participation,
                           "share": None if share is None
                           else round(share, 4)},
            "e": {"margin_shift": round(m_shift, 4), "pass": e_ok,
                  "evaluable": e_evaluable,
                  "margin_whole_stream_descriptive": round(m_all, 4)},
            "state": ("certified" if certified else
                      ("uncertifiable-untested"
                       if d_state == "uncertifiable-untested"
                       else "failed")),
            "certified": certified}


def certify_run_p003(engine, ref_engine, thresholds):
    check_alignment(engine, ref_engine)
    surface = shift_surface(engine)
    refmap = ref_resolved_map(ref_engine)
    scored_index = {e: i for i, e in enumerate(engine.scored)}
    n_scored = len(engine.scored)
    n_pre = sum(1 for e in engine.scored
                if engine.archive[e]["strata"]["window"] == "pre")
    results = {}
    for name, members in standard_units(engine):
        results[name] = evaluate_unit(engine, name, members, surface,
                                      refmap, scored_index, n_scored,
                                      n_pre, thresholds)
    certified = [n for n, r in results.items() if r["certified"]]
    marker = [n for n in certified if not results[n]["initial_kind"]]
    unc = [n for n, r in results.items()
           if r.get("state") == "uncertifiable-untested"]
    return {"units": results, "n_units": len(results),
            "certified": certified, "n_certified": len(certified),
            "uncertifiable_untested": unc,
            "marker_fired": bool(marker), "marker_units": marker,
            "surface_n": len(surface)}
