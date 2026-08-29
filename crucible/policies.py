"""Reference policies (spec 6.3): oracles, nulls, cheap-ceiling controls.

All sit behind the same proposal-only interface (spec 4.7).  Policies marked
wants_backdoor receive latent kinds / true dynamics: they are substrate-side
instruments (ceilings and floors), declared as such — contenders never get a
backdoor.  Every policy's own randomness comes from a literal-seeded RNG.

Batches may reference concepts created earlier in the same batch via "@i"
placeholders (resolved by the engine to the cid of the batch's i-th NEW op).
"""
import random
from . import constants as C

P, CH, SO, CR = C.CONDITIONS
DRY = frozenset({P, CH})
NOTSO = frozenset({P, CH, CR})
PCR = frozenset({P, CR})
ONLY = lambda c: frozenset({c})
MAXOPS = 96


class Policy:
    wants_backdoor = False

    def __init__(self, seed=90001):
        self.rng = random.Random(seed)
        self._member_queue = []
        self._batch_queue = []

    def begin_run(self): pass

    def begin_episode(self, obs):
        self.obs = {o["token"]: dict(o) for o in obs}

    def learner_action(self, obs):
        self.obs = {o["token"]: dict(o) for o in obs}
        toks = sorted(self.obs)
        act = self.rng.choice(C.ACTIONS)
        if act == "grind":
            a, b = self.rng.sample(toks, 2)
            return act, [a, b]
        return act, [self.rng.choice(toks)]

    def observe(self, event): pass

    def step_membership_ops(self):
        ops, self._member_queue = self._member_queue, []
        return ops

    def boundary_batches(self, idx):
        b, self._batch_queue = self._batch_queue, []
        return b

    def batch_result(self, idx, accepted, dmdl, new_ids): pass


class NullEmpty(Policy):
    """Empty library forever: ties with chance by construction (1/11)."""


class NullDefault(Policy):
    """P8 defaults tracking the running per-action majority outcome."""

    def begin_run(self):
        self.counts = {}
        self.default_cid = {}
        self.current = {}

    def observe(self, event):
        a, o = event["action"], event["outcome"]
        self.counts.setdefault(a, {}).setdefault(o, 0)
        self.counts[a][o] += 1

    def boundary_batches(self, idx):
        ops = []
        self._pending_actions = []
        for a in sorted(self.counts):
            outs = self.counts[a]
            best = max(sorted(outs), key=lambda o: outs[o])
            if a not in self.default_cid:
                ops.append(("new", {"p": "P8", "action": a, "out": best}))
                self._pending_actions.append(a)
                self.current[a] = best
            elif self.current[a] != best:
                ops.append(("revise", self.default_cid[a], "out", best))
                self.current[a] = best
        return [(ops, {})] if ops else []

    def batch_result(self, idx, accepted, dmdl, new_ids):
        for a, cid in zip(getattr(self, "_pending_actions", []), new_ids):
            self.default_cid[a] = cid
        self._pending_actions = []


def factored_ops():
    """One atomic batch building the true attribute-factored library
    (spec 6.3 oracle; also the A16 check-3 transition payload).
    Placeholders: @0..@2 = attrs A1..A3, @3.. = classes in kind order."""
    kinds = list(C.K0) + [C.K_NEW]
    ops = [("new", {"p": "P4"}) for _ in range(3)]
    ops += [("new", {"p": "P1"}) for _ in kinds]
    A1, A2, A3 = "@0", "@1", "@2"
    cls = {k: "@%d" % (3 + i) for i, k in enumerate(kinds)}
    for k, cid in cls.items():
        for ai, a_ref in enumerate((A1, A2, A3)):
            ops.append(("attr", cid, a_ref, k[ai]))
    U = lambda expr, cond, action, out: ("new", {
        "p": "P5", "expr": expr, "cond": cond, "action": action, "out": out})
    lit = lambda a, s: [("has", a, s)]
    ops += [
        U([("has", A1, 0), ("has", A2, 0)], DRY, "tap", "thud"),
        U([("has", A1, 0), ("has", A2, 1)], DRY, "tap", "crumble"),
        U([("has", A1, 1), ("has", A2, 0)], DRY, "tap", "ring"),
        U([("has", A1, 1), ("has", A2, 1)], DRY, "tap", "shatter"),
        U(None, ONLY(SO), "tap", "thud"),
        U(lit(A1, 0), ONLY(CR), "tap", "shatter"),
        U(lit(A1, 1), ONLY(CR), "tap", "crumble"),
        U(lit(A2, 1), PCR, "heat", "ignite"),
        U([("has", A2, 0), ("has", A1, 0)], PCR, "heat", "melt"),
        U([("has", A2, 0), ("has", A1, 1)], PCR, "heat", "null"),
        U(None, ONLY(CH), "heat", "null"),
        U(None, ONLY(SO), "heat", "hiss"),
        U(lit(A3, 1), NOTSO, "soak", "hiss"),
        U(lit(A3, 0), NOTSO, "soak", "null"),
        U(None, ONLY(SO), "soak", "null"),
    ]
    both = ("both", NOTSO)
    cp = lambda op, a, neg: ("cmp", op, a, a, neg)
    AP = lambda expr, out: ("new", {"p": "P6", "expr": expr, "mode": "sym",
                                    "cond": both, "out": out})
    ops += [
        AP([cp("and", A1, 0), cp("xor", A3, 1)], "shatter"),
        AP([cp("and", A1, 0), cp("xor", A3, 0)], "repel"),
        AP([cp("and", A1, 1), cp("xor", A3, 0)], "fuse"),
        AP([cp("and", A1, 1), cp("xor", A3, 1)], "crumble"),
        ("new", {"p": "P8", "action": "grind", "out": "null"}),
    ]
    return ops, kinds


