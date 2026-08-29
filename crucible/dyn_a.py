"""CRUCIBLE dynamics, implementation A (table-driven).

F1(alpha, condition, action) -> (outcome, condition'), deterministic.
F2(alpha_i, alpha_j, cond_i, cond_j) -> outcome, symmetric, deterministic.

Structure constraints (spec 2.3, frozen):
  - tap and heat read only (a1, a2); soak reads only a3.
  - no transition ever produces `cracked` (arrival-only condition, spec 2.6).
  - `cracked` is absorbing: no transition leaves it.
  - only tap behaves differently on cracked objects (the designed E_C cells);
    heat and soak give the same outcome symbols on cracked as on pristine.
  - F2 is symmetric and depends on the pair only through the comparisons
    c1 = a1 AND a1',  c2 = a3 XOR a3'  (plus the soaked guard).

Implementation B (dyn_b.py) re-implements the same frozen semantics
independently in a different style; tracecheck.py requires byte agreement.
"""
from .constants import PRISTINE, CHARRED, SOAKED, CRACKED

# tap outcome by (a1, a2); cracked variant differs for every vector
# (audit A2 found the original a1-only tap made majority-guessing too strong)
_TAP_NORMAL = {(0, 0): "thud", (0, 1): "crumble",
               (1, 0): "ring", (1, 1): "shatter"}
_TAP_CRACKED = {0: "shatter", 1: "crumble"}   # by a1; differs from normal
# for every (a1, a2): thud/crumble -> shatter, ring/shatter -> crumble

# heat outcome by (a1, a2) on pristine-like conditions
_HEAT_BASE = {(0, 0): "melt", (1, 0): "null", (0, 1): "ignite", (1, 1): "ignite"}

_SOAK = {0: "null", 1: "hiss"}

# F2 region table over (c1, c2)
_F2 = {(0, 0): "crumble", (0, 1): "fuse", (1, 0): "shatter", (1, 1): "repel"}


def f1(alpha, cond, action):
    a1, a2, a3 = alpha
    if action == "tap":
        if cond == CRACKED:
            return _TAP_CRACKED[a1], CRACKED
        if cond == SOAKED:
            # percussive dry-off: soaked is transient, else the world's
            # steady state under exploration is "everything is wet" and
            # the ambient confound drowns in nulls (audit A7)
            return "thud", PRISTINE
        return _TAP_NORMAL[(a1, a2)], cond
    if action == "heat":
        if cond == CRACKED:
            return _HEAT_BASE[(a1, a2)], CRACKED
        if cond == SOAKED:
            return "hiss", PRISTINE
        if cond == CHARRED:
            return "null", CHARRED
        # pristine
        out = _HEAT_BASE[(a1, a2)]
        return out, (CHARRED if a2 == 1 else PRISTINE)
    if action == "soak":
        if cond == CRACKED:
            return _SOAK[a3], CRACKED
        if cond == SOAKED:
            return "null", SOAKED
        return _SOAK[a3], SOAKED
    raise ValueError(action)


def f2(alpha_i, alpha_j, cond_i, cond_j):
    if cond_i == SOAKED or cond_j == SOAKED:
        return "null"
    c1 = alpha_i[0] & alpha_j[0]
    c2 = alpha_i[2] ^ alpha_j[2]
    return _F2[(c1, c2)]
