"""CRUCIBLE v0.1 frozen constants (spec L3_0_SPEC.md v0.3).

Every value here is a literal (programme rule: never derive seeds from hash()).
Frozen at the L3-1 gate by manifest digest of this file.
"""

# ---- observable alphabets (spec 2.1) -------------------------------------
CONDITIONS = ("pristine", "charred", "soaked", "cracked")
PRISTINE, CHARRED, SOAKED, CRACKED = CONDITIONS

OUTCOMES = ("thud", "ring", "crumble", "melt", "ignite", "hiss",
            "fuse", "repel", "shatter", "dissolve", "null")

UNARY_ACTIONS = ("tap", "heat", "soak")
BINARY_ACTIONS = ("grind",)
ACTIONS = UNARY_ACTIONS + BINARY_ACTIONS

AMBIENT_EVENTS = ("draft-heat", "rain-soak")   # ambient applications of heat / soak
AMBIENT_ACTION = {"draft-heat": "heat", "rain-soak": "soak"}

APPEARANCE_FEATURES = 3
APPEARANCE_VALUES = 5          # each feature in 0..4, iid uniform, kind-independent

# ---- latent structure (spec 2.2), generator-internal ----------------------
# attribute vector (a1, a2, a3); gloss: hardness, volatility, solubility
K0 = (
    (0, 0, 0),   # kind A  (k_old for the E_R split)
    (0, 1, 1),   # kind B
    (1, 0, 1),   # kind C
    (1, 1, 0),   # kind D
    (0, 1, 0),   # kind E
)
K_NEW = (0, 0, 1)   # matches A on (a1,a2), differs on a3; enters at E_R
K_OLD = (0, 0, 0)

# selection checks (spec 2.2 constraints) are asserted in gen.py at import.

# ---- schedule (spec 2.4, R6; T grown 24 -> 32 by A16 check-4 arithmetic:
# at T=24 the honest per-object rent margin was ~0.4 bits, inside noise) -----
N_OBJ = 5
T_STEPS = 32
SCORED_STEPS = (3, 7, 11, 15, 19, 23, 27, 31)   # 8 dedicated scored steps
AMBIENT_STEPS = (6, 14, 22, 30)                 # 4 ambient steps: more than
# ~4 saturates the attribute-positive targets (repeat hits go null) and
# washes out the declared confound — audit A7 caught exactly that
# remaining 20 steps are learner-chosen

EPISODES = 600
E_C = 300          # first episode with weathered (cracked) arrivals
E_R = 400          # first episode with k_new and open holdout cells
CRACK_P = 0.2      # weathered-arrival probability per object, episodes >= E_C

# kind sampling weights.  Pre-E_R draws are iid-with-rejection (holdout
# enforcement), which skews the EFFECTIVE marginals (kinds in more holdout
# cells are rejected more; under the rule-derived holdout, B sits in three
# cells): measured at seed 555001, N=200k episodes under HOLDOUT_PAIRS —
# A .3009, B .0330, C .3007, D .1985, E .1669.  Post-E_R weights are those
# measured marginals scaled by the non-k_new share, so the K0 marginal is
# CONTINUOUS at E_R and carries no side-channel beacon (audit A6 caught the
# jump when post weights were naively uniform).
KIND_W_PRE = {k: 0.2 for k in K0}                       # episodes < E_R
KIND_W_POST = {
    (0, 0, 0): 0.2257, (0, 1, 1): 0.0247, (1, 0, 1): 0.2255,
    (1, 1, 0): 0.1489, (0, 1, 0): 0.1252, K_NEW: 0.25,
}

AMBIENT_BIAS = 0.75   # probability the ambient event targets an attribute-positive object

# ---- co-occurrence holdout (spec 2.5, v0.4: selected BY RULE from a
# literal seed, not by hand — the T12 discipline: the constraint rule is
# stated first and the seed is drawn under it, accepting whatever comes out).
#
# Candidate space: the 10 unordered cross-kind K0 cells.  A 4-subset is
# ELIGIBLE iff all of:
#   H1 connectivity: every F2 region (c1, c2) retains >= 1 visible cell
#      (cross-kind or same-kind) pre-shift, so the factoring is identifiable;
#   H2 no-beacon (T8): every outcome reachable in a held-out cell is
#      reachable in some visible cell pre-shift;
#   H3 balance: no single outcome accounts for more than 2 of the 4 held-out
#      cells, so the transfer stratum is not majority-guessable (the first
#      hand-drafted holdout had 3/4 fuse cells and a majority-guess control
#      hit 0.833 on the stratum — audit A1's catch);
#   H4 split-family contact: at least one held-out cell contains K_OLD, so
#      the transfer test touches the family the E_R split concerns.
# Eligible subsets are ordered canonically and the choice is
# eligible[SEED_HOLDOUT % len(eligible)].  The F2 region map is duplicated
# here from the frozen dynamics; gen.py asserts the duplicate agrees with
# dyn_a cell-for-cell at import.
SEED_HOLDOUT = 731007
_F2_REGION = {(0, 0): "crumble", (0, 1): "fuse",
              (1, 0): "shatter", (1, 1): "repel"}


def _pristine_pair_outcome(a, b):
    return _F2_REGION[(a[0] & b[0], a[2] ^ b[2])]


def _derive_holdout():
    import itertools
    cross = sorted((tuple(sorted((a, b))) for i, a in enumerate(K0)
                    for b in K0[i + 1:]))
    same_regions = {(k[0] & k[0], 0) for k in K0}
    same_outs = {_pristine_pair_outcome(k, k) for k in K0}
    eligible = []
    for combo in itertools.combinations(cross, 4):
        held = set(combo)
        vis = [c for c in cross if c not in held]
        vis_regions = {(a[0] & b[0], a[2] ^ b[2]) for a, b in vis} \
            | same_regions
        if vis_regions != {(0, 0), (0, 1), (1, 0), (1, 1)}:
            continue                                        # H1
        vis_outs = {_pristine_pair_outcome(a, b) for a, b in vis} | same_outs
        held_outs = [_pristine_pair_outcome(a, b) for a, b in combo]
        if not set(held_outs) <= vis_outs:
            continue                                        # H2
        if max(held_outs.count(o) for o in set(held_outs)) > 2:
            continue                                        # H3
        if not any(K_OLD in c for c in combo):
            continue                                        # H4
        eligible.append(combo)
    eligible.sort()
    pick = eligible[SEED_HOLDOUT % len(eligible)]
    return tuple(frozenset(c) for c in pick), len(eligible)


HOLDOUT_PAIRS, N_ELIGIBLE_HOLDOUTS = _derive_holdout()
FIRST_COOC_FORCED = 5   # retained for reference; superseded by HYP_CAP in
# gen.py (hypothetical transfer queries, spec v0.4 D7)

# ---- literal RNG stream seeds (spec T9: one named stream per channel) ------
SEED_KIND = 731001
SEED_APPEARANCE = 731002
SEED_TOKEN = 731003
SEED_AMBIENT = 731004
SEED_ARRIVAL = 731005
SEED_QUERY = 731006
EVAL_SEEDS = (17, 18, 19)     # literal evaluation-stream seeds (offsets all streams)

# ---- MDL (spec 2.3 / 4.5) --------------------------------------------------
EPSILON = 1e-3
