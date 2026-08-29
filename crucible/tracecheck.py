"""Dual-implementation cross-check (spec 10): dyn_a and dyn_b must agree
byte-for-byte on every reachable cell and on a full corpus trace before
anything else runs.  Disagreement is a hard stop (CPL rule 1.1)."""
import itertools
from . import constants as C
from . import dyn_a, dyn_b
from .gen import generate_corpus


def check_cells():
    kinds = list(C.K0) + [C.K_NEW]
    n = 0
    for alpha in itertools.product((0, 1), repeat=3):
        for cond in C.CONDITIONS:
            for act in C.UNARY_ACTIONS:
                ra, rb = dyn_a.f1(alpha, cond, act), dyn_b.f1(alpha, cond, act)
                assert ra == rb, (alpha, cond, act, ra, rb)
                assert ra[0] in C.OUTCOMES and ra[1] in C.CONDITIONS
                assert ra[1] != "cracked" or cond == "cracked", \
                    "cracked produced by transition"
                n += 1
    for ka, kb in itertools.product(kinds, repeat=2):
        for ca, cb in itertools.product(C.CONDITIONS, repeat=2):
            ra = dyn_a.f2(ka, kb, ca, cb)
            rb = dyn_b.f2(ka, kb, ca, cb)
            assert ra == rb, (ka, kb, ca, cb, ra, rb)
            assert ra == dyn_a.f2(kb, ka, cb, ca), "F2 not symmetric"
            n += 1
    return n


def check_trace(eval_seed=C.EVAL_SEEDS[0], episodes=60):
    """Replay a corpus prefix through both implementations event-for-event."""
    import random
    corpus = generate_corpus(eval_seed, episodes=episodes)
    rng = random.Random(4242)
    mismatches = 0
    n_events = 0
    for epi in corpus:
        conds_a = list(epi["arrival"])
        conds_b = list(epi["arrival"])
        for step in range(C.T_STEPS):
            i = rng.randrange(C.N_OBJ)
            act = rng.choice(C.ACTIONS)
            if act == "grind":
                j = (i + 1 + rng.randrange(C.N_OBJ - 1)) % C.N_OBJ
                oa = dyn_a.f2(epi["kinds"][i], epi["kinds"][j],
                              conds_a[i], conds_a[j])
                ob = dyn_b.f2(epi["kinds"][i], epi["kinds"][j],
                              conds_b[i], conds_b[j])
                if oa != ob:
                    mismatches += 1
            else:
                oa, na = dyn_a.f1(epi["kinds"][i], conds_a[i], act)
                ob, nb = dyn_b.f1(epi["kinds"][i], conds_b[i], act)
                if (oa, na) != (ob, nb):
                    mismatches += 1
                conds_a[i], conds_b[i] = na, nb
            n_events += 1
    assert mismatches == 0, mismatches
    return n_events


if __name__ == "__main__":
    cells = check_cells()
    events = check_trace()
    print("tracecheck PASS: %d cells, %d trace events, 0 mismatches"
          % (cells, events))
