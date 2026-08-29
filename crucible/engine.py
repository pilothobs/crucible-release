"""Episode driver + substrate bookkeeping (spec 4.5-4.7, 6.1-6.2, v0.3).

Owns: the event ledger (prequential, every event coded), the op log, the
violation log, membership state, scored-query execution, and batch admission
(legality + budget gate; dMDL computed by replay over the affected archived
events, returned and recorded, never gating - v0.3 C2).

Reference policies may be constructed with a backdoor (latent kinds / true
dynamics); those are substrate-side instruments (oracles, controls), declared
as such - contenders never receive one.
"""
import math
from . import constants as C
from . import dyn_a
from . import grammar as G
from .library import Library

MAX_BATCHES, MAX_OPS = 4, 96


class Engine:
    def __init__(self, corpus, policy, dyn=dyn_a):
        self.corpus = corpus
        self.policy = policy
        self.dyn = dyn
        self.lib = Library()
        self.archive = []           # per-event records (substrate-side)
        self.scored = []            # scored-row indices into archive
        self.violations = []        # violation records
        self.oplog = []             # every admitted operation
        self.data_bits = 0.0
        self.charge_bits = 0.0      # cumulative description charges (A3 totals)
        self.ev_by_class = {}       # cid -> [eids]
        self.ev_by_action = {}      # action -> [eids]
        self._ep_events_by_token = {}
        self._run_ground_cells = set()   # audit-side: kind cells ever ground

    # ------------------------------------------------------------------ utils
    def _charge(self, bits):
        self.charge_bits += bits

    def _desc_sizes(self):
        return self.lib.counts_for_costs()

    def violations_for(self, cid):
        return [v for v in self.violations if cid in v["rule_ids"]]

    # ---------------------------------------------------------------- library ops
    def _apply_member(self, op, ep, step):
        kind_op, token, cid = op
        st = self.obj_state.get(token)
        assert st is not None, "unknown token %r" % token
        assert cid in self.lib.concepts and \
            self.lib.concepts[cid]["term"]["p"] in ("P1", "P7"), cid
        members = self.members.setdefault(token, set())
        if kind_op == "member+":
            if cid in members:
                return 0.0
            members.add(cid)
        else:
            if cid not in members:
                return 0.0
            members.discard(cid)
        n_cls, _, _ = self._desc_sizes()
        cost = G.member_cost(n_cls)
        self._charge(cost)
        # dMDL: retro-replay this episode's events on this token
        d = 0.0
        for eid in self._ep_events_by_token.get(token, []):
            rec = self.archive[eid]
            d += self._recode(rec) - rec["bits"]
        self.oplog.append({"ep": ep, "step": step, "op": kind_op,
                           "token": token, "cid": cid, "bits": cost,
                           "dmdl": d})
        return d

    def _recode(self, rec, excluded=frozenset()):
        views = []
        for v in rec["views"]:
            vv = dict(v)
            vv["members"] = self.members.get(v["token"], set()) \
                if rec["ep"] == self.cur_ep else v["members"]
            views.append(vv)
        resolved, pred, _ = self.lib.predict(rec["action"], views, excluded)
        return self.lib.code_bits(resolved, pred, rec["outcome"])

    def _affected(self, batch_ops):
        touched_all = False
        eids = set()
        for op in batch_ops:
            tag = op[0]
            if tag in ("attr",):
                touched_all = True
            elif tag == "new":
                term = op[1]
                if term["p"] in ("P4",):
                    touched_all = True
                elif term["p"] in ("P5", "P6", "P8", "P9", "P10"):
                    act = term.get("action", "grind")
                    eids.update(self.ev_by_action.get(act, []))
                elif term["p"] in ("P2", "P3"):
                    for key in ("cls", "c1", "c2"):
                        if key in term:
                            eids.update(self.ev_by_class.get(term[key], []))
            elif tag in ("revise", "retire"):
                cid = op[1]
                rec = self.lib.concepts.get(cid)
                if rec is None:
                    continue
                t = rec["term"]
                if t["p"] in ("P4",):
                    touched_all = True
                elif t["p"] in ("P1", "P7", "P10"):
                    eids.update(self.ev_by_class.get(cid, []))
                else:
                    act = t.get("action", "grind")
                    eids.update(self.ev_by_action.get(act, []))
            elif tag in ("member+", "member-"):
                eids.update(self._ep_events_by_token.get(op[1], []))
        if touched_all:
            return range(len(self.archive))
        return sorted(eids)

    @staticmethod
    def _resolve(value, created):
        """Resolve '@i' placeholders (the cid created by the i-th NEW op of
        this batch) inside op arguments and term fields."""
        if isinstance(value, str) and value.startswith("@"):
            return created[int(value[1:])]
        if isinstance(value, list):
            return [Engine._resolve(v, created) for v in value]
        if isinstance(value, tuple):
            return tuple(Engine._resolve(v, created) for v in value)
        if isinstance(value, dict):
            return {k: Engine._resolve(v, created) for k, v in value.items()}
        return value

    def _apply_batch(self, ops, meta, ep):
        assert len(ops) <= MAX_OPS, "batch over op budget"
        affected = self._affected(ops)
        if isinstance(affected, range):
            before = sum(self._recode(r) for r in self.archive)
        else:
            before = sum(self._recode(self.archive[e]) for e in affected)
        desc_delta = 0.0
        cites = meta.get("cites", [])
        assert all(v < len(self.violations) for v in cites), "bad citation"
        new_ids = []
        for raw_op in ops:
            op = self._resolve(raw_op, new_ids)
            tag = op[0]
            n_cls, n_att, n_con = self._desc_sizes()
            if tag == "new":
                term = op[1]
                cost = G.new_cost(term, n_cls, n_att, n_con)
                spell = G.spelling_cost(term, n_cls, n_att, n_con)
                cid = self.lib.new_concept(term, ep)
                new_ids.append(cid)
                self._charge(cost)
                desc_delta += spell
                self.oplog.append({"ep": ep, "op": "new", "cid": cid,
                                   "term": dict(term), "bits": cost})
            elif tag == "revise":
                _, cid, slot, value = op
                t = self.lib.concepts[cid]["term"]
                old_cost = G.slot_value_cost(t["p"], slot, t.get(slot),
                                             n_cls, n_att)
                cost = G.revise_cost(t["p"], slot, value, n_con, n_cls, n_att)
                self.lib.revise(cid, slot, value, ep, cites)
                self._charge(cost)
                desc_delta += G.slot_value_cost(t["p"], slot, value,
                                                n_cls, n_att) - old_cost
                self.oplog.append({"ep": ep, "op": "revise", "cid": cid,
                                   "slot": slot, "bits": cost,
                                   "cites": cites})
            elif tag == "retire":
                _, cid = op
                rec = self.lib.concepts[cid]
                spell = G.spelling_cost(rec["term"], n_cls, n_att, n_con)
                cost = G.retire_cost(n_con)
                self.lib.retire(cid)
                self._charge(cost)
                desc_delta -= spell
                self.oplog.append({"ep": ep, "op": "retire", "cid": cid,
                                   "bits": cost})
            elif tag == "attr":
                _, class_cid, attr_cid, sign = op
                cost = G.attribution_cost(n_cls, n_att)
                self.lib.attributions[(class_cid, attr_cid)] = sign
                self._charge(cost)
                desc_delta += cost - G.OP_COST
                self.oplog.append({"ep": ep, "op": "attr", "cls": class_cid,
                                   "attr": attr_cid, "sign": sign,
                                   "bits": cost})
            elif tag in ("member+", "member-"):
                self._apply_member(op, ep, "boundary")
            else:
                raise ValueError(tag)
        if isinstance(affected, range):
            after = sum(self._recode(r) for r in self.archive)
        else:
            after = sum(self._recode(self.archive[e]) for e in affected)
        dmdl = desc_delta + (after - before)
        footprint = sorted({op[1] for op in ops
                            if op[0] in ("revise", "retire")}
                           | set(new_ids))
        self.oplog.append({"ep": ep, "op": "batch-summary",
                           "revises": meta.get("revises"), "cites": cites,
                           "dmdl": dmdl, "footprint": footprint,
                           "n_ops": len(ops)})
        return dmdl, new_ids

    # ------------------------------------------------------------------- run
    def run(self, episodes=None):
        pol = self.policy
        if getattr(pol, "wants_backdoor", False):
            pol.backdoor = {"dyn": self.dyn}
        pol.begin_run()
        n_eps = episodes or len(self.corpus)
        # boundary 0 (before episode 1)
        self._boundary(0)
        for epi in self.corpus[:n_eps]:
            self._episode(epi)
            self._boundary(epi["episode"])
        return self._results()

    def _boundary(self, idx):
        batches = self.policy.boundary_batches(idx) or []
        assert len(batches) <= MAX_BATCHES
        for ops, meta in batches:
            dmdl, new_ids = self._apply_batch(ops, meta or {}, idx)
            self.policy.batch_result(idx, True, dmdl, new_ids)

    def _episode(self, epi):
        ep = epi["episode"]
        self.cur_ep = ep
        self.members = {}
        self._ep_events_by_token = {}
        self.obj_state = {}
        slots = []   # display order
        for slot in range(C.N_OBJ):
            li = epi["perm"][slot]
            token = "o%d" % slot
            st = {"token": token, "latent": li, "kind": epi["kinds"][li],
                  "appearance": epi["appearance"][li],
                  "cond": epi["arrival"][li],
                  "arrived_cracked": epi["arrival"][li] == "cracked",
                  "counts": {}, "prev": None, "n_events": 0,
                  "ambient_hits": 0, "slot": slot}
            self.obj_state[token] = st
            slots.append(st)
        self._lat2tok = {st["latent"]: st["token"] for st in slots}
        obs = [{"token": s["token"], "appearance": s["appearance"],
                "cond": s["cond"]} for s in slots]
        if getattr(self.policy, "wants_backdoor", False):
            self.policy.backdoor["kinds"] = {s["token"]: s["kind"]
                                             for s in slots}
        self.policy.begin_episode(obs)
        self._drain_member_ops(ep, -1)
        amb_i = q_i = 0
        for step in range(C.T_STEPS):
            if step in C.SCORED_STEPS:
                q = epi["queries"][q_i]
                act, idxs = q[0], q[1]
                hyp = len(q) > 2 and q[2]
                tokens = [self._lat2tok[i] for i in idxs]
                if hyp:
                    self._hypothetical(ep, step, act, tokens, epi, q_i)
                else:
                    self._event(ep, step, "scored", act, tokens, epi, q_i)
                q_i += 1
            elif step in C.AMBIENT_STEPS:
                ev, tgt = epi["ambient"][amb_i]
                token = self._lat2tok[tgt]
                self.obj_state[token]["ambient_hits"] += 1
                self._event(ep, step, "ambient", C.AMBIENT_ACTION[ev],
                            [token], epi, None, ambient_name=ev)
                amb_i += 1
            else:
                choice = self.policy.learner_action(self._obs())
                if choice is not None:
                    act, tokens = choice
                    self._event(ep, step, "learner", act, list(tokens), epi,
                                None)
            self._drain_member_ops(ep, step)

    def _obs(self):
        return [{"token": t, "appearance": s["appearance"], "cond": s["cond"]}
                for t, s in self.obj_state.items()]

    def _drain_member_ops(self, ep, step):
        ops = self.policy.step_membership_ops() or []
        for op in ops:
            self._apply_member(op, ep, step)

    def _hypothetical(self, ep, step, action, tokens, epi, q_i):
        """Hypothetical scored query (spec v0.4): prediction under stated
        pristine conditions, scored against the oracle outcome; never
        executed, never revealed, no state change, no ledger coding, no
        learner-visible violation — audit-side record only."""
        states = [self.obj_state[t] for t in tokens]
        views = [{"token": s["token"], "cond": "pristine",
                  "members": frozenset(self.members.get(s["token"], ())),
                  "counts": dict(s["counts"]), "prev": s["prev"]}
                 for s in states]
        resolved, pred, rule_ids = self.lib.predict(action, views)
        out = self.dyn.f2(states[0]["kind"], states[1]["kind"],
                          "pristine", "pristine")
        eid = len(self.archive)
        rec = {"eid": eid, "ep": ep, "step": step, "type": "scored_hyp",
               "action": action, "views": views, "outcome": out,
               "resolved": resolved, "predicted": pred, "bits": 0.0,
               "rule_ids": rule_ids,
               "audit": {"kinds": [s["kind"] for s in states],
                         "appearance": [s["appearance"] for s in states],
                         "slots": [s["slot"] for s in states],
                         "cracked_arrival": [s["arrived_cracked"]
                                             for s in states],
                         "n_prior": [s["n_events"] for s in states],
                         "ambient_hits": [s["ambient_hits"]
                                          for s in states]}}
        rec["strata"] = self._strata(ep, epi, q_i, states, hyp=True)
        self.archive.append(rec)
        self.scored.append(eid)

    def _event(self, ep, step, etype, action, tokens, epi, q_i,
               ambient_name=None):
        states = [self.obj_state[t] for t in tokens]
        views = [{"token": s["token"], "cond": s["cond"],
                  "members": frozenset(self.members.get(s["token"], ())),
                  "counts": dict(s["counts"]), "prev": s["prev"]}
                 for s in states]
        resolved, pred, rule_ids = self.lib.predict(action, views)
        # execute
        if action == "grind":
            out = self.dyn.f2(states[0]["kind"], states[1]["kind"],
                              states[0]["cond"], states[1]["cond"])
        else:
            out, newcond = self.dyn.f1(states[0]["kind"], states[0]["cond"],
                                       action)
            states[0]["cond"] = newcond
        bits = self.lib.code_bits(resolved, pred, out)
        self.data_bits += bits
        eid = len(self.archive)
        rec = {"eid": eid, "ep": ep, "step": step, "type": etype,
               "action": action, "views": views, "outcome": out,
               "resolved": resolved, "predicted": pred, "bits": bits,
               "rule_ids": rule_ids,
               "audit": {"kinds": [s["kind"] for s in states],
                         "appearance": [s["appearance"] for s in states],
                         "slots": [s["slot"] for s in states],
                         "cracked_arrival": [s["arrived_cracked"]
                                             for s in states],
                         "n_prior": [s["n_events"] for s in states],
                         "ambient_hits": [s["ambient_hits"] for s in states]}}
        self.archive.append(rec)
        self.ev_by_action.setdefault(action, []).append(eid)
        for v in views:
            for cid in v["members"]:
                self.ev_by_class.setdefault(cid, []).append(eid)
            self._ep_events_by_token.setdefault(v["token"], []).append(eid)
        if resolved and pred != out:
            vid = len(self.violations)
            self.violations.append({"vid": vid, "ep": ep, "step": step,
                                    "action": action, "tokens": tokens,
                                    "predicted": pred, "observed": out,
                                    "rule_ids": rule_ids})
            for cid in rule_ids:
                if cid in self.lib.concepts:
                    self.lib.concepts[cid]["violations"].append(vid)
        if etype == "scored":
            rec["strata"] = self._strata(ep, epi, q_i, states)
            self.scored.append(eid)
        if action == "grind":
            self._run_ground_cells.add(frozenset(s["kind"] for s in states))
        for s in states:
            s["counts"][action] = s["counts"].get(action, 0) + 1
            s["prev"] = (action, out)
            s["n_events"] += 1
        self.policy.observe({"step": step, "type": etype,
                             "ambient": ambient_name, "action": action,
                             "tokens": tokens, "outcome": out,
                             "conds_after": {s["token"]: s["cond"]
                                             for s in states}})

    @staticmethod
    def _window(ep):
        if ep < C.E_C:
            return "pre"
        return "mid" if ep < C.E_R else "post"

    def _strata(self, ep, epi, q_i, states, hyp=False):
        tags = {"window": self._window(ep), "hyp": hyp}
        tags["pre_ident"] = all(s["n_events"] == 0 for s in states)
        tags["k_new"] = any(s["kind"] == C.K_NEW for s in states)
        tags["weathered"] = any(s["arrived_cracked"] for s in states)
        tags["first_cooc"] = hyp
        if hyp:
            cell = frozenset(s["kind"] for s in states)
            unseen = cell not in self._run_ground_cells
            tags["fc_unseen"] = unseen
            tags["fc_seen"] = not unseen
        else:
            tags["fc_unseen"] = tags["fc_seen"] = False
        return tags

    # --------------------------------------------------------------- results
    def replay_scored(self, excluded=frozenset()):
        """Exact ablation replay of every scored query (spec 5.2)."""
        rows = []
        for eid in self.scored:
            rec = self.archive[eid]
            resolved, pred, _ = self.lib.predict(rec["action"], rec["views"],
                                                 excluded)
            rows.append((rec, resolved, pred))
        return rows

    def lifetime_rent(self, cid):
        """Criterion (c): data bits saved with the concept vs without, from
        its admission onward, both sides recoded under the final library
        state (declared convention), minus its description bits (spec 5.3)."""
        rec = self.lib.concepts.get(cid)
        if rec is None:
            return None
        start_ep = rec["admitted_ep"]
        saved = 0.0
        excl = frozenset({cid})
        for r in self.archive:
            if r["ep"] < start_ep:
                continue
            res_w, pred_w, _ = self.lib.predict(r["action"], r["views"])
            res_o, pred_o, _ = self.lib.predict(r["action"], r["views"], excl)
            saved += (self.lib.code_bits(res_o, pred_o, r["outcome"]) -
                      self.lib.code_bits(res_w, pred_w, r["outcome"]))
        n_cls, n_att, n_con = self._desc_sizes()
        desc = G.spelling_cost(rec["term"], n_cls, n_att, n_con)
        return saved - desc

    def _results(self):
        acc = {}
        for eid in self.scored:
            r = self.archive[eid]
            key = r["strata"]["window"]
            correct = int(r["resolved"] and r["predicted"] == r["outcome"])
            if not r["strata"]["hyp"]:
                acc.setdefault(key, []).append(correct)
                tags = ("pre_ident", "k_new", "weathered")
            else:
                tags = ("fc_unseen", "fc_seen")
            for tag in tags:
                if r["strata"].get(tag):
                    acc.setdefault(tag + ":" + key, []).append(correct)
        summary = {k: (sum(v) / len(v), len(v)) for k, v in acc.items()}
        return {"accuracy": summary,
                "data_bits": self.data_bits,
                "charge_bits": self.charge_bits,
                "total_bits": self.data_bits + self.charge_bits,
                "n_concepts": len(self.lib.concepts),
                "n_violations": len(self.violations)}
