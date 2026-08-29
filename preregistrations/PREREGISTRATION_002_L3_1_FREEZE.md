# EID-L3 — Preregistration 002: L3-1 Freeze Addendum

**Status:** binding, committed at the L3-1 gate **before any contender exists**.
Companion to `PREREGISTRATION_001_CONCEPT_CRITERIA.md` (criteria, unchanged and
untouched) and to `l3_1/MANIFEST.json` (the hash-certified authority for every
numeric value; on any discrepancy between prose here and the manifest, the
manifest wins and the discrepancy is a finding).

**Change control:** append-only. Revision requires `PREREGISTRATION_003_…`
committed before any further runs.

---

## 1. Frozen episode schedule (gap-8 disposition; C1 decoupling)

| Event | Episode | Meaning |
|---|---|---|
| E_C | **300** | weathered (cracked) arrivals begin — the body-edit contradiction stream for criterion (d) |
| E_R | **400** | k_new enters; co-occurrence holdout opens; Shift-T stream begins — the split contradiction stream for (d), the reuse stream for (e) |
| Total | **600** episodes | windows: pre = 1–299, mid = 300–399, post = 400–600 |

## 2. Frozen world and interface parameters

Authoritative values in `l3_1/MANIFEST.json` `parameters`; headline: 5 objects
× 32 steps (20 learner + 4 ambient + 8 scored), kinds K0 as listed with k_new
= (0,0,1) splitting from k_old = (0,0,0) on α3; holdout **selected by rule
from literal seed** (constraints H1–H4 stated first, spec §2.5 v0.4; 57
eligible subsets; derived set {A-B, B-C, B-E, D-E}, 2× fuse / 2× crumble);
post-E_R kind weights **marginal-matched** to the measured pre-E_R
rejection-sampling marginals under that holdout (A .3009, B .0330, C .3007,
D .1985, E .1669 — side-channel continuity at E_R); ε = 1e-3; proposal budget
4 × 96; membership ops per-step.

## 3. Frozen criteria thresholds ⟨L3-1⟩ (spec §5), set from the L3-1
measurements and frozen before any contender

| Threshold | Value | Anchor measurement |
|---|---|---|
| δ_b (load-bearing ablation margin, top-1) | **0.05** | cheap-probe noise band ≤ 0.03 (A4/A5/A8) |
| δ_e (reuse ablation margin, post-shift stream) | **0.05** | same noise band |
| f_d (revision locality: concepts touched outside c + new admissions) | **≤ 10%** | spec target, unchanged |
| τ_d (restoration: retained pre-shift ablation margin) | **0.05** | same noise band |
| A1 headroom floor | 0.25 | measured margins 0.335–1.0 |
| A2 identification floor | 0.15 | measured margins 0.211–0.259 |
| A3 floors (class-vs-empty / factored-vs-class model) | 5,000 / 300 bits | measured 42,786 / 474 |
| A4/A5/A8 leakage tolerance | 0.03 | measured ≤ 0.02 on gated features |
| A9 ambient-cue outcome tolerance | 0.06 | measured 0.019 (kind excess 0.04, reported) |
| A6 side-channel permutation p | ≥ 0.05 | measured 0.975 |
| A7 causal-trap gap floor | 0.05 | measured 0.134 |

## 4. The transfer stratum (criterion (e) and the marker's decisive surface)

**Hypothetical held-out-cell queries.** Up to 12 post-E_R episodes per
held-out cell receive, at scored step 19, a *hypothetical* grind query on the
cell's pair under **stated pristine conditions**: the substrate records the
library's prediction and scores it against the generator outcome; the query
is never executed, its outcome is never revealed to any policy, and no state
changes. It is therefore dry by construction, non-disturbing, and carries no
information channel. Two executed-query designs were tried and discarded
with evidence (early queries measured identification, not composition; late
executed queries collapsed to the trivial soaked-null and handed the
memorizer the withheld datum) — the discard trail is in `L3_1_REPORT.md`.

