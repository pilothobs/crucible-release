"""L3-1 audit suite A1-A16 (spec 6.4; threat-model roll-up).

Every probe is decision-level (the scored-query unit) unless stated.  Each
audit returns a dict with a "pass" bool and its evidence; the runner collects
them into the gate artifact.  Probes are validated against planted leaks in
planted.py before their silence here counts (T15).
"""
import math
import subprocess
import sys
from . import constants as C
from . import grammar as G
from .gen import generate_corpus, corpus_digest
from .engine import Engine
from . import policies as PL

UNRES = math.log2(len(C.OUTCOMES))
WRONG = math.log2(10 / C.EPSILON)
HIT = -math.log2(1 - C.EPSILON)


# ---------------------------------------------------------------- probe core
def probe_feature(rows, feat_fn, target_fn, baseline):
    """Majority-map probe with an episode-parity train/eval split.
    Returns (accuracy, excess-over-baseline, n)."""
    train = {}
    for r in rows:
        if r["ep"] % 2 == 0:
            continue
        f, t = feat_fn(r), target_fn(r)
        train.setdefault(f, {}).setdefault(t, 0)
        train[f][t] += 1
    table = {f: max(sorted(d), key=lambda t: d[t]) for f, d in train.items()}
    hits = n = 0
    for r in rows:
        if r["ep"] % 2 == 1:
            continue
        n += 1
        if table.get(feat_fn(r)) == target_fn(r):
            hits += 1
    acc = hits / n if n else 0.0
    return acc, acc - baseline, n


def scored_rows(engine):
    """Probe rows: EXECUTED scored queries only — hypothetical queries have
    stated conditions and unrevealed outcomes, a stylized subset that would
    dilute decision-level probes of the real surface."""
    rows = []
    for eid in engine.scored:
        r = engine.archive[eid]
        if r["type"] == "scored_hyp":
            continue
        a = r["audit"]
        rows.append({
            "ep": r["ep"], "step": r["step"],
            "action": r["action"], "outcome": r["outcome"],
            "kind": a["kinds"][0], "kinds": a["kinds"],
            "appearance": a["appearance"][0], "slot": a["slots"][0],
            "cond": r["views"][0]["cond"], "n_prior": a["n_prior"][0],
            "ambient_hits": a["ambient_hits"][0],
            "prev": r["views"][0]["prev"],
            "counts": r["views"][0]["counts"],
            "cracked": a["cracked_arrival"][0],
            "strata": r["strata"],
            "correct": int(r["resolved"] and r["predicted"] == r["outcome"]),
        })
    return rows


def kind_baseline(rows):
    counts = {}
    for r in rows:
        counts[r["kind"]] = counts.get(r["kind"], 0) + 1
    return max(counts.values()) / len(rows)


def outcome_baseline(rows):
    counts = {}
    for r in rows:
        counts[r["outcome"]] = counts.get(r["outcome"], 0) + 1
    return max(counts.values()) / len(rows)


# ------------------------------------------------------------------- audits
def stratum_table(results):
    keys = sorted({k for r in results.values() for k in r["accuracy"]})
    return {name: {k: res["accuracy"].get(k, (None, 0))
                   for k in keys} for name, res in results.items()}


CHEAP = ("lookup", "cluster", "static", "ambient_corr", "null_default")
PRIMARY = ("pre", "mid", "post", "fc_unseen:post", "k_new:post",
           "weathered:mid", "weathered:post")


def a1_headroom(results, floor=0.25):
    out = {"floor": floor, "strata": {}, "pass": True}
    for key in PRIMARY:
        orc = results["oracle_full"]["accuracy"].get(key)
        if not orc or orc[1] < 8:
            continue
        cheap_best, cheap_who = -1, None
        for name in CHEAP:
            v = results[name]["accuracy"].get(key)
            if v and v[0] > cheap_best:
                cheap_best, cheap_who = v[0], name
        margin = orc[0] - cheap_best
        out["strata"][key] = {"oracle": orc[0], "cheap_best": cheap_best,
                              "cheap_who": cheap_who, "margin": margin,
                              "n": orc[1]}
        if margin < floor:
            out["pass"] = False
    return out


