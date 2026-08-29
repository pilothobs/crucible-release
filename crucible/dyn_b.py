"""CRUCIBLE dynamics, implementation B.

Independent re-implementation of the frozen semantics in dyn_a's docstring,
written as explicit conditional logic with no shared tables or helpers.
tracecheck.py requires byte agreement with implementation A on every cell and
on full corpus traces before anything else may run (spec 10, CPL rule 1.1).
"""


def f1(alpha, cond, action):
    hardness, volatility, solubility = alpha

    if action == "tap":
        if cond == "cracked":
            if hardness == 1:
                return "crumble", "cracked"
            return "shatter", "cracked"
        if cond == "soaked":
            return "thud", "pristine"
        if hardness == 1:
            if volatility == 1:
                return "shatter", cond
            return "ring", cond
        if volatility == 1:
            return "crumble", cond
        return "thud", cond

    if action == "heat":
        if cond == "soaked":
            return "hiss", "pristine"
        if cond == "charred":
            return "null", "charred"
        # pristine or cracked share outcome symbols; cracked never transitions
        if volatility == 1:
            out = "ignite"
        elif hardness == 0:
            out = "melt"
        else:
            out = "null"
        if cond == "cracked":
            return out, "cracked"
        if volatility == 1:
            return out, "charred"
        return out, "pristine"

    if action == "soak":
        if cond == "soaked":
            return "null", "soaked"
        out = "hiss" if solubility == 1 else "null"
        if cond == "cracked":
            return out, "cracked"
        return out, "soaked"

    raise ValueError("unknown action: %r" % (action,))


def f2(alpha_i, alpha_j, cond_i, cond_j):
    if "soaked" in (cond_i, cond_j):
        return "null"
    both_hard = (alpha_i[0] == 1 and alpha_j[0] == 1)
    sol_differ = (alpha_i[2] != alpha_j[2])
    if both_hard and sol_differ:
        return "repel"
    if both_hard:
        return "shatter"
    if sol_differ:
        return "fuse"
    return "crumble"
