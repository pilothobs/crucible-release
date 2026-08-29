"""L3-2 additional cheap contenders (frozen tree untouched — these subclass
the frozen policies from outside and add no engine changes).

ClusterWild — clustering-plus-relabelling whose rules are spelled with
wildcard cond_patterns (the MDL-cheap spelling pre-E_C).  It therefore FACES
contradictions at E_C (cracked-tap breaks its wildcard tap rules) and repairs
by ADDING masked rules — which under the flat rank semantics conflict with
the wildcard originals.  Its (d) record is tested-and-unrepaired.

ClusterGreedy — the §9.1 arms-race wrapper: same base, but on detected
contradictions it issues locally-correct REVISE repairs (narrow the wildcard
rule's cond mask to DRY, add the observed-cond rule in the same batch) and
cites the real violation ids through the R3 read path (wired by the runner;
interface-law compliant — the contradictions are derivable from its own
observations).  The strongest cheap attempt to imitate (d)'s identity
continuity and locality.
"""
from crucible import constants as C
from crucible.policies import Policy, ClusterRelabel

P, CH, SO, CR = C.CONDITIONS
DRY = frozenset({P, CH})
NOTSO = frozenset({P, CH, CR})
MASK = {"DRY": DRY, "CR": frozenset({CR}), "SO": frozenset({SO})}
MAXB = 90


class ClusterWild(ClusterRelabel):
    """Signature clustering with wildcard-cond rules; repairs by ADD."""

    REPAIR_BY_REVISE = False

    def begin_run(self):
        super().begin_run()
        self.rule_cid = {}        # (class_cid, action) -> wildcard-rule info
        self.have_rule = set()    # (class_cid, action, condkey-or-WILD)
        self.contradictions = []  # (class_cid, action, condkey, outcome)
        self.read_violations = None   # wired by runner for the greedy child
        self._emit_queues = []

    # -- contradiction detection against our own wildcard rules ------------
    def observe(self, event):
        pre_conds = dict(self.conds)
        super().observe(event)
        if event["action"] == "grind":
            return
        tok = event["tokens"][0]
        cid = self.tok_class.get(tok)
        if not cid:
            return
        a, out = event["action"], event["outcome"]
        ck = self._condkey(pre_conds.get(tok, P))
        info = self.rule_cid.get((cid, a))
        if info and info["wild"] and info["out"] != out:
            self.contradictions.append((cid, a, ck, out))

    # -- proposals ----------------------------------------------------------
    def boundary_batches(self, idx):
        self._emit_queues = []
        ops, emit = [], []
        pend = [s for s, cid in sorted(self.sig_class.items()) if cid is None]
        for sig in pend[:8]:
            ref = "@%d" % len(emit)
            ops.append(("new", {"p": "P1"}))
            emit.append(("class", sig))
            for (sa, _m), out in zip(self.SIG, sig):
                ops.append(("new", {"p": "P2", "cls": ref, "cond": None,
                                    "action": sa, "out": out}))
                emit.append(("rule", ref, sa, "WILD", out))
        for cid in sorted(self.rule_obs):
            for (a, ck) in sorted(self.rule_obs[cid]):
                if len(ops) >= MAXB:
                    continue
                outs = self.rule_obs[cid][(a, ck)]
                best = max(sorted(outs), key=lambda o: outs[o])
                if ck == "DRY" and (cid, a, "WILD") not in self.have_rule \
                        and (cid, a) not in self.rule_cid:
                    self.have_rule.add((cid, a, "WILD"))
                    ops.append(("new", {"p": "P2", "cls": cid, "cond": None,
                                        "action": a, "out": best}))
                    emit.append(("rule", cid, a, "WILD", best))
                elif ck != "DRY" and (cid, a, ck) not in self.have_rule:
                    self.have_rule.add((cid, a, ck))
                    ops.append(("new", {"p": "P2", "cls": cid,
                                        "cond": MASK[ck], "action": a,
                                        "out": best}))
                    emit.append(("rule", cid, a, ck, best))
        for pair in sorted(self.pair_obs, key=sorted):
            if pair in self.pair_done or len(ops) >= MAXB:
                continue
            self.pair_done.add(pair)
            mem = sorted(pair)
            outs = self.pair_obs[pair]
            best = max(sorted(outs), key=lambda o: outs[o])
            ops.append(("new", {"p": "P3", "c1": mem[0], "c2": mem[-1],
                                "mode": "sym", "cond": ("both", NOTSO),
                                "out": best}))
            emit.append(("pair", pair))
        if self.need_grind_default and not self.grind_default_made:
            self.grind_default_made = True
            ops.append(("new", {"p": "P8", "action": "grind", "out": "null"}))
            emit.append(("default",))
        batches = []
        if ops:
            batches.append((ops, {}))
            self._emit_queues.append(emit)
        repair = self._repair_batch()
        if repair:
            batches.append(repair[0])
            self._emit_queues.append(repair[1])
        return batches[:4]

    def _repair_batch(self):
        """ADD-only repair (ClusterWild): the masked rule lands in the main
        batch already (rule_obs carries the CR/SO cells), so contradictions
        are simply dropped — the wildcard rule is never revised."""
        self.contradictions = []
        return None

    def batch_result(self, idx, accepted, dmdl, new_ids):
        if not self._emit_queues:
            return
        emit = self._emit_queues.pop(0)
        assert len(emit) == len(new_ids), (len(emit), len(new_ids))
        for entry, cid in zip(emit, new_ids):
            if entry[0] == "class":
                self.sig_class[entry[1]] = cid
            elif entry[0] == "rule":
                _, cls_ref, a, ck, out = entry
                cls_cid = (new_ids[int(cls_ref[1:])]
                           if str(cls_ref).startswith("@") else cls_ref)
                if ck == "WILD":
                    self.rule_cid[(cls_cid, a)] = {"cid": cid, "wild": True,
                                                   "out": out}


class ClusterGreedy(ClusterWild):
    """REVISE-with-citations repair: the (d)-imitation arms race."""

    REPAIR_BY_REVISE = True

    def _repair_batch(self):
        ops, cites, revised = [], [], []
        seen = set()
        for (cid, a, ck, out) in self.contradictions:
            key = (cid, a)
            info = self.rule_cid.get(key)
            if key in seen or info is None or not info["wild"] or ck == "DRY":
                continue
            seen.add(key)
            ops.append(("revise", info["cid"], "cond", DRY))
            info["wild"] = False
            revised.append(info["cid"])
            if self.read_violations is not None:
                cites.extend(v["vid"]
                             for v in self.read_violations(info["cid"]))
            # the masked replacement rule for the contradicting cell rides
            # the main batch via rule_obs (already observed there)
        self.contradictions = []
        if not ops:
            return None
        meta = {"revises": revised, "cites": sorted(set(cites))}
        return (ops, meta), []   # revise ops consume no new_ids
