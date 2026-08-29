"""Per-concept certification against the frozen criteria (spec 5.1-5.7,
thresholds PREREGISTRATION_002 §3).  Read-only over a completed Engine run —
the frozen tree is never modified; sub-operationalization decisions made here
are declared in the L3-2/L3-3 reports:

  - (b)/(e) ablation surface: ALL scored queries (executed + hypothetical),
    paired per query; significance by sign test on discordant pairs (exact
    to n=200, normal approximation beyond), alpha 0.05.
  - affected-set replay, exact: a concept's removal can only change events
    that reference it (its class's member-events intersected with its
    action, via the engine's archive indexes); unaffected events cancel in
    every with/without comparison, so margins and rents computed on the
    affected set equal the full-archive values.
  - fail-fast prefilter, exact: if a concept's affected SCORED count is
    below delta_b * n_scored, its (b) margin cannot reach delta_b; it is
    reported as failing (b) with the bound, and (c)/(e) are not evaluated
    ("prefiltered").  This is what makes certifying a 10,000-concept lookup
    library tractable — and every prefiltered concept is by construction
    uncertifiable.
  - (c) description bits: spelling at final table sizes plus every logged
    assertion op referencing the concept; rent on the affected set.
  - a concept "faced contradiction" iff violations attach to it directly
    (rules) or to a rule it hosts (classes).
  - (d) locality: repair-batch footprint over library size at that boundary
    (from the op log); restoration: no violations after the last revision
    and pre-window ablation margin >= delta_b - tau_d.
"""
import math

TH = {"delta_b": 0.05, "delta_e": 0.05, "f_d": 0.10, "tau_d": 0.05,
      "alpha": 0.05}
INITIAL = ("P1", "P2", "P3", "P8")


def _sign_test(gains, losses):
    n = gains + losses
    if n == 0:
        return 1.0
    if n <= 200:
        k = min(gains, losses)
        total = sum(math.comb(n, i) for i in range(0, k + 1))
        return min(1.0, 2.0 * total / float(2 ** n))
    z = abs(gains - losses) / math.sqrt(n)
    return math.erfc(z / math.sqrt(2.0))


def _affected_eids(engine, cid):
    rec = engine.lib.concepts[cid]
    t = rec["term"]
    p = t["p"]
    if p in ("P1", "P7", "P10"):
        return set(engine.ev_by_class.get(cid, ()))
    if p == "P4":
        return set(range(len(engine.archive)))
    act = t.get("action", "grind")
    act_ev = set(engine.ev_by_action.get(act, ()))
    host = t.get("cls") or t.get("c1")
    if p in ("P2", "P9") and host:
        return act_ev & set(engine.ev_by_class.get(host, ()))
    if p == "P3":
        hosts = set(engine.ev_by_class.get(t["c1"], ())) \
            | set(engine.ev_by_class.get(t["c2"], ()))
        return act_ev & hosts
    return act_ev          # P5/P6/P8 and expr-based: class-free


def _scored_affected(engine, cid):
    scored = set(engine.scored)
    return sorted(_affected_eids(engine, cid) & scored)


def _ablation_windows(engine, cid, eids):
    """Paired ablation over the affected scored rows; per-window tallies."""
    excl = frozenset({cid})
    tall = {}
    for eid in eids:
        rec = engine.archive[eid]
        res_o, pred_o, _ = engine.lib.predict(rec["action"], rec["views"],
                                              excl)
        w = int(rec["resolved"] and rec["predicted"] == rec["outcome"])
        wo = int(res_o and pred_o == rec["outcome"])
        for key in ("all", rec["strata"]["window"]):
            t = tall.setdefault(key, [0, 0, 0, 0])   # gains, losses
            if w and not wo:
                t[0] += 1
            elif wo and not w:
                t[1] += 1
    return tall


def _margin(tally, key, n_total):
    g, l = tally.get(key, [0, 0, 0, 0])[:2]
    return (g - l) / n_total if n_total else 0.0, g, l


def _rent(engine, cid):
    """Lifetime rent on the affected archive subset (exact), minus
    description bits (spelling + assertions referencing cid)."""
    rec = engine.lib.concepts[cid]
    excl = frozenset({cid})
    start = rec["admitted_ep"]
    saved = 0.0
    for eid in _affected_eids(engine, cid):
        r = engine.archive[eid]
        if r["ep"] < start or r["type"] == "scored_hyp":
            continue
        res_w, pred_w, _ = engine.lib.predict(r["action"], r["views"])
        res_o, pred_o, _ = engine.lib.predict(r["action"], r["views"], excl)
        saved += (engine.lib.code_bits(res_o, pred_o, r["outcome"]) -
                  engine.lib.code_bits(res_w, pred_w, r["outcome"]))
    from crucible import grammar as G
    n_cls, n_att, n_con = engine.lib.counts_for_costs()
    desc = G.spelling_cost(rec["term"], n_cls, n_att, n_con)
    assertion = 0.0
    for op in engine.oplog:
        tag = op.get("op")
        if tag in ("member+", "member-") and op.get("cid") == cid:
            assertion += op["bits"]
        elif tag == "attr" and cid in (op.get("cls"), op.get("attr")):
            assertion += op["bits"]
    return saved - desc - assertion


