"""Candidate E ("KEYSTONE") — EXP1 contender, preregistered in
PREREGISTRATION_L35_EXP1.md section 2.

A failure-localized redesign of Candidate D: identical repair, growth,
compression, inference and decoy machinery (inherited), with two localized
changes: (1) two-tier identification — canonical-signature classing primary
(eliminating D's duplicate-class churn; D's merge machinery is disabled as
unnecessary), ranked best-fit fallback secondary (deliberately allowed one
conflicting cell so weathered/k_new objects become identifiable and their
wrongness feeds the (d) repair streams); (2) targeted pair exploration so
stage-2's evidence actually accumulates.  Genesis is signature-keyed; a
novel signature first tries a zero-conflict fit against existing classes
(split-born classes have no signature) and registers itself there, so splits
and genesis never duplicate.
"""
import itertools
import sys

sys.path.insert(0, ".")
from crucible import constants as C
from crucible import grammar as G
from l3_3.proposer import (CandidateD, CONDS, OPS2, BEAM_PARTITIONS,
                           BEAM_PAIRCMP)

P, CH, SO, CR = CONDS
DRY = frozenset({P, CH})
SIG_BASIS = (("tap", DRY), ("heat", frozenset({P})), ("soak", DRY))
POS_MIN, CONF_MAX, GAP_MIN = 2, 1, 1


