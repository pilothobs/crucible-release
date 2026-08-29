"""Meta-grammar (spec 4.3, v0.3) and MDL spelling costs (spec 4.5).

Terms are dicts with a 'p' production tag.  Costs are derived mechanically
from declared alphabet sizes; no per-production hand prices (T11).

Productions: P1 Class, P2 URule, P3 PRule, P4 Attr, P5 AURule, P6 APRule,
P7 CondClass, P8 Default, P9 HRule, P10 CountClass.
Initial concept-kind set: {P1, P2, P3, P8}.

Pair cond_patterns carry a quantifier (both/either) over a condition mask —
declared here as the build-level completion of the spec's cond_pattern shape.
Unary/pair attr_exprs allow a conjunction of at most two literals/comparisons.
"""
import math
from . import constants as C

LOG2 = math.log2
N_OPS = 6            # NEW, REVISE, RETIRE, member+, member-, attribution
N_PROD = 10
OP_COST = LOG2(N_OPS)
PROD_COST = LOG2(N_PROD)
ACTION_COST = LOG2(len(C.ACTIONS))
OUTCOME_COST = LOG2(len(C.OUTCOMES))
COND_COST = LOG2(len(C.CONDITIONS))
INITIAL_PRODUCTIONS = ("P1", "P2", "P3", "P8")

PRICE_TWEAK = {"rule_bonus": 0.0}   # audit A13 sensitivity hook only


def elias_gamma(n):
    assert n >= 1
    return 2 * math.floor(LOG2(n)) + 1


def ref_cost(table_size):
    return LOG2(max(2, table_size))


def cond_pattern_cost(pat):
    # unary: None (wild, 1 bit) or a condition mask (1 + 4 bits)
    return 1.0 if pat is None else 1.0 + len(C.CONDITIONS)


def pair_cond_pattern_cost(pat):
    # None (wild, 1 bit) or (quant in {both, either}, mask): 1 + 1 + 4 bits
    return 1.0 if pat is None else 2.0 + len(C.CONDITIONS)


def unary_expr_cost(expr, n_attrs):
    # None (any): 1 bit.  Else 1 + conj bit + per literal (attr ref + sign).
    if expr is None:
        return 1.0
    lits = expr if isinstance(expr, list) else [expr]
    return 2.0 + sum(ref_cost(n_attrs) + 1.0 for _ in lits)


def pair_expr_cost(expr, n_attrs):
    # None (any): 1 bit.  Else 1 + conj bit + per comparison
    # (op in {and,or,xor,eq}: 2 bits) + two attr refs + neg bit.
    if expr is None:
        return 1.0
    cmps = expr if isinstance(expr, list) else [expr]
    return 2.0 + sum(2.0 + 2 * ref_cost(n_attrs) + 1.0 for _ in cmps)


def newcond_cost(nc):
    return 1.0 if nc is None else 1.0 + COND_COST


def spelling_cost(term, n_classes, n_attrs, n_concepts):
    p = term["p"]
    c = PROD_COST
    if p == "P1":
        pass
    elif p == "P2":
        c += (ref_cost(n_classes) + cond_pattern_cost(term["cond"]) +
              ACTION_COST + OUTCOME_COST + newcond_cost(term.get("newcond")))
        c += PRICE_TWEAK["rule_bonus"]
    elif p == "P3":
        c += (2 * ref_cost(n_classes) + 1.0 +  # mode bit
              pair_cond_pattern_cost(term["cond"]) + OUTCOME_COST)
        c += PRICE_TWEAK["rule_bonus"]
    elif p == "P4":
        pass
    elif p == "P5":
        c += (unary_expr_cost(term["expr"], n_attrs) +
              cond_pattern_cost(term["cond"]) + ACTION_COST + OUTCOME_COST +
              newcond_cost(term.get("newcond")))
        c += PRICE_TWEAK["rule_bonus"]
    elif p == "P6":
        c += (pair_expr_cost(term["expr"], n_attrs) + 1.0 +
              pair_cond_pattern_cost(term["cond"]) + OUTCOME_COST)
        c += PRICE_TWEAK["rule_bonus"]
    elif p == "P7":
        c += ref_cost(n_classes) + COND_COST
    elif p == "P8":
        c += ACTION_COST + OUTCOME_COST
    elif p == "P9":
        prev = term["prev"]           # None or (action, outcome)
        c += 1.0 + (0.0 if prev is None else ACTION_COST + OUTCOME_COST)
        c += 1.0    # cls-vs-expr selector bit
        c += (ref_cost(n_classes) if "cls" in term
              else unary_expr_cost(term["expr"], n_attrs))
        c += ACTION_COST + OUTCOME_COST + cond_pattern_cost(term.get("cond"))
    elif p == "P10":
        c += ACTION_COST + elias_gamma(term["theta"])
    else:
        raise ValueError(p)
    return c


SLOTS = {  # editable slots per production, for REVISE slot selectors
    "P2": ("cls", "cond", "action", "out", "newcond"),
    "P3": ("c1", "c2", "mode", "cond", "out"),
    "P5": ("expr", "cond", "action", "out", "newcond"),
    "P6": ("expr", "mode", "cond", "out"),
    "P7": ("cls", "cond"),
    "P8": ("action", "out"),
    "P9": ("prev", "cls", "action", "out", "cond"),
    "P10": ("action", "theta"),
}


def slot_value_cost(prod, slot, value, n_classes, n_attrs):
    if slot in ("cls", "c1", "c2"):
        return ref_cost(n_classes)
    if slot == "cond":
        return (pair_cond_pattern_cost(value) if prod in ("P3", "P6")
                else cond_pattern_cost(value))
    if slot == "action":
        return ACTION_COST
    if slot == "out":
        return OUTCOME_COST
    if slot == "newcond":
        return newcond_cost(value)
    if slot == "mode":
        return 1.0
    if slot == "expr":
        return (pair_expr_cost(value, n_attrs) if prod == "P6"
                else unary_expr_cost(value, n_attrs))
    if slot == "prev":
        return 1.0 + (0.0 if value is None else ACTION_COST + OUTCOME_COST)
    if slot == "theta":
        return elias_gamma(value)
    raise ValueError((prod, slot))


def member_cost(n_classes):
    return OP_COST + LOG2(C.N_OBJ) + ref_cost(n_classes)


def attribution_cost(n_classes, n_attrs):
    return OP_COST + ref_cost(n_classes) + ref_cost(n_attrs) + 1.0


def new_cost(term, n_classes, n_attrs, n_concepts):
    return OP_COST + spelling_cost(term, n_classes, n_attrs, n_concepts)


def revise_cost(prod, slot, value, n_concepts, n_classes, n_attrs):
    c = (OP_COST + ref_cost(n_concepts) + ref_cost(len(SLOTS[prod])) +
         slot_value_cost(prod, slot, value, n_classes, n_attrs))
    return c


def retire_cost(n_concepts):
    return OP_COST + ref_cost(n_concepts)
