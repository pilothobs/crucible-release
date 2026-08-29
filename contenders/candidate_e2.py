"""Candidate E.2 — EXP2 contender (PREREGISTRATION_L35_EXP2).

Candidate E's frozen machinery plus two evidence-use changes, no budget
change (EXP2 section 2), targeting the measured steady-state abstention
(dev 998 decomposition: ~146 soaked-pair queries with no covering rule
ever; ~150 partner-unidentified pairs and ~153 unidentified-object unary
queries dominated by per-episode identification latency):

M1 — soaked-pair guard.  Candidate E discards soaked-grind observations
outright; the reference resolves every soaked pair.  E.2 records them as
condition-level evidence and, once support is unanimous (>= 3 events,
single outcome), proposes ONE P6 rule with an empty expression and pair
condition ("either", {soaked}) — exactly the observed regularity: any
grind involving a soaked participant yields that outcome.  The rule is
membership-free, conflicts with nothing (the adopted attr pair rules
exclude soaked), and is kept out of the aprule mirror so pair
exploration is unaffected (its emit kind, "guard", is a no-op in the
inherited batch_result).

M2 — two-probe identification.  Probe order (tap, soak, heat) instead of
(tap, heat, soak): the published F1 structure reads (a1, a2) through tap
and a3 through soak, so tap+soak determine the full attribute vector and
ANY kind not yet known must conflict on one of them.  Tier-1.5 asserts
after those two probes when exactly one class fits every observed cell
perfectly and every other class conflicts; otherwise the full signature
(and genesis for novel kinds, unchanged tuple order) proceeds as in E.
One learner step saved per object per episode moves identification ahead
of the early query steps.  (A two-cell assert off tap+heat would be
UNSAFE — kinds differing only in a3 are tap+heat twins, the E-era churn
trap — which is why the reorder and the assert come together.)

The signature capture masks are identical to E's (tap@DRY, soak@DRY,
heat@pristine), so the inherited capture, tier-1 mapping, and genesis
keying are reused untouched; only the PROBE ORDER and the early-assert
pass are new.
"""
import sys

sys.path.insert(0, ".")
from crucible import constants as C
from l3_5.candidate_e import CandidateE, P, CH, SO, CR, DRY

PROBE_ORDER = (("tap", DRY), ("soak", DRY), ("heat", frozenset({P})))
GUARD_SUPPORT = 3


class CandidateE2(CandidateE):

    # ------------------------------------------------------------- M1
    def begin_run(self):
        super().begin_run()
        self._soak_grind = {}
        self._guard_cid = None
        self._guard_inflight = False

    def observe(self, event):
        if event["action"] == "grind":
            t1, t2 = event["tokens"]
            if SO in (self.conds.get(t1), self.conds.get(t2)):
                out = event["outcome"]
                self._soak_grind[out] = self._soak_grind.get(out, 0) + 1
        super().observe(event)

    def _growth_batch(self):
        # the guard rides its own single-op batch (the swap queue), so a
        # rejected growth batch cannot take it down atomically; adoption
        # is confirmed in batch_result and retried until admitted
        if self._guard_cid is None and not self._guard_inflight \
                and len(self._soak_grind) == 1 \
                and sum(self._soak_grind.values()) >= GUARD_SUPPORT:
            out = next(iter(self._soak_grind))
            op = ("new", {"p": "P6", "expr": None, "mode": "sym",
                          "cond": ("either", frozenset({SO})),
                          "out": out})
            self._swap_queue.append(([op], {}, [("guard", out)]))
            self._guard_inflight = True
        return super()._growth_batch()

    def batch_result(self, idx, accepted, dmdl, new_ids):
        if self._emit_queues:
            for entry, cid in zip(self._emit_queues[0], new_ids):
                if entry[0] == "guard":
                    if accepted and cid:
                        self._guard_cid = cid
                    self._guard_inflight = False
        super().batch_result(idx, accepted, dmdl, new_ids)

    # ------------------------------------------------------------- M2
    def _maybe_assert(self):
        # tier 1.5: two-probe assert once tap+soak are both captured —
        # unique perfect fit on all observed cells, every other class
        # conflicted.  Cracked objects keep the cohort machinery.
        # (A 2-cell cracked assert against mapped cohort signatures was
        # built and MEASURED OUT in development: it raises raw accuracy
        # but routes cracked resolution through class rules, thinning the
        # attribute composite's ablation margin below delta_b — better
        # world performance at the price of the certified unit's
        # load-bearing.  Dev 997/999: composite b 0.023-0.041 with it,
        # 0.05+ without; marker 15/15 without, 0/6 with.)
        for tok, cells in list(self.obj_cells.items()):
            if tok in self.member_of or self.conds.get(tok) == CR:
                continue
            rec = self.partial_sig.get(tok, {})
            if "tap" not in rec or "soak" not in rec or len(rec) >= 3:
                continue
            res = self._consistency(tok)
            perfect = [c for c, (cf, ps) in res.items()
                       if cf == 0 and ps == len(cells) and ps >= 2]
            if len(perfect) == 1 and len(res) > 1 and all(
                    cf >= 1 for c, (cf, _ps) in res.items()
                    if c != perfect[0]):
                self._assert_to(tok, perfect[0], cells)
        super()._maybe_assert()

    def learner_action(self, obs):
        # priority (a) with the v2 probe order; everything else (a2, b,
        # c, d) delegates to E unchanged — identical budgets throughout
        for o in obs:
            self.conds[o["token"]] = o["cond"]
        toks = sorted(self.obj_cells)
        for tok in toks:
            if tok in self.member_of:
                continue
            rec = self.partial_sig.get(tok, {})
            cond = self.conds[tok]
            for (sa, mask) in PROBE_ORDER:
                if sa not in rec and cond in mask:
                    return sa, [tok]
            if len(self.obj_cells[tok]) < 3:
                for a in C.UNARY_ACTIONS:
                    if (cond, a) not in self.obj_cells[tok]:
                        return a, [tok]
        return super().learner_action(obs)
