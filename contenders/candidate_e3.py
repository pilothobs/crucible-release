"""Candidate E.3 — EXP3 (PREREGISTRATION_L35_EXP3): Candidate E.2 plus
the boundary-truncation bookkeeping repair, NOTHING else.

The D-lineage `boundary_batches` constructs every source's batch (each
construction mutating the proposer mirror and, for the compress path,
popping the swap queue) and then submits `batches[:4]` — so a fifth
constructed batch is half-consumed: its side-effects applied, the batch
never admitted.  On stream 1013 this consumed E.2's soaked-pair guard
with its inflight flag stuck, the whole systematic miss.  The repair:
construct source-by-source in D's exact order and simply DO NOT INVOKE
a source when four batches already exist — deferral instead of
destruction.  Submission caps unchanged; nothing is ever submitted that
the D lineage would not have; deferred proposals surface at later
boundaries through their sources' own state (repair contradictions,
genesis pool, growth backlog, swap queue).  `truncations_prevented`
counts boundaries where deferral occurred, for the V-pass."""
import sys

sys.path.insert(0, ".")
from crucible import constants as C
from l3_3.proposer import W_COMPRESS
from l3_5.candidate_e2 import CandidateE2


class CandidateE3(CandidateE2):

    def begin_run(self):
        super().begin_run()
        self.truncations_prevented = 0

    def boundary_batches(self, idx):
        self.boundary_ord += 1
        self._emit_queues = []
        batches = list(self._repair_batches())
        if len(batches) > 4:
            # repair batches cannot be deferred (their mirror mutations
            # apply at construction in the D lineage regardless); this
            # overflow is handled exactly as D handles it — truncation,
            # with the excess emits discarded at the next boundary's
            # queue reset.  The REPAIR here concerns only the sources
            # whose construction can be deferred cleanly.
            batches = batches[:4]
        deferred = False
        if len(batches) < 4:
            gen = self._genesis_batch()
            if gen:
                batches.append(gen)
        else:
            deferred = True
        if len(batches) < 4:
            grow = self._growth_batch()
            if grow:
                batches.append(grow)
        else:
            deferred = True
        if self.boundary_ord % W_COMPRESS == 0 or idx >= C.EPISODES:
            if len(batches) < 4:
                comp = self._compress_batch()
                if comp:
                    batches.append(comp)
            else:
                deferred = True
        if deferred:
            self.truncations_prevented += 1
        for ops, _meta in batches:
            self.stats["ops_submitted"] += len(ops)
        self.stats["batches"] += len(batches)
        assert len(batches) <= 4
        return batches