def a2_identification(results, floor=0.15):
    out = {"floor": floor, "strata": {}, "pass": True}
    for key in ("pre", "mid", "post"):
        ident = results["oracle_ident"]["accuracy"].get(key)
        cheap_best = max(results[n]["accuracy"].get(key, (0, 0))[0]
                         for n in CHEAP)
        margin = ident[0] - cheap_best
        out["strata"][key] = {"oracle_ident": ident[0],
                              "cheap_best": cheap_best, "margin": margin}
        if margin < floor:
            out["pass"] = False
    return out


def a3_mdl(results, engines, floor_class=5000.0, floor_factored=300.0):
    empty = results["null_empty"]["total_bits"]
    lookup = results["lookup"]["total_bits"]
    class_only = results["class_only"]["total_bits"]
    factored = results["oracle_full"]["total_bits"]
    # factored-vs-class model gap measured on description charges alone
    # (memberships are backdoor-identical for the two oracles)
    gap_model = (results["class_only"]["charge_bits"] -
                 results["oracle_full"]["charge_bits"])
    out = {
        "empty_total": empty, "lookup_total": lookup,
        "lookup_divergence": lookup - empty,
        "class_gap_vs_empty": empty - class_only,
        "factored_gap_vs_class_total": class_only - factored,
        "factored_gap_vs_class_model": gap_model,
        "floors": {"class_vs_empty": floor_class,
                   "factored_vs_class_model": floor_factored},
    }
    out["pass"] = (lookup > empty and
                   out["class_gap_vs_empty"] >= floor_class and
                   gap_model >= floor_factored)
    return out


def a4_appearance(rows, tol=0.03):
    out = {"tol": tol, "features": {}, "pass": True}
    kb, ob = kind_baseline(rows), outcome_baseline(rows)
    for i in range(C.APPEARANCE_FEATURES):
        f = lambda r, i=i: r["appearance"][i]
        acc_k, exc_k, _ = probe_feature(rows, f, lambda r: r["kind"], kb)
        acc_o, exc_o, _ = probe_feature(rows, f, lambda r: r["outcome"], ob)
        out["features"]["app%d" % i] = {"kind_excess": exc_k,
                                        "outcome_excess": exc_o}
        if exc_k > tol or exc_o > tol:
            out["pass"] = False
    return out


def a5_feature_sweep(rows, tol=0.03):
    """Decision-level sweep.  Gated features must sit at floor for BOTH
    targets; measured features (condition, counts, prev) are legitimate
    structure (T4) and are reported, not gated.  Includes the decoy checks:
    history (prev), counts, and pair-order asymmetry (R4)."""
    kb, ob = kind_baseline(rows), outcome_baseline(rows)
    gated = {
        "token_slot": lambda r: r["slot"],
        "app_joint": lambda r: r["appearance"],
    }
    measured = {
        # ambient_hits is kind-correlated BY DECLARATION (the causal-trap
        # confound); its dedicated gate is A9 (outcome excess), so here it is
        # measured, not gated — v0.4: it sat in the gated set by mistake and
        # the rule-derived marginals exposed the contradiction
        "ambient_hits": lambda r: min(r["ambient_hits"], 4),
        "condition": lambda r: r["cond"],
        "n_prior": lambda r: min(r["n_prior"], 6),
        "prev_event": lambda r: r["prev"],
        "count_tap": lambda r: min(r["counts"].get("tap", 0), 4),
    }
    out = {"tol": tol, "gated": {}, "measured": {}, "pass": True}
    for name, f in gated.items():
        _, exc_k, _ = probe_feature(rows, f, lambda r: r["kind"], kb)
        _, exc_o, _ = probe_feature(rows, f, lambda r: r["outcome"], ob)
        out["gated"][name] = {"kind_excess": exc_k, "outcome_excess": exc_o}
        if exc_k > tol or exc_o > tol:
            out["pass"] = False
    for name, f in measured.items():
        _, exc_k, _ = probe_feature(rows, f, lambda r: r["kind"], kb)
        _, exc_o, _ = probe_feature(rows, f, lambda r: r["outcome"], ob)
        out["measured"][name] = {"kind_excess": exc_k, "outcome_excess": exc_o}
    # decoy: memorylessness given condition — does prev add outcome
    # predictiveness beyond (action already fixed per-probe) cond?
    base_f = lambda r: (r["action"], r["cond"], r["kind"])
    hist_f = lambda r: (r["action"], r["cond"], r["kind"], r["prev"])
    acc_b, _, _ = probe_feature(rows, base_f, lambda r: r["outcome"], ob)
    acc_h, _, _ = probe_feature(rows, hist_f, lambda r: r["outcome"], ob)
    out["memoryless_given_cond"] = {"base": acc_b, "with_history": acc_h,
                                    "history_gain": acc_h - acc_b}
    if acc_h - acc_b > tol:
        out["pass"] = False
    return out


