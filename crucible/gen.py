"""CRUCIBLE corpus generator.

Pre-draws every policy-independent channel for a full run (600 episodes) from
named, separately seeded RNG streams (threat T9): kind assignment, appearance,
token/display permutation, arrival conditions, ambient schedule + targets, and
scored-query designs.  Policies never touch these streams, which is what makes
the scored stream identical across policies (A14) and the seed-surgery audit
(A11) meaningful.

`leak` selects a planted-leak variant for probe validation (T15); None is the
real generator.  Leak variants are quarantined here on purpose: every probe
must fire on its planted leak before its silence on the real generator counts.
"""
import random
from . import constants as C

# ---- import-time checks on the frozen latent structure (spec 2.2/2.5) ------
def _check_frozen_structure():
    k0 = C.K0
    n = len(k0)
    assert len(set(k0)) == n == 5
    for i in range(3):  # no constant attribute
        vals = {k[i] for k in k0}
        assert vals == {0, 1}, f"attribute {i} constant over K0"
    for i in range(3):  # no perfectly correlated attribute pair
        for j in range(i + 1, 3):
            pairs = {(k[i], k[j]) for k in k0}
            assert len(pairs) >= 3, f"attributes {i},{j} perfectly correlated"
    assert C.K_NEW not in k0
    assert C.K_NEW[:2] == C.K_OLD[:2] and C.K_NEW[2] != C.K_OLD[2]
    assert C.K_OLD[0] == 0  # so both-hard never preempts k_old pairs
    # holdout connectivity: every F2 region (c1,c2) has >= 1 visible cell
    from .dyn_a import f2
    visible_regions = set()
    for i, a in enumerate(k0):
        for b in k0[i:]:
            if frozenset({a, b}) in C.HOLDOUT_PAIRS:
                continue
            visible_regions.add((a[0] & b[0], a[2] ^ b[2]))
    assert visible_regions == {(0, 0), (0, 1), (1, 0), (1, 1)}, visible_regions
    # T8: no outcome symbol first reachable via held-out cells only
    visible_outs = set()
    heldout_outs = set()
    for i, a in enumerate(k0):
        for b in k0[i:]:
            o = f2(a, b, "pristine", "pristine")
            (heldout_outs if frozenset({a, b}) in C.HOLDOUT_PAIRS
             else visible_outs).add(o)
    assert heldout_outs <= visible_outs, (heldout_outs, visible_outs)
    # the holdout-derivation rule duplicates the F2 region map inside
    # constants.py; assert the duplicate agrees with the real dynamics
    # cell-for-cell (single-source-of-truth guard)
    allk = list(k0) + [C.K_NEW]
    for a in allk:
        for b in allk:
            assert C._pristine_pair_outcome(a, b) == \
                f2(a, b, "pristine", "pristine"), (a, b)
    # H3 balance, re-asserted on the derived set
    held = [C._pristine_pair_outcome(*sorted(cell)) for cell in
            C.HOLDOUT_PAIRS]
    assert max(held.count(o) for o in set(held)) <= 2, held

_check_frozen_structure()


def _streams(eval_seed, surgery=None):
    """Named streams; `surgery` maps a stream name to an alternative sub-seed
    (audit A11: redrawing one stream must leave the others byte-identical)."""
    base = {
        "kind": C.SEED_KIND, "appearance": C.SEED_APPEARANCE,
        "token": C.SEED_TOKEN, "ambient": C.SEED_AMBIENT,
        "arrival": C.SEED_ARRIVAL, "query": C.SEED_QUERY,
    }
    if surgery:
        base.update(surgery)
    off = eval_seed * 1000003
    return {name: random.Random(seed + off) for name, seed in base.items()}


def _draw_kinds(rk, episode):
    post = episode >= C.E_R
    weights = C.KIND_W_POST if post else C.KIND_W_PRE
    kinds_list = list(weights)
    wts = [weights[k] for k in kinds_list]
    for _ in range(10000):
        kinds = tuple(rk.choices(kinds_list, weights=wts, k=C.N_OBJ))
        if post:
            return kinds
        ok = True
        for i in range(C.N_OBJ):
            for j in range(i + 1, C.N_OBJ):
                if frozenset({kinds[i], kinds[j]}) in C.HOLDOUT_PAIRS:
                    ok = False
        if ok:
            return kinds
    raise RuntimeError("rejection sampling failed")