class CandidateE(CandidateD):

    def begin_run(self):
        super().begin_run()
        self.class_of_sig = {}     # completed signature -> class cid
        self._sig_pool = {}        # novel signature -> profile cells
        self.crsig_map = {}        # cracked outcome-triple -> class cid
        # learned per-action edit stats: does a cracked object's outcome
        # match its class's pristine cell?  [stable, changed] counts,
        # updated at each cohort resolution
        self._organ_stats = {a: [0, 0] for a in C.UNARY_ACTIONS}
        self._swap_queue = []      # follow-up batches of an adoption swap

    def begin_episode(self, obs):
        super().begin_episode(obs)
        self.partial_sig = {o["token"]: {} for o in obs}
        self._tok_crsig = {}
        self._upair = {}     # unidentified tok -> [(partner class, outcome)]

    # ---------------------------------------------------- identification
    def observe(self, event):
        # capture signature cells against the PRE-event condition
        if event["action"] != "grind":
            tok = event["tokens"][0]
            cond = self.conds.get(tok)
            rec = self.partial_sig.get(tok)
            if rec is not None:
                for (sa, mask) in SIG_BASIS:
                    if event["action"] == sa and cond in mask \
                            and sa not in rec:
                        rec[sa] = event["outcome"]
        else:
            # grind of an unidentified object against an identified member:
            # discrimination evidence for tier-2 (pair outcome depends on
            # the hidden pair region, so tied leaders can be separated)
            t1, t2 = event["tokens"]
            for (u, m) in ((t1, t2), (t2, t1)):
                if u not in self.member_of and m in self.member_of \
                        and "soaked" not in (self.conds.get(u),
                                             self.conds.get(m)):
                    self._upair.setdefault(u, []).append(
                        (self.member_of[m], event["outcome"]))
        super().observe(event)

    def _discrim_score(self, cand, tok):
        """+/- evidence for candidate class from grinds of this (still
        unidentified) object against identified members, compared with the
        settled class-pair evidence the library's pair table already holds."""
        sc = 0
        for (pcls, out) in self._upair.get(tok, ()):
            pair = frozenset({cand, pcls}) if cand != pcls \
                else frozenset({cand})
            cnt = self.pair_cells.get(pair)
            if cnt:
                exp = max(sorted(cnt), key=lambda o: cnt[o])
                sc += 2 if exp == out else -2
        return sc

    def _maybe_assert(self):
        for tok, cells in self.obj_cells.items():
            if tok in self.member_of:
                continue
            # ---- tier 1: completed canonical signature
            rec = self.partial_sig.get(tok, {})
            if len(rec) == len(SIG_BASIS):
                sig = tuple(rec[sa] for sa, _m in SIG_BASIS)
                cid = self.class_of_sig.get(sig)
                if cid is not None and cid in self.classes:
                    self._assert_to(tok, cid, cells)
                    continue
                # novel signature: adopt a zero-conflict existing class
                # (split-born classes carry no signature) before genesis
                res = self._consistency(tok)
                sigged = set(self.class_of_sig.values())
                zero = [c for c, (conf, pos) in res.items()
                        if conf == 0 and pos >= 2 and c not in sigged]
                if len(zero) == 1:
                    self.class_of_sig[sig] = zero[0]
                    self._assert_to(tok, zero[0], cells)
                    continue
                if sig not in self.class_of_sig:
                    self._sig_pool.setdefault(sig, dict(cells))
                continue
            # ---- tier 2: ranked best-fit fallback, ONLY for objects whose
            # signature can never complete (cracked is absorbing; anything
            # dry finishes tier 1, and soaked dries).  Letting tier 2 race
            # tier 1 on partially-observed pristine objects mis-asserts on
            # 2-cell evidence and split-churns junk classes (dev finding).
            if self.conds.get(tok) != CR:
                continue
            # full 3-cell profile required: premature 2-cell assertion loses
            # the cohort key and mixes cohorts inside one class (dev finding)
            crsig = self._crsig(tok, cells)
            if crsig is None:
                continue
            self._tok_crsig[tok] = crsig
            cid = self.crsig_map.get(crsig)
            if cid is not None and cid in self.classes:
                self._assert_to(tok, cid, cells)
                continue
            # Candidates: every class within the conflict/positive
            # thresholds.  Unary evidence CANNOT decide alone — a cracked
            # kind's profile can be identical to another kind's pristine
            # profile (the crack edit collapses tap to two symbols), so a
            # perfect (0, 3) fit may be the impostor and the true class sits
            # second at (1, 2).  Grind discrimination against the settled
            # pair table is the deciding evidence; while an informative
            # partner is present and un-ground, defer and let exploration
            # grind.  The resolved mapping is cohort-permanent (crsig_map).
            res = self._consistency_ev(tok)
            cands = [c for c, (cf, ps) in sorted(res.items())
                     if cf <= CONF_MAX and ps >= POS_MIN]
            if not cands:
                continue
            souts = dict(zip(sorted(("tap", "heat", "soak")), crsig))
            disc = {c: self._discrim_score(c, tok) for c in cands}
            stab = {c: self._stability_score(c, souts) for c in cands}
            cev = {c: self._cell_evidence(c, cells) for c in cands}
            claimed = set(self.crsig_map.values())
            cands.sort(key=lambda c: (-disc[c], -stab[c], -cev[c],
                                      res[c][0], -res[c][1],
                                      c in claimed,
                                      self.classes[c]["born"]))
            w = cands[0]
            runner = cands[1] if len(cands) > 1 else None
            # stability evidence may decide only once the edit pattern is
            # learned (some organ proven crack-stable, some proven edited);
            # before that an impostor's perfect profile out-scores the truth.
            # Either way the winner must be STRICT on the full evidence
            # triple (grind discrimination, organ stability, exact-cond cell
            # evidence): a mapping is cohort-permanent, and dev showed every
            # tie broken by anything weaker picks wrong half the time.
            stats_ready = (
                any(st >= 2 and ch == 0
                    for st, ch in self._organ_stats.values())
                and any(ch >= 2 and st == 0
                        for st, ch in self._organ_stats.values()))
            strict = runner is None or \
                (disc[w], stab[w], cev[w]) > \
                (disc[runner], stab[runner], cev[runner])
            decisive = strict and (
                disc[w] > 0 or (stats_ready and disc[w] >= 0
                                and stab[w] > 0))
            if not decisive:
                # not mappable yet: grind if a discriminating partner is
                # present, else wait for the pair table / organ stats /
                # the true class's genesis — a cohort mapping is permanent,
                # so a weak pick now is worse than an unidentified episode
                continue
            self.crsig_map[crsig] = w
            if disc[w] > 0:
                # organ stats learn only from grind-verified resolutions —
                # an impostor-matched mapping would poison the edit pattern
                for a, out in souts.items():
                    m = self._cell_majority(self.classes[w]["cells"], a, P)
                    if m is not None:
                        self._organ_stats[a][0 if m == out else 1] += 1
            self._assert_to(tok, w, cells)

    def _stability_score(self, cls, souts):
        """Learned edit-organ evidence: match the cohort's cracked outcomes
        against the class's pristine cells, weighting each action by how
        reliably resolved cohorts have shown it survives the crack edit."""
        sc = 0
        ccells = self.classes[cls]["cells"]
        for a, out in souts.items():
            m = self._cell_majority(ccells, a, P)
            if m is None:
                continue
            st, ch = self._organ_stats[a]
            w = 2 if st >= 2 and ch == 0 else (0 if ch > st else 1)
            sc += w * (1 if m == out else -1)
        return sc

    def _table_ready(self, tok, cands):
        """True if some present identified non-soaked partner has settled
        pair-table entries for EVERY candidate — the table has an opinion,
        even if it is 'indistinguishable'.  Until then, mapping a cohort on
        unary evidence alone locks in the impostor (dev finding)."""
        for t2 in sorted(self.obj_cells):
            X = self.member_of.get(t2)
            if X is None or self.conds.get(t2) == SO:
                continue
            if all(self.pair_cells.get(
                    frozenset({c, X}) if c != X else frozenset({c}))
                    for c in cands):
                return True
        return False

    def _informative_partner(self, tok, cands):
        """A present, identified, non-soaked member whose class's settled
        pair-table entries DIFFER across at least two candidates, and which
        this object has not been ground against yet.  None if no such
        partner exists (then the ranking decides on what evidence there is)."""
        done = {p for (p, _o) in self._upair.get(tok, ())}
        for t2 in sorted(self.obj_cells):
            X = self.member_of.get(t2)
            if X is None or X in done or self.conds.get(t2) == SO:
                continue
            outs = set()
            for c in cands:
                pair = frozenset({c, X}) if c != X else frozenset({c})
                cnt = self.pair_cells.get(pair)
                if cnt:
                    outs.add(max(sorted(cnt), key=lambda o: cnt[o]))
            if len(outs) >= 2:
                return t2
        return None

    def _crsig(self, tok, cells):
        conds = {cond for (cond, _a) in cells}
        if conds != {CR}:
            return None
        outs = {a: out for (_c, a), out in cells.items()}
        if len(outs) < 3:
            return None
        return tuple(outs[a] for a in sorted(outs))

    @staticmethod
    def _cell_majority(ccells, a, cond):
        cnt = ccells.get((a, cond))
        if not cnt:
            return None
        return max(sorted(cnt), key=lambda o: cnt[o])

    def _consistency_ev(self, tok):
        """Tier-2 ranking: rule prediction where the library resolves; the
        class's own cell-evidence majority where it does not (overlapping
        repair masks leave never-observed conds unresolved); pristine
        evidence as the last-resort similarity basis for cracked cells.
        For cracked cells with learned organ stats, trust the learned edit
        pattern over raw CR cell counts, which a transiently mis-placed
        cohort can pollute (splits move members but not their cell counts).
        Proposer-internal heuristic only — no authority."""
        res = {}
        for cls in self.classes:
            ccells = self.classes[cls]["cells"]
            conf = pos = 0
            for (cond, a), out in self.obj_cells[tok].items():
                if cond == CR:
                    pred = self._predict_cr(cls, a)
                else:
                    pred = self._predict_unary(cls, cond, a)
                    if pred is None:
                        pred = self._cell_majority(ccells, a, cond)
                if pred is None:
                    continue
                if pred == out:
                    pos += 1
                else:
                    conf += 1
            res[cls] = (conf, pos)
        return res

    def _predict_cr(self, cls, a):
        """Cracked-cell expectation for ranking: an explicit CR-narrow rule
        (the designed body-edit) first; then the learned edit pattern —
        pristine evidence for a proven-stable organ, no signal for a proven-
        edited one; raw majorities only while the pattern is unlearned."""
        for r in self.rules_of.get((cls, a), ()):
            rule = self.rules[r]
            if rule["cond"] is not None and CR in rule["cond"] \
                    and len(rule["cond"]) == 1:
                return rule["out"]
        ccells = self.classes[cls]["cells"]
        st, ch = self._organ_stats[a]
        if st >= 2 and ch == 0:
            return self._cell_majority(ccells, a, P)
        if ch > st and ch >= 2:
            return None
        pred = self._predict_unary(cls, CR, a)
        if pred is None:
            pred = self._cell_majority(ccells, a, CR)
        if pred is None:
            pred = self._cell_majority(ccells, a, P)
        return pred

    # evidence-narrow: revise any rule whose cond mask includes a condition
    # where the class's own accumulated cell evidence contradicts the rule's
    # outcome.  This is what dissolves the overlapping-mask deadlock at
    # `cracked` once cracked members' cells land in a class.
    def _repair_batches(self):
        by_cls = {}
        for (cls, a), rcids in sorted(self.rules_of.items()):
            if cls not in self.classes:
                continue
            ccells = self.classes[cls]["cells"]
            for rcid in list(rcids):
                rule = self.rules.get(rcid)
                if rule is None:
                    continue
                mask = set(rule["cond"]) if rule["cond"] is not None \
                    else set(CONDS)
                drop = {cond for cond in mask
                        if (m := self._cell_majority(ccells, a, cond))
                        is not None and m != rule["out"]}
                if drop and mask - drop:
                    newmask = frozenset(mask - drop)
                    rule["cond"] = newmask
                    cites = []
                    if self.read_violations is not None:
                        cites = [v["vid"]
                                 for v in self.read_violations(rcid)]
                    by_cls.setdefault(cls, ([], [], []))
                    by_cls[cls][0].append(("revise", rcid, "cond", newmask))
                    by_cls[cls][1].append(rcid)
                    by_cls[cls][2].extend(cites)
        batches = []
        # one batch per class: an evidence-narrow event stays local to the
        # class it narrows (f_d locality is per revision event)
        for cls in sorted(by_cls):
            ops, revs, cites = by_cls[cls]
            batches.append((ops[:96], {"revises": sorted(set(revs)),
                                       "cites": sorted(set(cites))}))
            self._emit_queues.append([])
        return batches + super()._repair_batches()

    def _cell_evidence(self, cls, cells):
        """Exact-condition cell-evidence match, weighted by the learned
        edit pattern: for cracked cells the EDITED organ's CR evidence is
        the only component that carries class identity (stable organs match
        trivially across heat-group partners and wash the signal out —
        dev finding), so edited organs weigh 2, proven-stable 0, unknown 1."""
        ev = 0
        for (cond, a), out in cells.items():
            cnt = self.classes[cls]["cells"].get((a, cond))
            if not cnt:
                continue
            maj = max(sorted(cnt), key=lambda o: cnt[o])
            if cond == CR:
                st, ch = self._organ_stats[a]
                w = 2 if ch > st and ch >= 2 else \
                    (0 if st >= 2 and ch == 0 else 1)
            else:
                w = 1
            ev += w * (1 if maj == out else -1)
        return ev

    def _assert_to(self, tok, cls, cells):
        self.member_of[tok] = cls
        self.classes[cls]["n_members"] = \
            self.classes[cls].get("n_members", 0) + 1
        self._member_queue.append(("member+", tok, cls))
        for (cond, a), out in cells.items():
            cnt = self.classes[cls]["cells"].setdefault((a, cond), {})
            cnt[out] = cnt.get(out, 0) + 1

    # ------------------------------------------------------------ genesis
    def _genesis_batch(self):
        if not self._sig_pool:
            return None
        ops, emit = [], []
        n_new = 0
        for sig in sorted(self._sig_pool):
            cells = {}
            for (cond, a), out in self._sig_pool[sig].items():
                cells.setdefault((a, cond), {})[out] = 1
            ref = "@%d" % n_new
            ops.append(("new", {"p": "P1"}))
            toks = tuple(
                t for t, rec in self.partial_sig.items()
                if len(rec) == len(SIG_BASIS)
                and tuple(rec[sa] for sa, _m in SIG_BASIS) == sig
                and t not in self.member_of)
            emit.append(("class", cells, toks, True, sig))
            n_new += 1
            for (a, cond, out) in self._cheapest_spelling(cells):
                ops.append(("new", {"p": "P2", "cls": ref, "cond": cond,
                                    "action": a, "out": out}))
                emit.append(("rule", ref, a, cond, out))
                n_new += 1
            if len(ops) > 80:
                break
        self._sig_pool = {}
        if not ops:
            return None
        self._emit_queues.append(emit)
        return (ops, {})

    def batch_result(self, idx, accepted, dmdl, new_ids):
        # register signatures for genesis-born classes; remap cracked
        # cohorts whose members a repair split out; then defer to D
        if self._emit_queues:
            for entry, cid in zip(self._emit_queues[0], new_ids):
                if entry[0] != "class":
                    continue
                if len(entry) > 4:
                    self.class_of_sig[entry[4]] = cid
                elif len(entry) > 3 and entry[3] is False:
                    for tok in entry[2]:
                        sig = self._tok_crsig.get(tok)
                        if sig is None:
                            cl = self.obj_cells.get(tok)
                            sig = self._crsig(tok, cl) if cl else None
                        if sig is not None:
                            self.crsig_map[sig] = cid
        super().batch_result(idx, accepted, dmdl, new_ids)

    def _merge_duplicates(self, ops):
        return   # signature-keyed genesis cannot duplicate (EXP1 section 2)

    # ------------------------------------------------- joint compression
    # Stage 1 alone cannot pay at 6 classes on this pricing (dev finding:
    # every true-partition set scores negative; the one positive plan was a
    # free-riding attribute whose aurules carried no literals).  The economy
    # lives in the PAIR table: 20+ per-pair P3 rules compress into a few
    # attr-comparison P6 rules — but only if attrs exist.  So Candidate E
    # scores attrs + aurules + aprules as ONE exact-compression plan: the
    # pair savings subsidize the attribute layer.  Same arithmetic, same
    # decoys, same admission path — one plan instead of two stages.
    def _compress_attrs_stage(self):
        mature = sorted(c for c in self.classes
                        if self.classes[c].get("n_members", 0) >= 3)
        if len(mature) < 3:
            return None
        classes = mature
        cols = self._class_matrix(classes)
        while True:
            full = {col: row for col, row in cols.items()
                    if all(c in row for c in classes)}
            if len(full) >= 4 or len(classes) <= 3:
                break
            coverage = {c: sum(1 for row in cols.values() if c in row)
                        for c in classes}
            classes = sorted(c for c in classes
                             if c != min(coverage, key=lambda x:
                                         (coverage[x], x)))
        cols = {col: row for col, row in cols.items()
                if all(c in row for c in classes)}
        if len(cols) < 4 or len(classes) < 3:
            return None
        # adoption timing gate: wait until every pristine column is settled
        # for the whole core.  Adopting off the earliest settled columns
        # locks in partitions the discriminative columns cannot use, and
        # the path dependence is permanent — the misaligned layer's savings
        # are spent, so the aligned layer never scores positive afterwards
        # (dev 999/997: heat@P and tap@P had no aurules to the end).
        if not self.attrs and any((a, P) not in cols
                                  for a in C.UNARY_ACTIONS):
            return None
        # ... and until the core carries five classes (the rare kind
        # matures late; a factorization fitted to four mis-generalizes the
        # moment it arrives).  Fallback at ep 150 so a starved stream still
        # adopts pre-shift.
        if not self.attrs and len(classes) < 5 and self.ep_ord < 150:
            return None
        cands, seen = [], set()
        for col, row in sorted(cols.items()):
            groups = {}
            for c in classes:
                groups.setdefault(row[c], set()).add(c)
            gl = sorted(groups.values(), key=sorted)
            for r in range(1, len(gl)):
                for combo in itertools.combinations(range(len(gl)), r):
                    S = frozenset().union(*(gl[i] for i in combo))
                    if 0 < len(S) < len(classes) and S not in seen \
                            and frozenset(set(classes) - S) not in seen:
                        seen.add(S)
                        cands.append(S)
        cands = cands[:BEAM_PARTITIONS]
        self.stats["internal_evals"] += len(cands)

        # bounded exhaustive subset search: greedy locks in whichever
        # partitions the earliest settled columns suggest, and a misaligned
        # early pick permanently poisons block-constancy for the
        # discriminative columns (dev 999/997: heat@P and tap@P never got
        # aurules; the k_new class stayed unattributable).  All subsets
        # (<= 4) of the top-12 single-partition candidates, unary NF gain
        # for all, pair gain for the best 30 by unary.
        singles = sorted(
            cands, key=lambda S:
            -self._score_attr_set_nf([S], cols, classes)[0])[:12]
        self.stats["internal_evals"] += len(cands)
        scored_subsets = []
        for r in (1, 2, 3, 4):
            for T in itertools.combinations(singles, r):
                g, _pl = self._score_attr_set_nf(list(T), cols, classes)
                scored_subsets.append((g, T))
        self.stats["internal_evals"] += len(scored_subsets)
        scored_subsets.sort(key=lambda x: (-x[0], [sorted(S) for S in x[1]]))
        chosen, best_gain = None, 0.0
        for g, T in scored_subsets[:30]:
            pg, _pp, _pr = self._joint_pair_score(list(T), classes)
            self.stats["internal_evals"] += 1
            if g + pg > best_gain:
                best_gain, chosen = g + pg, list(T)
        self._score_decoys(cols, classes)
        if not chosen:
            return None
        gain, plan = self._score_attr_set_nf(chosen, cols, classes)
        pg, pplan, pretire = self._joint_pair_score(chosen, classes)
        gain += pg
        if gain <= 0 or plan is None:
            return None
        base_ids = sorted(self.attrs)
        mapping = {}
        for S in chosen:
            for a in base_ids:
                rows = [(c, self.attributions[(c, a)]) for c in classes
                        if (c, a) in self.attributions]
                if rows and all((c in S) == bool(sg) for c, sg in rows):
                    mapping[S] = a
                    break
        return self._emit_joint(chosen, mapping, plan, pplan, pretire,
                                classes)

    def _score_attr_set_nf(self, attrs, cols, classes):
        """Normal-form exact comparison (EXP1 amendment 1): the attribute
        plan is priced against the FLAT spelling of the same settled
        evidence — two normal forms of today's knowledge — rather than
        against whichever rules the incremental history happens to hold.
        The incremental form (score vs current spellings, minus retire
        fees) is a hill-climbing trap: flat rules are sunk costs, so the
        true factorization scores negative at every local step in a
        6-class world (measured, dev 997-999).  Decoys are priced by the
        SAME criterion and still fail: they cover no evidence more cheaply
        than the flat form.  Plan/aurule construction is unchanged from
        the inherited arithmetic; only `saved` changes meaning."""
        n_cls = len(classes)
        n_att = max(2, len(attrs))
        base = self._score_attr_set(attrs, cols, classes)
        if base[1] is None:
            return base
        _g_incr, plan = base
        covered = {}
        for (expr, a, condset, out) in plan["aurules"]:
            covered.setdefault(a, set()).update(condset)
        cost = 0.0
        for (expr, a, condset, out) in plan["aurules"]:
            cost += G.OP_COST + G.spelling_cost(
                {"p": "P5",
                 "expr": [("has", "x", s) for (_h, _i, s) in expr] or None,
                 "cond": condset, "action": a, "out": out},
                n_cls, n_att, 40)
        cost += len(attrs) * (G.OP_COST + G.spelling_cost({"p": "P4"},
                                                          n_cls, n_att, 40))
        cost += len(attrs) * n_cls * G.attribution_cost(n_cls, n_att)
        # flat normal form of the covered evidence: per class/action, the
        # cheapest rule spelling of its settled cells over covered conds
        saved = 0.0
        for cls in classes:
            ccells = self.classes[cls]["cells"]
            for a, conds in covered.items():
                sub = {}
                for cond in conds:
                    cnt = ccells.get((a, cond))
                    if cnt:
                        tot = sum(cnt.values())
                        out = max(sorted(cnt), key=lambda o: cnt[o])
                        if tot >= 3 and cnt[out] / tot >= 0.8:
                            sub[(cond, a)] = cnt
                for (ra, rcond, rout) in self._cheapest_spelling(sub):
                    saved += G.OP_COST + G.spelling_cost(
                        {"p": "P2", "cls": cls, "cond": rcond,
                         "action": ra, "out": rout}, n_cls, n_att, 40)
        return saved - cost, plan

    def _joint_pair_score(self, chosen, classes):
        """Exact pair-compression gain available on TOP of an attr-set: the
        cheapest consistent attr-comparison region map over the settled
        pair cells among these classes, minus P6 spelling, plus the P3
        rules it retires.  (0, [], []) when nothing consistent/positive."""
        if not chosen or self._pair_adopted:
            return 0.0, [], []
        assign = {c: tuple(int(c in S) for S in chosen) for c in classes}
        cells = {}
        for pair, cnt in self.pair_cells.items():
            mem = sorted(pair)
            if mem[0] in assign and mem[-1] in assign:
                out = max(sorted(cnt), key=lambda o: cnt[o])
                cells[(mem[0], mem[-1])] = out
        if len(cells) < 6:
            return 0.0, [], []
        n_cls = max(2, len(classes))
        n_att = max(2, len(chosen))
        idx = range(len(chosen))
        # diagonal comparisons first: symmetric same-attribute comparisons
        # are the natural shape for a sym-mode pair law, and the 2-combo
        # beam draws from the front of this list
        pairs_idx = sorted(itertools.product(idx, idx),
                           key=lambda ij: (ij[0] != ij[1], ij))
        cand = [(op, i, j, neg) for (i, j) in pairs_idx
                for op in OPS2 for neg in (0, 1)][:BEAM_PAIRCMP]
        self.stats["internal_evals"] += len(cand)

        def cmpv(c1, c2, cm):
            op, i, j, neg = cm
            x, y = assign[c1][i], assign[c2][j]
            v = {"and": x & y, "or": x | y, "xor": x ^ y,
                 "eq": 1 - (x ^ y)}[op]
            return v ^ neg

        best = None
        for combo in ([(c,) for c in cand] +
                      list(itertools.combinations(cand[:24], 2))):
            regions = {}
            for (c1, c2), out in cells.items():
                key = tuple(cmpv(c1, c2, cm) for cm in combo)
                regions.setdefault(key, set()).add(out)
            if any(len(v) > 1 for v in regions.values()):
                continue
            pplan, cost = [], 0.0
            for key, outs in sorted(regions.items()):
                out = next(iter(outs))
                expr = []
                for cm, kv in zip(combo, key):
                    op, i, j, neg = cm
                    expr.append((op, i, j, neg ^ (1 - kv)))
                pplan.append((expr, out))
                cost += G.OP_COST + G.spelling_cost(
                    {"p": "P6", "expr": [("cmp", "and", "x", "x", 0)
                                         for _ in expr], "mode": "sym",
                     "cond": ("both", frozenset({"pristine"})),
                     "out": out}, n_cls, n_att, 40)
            # normal-form: the flat spelling of the settled pair evidence
            # is one P3 per covered pair cell (amendment 1, same criterion
            # change as the unary side)
            saved = len(cells) * (G.OP_COST + G.spelling_cost(
                {"p": "P3", "c1": "a", "c2": "b", "mode": "sym",
                 "cond": ("both", frozenset({"pristine"})),
                 "out": "x"}, n_cls, n_att, 40))
            retire = [rcid for rcid, r in self.prules.items()
                      if r["c1"] in assign and r["c2"] in assign]
            g = saved - cost
            if g > 0 and (best is None or g > best[0]):
                best = (g, pplan, retire)
        return best if best else (0.0, [], [])

    def _compress_batch(self):
        if self._swap_queue:
            ops, meta, emit = self._swap_queue.pop(0)
            self._emit_queues.append(emit)
            return (ops, meta)
        return super()._compress_batch()

    def _emit_joint(self, attrs, mapping, plan, pplan, pretire, classes):
        ops, emit = [], []
        n_new = 0
        attr_refs = []
        emitted_something = False
        for S in attrs:
            if S in mapping:
                attr_refs.append(mapping[S])
            else:
                ops.append(("new", {"p": "P4"}))
                emit.append(("attr", [(c, int(c in S)) for c in classes]))
                attr_refs.append("@%d" % n_new)
                n_new += 1
                emitted_something = True
        for i, S in enumerate(attrs):
            if str(attr_refs[i]).startswith("@"):
                for c in classes:
                    ops.append(("attr", c, attr_refs[i], int(c in S)))
        existing_sigs = {
            (frozenset((attr, sg) for (_h, attr, sg) in r["expr"]),
             r["action"], r["cond"], r["out"])
            for r in self.arules.values()}
        for (expr, a, condset, out) in plan["aurules"]:
            spelled = [("has", attr_refs[i], sg) for (_h, i, sg) in expr]
            if all(not str(attr_refs[i]).startswith("@")
                   for (_h, i, sg) in expr):
                sig = (frozenset((attr_refs[i], sg) for (_h, i, sg) in expr),
                       a, condset, out)
                if sig in existing_sigs:
                    continue
            ops.append(("new", {"p": "P5", "expr": spelled or None,
                                "cond": condset, "action": a, "out": out}))
            emit.append(("arule", [("has", attr_refs[i], sg)
                                   for (_h, i, sg) in expr], a, condset, out))
            n_new += 1
            emitted_something = True
        for (expr, out) in pplan:
            refs = [(op, attr_refs[i], attr_refs[j], neg)
                    for (op, i, j, neg) in expr]
            ops.append(("new", {"p": "P6",
                                "expr": [("cmp", op, a1, a2, neg)
                                         for (op, a1, a2, neg) in refs],
                                "mode": "sym",
                                "cond": ("both", frozenset(
                                    {"pristine", "charred", "cracked"})),
                                "out": out}))
            emit.append(("aprule", refs, out))
            n_new += 1
            emitted_something = True
        if not emitted_something:
            return None
        # ---- full swap: the flat spellings the plan replaces must GO, or
        # the new units stay redundant on every query they should carry
        # (dev finding: composite ablation margins ~0.02 with leftovers
        # present).  Rules fully inside the covered conds retire; rules
        # straddling covered/uncovered conds retire AND their uncovered
        # residual evidence is respelled as fresh P2s — retire+new, never
        # revise, so the (d) repair stream stays purely the repair
        # machinery's.  Overflow beyond one batch queues for the next
        # boundaries.
        covered = {}
        for (_expr, a, condset, _out) in plan["aurules"]:
            covered.setdefault(a, set()).update(condset)
        ops2, emit2 = [], []
        for cls in classes:
            ccells = self.classes[cls]["cells"]
            for a, conds in sorted(covered.items()):
                doomed = [rcid for rcid in list(self.rules_of.get(
                    (cls, a), ()))
                    if (set(self.rules[rcid]["cond"])
                        if self.rules[rcid]["cond"] is not None
                        else set(CONDS)) & conds]
                if not doomed:
                    continue
                residual_conds = set()
                for rcid in doomed:
                    rc = self.rules[rcid]["cond"]
                    residual_conds |= (set(rc) if rc is not None
                                       else set(CONDS)) - conds
                sub = {}
                for cond in residual_conds:
                    cnt = ccells.get((a, cond))
                    if cnt:
                        sub[(cond, a)] = cnt
                for (ra, rcond, rout) in self._cheapest_spelling(sub):
                    rcond = rcond if rcond is not None \
                        else frozenset(residual_conds)
                    ops2.append(("new", {"p": "P2", "cls": cls,
                                         "cond": rcond, "action": ra,
                                         "out": rout}))
                    emit2.append(("rule", cls, ra, rcond, rout))
                for rcid in doomed:
                    ops2.append(("retire", rcid))
                    r = self.rules.pop(rcid)
                    self.rules_of.get((r["cls"], r["action"]),
                                      []).remove(rcid)
        for rcid in pretire:
            if rcid in self.prules:
                ops2.append(("retire", rcid))
                self.prules.pop(rcid)
        if pplan:
            self._pair_adopted = True
        self.stats["adoption_eps"].append(self.ep_ord)
        # chunk: batch 1 = the new layer; follow-ups = respell/retire,
        # keeping each batch's emit aligned with its "new" ops
        assert len(ops) <= 96, len(ops)
        assert len(emit) == sum(1 for o in ops if o[0] == "new")
        i = 0
        while i < len(ops2):
            chunk, chunk_emit, n = [], [], 0
            while i < len(ops2) and n < 96:
                op = ops2[i]
                chunk.append(op)
                if op[0] == "new":
                    chunk_emit.append(emit2.pop(0))
                i += 1
                n += 1
            self._swap_queue.append((chunk, {}, chunk_emit))
        self._emit_queues.append(emit)
        return (ops, {})

    # -------------------------------------------------------- exploration
    def learner_action(self, obs):
        for o in obs:
            self.conds[o["token"]] = o["cond"]
        toks = sorted(self.obj_cells)
        # (a) identify the unidentified: signature probes where possible,
        # otherwise any unobserved cell (weathered arrivals cannot produce
        # signature cells and must be fed evidence for the tier-2 fallback)
        for tok in toks:
            if tok in self.member_of:
                continue
            rec = self.partial_sig.get(tok, {})
            cond = self.conds[tok]
            for (sa, mask) in SIG_BASIS:
                if sa not in rec and cond in mask:
                    return sa, [tok]
            if len(self.obj_cells[tok]) < 3:
                for a in C.UNARY_ACTIONS:
                    if (cond, a) not in self.obj_cells[tok]:
                        return a, [tok]
        # (a2) grind an unmapped cracked object against the most informative
        # identified partner so tier-2's candidates become discriminable
        for tok in toks:
            if tok in self.member_of or self.conds[tok] != CR:
                continue
            cells = self.obj_cells[tok]
            if self._crsig(tok, cells) is None \
                    or self._crsig(tok, cells) in self.crsig_map:
                continue
            res = self._consistency_ev(tok)
            cands = [c for c, (cf, ps) in sorted(res.items())
                     if cf <= CONF_MAX and ps >= POS_MIN]
            if len(cands) > 1:
                t2 = self._informative_partner(tok, cands)
                if t2 is not None:
                    return "grind", [tok, t2]
        # (b) grind pairs whose class-pair cell is unknown
        ided = [(t, self.member_of[t]) for t in toks if t in self.member_of]
        best = None
        for i in range(len(ided)):
            for j in range(i + 1, len(ided)):
                t1, c1 = ided[i]
                t2, c2 = ided[j]
                if SO in (self.conds[t1], self.conds[t2]):
                    continue
                pair = frozenset({c1, c2}) if c1 != c2 else frozenset({c1})
                if pair not in self.pair_cells \
                        and not self._pair_attr_predicts(pair):
                    best = (t1, t2)
                    break
            if best:
                break
        if best:
            return "grind", list(best)
        # (c) build class-matrix support: probe cells of identified members
        # where the class's evidence is below the matrix support threshold
        # (rule-resolved or not — the dense core needs settled evidence),
        # deliberately charring a pristine member when its class lacks
        # charred-column support
        for tok, cls in ided:
            cond = self.conds[tok]
            ccells = self.classes[cls]["cells"]
            for a in C.UNARY_ACTIONS:
                cnt = ccells.get((a, cond), {})
                if sum(cnt.values()) < 3 and (cond, a) \
                        not in self.obj_cells[tok]:
                    return a, [tok]
            if cond == P:
                for a in C.UNARY_ACTIONS:
                    cnt = ccells.get((a, CH), {})
                    if sum(cnt.values()) < 3:
                        return "heat", [tok]
        # (d) uniform (seeded)
        act = self.rng.choice(C.ACTIONS)
        if act == "grind" and len(toks) >= 2:
            a, b = self.rng.sample(toks, 2)
            return act, [a, b]
        if act == "grind":
            act = self.rng.choice(C.UNARY_ACTIONS)
        return act, [self.rng.choice(toks)]