def a5_pair_order(engine, tol=0.0):
    """F2 symmetry, measured: grind outcome must be invariant to order."""
    from .dyn_a import f2
    diffs = 0
    n = 0
    for eid in engine.scored:
        r = engine.archive[eid]
        if r["action"] != "grind":
            continue
        k = r["audit"]["kinds"]
        c = [v["cond"] for v in r["views"]]
        n += 1
        if f2(k[0], k[1], c[0], c[1]) != f2(k[1], k[0], c[1], c[0]):
            diffs += 1
    return {"n": n, "order_asymmetries": diffs, "pass": diffs == 0}


def a6_shift_invisibility(engine, window=20, tol=0.25):
    """Side-channel probe at E_R: nearest-centroid classification of
    20-episode outcome-frequency windows (k_new events excluded), plus
    ambient-rate and episode-shape checks.  Must sit near chance."""
    lo, hi = C.E_R - 100, C.E_R + 100
    windows = []
    for start in range(lo, hi, window):
        counts = {}
        n = 0
        for r in engine.archive:
            if not (start <= r["ep"] < start + window):
                continue
            if any(k == C.K_NEW for k in r["audit"]["kinds"]):
                continue
            if r["action"] == "grind":
                # the grind channel's pair-mix change at E_R IS Shift-T (the
                # holdout opening), a designed and declared distribution
                # change priced under T7 — A6's side-channel claim is scoped
                # to the unary conditionals, ambient rates and episode shape
                continue
            key = (r["action"], r["outcome"])
            counts[key] = counts.get(key, 0) + 1
            n += 1
        # per-action conditional vectors: joint frequencies are distorted by
        # the exclusion itself (k_new eats ambient-soak targets), which is an
        # audit artifact, not a learner-visible side channel
        per_action = {}
        for (a, o), v in counts.items():
            per_action.setdefault(a, {})[o] = v
        vec = {}
        for a, outs in per_action.items():
            tot = sum(outs.values())
            for o, v in outs.items():
                vec[(a, o)] = v / tot
        windows.append((start + window <= C.E_R, vec))
    # permutation test on the pre/post centroid distance (leave-one-out
    # nearest-centroid at n=10 anti-predicts systematically — an artifact,
    # found when the audit returned 0.1 accuracy on identical distributions)
    import random as _random

    def centroid(vecs):
        keys = {k for v in vecs for k in v}
        return {k: sum(v.get(k, 0) for v in vecs) / len(vecs) for k in keys}

    def dist(a, b):
        keys = set(a) | set(b)
        return sum((a.get(k, 0) - b.get(k, 0)) ** 2 for k in keys)

    labels = [is_pre for is_pre, _ in windows]
    vecs = [v for _, v in windows]

    def stat(lab):
        pre = [v for l, v in zip(lab, vecs) if l]
        post = [v for l, v in zip(lab, vecs) if not l]
        return dist(centroid(pre), centroid(post))

    observed = stat(labels)
    rng = _random.Random(424243)
    n_perm, ge = 400, 0
    for _ in range(n_perm):
        lab = list(labels)
        rng.shuffle(lab)
        if stat(lab) >= observed:
            ge += 1
    p = (ge + 1) / (n_perm + 1)
    return {"windows": len(windows), "observed_distance": observed,
            "permutation_p": p, "pass": p >= 0.05}