def generate_corpus(eval_seed, leak=None, surgery=None, episodes=None):
    episodes = episodes or C.EPISODES
    st = _streams(eval_seed, surgery)
    rk, ra, rt = st["kind"], st["appearance"], st["token"]
    rv, rb, rq = st["arrival"], st["ambient"], st["query"]
    corpus = []
    for ep in range(1, episodes + 1):
        kinds = _draw_kinds(rk, ep)
        appearance = [tuple(ra.randrange(C.APPEARANCE_VALUES)
                            for _ in range(C.APPEARANCE_FEATURES))
                      for _ in range(C.N_OBJ)]
        if leak == "appearance":     # PL1: appearance encodes kind
            allk = list(C.K0) + [C.K_NEW]
            appearance = [(allk.index(k), a[1], a[2])
                          for k, a in zip(kinds, appearance)]
        # display permutation: slot -> latent index
        perm = list(range(C.N_OBJ))
        rt.shuffle(perm)
        if leak == "token":          # PL2: display order sorted by kind
            allk = list(C.K0) + [C.K_NEW]
            perm = sorted(range(C.N_OBJ), key=lambda i: allk.index(kinds[i]))
        crack_from = 1 if leak == "cracked_early" else C.E_C
        arrival = [("cracked" if ep >= crack_from and rv.random() < C.CRACK_P
                    else "pristine") for _ in range(C.N_OBJ)]
        # ambient schedule: event type + latent target index per ambient step
        ambient = []
        hit = set()   # ambient prefers not-yet-targeted positives, so the
        # confound stays sharp instead of saturating on charred/soaked
        # repeats (audit A7 found the first design's trap had no teeth);
        # targeting remains policy-independent by construction.
        for _ in C.AMBIENT_STEPS:
            ev = rb.choice(C.AMBIENT_EVENTS)
            attr = 1 if ev == "draft-heat" else 2   # a2 for heat, a3 for soak
            if leak == "ambient":   # PL3: targeting becomes a hard kind label
                # planted on K_OLD, a common kind under the rule-derived
                # marginals (the original fixture targeted B, which the
                # derived holdout makes rare — a silent fixture tests nothing)
                positives = [i for i in range(C.N_OBJ)
                             if kinds[i] == C.K_OLD]
                bias = 1.0
            else:
                positives = [i for i in range(C.N_OBJ)
                             if kinds[i][attr] == 1 and i not in hit]
                if not positives:
                    positives = [i for i in range(C.N_OBJ)
                                 if kinds[i][attr] == 1]
                bias = C.AMBIENT_BIAS
            if positives and rb.random() < bias:
                tgt = rb.choice(positives)
            else:
                tgt = rb.randrange(C.N_OBJ)
            hit.add(tgt)
            ambient.append((ev, tgt))
        # scored-query designs: (action, latent indices)
        queries = []
        for _ in C.SCORED_STEPS:
            act = rq.choice(C.ACTIONS)
            if act == "grind":
                i = rq.randrange(C.N_OBJ)
                j = rq.randrange(C.N_OBJ - 1)
                if j >= i:
                    j += 1
                queries.append((act, (i, j)))
            else:
                queries.append((act, (rq.randrange(C.N_OBJ),)))
        corpus.append({
            "episode": ep, "kinds": kinds, "appearance": appearance,
            "perm": perm, "arrival": arrival, "ambient": ambient,
            "queries": queries,
        })
    _force_first_cooccurrence_queries(corpus)
    return corpus


FC_QUERY_INDEX = 4   # primary hypothetical slot: scored step 19 (late enough
# that identification is feasible — at step 3 even oracle-with-identification
# scored 0.083 and the stratum measured identification, not composition).
HYP_SLOTS = (4, 2, 6)   # slot priority = scored steps 19, 11, 23 (P003 C3)
HYP_CAP = 24            # per-cell target, equalized (P003 Condition 3;
# re-frozen under PREREGISTRATION_003 — was 12 with one slot per episode.
# Up to three hypothetical slots per qualifying episode until the cell
# reaches target; intra-episode repeats share membership-state evolution and
# are declared correlated trials, reported with episode counts alongside.)


def _force_first_cooccurrence_queries(corpus):
    """Post-E_R, episodes where a held-out cell co-occurs get HYPOTHETICAL
    grind queries on that pair (stated-pristine, scored-not-executed, never
    revealed) at up to three scored slots, until the cell reaches HYP_CAP
    queries.  Executed transfer queries proved doubly confounded — wet
    objects collapse to the trivial soaked-null, and executing the query
    hands the memorizer the very datum the stratum is supposed to
    withhold."""
    seen = {}       # cell -> hypothetical queries scheduled
    eps = {}        # cell -> qualifying episodes used
    for epi in corpus:
        if epi["episode"] < C.E_R:
            continue
        kinds = epi["kinds"]
        found = None
        for i in range(C.N_OBJ):
            for j in range(i + 1, C.N_OBJ):
                cell = frozenset({kinds[i], kinds[j]})
                if (cell in C.HOLDOUT_PAIRS
                        and seen.get(cell, 0) < HYP_CAP):
                    found = (cell, i, j)
                    break
            if found:
                break
        if not found:
            continue
        cell, i, j = found
        n_slots = min(len(HYP_SLOTS), HYP_CAP - seen.get(cell, 0))
        for slot in HYP_SLOTS[:n_slots]:
            epi["queries"][slot] = ("grind", (i, j), True)
        seen[cell] = seen.get(cell, 0) + n_slots
        eps[cell] = eps.get(cell, 0) + 1
        epi["first_cooc"] = tuple(sorted(cell))
        epi["first_cooc_rank"] = eps[cell]


def corpus_digest(corpus):
    import hashlib, json
    blob = json.dumps(corpus, sort_keys=True, default=list).encode()
    return hashlib.sha256(blob).hexdigest()