class OracleFull(Policy):
    """True structure + backdoor memberships: the ceiling (spec 6.3)."""
    wants_backdoor = True

    def begin_run(self):
        self.class_of = {}
        self._done = False

    def boundary_batches(self, idx):
        if not self._done:
            self._done = True
            ops, self._kinds = factored_ops()
            return [(ops, {})]
        return []

    def batch_result(self, idx, accepted, dmdl, new_ids):
        if not self.class_of:
            self.class_of = {k: new_ids[3 + i]
                             for i, k in enumerate(self._kinds)}

    def begin_episode(self, obs):
        super().begin_episode(obs)
        for o in obs:
            k = self.backdoor["kinds"][o["token"]]
            self._member_queue.append(("member+", o["token"],
                                       self.class_of[k]))


class OracleIdent(OracleFull):
    """True structure, but memberships must be earned by interaction (A2)."""

    def begin_episode(self, obs):
        Policy.begin_episode(self, obs)
        allk = list(C.K0) + [C.K_NEW]
        self.cands = {o["token"]: set(allk) for o in obs}
        self.conds = {o["token"]: o["cond"] for o in obs}
        self.asserted = set()

    def observe(self, event):
        tok = event["tokens"][0] if event["action"] != "grind" else None
        pre = self.conds.get(tok) if tok else None
        for t, c in event["conds_after"].items():
            if t in self.conds:
                self.conds[t] = c
        if tok is None or tok not in self.cands or tok in self.asserted:
            return
        dyn = self.backdoor["dyn"]
        # invert against the condition the object had *before* the event
        keep = {k for k in self.cands[tok]
                if dyn.f1(k, pre, event["action"])[0] == event["outcome"]}
        if keep:
            self.cands[tok] = keep
        if len(self.cands[tok]) == 1:
            k = next(iter(self.cands[tok]))
            self.asserted.add(tok)
            self._member_queue.append(("member+", tok, self.class_of[k]))

    def learner_action(self, obs):
        self.obs = {o["token"]: dict(o) for o in obs}
        for o in obs:
            self.conds[o["token"]] = o["cond"]
        unknown = [t for t in sorted(self.cands)
                   if len(self.cands[t]) > 1 and t not in self.asserted]
        for tok in unknown:
            cond = self.conds[tok]
            dyn = self.backdoor["dyn"]
            for act in C.UNARY_ACTIONS:
                outs = {dyn.f1(k, cond, act)[0] for k in self.cands[tok]}
                if len(outs) > 1:
                    return act, [tok]
        return Policy.learner_action(self, obs)