def a7_causal_trap(results, engines, floor=0.05):
    """AmbientCorr: passive-stream fit vs interventional scored accuracy."""
    eng = engines["ambient_corr"]
    pol = eng.policy
    amb_hits = amb_n = 0
    for r in eng.archive:
        if r["type"] != "ambient":
            continue
        amb_n += 1
        if pol.current.get(r["action"]) == r["outcome"]:
            amb_hits += 1
    passive = amb_hits / amb_n
    sc_hits = sc_n = 0
    for eid in eng.scored:
        r = eng.archive[eid]
        if r["action"] not in ("heat", "soak"):
            continue
        sc_n += 1
        sc_hits += int(r["resolved"] and r["predicted"] == r["outcome"])
    interventional = sc_hits / sc_n
    gap = passive - interventional
    return {"passive_fit": passive, "interventional": interventional,
            "gap": gap, "floor": floor, "pass": gap >= floor}


def a8_token_position(rows, tol=0.03):
    kb = kind_baseline(rows)
    _, exc, n = probe_feature(rows, lambda r: r["slot"],
                              lambda r: r["kind"], kb)
    return {"slot_kind_excess": exc, "n": n, "tol": tol, "pass": exc <= tol}


def a9_ambient_targeting(rows, tol=0.06):
    """ambient_hits IS kind-correlated by design; the audit measures how far
    the cue carries into outcome prediction and requires the cheap ceiling
    (not zero).  Gate: outcome excess below tol.  Probed on late-step rows
    (hits have accumulated), where the cue is strongest — probing early rows
    diluted the planted-leak fixture into silence (T15)."""
    late = [r for r in rows if r["step"] >= 15]
    ob = outcome_baseline(late)
    _, exc_o, _ = probe_feature(late, lambda r: min(r["ambient_hits"], 2),
                                lambda r: r["outcome"], ob)
    kb = kind_baseline(late)
    _, exc_k, _ = probe_feature(late, lambda r: min(r["ambient_hits"], 2),
                                lambda r: r["kind"], kb)
    return {"outcome_excess": exc_o, "kind_excess_reported": exc_k,
            "n_late": len(late), "tol": tol, "pass": exc_o <= tol}


def ambient_crosstype_overlap(corpus):
    """Fraction of episodes in which some object is targeted by BOTH ambient
    event types.  In the real generator the two types target different
    attribute sets (a2+ for draft-heat, a3+ for rain-soak; overlap only on
    the rare kind B), so this rate is structurally low; a planted
    single-kind targeting label drives it high.  This is PL3's
    discriminating statistic — magnitude of the kind cue cannot separate
    the declared confound from a planted label, structure can."""
    n = hit = 0
    for epi in corpus:
        by_type = {}
        for ev, tgt in epi["ambient"]:
            by_type.setdefault(ev, set()).add(tgt)
        n += 1
        sets = list(by_type.values())
        if len(sets) == 2 and sets[0] & sets[1]:
            hit += 1
    return hit / n


