# WO-EID-L3-5 / EXP3 — Candidate E.3: the boundary-truncation repair,
# with a committed prediction (the Director's countersigned confirmation)

**Status:** preregistered and committed BEFORE any E.3 code exists,
before the fresh stream is generated, before any scored run.
Certification: frozen P004 machinery, θ_comp = 0.4022 (constant).
Governing texts: `l3_5/DIRECTOR_COUNTERSIGN_EXP2.md` ("E.3 = E.2 plus
the bookkeeping repair, nothing else, prediction committed before
scoring that 1013 fires and composite shares tighten, budgets
identical, same streams plus one fresh rule-drawn stream").

## 1. The defect, characterized precisely (correcting the V-pass note)

`boundary_batches` (D lineage, frozen) resets the emit queue each
boundary and returns `batches[:4]`. There is therefore NO cross-boundary
emit misalignment (the EXP2 V-pass note overstated that part — corrected
here). The real mechanism: when more than four batches are CONSTRUCTED,
the excess batches' construction side-effects have already been applied
to the proposer's mirror — in particular `_compress_batch` pops the
swap queue and E.2's guard proposal sets `_guard_inflight = True` — but
the batch is never submitted. The guard is thereby consumed-but-never-
admitted and, with its inflight flag stuck, never re-proposed. That is
the whole 1013 signature: guard absent, 110 soaked-pair abstentions
back, composites 0.539–0.652. Direction strictly against the contender;
E's scored runs carried 1–4 such truncated batches per run (lost
growth/compress proposals; substrate authority untouched throughout).

## 2. Candidate E.3 = E.2 + the repair, NOTHING else

`l3_5/candidate_e3.py`: subclass of the frozen CandidateE2 overriding
ONLY `boundary_batches`: batches are constructed source-by-source in
D's exact order (repair → genesis → growth → compress) and a source is
simply NOT INVOKED when four batches already exist — deferral instead
of half-consumption; every constructed batch is submitted. No budget
change (the 4-batch/96-op submission caps are untouched; nothing new is
ever submitted that the D lineage would not have submitted — proposals
are deferred to later boundaries instead of destroyed). No other method
is touched.

## 3. The committed prediction (before any E.3 run anywhere)

- **P1 (mechanism):** on stream 1013, the guard is admitted for all 5
  seeds and the marker fires for ≥ 4/5 seeds.
- **P2 (no harm):** on 1009 and 1019 the marker still fires for every
  seed, and each run's best composite share is no worse than E.2's by
  more than +0.02 (tightening expected).
- **P3 (anti-tuning guard):** on the fresh stream the marker fires for
  ≥ 4/5 seeds.
- **Verdict:** E3-CONFIRMED (P1 ∧ P2 ∧ P3 — the systematic 1013 failure
  converts into a confirmed mechanism); E3-REFUTED (P1 fails — the
  defect story was wrong; report, and that matters more);
  E3-MIXED (anything else — report, Director).

## 4. Streams, seeds, budgets

Scored: the same verdict streams 1009/1013/1019 (the controlled
comparison the prediction is ABOUT) plus the fresh stream drawn by the
standing ledger rule — the smallest prime > 1000 not in the ledger
(1009, 1013, 1019 now in it) → **1021** — generated first at its
two-sided validation (A10; both oracles certify the marker at composite
level under θ_comp; all controls certify nothing; cluster regression
form; no bare P4), any failure an apparatus stop. Seeds 301–305
(same, for the controlled comparison). Budgets identical (EXP2 §2
binding; the repair changes only which boundary a proposal is submitted
at). E.3 frozen by digest before scoring. Falsification on the result:
determinism, guard-cid verification, truncation counter must read zero
constructed-over-limit events, composite-share comparison table vs
E.2, exploration-distribution vs E.2.