class ClassOnlyOracle(OracleFull):
    """True structure expressed only with initial kinds P1/P2/P3/P8:
    the Level-2 ceiling for the A3 factored-vs-class gap."""

    def boundary_batches(self, idx):
        if self._done:
            return []
        self._done = True
        from .dyn_a import f1, f2
        kinds = list(C.K0) + [C.K_NEW]
        self._kinds = kinds
        ops = [("new", {"p": "P1"}) for _ in kinds]
        cls = {k: "@%d" % i for i, k in enumerate(kinds)}
        U = lambda cid, cond, action, out: ("new", {
            "p": "P2", "cls": cid, "cond": cond, "action": action, "out": out})
        for k, cid in cls.items():
            ops += [
                U(cid, DRY, "tap", f1(k, P, "tap")[0]),
                U(cid, ONLY(CR), "tap", f1(k, CR, "tap")[0]),
                U(cid, PCR, "heat", f1(k, P, "heat")[0]),
                U(cid, ONLY(SO), "heat", "hiss"),
                U(cid, NOTSO, "soak", f1(k, P, "soak")[0]),
            ]
        for i, a in enumerate(kinds):
            for b in kinds[i:]:
                ops.append(("new", {"p": "P3", "c1": cls[a], "c2": cls[b],
                                    "mode": "sym", "cond": ("both", NOTSO),
                                    "out": f2(a, b, P, P)}))
        for act, out in (("tap", "thud"), ("heat", "null"),
                         ("soak", "null"), ("grind", "null")):
            ops.append(("new", {"p": "P8", "action": act, "out": out}))
        assert len(ops) <= MAXOPS, len(ops)
        return [(ops, {})]

    def batch_result(self, idx, accepted, dmdl, new_ids):
        if not self.class_of:
            self.class_of = {k: new_ids[i]
                             for i, k in enumerate(self._kinds)}


class Lookup(Policy):
    """Per-object memorizer.  Structural ops are boundary-only, so its
    per-object classes are created after the objects expire: it exists to
    demonstrate the MDL divergence (A3) and the structural deadness of
    memorization under this interface, both recorded as findings."""

    def begin_run(self):
        self.ep_cells = {}

    def begin_episode(self, obs):
        super().begin_episode(obs)
        self.ep_cells = {}

    def observe(self, event):
        if event["action"] == "grind":
            return
        tok = event["tokens"][0]
        self.ep_cells.setdefault(tok, set()).add(
            (event["action"], event["outcome"]))

    def boundary_batches(self, idx):
        ops = []
        n_new = 0
        for tok in sorted(self.ep_cells):
            if len(ops) + 1 + len(self.ep_cells[tok]) > MAXOPS:
                break
            ref = "@%d" % n_new
            ops.append(("new", {"p": "P1"}))
            n_new += 1
            for (a, o) in sorted(self.ep_cells[tok]):
                ops.append(("new", {"p": "P2", "cls": ref, "cond": None,
                                    "action": a, "out": o}))
                n_new += 1
        self.ep_cells = {}
        return [(ops, {})] if ops else []