def a10_scans(corpora):
    """Holdout + weathered enforcement scans over every eval-seed corpus."""
    bad_pairs = bad_crack = 0
    first_cooc_eps = {}
    for seed, corpus in corpora.items():
        for epi in corpus:
            ep = epi["episode"]
            if ep < C.E_R:
                for i in range(C.N_OBJ):
                    for j in range(i + 1, C.N_OBJ):
                        cell = frozenset({epi["kinds"][i], epi["kinds"][j]})
                        if cell in C.HOLDOUT_PAIRS:
                            bad_pairs += 1
            if ep < C.E_C and any(a == "cracked" for a in epi["arrival"]):
                bad_crack += 1
            if "first_cooc" in epi:
                first_cooc_eps.setdefault(seed, []).append(ep)
    return {"holdout_violations_pre_ER": bad_pairs,
            "cracked_pre_EC": bad_crack,
            "first_cooc_episodes": first_cooc_eps,
            "ambient_crosstype_overlap": {
                str(s): ambient_crosstype_overlap(c)
                for s, c in corpora.items()},   # PL3's real-side statistic
            "pass": bad_pairs == 0 and bad_crack == 0}


def a11_stream_independence(eval_seed, episodes=None):
    # window must span E_C, else the arrival stream is never consumed and
    # its surgery check is vacuous (found on the first audit run)
    episodes = episodes or (C.E_C + 40)
    base = generate_corpus(eval_seed, episodes=episodes)
    owned = {"appearance": ("appearance",), "token": ("perm",),
             "arrival": ("arrival",), "query": ("queries",),
             "ambient": ("ambient",)}
    seeds = {"appearance": C.SEED_APPEARANCE, "token": C.SEED_TOKEN,
             "arrival": C.SEED_ARRIVAL, "query": C.SEED_QUERY,
             "ambient": C.SEED_AMBIENT}
    out = {"streams": {}, "pass": True}
    for name, fields in owned.items():
        alt = generate_corpus(eval_seed, episodes=episodes,
                              surgery={name: seeds[name] + 977})
        changed_own = any(b[f] != a[f] for b, a in zip(base, alt)
                          for f in fields)
        others_equal = all(
            b[f] == a[f] for b, a in zip(base, alt)
            for f in ("kinds", "appearance", "perm", "arrival", "ambient",
                      "queries") if f not in fields)
        out["streams"][name] = {"own_changed": changed_own,
                                "others_identical": others_equal}
        if not (changed_own and others_equal):
            out["pass"] = False
    return out


def a11_hashseed(eval_seed):
    code = ("import sys; sys.path.insert(0, %r); "
            "from crucible.gen import generate_corpus, corpus_digest; "
            "print(corpus_digest(generate_corpus(%d, episodes=40)))") % (
        _pkg_root(), eval_seed)
    digs = {}
    for hs in ("0", "12345", None):
        env = dict(__import__("os").environ)
        env.pop("PYTHONHASHSEED", None)
        if hs is not None:
            env["PYTHONHASHSEED"] = hs
        r = subprocess.run([sys.executable, "-c", code], env=env,
                           capture_output=True, text=True, check=True)
        digs[hs or "unset"] = r.stdout.strip()
    ok = len(set(digs.values())) == 1
    return {"digests": digs, "pass": ok}


