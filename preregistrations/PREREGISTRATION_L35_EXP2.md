# WO-EID-L3-5 / EXP2 — Candidate E.2: closing the abstention gap under
# the composite blade

**Status:** preregistered and committed before any E.2 code, before any
new stream is generated, before any scored run (invariant c). Harness:
frozen CRUCIBLE v0.1; criteria P001 untouched; certification: the P004
machinery (`l3_2/certify_p004.py`, digest in `l3_5/FREEZE_P004.json`),
with **θ_comp = 0.4022 henceforth a frozen constant, not re-derived**
(the EXP1-§4 treatment of thresholds); ClusterRelabel remains the
standing regression fixture. Governing ruling:
`l3_5/DIRECTOR_RULING_H2.md`, including the three approval changes,
all binding here.

## 1. What this experiment attacks (from the P004 relabel record)

Candidate E under P004: marker 0/15 — attribute-composite abstention
shares 0.5645–0.6954 vs θ_comp 0.4022, honest-oracle reachability
S_or = 0.2011. The gap is coverage, not invention (the ruling's words):
(i) executed-grind resolution — pair queries with unidentified partners
and soaked-era contexts abstain where the reference resolves;
(ii) the k_new/E attribution ambiguity (EXP1 A1.1(4)) leaves the D–E
holdout cell unresolvable (hyp 0.0/3 across runs); (iii) residual unary
coverage gaps from the adoption swap's respell. E.2 must close the
composite-scope share from ~0.60 to ≤ 0.4022 **by better use of
evidence under the same interface and budgets** (approval change 3).

## 2. Budget identity (approval change 3 — binding)

E.2 runs under budgets IDENTICAL to Candidate E's freeze: the world
interface unchanged (20 learner steps/episode, the query schedule, HYP
caps); proposal-side W_COMPRESS = 25, beams 40 partitions / 200
pair-comparisons, subset search top-12/≤4/top-30, batches ≤ 96 ops and
≤ 4 per boundary, K_ASSERT = 2, cell support (3, 0.8), tier-2
thresholds, and every constant in EXP1 Amendment A1.3. **Any budget
change is its own declared amendment with re-validated references.**
The falsification pass gains a standing check: E.2's exploration-action
distribution (per-action counts of learner actions, per stream)
reported against Candidate E's replayed distribution on the same
streams, so a reviewer can see whether the gain came from inference or
from spending.

## 3. Exposure ledger and the verdict-stream draw (approval change 2)

Every generator seed ever used anywhere in the programme:

| Seed(s) | Role |
|---|---|
| 17 | D-era eval stream; ALSO exposed in D development (declared in l3_3/FREEZE.json); used with leak variants in L3-1 audit/planted-fixture runs (EVAL_SEEDS[0]) |
| 18, 19 | D-era eval streams (D scoring, L3-2 controls, L3-3 V-pass) |
| 23, 29, 31 | EXP1 verdict streams — burned (E scoring, H2/per-cell analyses, P004 validation and replay) |
| 997, 998, 999 | EXP1 development streams (E and, henceforth, E.2 dev only; never verdict-bearing) |
| 731001–731006 | named internal RNG stream constants (offset by corpus seed; not corpus seeds) |
| 731007 | SEED_HOLDOUT (holdout-pair draw under the preregistered rule) |

**Draw rule, committed before any stream is generated:** the EXP2
verdict streams are the three smallest prime numbers greater than 1000
that do not appear in the ledger above → **1009, 1013, 1019**. Policy
training seeds for E.2: literals **301–305** (fresh namespace; 101–105
were D's, 201–205 E's).

**Stream validation before any E.2 exposure**, two-sided, on each of
1009/1013/1019: A10-class scans pass; OracleFull certifies with the
marker at composite level under P004/θ_comp; OracleIdent certifies the
marker (reachability re-confirmed per stream — an oracle failure on a
new stream is an apparatus stop, not a threshold adjustment);
ClusterRelabel and every control certify nothing; the STOP-era cluster
regression form holds; no bare P4 certifiable. Any failure is an
apparatus stop before EXP2 begins.

## 4. Candidate E.2, design frame

Candidate E's frozen machinery plus proposer-side changes confined to
the three named targets in §1 — evidence-use changes only (e.g.
attribution disambiguation from already-collected pair evidence;
membership resolution timing; coverage-preserving respell), no new
authority, no budget change. The full mechanism specification and its
hyperparameters are fixed by a pre-freeze amendment to THIS
preregistration after development on streams 997–999 only (the EXP1
pattern: dev findings supersede by dated amendment, original text
retained; the freeze digest covers the final design). A12 both
directions unchanged: decoy inventory spanned, generated, scored by the
same normal-form arithmetic, counts logged.

## 5. Endpoints and verdict mapping (evaluated by frozen certify_p004)

- **Primary:** the Level 3 marker — a certified P004 unit with top
  production outside {P1, P2, P3, P8} — in ≥ 3 of 5 training seeds
  (301–305), a seed counting iff the marker fires on ≥ 2 of 3 verdict
  streams (1009/1013/1019).
- **Secondary, always reported:** (1) both (d) branches at designed
  sites (body-edit; split-or-genesis with the EXP1 structural note
  standing); (2) per-cell transfer with counts, D–E standalone;
  (3) every stratum, never merged; (4) MDL totals vs oracle and
  cluster; (5) decoy counts (adopted expected 0); (6) composite-share
  distribution of all attribute composites vs θ_comp; (7) the
  exploration-action distribution check of §2.
- **Verdict:** EXP2-POSITIVE (primary met, V-pass sustains — feeds the
  WO's exit 1); EXP2-QUALIFIED (primary met, named narrowing);
  EXP2-PARTIAL (certifications without the marker at threshold);
  EXP2-NEGATIVE (no marker at threshold — failure re-localized, next
  step preregistered or impossibility case built); APPARATUS-INVALID
  (stop, preserve, report).

## 6. Discipline

E.2 frozen by digest before its first scored run; development on
997–999 only; verdict streams 1009/1013/1019 generated only at their
validation step and never touched by any contender before the freeze;
no mid-run changes; every positive gets the full falsification pass —
now including the composite blade as binding, the attributed-classes
sensitivity as a standing check, and the exploration-distribution
comparison — before any verdict. DECISIONS.md appended at this
preregistration, at the design amendment, at the freeze, and at the
verdict.

---

## AMENDMENT 1 (2026-08-30, development-stage, committed BEFORE the digest
## freeze and before any verdict stream exists — invariant (c) intact)

Development on streams 997–999 only. The §4 design frame is filled in as
follows; budgets identical to Candidate E throughout (§2 holds: no step,
proposal, beam, batch, or schedule constant changed).

### A1.1 Candidate E.2, final design (l3_5/candidate_e2.py)

Candidate E's frozen machinery (subclass; candidate_e.py untouched at
its digest) plus:

- **M1 — soaked-pair guard.** Soaked-grind observations (discarded
  outright by E) are recorded as condition-level evidence; at unanimous
  support (>= 3 events, single outcome — frozen constant) ONE P6 rule is
  proposed: expr None, mode sym, cond ("either", {soaked}), the observed
  outcome. It rides its own single-op batch (a growth-batch rejection
  cannot take it down atomically — dev 997 finding), adoption confirmed
  in batch_result and retried until admitted. Membership-free,
  conflict-free (adopted attr pair rules exclude soaked), kept out of
  the aprule mirror (emit kind "guard" is a no-op) so pair exploration
  is unaffected.
- **M2 — two-probe identification.** Probe order (tap, soak, heat):
  tap reads (a1, a2), soak reads a3 (published F1 structure), so
  tap+soak determine the full vector and any not-yet-known kind must
  conflict on one of them. Tier-1.5 asserts after those two probes when
  exactly one class fits every observed cell perfectly and every other
  class conflicts; otherwise the full signature and genesis proceed
  unchanged. Capture masks are E's; only probe order and the
  early-assert pass are new.
- **Measured out and excluded:** a 2-cell cracked assert against mapped
  cohort signatures raises raw accuracy (post 0.76 on dev 997) but
  routes cracked resolution through class rules and thins the attribute
  composite's ablation margin below delta_b (b 0.023–0.041 with it vs
  0.05+ without; marker 0/6 with, 15/15 without). Excluded from the
  frozen design; recorded here because the trade — world performance
  against certified-unit load-bearing — is itself a finding.

### A1.2 Dev results at this amendment (P004 machinery, theta_comp 0.4022)

Marker fires 15/15 (seeds 301–305 x dev 997/998/999) at COMPOSITE level;
best composite shares 0.273–0.377 vs theta_comp 0.4022; soaked-pair
abstention eliminated by the guard on all runs; steady-state residual is
the early-query identification floor (queries at steps <= 12 preceding
the 2-probe-per-object schedule) plus the D/E-style collisions that
genuinely need a third probe.

### A1.3 Everything else

Endpoints, verdict mapping, stream draw (1009/1013/1019 by the §3 rule,
still ungenerated), validation protocol, and the falsification-pass
additions are unchanged from §3–§6.