class ClusterRelabel(Policy):
    """Clustering-plus-relabelling on interaction response profiles: the
    canonical Level-2 cheap contender (spec 6.3, 9.1)."""

    SIG = (("tap", DRY), ("heat", ONLY(P)), ("soak", DRY))

    def begin_run(self):
        self.sig_class = {}      # signature -> cid
        self.known_rules = {}    # cid -> set((action, condkey))
        self.rule_obs = {}       # cid -> {(action, condkey): {out: n}}
        self.pair_obs = {}       # frozenset -> {out: n}
        self.pair_done = set()
        self.need_grind_default = False
        self.grind_default_made = False

    def begin_episode(self, obs):
        super().begin_episode(obs)
        self.conds = {o["token"]: o["cond"] for o in obs}
        self.partial = {o["token"]: {} for o in obs}
        self.tok_class = {}

    @staticmethod
    def _condkey(cond):
        return {CR: "CR", SO: "SO"}.get(cond, "DRY")

    def observe(self, event):
        pre_conds = dict(self.conds)
        for t, c in event["conds_after"].items():
            if t in self.conds:
                self.conds[t] = c
        a, out = event["action"], event["outcome"]
        if a == "grind":
            t1, t2 = event["tokens"]
            if SO in (pre_conds.get(t1), pre_conds.get(t2)):
                self.need_grind_default = True
                return
            c1, c2 = self.tok_class.get(t1), self.tok_class.get(t2)
            if c1 and c2:
                d = self.pair_obs.setdefault(frozenset({c1, c2}), {})
                d[out] = d.get(out, 0) + 1
            return
        tok = event["tokens"][0]
        cond = pre_conds.get(tok, P)
        rec = self.partial.get(tok)
        if rec is not None:
            for (sa, mask) in self.SIG:
                if a == sa and cond in mask and sa not in rec:
                    rec[sa] = out
            if len(rec) == 3 and tok not in self.tok_class:
                sig = tuple(rec[sa] for sa, _ in self.SIG)
                cid = self.sig_class.get(sig)
                if cid:
                    self.tok_class[tok] = cid
                    self._member_queue.append(("member+", tok, cid))
                elif sig not in self.sig_class:
                    self.sig_class[sig] = None   # pending creation
        cid = self.tok_class.get(tok)
        if cid:
            d = self.rule_obs.setdefault(cid, {}).setdefault(
                (a, self._condkey(cond)), {})
            d[out] = d.get(out, 0) + 1

    def learner_action(self, obs):
        self.obs = {o["token"]: dict(o) for o in obs}
        for o in obs:
            self.conds[o["token"]] = o["cond"]
        for tok in sorted(self.partial):
            rec = self.partial[tok]
            cond = self.conds[tok]
            for (sa, mask) in self.SIG:
                if sa not in rec and cond in mask:
                    return sa, [tok]
        return Policy.learner_action(self, obs)

    def boundary_batches(self, idx):
        ops = []
        pend = [s for s, cid in sorted(self.sig_class.items()) if cid is None]
        self._pending_sigs = pend[:8]
        MASK = {"DRY": DRY, "CR": ONLY(CR), "SO": ONLY(SO)}
        n_new = 0
        for sig in self._pending_sigs:
            ref = "@%d" % n_new
            ops.append(("new", {"p": "P1"}))
            n_new += 1
            for (sa, mask), out in zip(self.SIG, sig):
                ops.append(("new", {"p": "P2", "cls": ref, "cond": mask,
                                    "action": sa, "out": out}))
                n_new += 1
        self._n_header = n_new
        for cid in sorted(self.rule_obs):
            known = self.known_rules.setdefault(cid, set())
            for (a, ck) in sorted(self.rule_obs[cid]):
                if (a, ck) in known or len(ops) >= MAXOPS - 1:
                    continue
                outs = self.rule_obs[cid][(a, ck)]
                best = max(sorted(outs), key=lambda o: outs[o])
                known.add((a, ck))
                ops.append(("new", {"p": "P2", "cls": cid, "cond": MASK[ck],
                                    "action": a, "out": best}))
                n_new += 1
        for pair in sorted(self.pair_obs, key=sorted):
            if pair in self.pair_done or len(ops) >= MAXOPS - 1:
                continue
            self.pair_done.add(pair)
            mem = sorted(pair)
            c1, c2 = (mem[0], mem[-1])
            outs = self.pair_obs[pair]
            best = max(sorted(outs), key=lambda o: outs[o])
            ops.append(("new", {"p": "P3", "c1": c1, "c2": c2, "mode": "sym",
                                "cond": ("both", NOTSO), "out": best}))
            n_new += 1
        if self.need_grind_default and not self.grind_default_made:
            self.grind_default_made = True
            ops.append(("new", {"p": "P8", "action": "grind", "out": "null"}))
        return [(ops, {})] if ops else []

    def batch_result(self, idx, accepted, dmdl, new_ids):
        i = 0
        for sig in getattr(self, "_pending_sigs", []):
            self.sig_class[sig] = new_ids[i]
            i += 4   # class + its three signature rules
        self._pending_sigs = []


class StaticFeat(Policy):
    """Appearance-bucket classes + majority rules: the static-feature
    learner.  Appearance is null by construction, so this must land at
    the deterministic floor (A4)."""

    def begin_run(self):
        self.buckets = {}
        self.rule_done = set()
        self.obs_counts = {}
        self._made = False

    def boundary_batches(self, idx):
        if not self._made:
            self._made = True
            return [([("new", {"p": "P1"})
                      for _ in range(C.APPEARANCE_VALUES)], {})]
        ops = []
        for (cid, a) in sorted(self.obs_counts):
            if (cid, a) in self.rule_done:
                continue
            outs = self.obs_counts[(cid, a)]
            if sum(outs.values()) < 5:
                continue
            best = max(sorted(outs), key=lambda o: outs[o])
            self.rule_done.add((cid, a))
            ops.append(("new", {"p": "P2", "cls": cid, "cond": None,
                                "action": a, "out": best}))
        return [(ops, {})] if ops else []

    def batch_result(self, idx, accepted, dmdl, new_ids):
        if not self.buckets and new_ids:
            self.buckets = {v: cid for v, cid in enumerate(new_ids)}

    def begin_episode(self, obs):
        super().begin_episode(obs)
        if self.buckets:
            for o in obs:
                cid = self.buckets[o["appearance"][0]]
                self._member_queue.append(("member+", o["token"], cid))

    def observe(self, event):
        if event["action"] == "grind" or not self.buckets:
            return
        tok = event["tokens"][0]
        o = self.obs.get(tok)
        if not o:
            return
        cid = self.buckets[o["appearance"][0]]
        d = self.obs_counts.setdefault((cid, event["action"]), {})
        d[event["outcome"]] = d.get(event["outcome"], 0) + 1


class AmbientCorr(NullDefault):
    """Fits per-action majorities on the passive ambient stream only.
    Inherits the declared confound; A7 measures the interventional gap."""

    def observe(self, event):
        if event["type"] != "ambient":
            return
        NullDefault.observe(self, event)