def _pkg_root():
    import os
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def a13_mdl_sensitivity(perturb=2.0):
    """Library-cost orderings must be stable under +-2 bits/rule and under
    epsilon x10 either way (analytic)."""
    from .policies import factored_ops, ClassOnlyOracle
    ops_f, _ = factored_ops()

    def lib_cost(ops, bonus):
        G.PRICE_TWEAK["rule_bonus"] = bonus
        n_cls = sum(1 for o in ops if o[0] == "new" and o[1]["p"] == "P1")
        n_att = sum(1 for o in ops if o[0] == "new" and o[1]["p"] == "P4")
        total = 0.0
        for o in ops:
            if o[0] == "new":
                total += G.spelling_cost(o[1], max(2, n_cls), max(2, n_att),
                                         40)
            elif o[0] == "attr":
                total += G.attribution_cost(n_cls, n_att)
        G.PRICE_TWEAK["rule_bonus"] = 0.0
        return total

    pol = ClassOnlyOracle()
    pol.begin_run()
    pol._done = False
    batches = pol.boundary_batches(0)
    ops_c = batches[0][0]
    out = {"points": {}, "pass": True}
    for b in (-perturb, 0.0, perturb):
        cf, cc = lib_cost(ops_f, b), lib_cost(ops_c, b)
        out["points"]["%+.0f" % b] = {"factored": cf, "class_only": cc,
                                      "factored_cheaper": cf < cc}
        if cf >= cc:
            out["pass"] = False
    # epsilon sensitivity: cost ordering of coding outcomes
    for eps in (C.EPSILON / 10, C.EPSILON, C.EPSILON * 10):
        assert -math.log2(1 - eps) < math.log2(len(C.OUTCOMES)) \
            < math.log2(10 / eps)
    out["epsilon_ordering"] = "hit < unresolved < wrong at eps/10, eps, 10eps"
    return out


def a14_determinism(corpus, results_digest_fn):
    eng1 = Engine(corpus, PL.OracleFull())
    r1 = eng1.run()
    eng2 = Engine(corpus, PL.OracleFull())
    r2 = eng2.run()
    d1, d2 = results_digest_fn(eng1), results_digest_fn(eng2)
    ledger_ok = abs(sum(r["bits"] for r in eng1.archive)
                    - eng1.data_bits) < 1e-6
    return {"rerun_digest_equal": d1 == d2, "digest": d1[:16],
            "ledger_recompute_ok": ledger_ok,
            "pass": d1 == d2 and ledger_ok}


def a15_no_peek(corpus):
    """Scramble every outcome after prediction: the prediction sequence must
    be byte-identical to the normal run's (predictions cannot depend on
    outcomes of their own events)."""
    from . import dyn_a

    class Scrambled:
        @staticmethod
        def f1(alpha, cond, action):
            out, nc = dyn_a.f1(alpha, cond, action)
            i = C.OUTCOMES.index(out)
            return C.OUTCOMES[(i + 5) % len(C.OUTCOMES)], nc

        @staticmethod
        def f2(ai, aj, ci, cj):
            out = dyn_a.f2(ai, aj, ci, cj)
            return C.OUTCOMES[(C.OUTCOMES.index(out) + 5) % len(C.OUTCOMES)]

    e1 = Engine(corpus[:80], PL.OracleFull())
    e1.run()
    e2 = Engine(corpus[:80], PL.OracleFull(), dyn=Scrambled)
    e2.run()
    seq1 = [(r["ep"], r["step"], r["predicted"]) for r in e1.archive]
    seq2 = [(r["ep"], r["step"], r["predicted"]) for r in e2.archive]
    return {"n_events": len(seq1), "pass": seq1 == seq2}