def _lib_size_before(engine, ep):
    n = 0
    for op in engine.oplog:
        if op["ep"] >= ep:
            break
        if op.get("op") == "new":
            n += 1
        elif op.get("op") == "retire":
            n -= 1
    return max(1, n)


def _contradictions(engine, cid):
    rec = engine.lib.concepts.get(cid)
    vids = list(rec["violations"])
    if rec["term"]["p"] in ("P1", "P7", "P10"):
        for rid, r in engine.lib.concepts.items():
            if r["term"].get("cls") == cid or cid in (r["term"].get("c1"),
                                                      r["term"].get("c2")):
                vids.extend(r["violations"])
    return sorted(set(vids))


def _d_criterion(engine, cid, ab_pre_margin):
    vids = _contradictions(engine, cid)
    if not vids:
        return {"tested": False}
    rec = engine.lib.concepts[cid]
    first_v_ep = min(engine.violations[v]["ep"] for v in vids)
    post_revs = [r for r in rec["revisions"] if r["ep"] >= first_v_ep]
    out = {"tested": True, "n_contradictions": len(vids),
           "n_revisions_after": len(post_revs)}
    if not post_revs:
        out.update({"pass": False, "why": "no revision after contradiction"})
        return out
    cited = [v for r in post_revs for v in r["cites"]]
    ok_cites = bool(cited) and all(
        v < len(engine.violations) and engine.violations[v]["ep"] <= r["ep"]
        for r in post_revs for v in r["cites"])
    frac = 0.0
    for op in engine.oplog:
        if op.get("op") == "batch-summary" and op.get("revises"):
            revs = (op["revises"] if isinstance(op["revises"], list)
                    else [op["revises"]])
            if cid in revs:
                frac = max(frac, len(op["footprint"]) /
                           _lib_size_before(engine, op["ep"] + 1))
    last_rev_ep = max(r["ep"] for r in post_revs)
    later = [v for v in vids if engine.violations[v]["ep"] > last_rev_ep]
    restored = (len(later) == 0
                and ab_pre_margin >= TH["delta_b"] - TH["tau_d"])
    ok = ok_cites and frac <= TH["f_d"] and restored
    out.update({"cites_valid": ok_cites, "footprint_frac": round(frac, 3),
                "later_violations": len(later), "restored": restored,
                "pass": ok})
    return out


def certify_run(engine):
    n_scored = len(engine.scored)
    n_windows = {}
    for eid in engine.scored:
        w = engine.archive[eid]["strata"]["window"]
        n_windows[w] = n_windows.get(w, 0) + 1
    min_affected = TH["delta_b"] * n_scored
    results = {}
    for cid in list(engine.lib.order):
        rec = engine.lib.concepts[cid]
        prod = rec["term"]["p"]
        eids = _scored_affected(engine, cid)
        if len(eids) < min_affected:
            results[cid] = {"production": prod,
                            "initial_kind": prod in INITIAL,
                            "prefiltered": True,
                            "affected_scored": len(eids),
                            "b": {"margin_bound": len(eids) / n_scored,
                                  "pass": False},
                            "certified": False}
            continue
        tall = _ablation_windows(engine, cid, eids)
        m_all, g, l = _margin(tall, "all", n_scored)
        b_ok = m_all >= TH["delta_b"] and _sign_test(g, l) < TH["alpha"]
        m_pre, _, _ = _margin(tall, "pre", n_windows.get("pre", 1))
        m_post, gp, lp = _margin(tall, "post", n_windows.get("post", 1))
        e_ok = (m_post >= TH["delta_e"]
                and _sign_test(gp, lp) < TH["alpha"])
        rent = _rent(engine, cid)
        c_ok = rent > 0
        d = _d_criterion(engine, cid, m_pre)
        d_ok = d["pass"] if d["tested"] else True
        certified = b_ok and c_ok and e_ok and d_ok
        results[cid] = {
            "production": prod, "initial_kind": prod in INITIAL,
            "prefiltered": False, "affected_scored": len(eids),
            "b": {"margin": round(m_all, 4), "p": _sign_test(g, l),
                  "pass": b_ok},
            "c": {"rent_bits": round(rent, 1), "pass": c_ok},
            "d": d,
            "e": {"margin_post": round(m_post, 4),
                  "p": _sign_test(gp, lp), "pass": e_ok},
            "certified": certified,
        }
    certified = [cid for cid, r in results.items() if r["certified"]]
    marker = [cid for cid in certified if not results[cid]["initial_kind"]]
    return {"concepts": results, "n_concepts": len(results),
            "certified": certified, "n_certified": len(certified),
            "marker_fired": bool(marker), "marker_concepts": marker}
