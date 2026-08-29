"""Concept library + library-induced predictor (spec 4.2-4.4, v0.3).

Substrate-owned.  The learner has no prediction channel (spec 4.1): every
prediction is computed here from admitted concepts, current memberships and
attributions.  Rank semantics (v0.4, by A16 check-1 arithmetic): level B =
ALL non-default rules (P2/P3/P5/P6/P9/P10 and P7-attached alike — P7's v0.2
rank privilege made the CondClass shadow cheaper than the designed body-edit,
so it was removed and P7 is now a genuine decoy); level C = P8 defaults;
cond_pattern narrowness confers no rank; conflicting outcomes in the deciding
level -> unresolved.
"""
import math
from . import constants as C
from . import grammar as G

_OPS = {"and": lambda x, y: x & y, "or": lambda x, y: x | y,
        "xor": lambda x, y: x ^ y, "eq": lambda x, y: 1 - (x ^ y)}


class Library:
    def __init__(self):
        self.concepts = {}          # cid -> concept record
        self.order = []             # insertion order of cids
        self.attributions = {}      # (class_cid, attr_cid) -> 0/1
        self.next_id = 1
        self.rules_by_cls = {}      # (action, class_cid) -> [cid]
        self.rules_free = {}        # action -> [cid], class-free rules
        self.p10_ids = []           # P10 CountClass concepts
        self.model_bits = 0.0       # cumulative description charges

    # ---- structure queries -------------------------------------------------
    def n_classes(self):
        return sum(1 for c in self.concepts.values()
                   if c["term"]["p"] in ("P1", "P7", "P10"))

    def n_attrs(self):
        return sum(1 for c in self.concepts.values() if c["term"]["p"] == "P4")

    def counts_for_costs(self):
        return self.n_classes(), self.n_attrs(), max(1, len(self.concepts))

    # ---- mutation (engine-mediated only) -----------------------------------
    def _index_rule(self, cid, term):
        p = term["p"]
        act = term.get("action", "grind")
        if p == "P2":
            host = self.concepts.get(term["cls"])
            if host is not None and host["term"]["p"] == "P1":
                self.rules_by_cls.setdefault((act, term["cls"]),
                                             []).append(cid)
                return
            self.rules_free.setdefault(act, []).append(cid)
        elif p == "P3":
            for key in {term["c1"], term["c2"]}:
                self.rules_by_cls.setdefault(("grind", key), []).append(cid)
        elif p in ("P5", "P6", "P8", "P9"):
            self.rules_free.setdefault(act, []).append(cid)

    def _unindex_rule(self, cid):
        for d in (self.rules_by_cls, self.rules_free):
            for lst in d.values():
                if cid in lst:
                    lst.remove(cid)

    def new_concept(self, term, ep, dmdl=None):
        cid = "k%d" % self.next_id
        self.next_id += 1
        rec = {"id": cid, "term": dict(term), "admitted_ep": ep,
               "admission_dmdl": dmdl, "revisions": [], "violations": []}
        self.concepts[cid] = rec
        self.order.append(cid)
        if term["p"] in ("P2", "P3", "P5", "P6", "P8", "P9"):
            self._index_rule(cid, term)
        elif term["p"] == "P10":
            self.p10_ids.append(cid)
        return cid

    def revise(self, cid, slot, value, ep, cites):
        rec = self.concepts[cid]
        old = rec["term"].get(slot)
        rec["term"][slot] = value
        rec["revisions"].append({"ep": ep, "slot": slot, "old": old,
                                 "new": value, "cites": list(cites)})
        if slot in ("cls", "c1", "c2", "action"):
            self._unindex_rule(cid)
            if rec["term"]["p"] in ("P2", "P3", "P5", "P6", "P8", "P9"):
                self._index_rule(cid, rec["term"])

    def retire(self, cid):
        rec = self.concepts.pop(cid)
        self.order.remove(cid)
        self._unindex_rule(cid)
        if cid in self.p10_ids:
            self.p10_ids.remove(cid)
        for key in [k for k in self.attributions if cid in k]:
            del self.attributions[key]
        return rec

    # ---- expression evaluation --------------------------------------------
    def _attr(self, class_cid, attr_cid, excluded):
        if attr_cid in excluded or class_cid in excluded:
            return None
        return self.attributions.get((class_cid, attr_cid))

    def _unary_expr_ok(self, expr, class_cid, excluded):
        if expr is None:
            return True
        lits = expr if isinstance(expr, list) else [expr]
        for (_tag, attr_cid, sign) in lits:
            v = self._attr(class_cid, attr_cid, excluded)
            if v is None or v != sign:
                return False
        return True

    def _pair_expr_ok(self, expr, ci, cj, excluded):
        if expr is None:
            return True
        cmps = expr if isinstance(expr, list) else [expr]
        for (_tag, op, a1, a2, neg) in cmps:
            x = self._attr(ci, a1, excluded)
            y = self._attr(cj, a2, excluded)
            if x is None or y is None:
                return False
            if (_OPS[op](x, y) ^ neg) != 1:
                return False
        return True

    # ---- applicability -----------------------------------------------------
    @staticmethod
    def _cond_ok(pat, cond):
        return pat is None or cond in pat

    @staticmethod
    def _pair_cond_ok(pat, ci_cond, cj_cond):
        if pat is None:
            return True
        quant, mask = pat
        inside = (ci_cond in mask, cj_cond in mask)
        return all(inside) if quant == "both" else any(inside)

    def _memberships(self, view, excluded):
        base = [c for c in view["members"] if c not in excluded]
        # P10 CountClass auto-membership (substrate-derived from counts)
        for cid in self.p10_ids:
            if cid in excluded:
                continue
            t = self.concepts[cid]["term"]
            if view["counts"].get(t["action"], 0) >= t["theta"]:
                base.append(cid)
        return base

    def _candidates(self, action, views, excluded):
        cand = list(self.rules_free.get(action, ()))
        seen = set(cand)
        for v in views:
            for m in self._memberships(v, excluded):
                for cid in self.rules_by_cls.get((action, m), ()):
                    if cid not in seen:
                        seen.add(cid)
                        cand.append(cid)
        return cand

    def predict(self, action, views, excluded=frozenset()):
        """views: list of per-object dicts {token, cond, members, counts, prev}
        Returns (resolved, outcome|None, deciding_rule_ids)."""
        levels = {"B": [], "C": []}
        cand = self._candidates(action, views, excluded)
        for cid in cand:
            if cid in excluded:
                continue
            t = self.concepts[cid]["term"]
            p = t["p"]
            if p == "P8":
                levels["C"].append((cid, t["out"]))
                continue
            if action == "grind":
                if p not in ("P3", "P6"):
                    continue
                v1, v2 = views
                if not self._pair_cond_ok(t.get("cond"), v1["cond"], v2["cond"]):
                    continue
                m1 = self._memberships(v1, excluded)
                m2 = self._memberships(v2, excluded)
                ok = False
                if p == "P3":
                    orders = [(t["c1"], t["c2"])]
                    if t.get("mode", "sym") == "sym":
                        orders.append((t["c2"], t["c1"]))
                    for (r1, r2) in orders:
                        if r1 in m1 and r2 in m2:
                            ok = True
                else:  # P6
                    pairs = [(ci, cj) for ci in m1 for cj in m2]
                    if t.get("mode", "sym") == "sym":
                        pairs += [(cj, ci) for ci in m1 for cj in m2]
                    if t["expr"] is None:
                        ok = True
                    else:
                        ok = any(self._pair_expr_ok(t["expr"], ci, cj, excluded)
                                 for ci, cj in pairs)
                if ok:
                    levels["B"].append((cid, t["out"]))
                continue
            # unary rules
            view = views[0]
            if p == "P2":
                cls = t["cls"]
                if cls in excluded:
                    continue
                host = self.concepts.get(cls)
                if host is None:
                    continue
                if host["term"]["p"] == "P7":   # refinement-attached: rank B
                    base_cls = host["term"]["cls"]
                    if (base_cls not in excluded
                            and base_cls in self._memberships(view, excluded)
                            and view["cond"] == host["term"]["cond"]
                            and self._cond_ok(t.get("cond"), view["cond"])):
                        levels["B"].append((cid, t["out"]))
                    continue
                if (cls in self._memberships(view, excluded)
                        and self._cond_ok(t.get("cond"), view["cond"])):
                    levels["B"].append((cid, t["out"]))
            elif p == "P5":
                if not self._cond_ok(t.get("cond"), view["cond"]):
                    continue
                if t["expr"] is None:
                    levels["B"].append((cid, t["out"]))
                elif any(self._unary_expr_ok(t["expr"], m, excluded)
                         for m in self._memberships(view, excluded)):
                    levels["B"].append((cid, t["out"]))
            elif p == "P9":
                prev = t["prev"]
                if prev is not None and view["prev"] != tuple(prev):
                    continue
                if not self._cond_ok(t.get("cond"), view["cond"]):
                    continue
                if "cls" in t:
                    if t["cls"] in self._memberships(view, excluded):
                        levels["B"].append((cid, t["out"]))
                else:
                    if t["expr"] is None or any(
                            self._unary_expr_ok(t["expr"], m, excluded)
                            for m in self._memberships(view, excluded)):
                        levels["B"].append((cid, t["out"]))
        for lvl in ("B", "C"):
            if levels[lvl]:
                outs = {o for _, o in levels[lvl]}
                ids = [cid for cid, _ in levels[lvl]]
                if len(outs) == 1:
                    return True, next(iter(outs)), ids
                return False, None, ids       # same-rank conflict -> unresolved
        return False, None, []

    def code_bits(self, resolved, predicted, outcome):
        if resolved:
            p = (1 - C.EPSILON) if predicted == outcome else C.EPSILON / 10
        else:
            p = 1.0 / len(C.OUTCOMES)
        return -math.log2(p)