def a16_reachability(corpora):
    """The five analytic checks (threat model A16, v0.3)."""
    n_cls, n_att, n_con = 6, 3, 40   # steady-state oracle library sizes
    rule_new = G.OP_COST + G.spelling_cost(
        {"p": "P5", "expr": [("has", "a", 1)], "cond": frozenset({"cracked"}),
         "action": "tap", "out": "shatter"}, n_cls, n_att, n_con)
    edit = G.revise_cost("P5", "cond", frozenset({"pristine", "charred",
                                                  "soaked"}),
                         n_con, n_cls, n_att)
    p7_new = G.OP_COST + G.spelling_cost({"p": "P7", "cls": "c", "cond":
                                          "cracked"}, n_cls, n_att, n_con)
    retire = G.retire_cost(n_con)
    # measured cracked-tap exposure from the real corpora (mid+post windows)
    n_cracked_tap = 0
    n_runs = len(corpora)
    for corpus in corpora.values():
        for epi in corpus:
            if epi["episode"] < C.E_C:
                continue
            # scored tap queries on cracked arrivals (policy-independent floor)
            for q in epi["queries"]:
                act, idxs = q[0], q[1]
                if act == "tap" and any(epi["arrival"][i] == "cracked"
                                        for i in idxs):
                    n_cracked_tap += 1
    n_events = n_cracked_tap / n_runs      # per-run scored floor
    repairs = {
        "do_nothing": n_events * WRONG,
        "add_only": rule_new + n_events * UNRES,
        "narrow_only": edit + n_events * UNRES,
        "narrow_plus_add": edit + rule_new + n_events * HIT,
        "p7_shadow": p7_new + rule_new + n_events * UNRES,  # rank-B conflict
        "retire_respell": retire + 2 * rule_new + n_events * HIT,
    }
    best = min(repairs, key=repairs.get)
    check1 = {"repairs_bits": repairs, "cracked_tap_scored_per_run": n_events,
              "optimal": best, "pass": best == "narrow_plus_add"}
    # check 2: split at E_R for the factored library
    new_class_split = (G.OP_COST + G.spelling_cost({"p": "P1"}, n_cls, n_att,
                                                   n_con)
                       + 3 * G.attribution_cost(n_cls, n_att))
    n_knew_events = 0
    for corpus in corpora.values():
        for epi in corpus:
            if epi["episode"] < C.E_R:
                continue
            n_knew_events += sum(1 for k in epi["kinds"] if k == C.K_NEW) * 2
    n_knew = n_knew_events / n_runs
    split_repairs = {
        "do_nothing_misassert": n_knew * 0.3 * WRONG,
        "split_with_continuity": new_class_split,
        "retire_respell_class": retire + new_class_split + 5 * rule_new,
    }
    best2 = min(split_repairs, key=split_repairs.get)
    check2 = {"repairs_bits": split_repairs, "knew_objects_per_run": n_knew,
              "optimal": best2, "pass": best2 == "split_with_continuity"}
    # check 3: factoring transition op count
    from .policies import factored_ops
    ops_f, _ = factored_ops()
    transition_ops = (len([o for o in ops_f
                           if o[0] in ("new", "attr")
                           and (o[0] == "attr" or o[1]["p"] in
                                ("P4", "P5", "P6"))])
                      + 30 + 21 + 3)   # retire URules + PRules + 3 defaults
    check3 = {"transition_ops": transition_ops, "limit": 96,
              "pass": transition_ops <= 96}
    # check 4: genesis rent arithmetic at frozen schedule
    events_per_obj = C.T_STEPS / C.N_OBJ
    probes = 2.4
    member = G.member_cost(n_cls)
    rent_per_obj = (events_per_obj - probes) * UNRES - member
    class_genesis = (G.OP_COST + G.spelling_cost({"p": "P1"}, 2, 2, 4)
                     + 3 * (G.OP_COST + G.spelling_cost(
                         {"p": "P2", "cls": "c", "cond": None,
                          "action": "tap", "out": "thud"}, 2, 2, 4)))
    objs_per_class_run = C.EPISODES * C.N_OBJ / 6
    payback_objects = class_genesis / max(rent_per_obj, 1e-9)
    check4 = {"events_per_object": events_per_obj,
              "assumed_probes": probes, "member_bits": member,
              "rent_per_object_bits": rent_per_obj,
              "class_genesis_bits": class_genesis,
              "payback_objects": payback_objects,
              "objects_per_class_per_run": objs_per_class_run,
              "pass": rent_per_obj > 2.0 and
              payback_objects < objs_per_class_run}
    # check 5: membership evidence number
    k_events = math.ceil(member / UNRES)
    check5 = {"member_bits": member, "bits_per_resolved_event": UNRES,
              "events_to_justify": k_events, "pass": k_events <= 3}
    ok = all(c["pass"] for c in (check1, check2, check3, check4, check5))
    return {"check1_body_edit": check1, "check2_split": check2,
            "check3_batch_fit": check3, "check4_genesis": check4,
            "check5_membership_evidence": check5, "pass": ok}