**Stratum semantics, fixed now:** a hypothetical query is **fc_unseen** iff
no grind event on that kind-cell has occurred earlier in the run — which is
policy-dependent, because "never trained on" is a property of the run;
per-policy n is therefore unequal and is always reported alongside.
Remaining hypothetical queries are **fc_seen**. Measured at the freeze
(rule-derived holdout): oracle 1.000 (n=12) and oracle-with-identification
1.000 (n=12) on fc_unseen, **every cheap control 0.000** — the compositional
headroom exists and memorization cannot reach it.

**Scoring convention, fixed now (gate-hold check 2):** on the top-1 accuracy
surface an **unresolved query scores 0** — declining to predict is not a
hit; no realized uniform draw, no tie-break; one engine code path applies
this to every policy and stratum. The uniform-chance reference 1/11 lives on
the *coding* surface, where an unresolved query costs exactly log₂ 11 ≈ 3.46
bits. Null-empty therefore scores 0.000 top-1 by construction while coding
at exactly the uniform-chance bit rate — the corrected sense of "ties with
chance by construction" (spec §6.2/§6.3 v0.4).

## 5. Verbatim re-anchoring of the marker's evidence (gate confirmation 3)

From `L3_0_SPEC.md` §8b, carried here word for word as instructed:

> **criterion (c) for the marker concept is satisfied by strict arithmetic,
> but the *decisive* marker evidence is the first-co-occurrence stratum
> accuracy plus ablation margins (b)/(e)** — MDL admission alone is not
> presented as the headline.

The measured factored-vs-class model gap is 474 bits (floor 300): real,
thin as a fraction of total MDL, and never to be read as the marker's proof.

## 6. A16-driven amendments, declared with their arithmetic before any
contender (each is in the spec v0.4 change log with its evidence)

1. **P7 rank privilege removed** (all non-default rules at one rank): with
   the privilege, the CondClass shadow (≈ 31 bits) undercut the designed
   body-edit (≈ 36 bits) and criterion (d)'s REVISE branch was again not
   optimal — A16 check 1 fired exactly as designed. P7 is now a genuine
   decoy (strictly dominated by cond_pattern masks). Post-change repair
   table: narrow+add 37.3 bits, strictly optimal; nearest alternative
   (retire+respell) 52.0; every other option ≥ 395 bits.
2. **T = 32 steps** (was 24): at T=24 the honest per-object rent margin was
   ≈ +0.4 bits (inside noise); at T=32 it is ≈ +6.35 bits/object, genesis
   payback ≈ 7.7 objects against ≈ 500 available per class per run
   (A16 check 4).
3. **Membership evidence number: 3 events** (7.49-bit assertion ÷ 3.46
   bits/event; A16 check 5) — the identification burden is a computed
   number.
4. **Factoring transition = 94 ops ≤ 96** in one atomic batch
   (A16 check 3).
5. **Admission semantics** are the v0.3 C2 semantics (legality + budget;
   ΔMDL recorded, returned, never gating); criterion (c) is the lifetime
   rent check alone.

## 7. Standing limitations recorded at freeze (not defects; bounds)

- The oracle reference library resolves grind queries on unidentified pairs
  through its grind default and accepts a small violation stream there;
  reference-policy violations of this type are a modeling trade, not
  substrate unsoundness.
- The ambient cue's kind excess is ≈ 0.10 under the rule-derived marginals —
  by declaration (the causal-trap confound), priced by A9's outcome-excess
  gate (measured 0.004, tol 0.06). The PL3 fixture is therefore
  **differential**: it fires iff the planted excess exceeds the real
  generator's measured excess by > 0.05 (measured: planted 0.19 vs real
  0.10 → Δ ≈ 0.09, fires).
- Under the rule-derived holdout, kind B's effective marginal is 0.033
  pre-E_R (it sits in three held-out cells) — a declared consequence of
  rejection enforcement; ≈ 99 B objects still occur pre-E_R, and A2/A1
  margins clear their floors under this distribution.
- `dissolve` is a declared outcome symbol that no reachable cell produces in
  v0.1; it is reserved, and its appearance anywhere is a stop condition.
- Per-object memorization is *structurally* dead under this interface
  (structural ops are boundary-only, objects are episode-scoped), so the
  lookup control demonstrates MDL divergence (+246k bits) rather than a
  competitive ceiling. Recorded so L3-2 does not over-claim the lookup
  failure as an empirical discovery.
