# CRUCIBLE

CRUCIBLE is a preregistered, adversarially validated instrument for
certifying **concept invention**: a frozen deterministic world plus a
substrate with no learner prediction channel, under which a learning
system's only output is operations on an inspectable concept library,
and five criteria — named-and-inspectable, load-bearing under ablation,
paid-for under a frozen MDL accounting, revised-not-replaced, reused
across a distribution shift — were committed verbatim before any code
existed. The certified result: contender **E.3** invents attribute-like
units by compression competition against ~1,200 generated decoys per
run (zero adopted), transfers them to held-out object-pair interactions
its experience never contained, and clears an abstention bar derived
from an honest reference before the contender existed — 20/20 runs
across five seeds and four rule-drawn, never-exposed streams,
deterministic, replicated byte-for-byte in a clean environment. What
this is **not**, in the programme's own preregistered words: *"The
maximum claim at full success … is: 'under a frozen synthetic world
with substrate-guaranteed bookkeeping, a system invented, revised, and
reused inspectable concepts satisfying preregistered criteria that
cheap controls fail.' Nothing in this programme demonstrates AGI,
general reasoning, or an LLM replacement, and no report may imply it."*

## Replicate it

```
make replicate        # or: python3 replicate.py
```

Stock Python 3.12, zero dependencies, no network. Expected output: a
PASS line for the corpus fingerprints (10 streams) and for each of the
three verdict artifacts — the E.2 scored matrix, the P004 replay of
Candidate E (the retraction artifact), and the E.3 matrix with its
prediction evaluation — ending `TOTAL: PASS` in roughly 2–4 minutes on
a modern CPU. `make verify` checks every file in this repository
against `MANIFEST.json` by SHA-256.

## Why you can trust the instrument: it retracted its own team first

Before any external reviewer saw this work, the test took back its own
team's first positive result. Candidate E certified the Level 3 marker
under the then-frozen criteria and survived that era's falsification
pass — and a subsequent falsification-pass extension showed the
certification depended on a scope hole: the abstention blade could not
reach the unit granularity the marker certified at, while the designed
reach (the composite) failed it at roughly 0.60 against an honest
oracle near 0.15. The operationalization was amended (preregistered
formula committed before the reference measurement existed), the
archives were replayed, and the result was relabelled negative — the
corrected bar rejecting the very contender whose false positive
motivated it (0.56–0.70 vs the new bar of 0.4022). Only substantive
changes (E.2, then E.3 with a preregistered mechanism prediction,
confirmed 20/20) cleared it. Every step of that history is in
`preregistrations/` and `artifacts/`, unedited.

---

## The challenge

The bar is precise, and it is open:

- **Certify the Level 3 marker at composite level under P004**: a
  certified unit whose top production lies outside the initial
  inventory {P1, P2, P3, P8}, where attribute content certifies only as
  its declared composite (attribute + attributions + referencing
  rules).
- **Composite abstention share ≤ θ_comp = 0.4022** (frozen constant,
  derived by preregistered formula from the identification oracle's
  measured reachability before any contender existed), alongside the
  frozen criteria thresholds (δ_b 0.05, δ_e 0.05, θ_ev 0.15, f_d 10%,
  τ_d 0.05, α 0.05).
- **Fresh rule-drawn streams**: extend `artifacts/EXPOSURE_LEDGER.md`
  by its stated rule, validate each stream two-sidedly (both oracles
  certify; all eight controls certify nothing; the cluster regression
  form holds) before your contender sees it.
- **Falsification pass required**: determinism, independent
  (d) re-derivation from raw logs, control ceilings, decoy accounting,
  the attributed-classes sensitivity, and an exploration-distribution
  report against the E lineage if you claim budget parity.

**Implementing a contender**: subclass or replace the policy interface
in `crucible/engine.py` — `begin_run / begin_episode / observe /
learner_action / step_membership_ops / boundary_batches /
batch_result`. Your contender proposes library operations; the
substrate predicts, prices, and logs. It never sees kind labels, and
neither do you at run time: the scoring is decided by the frozen
certifiers in `certifiers/`.

## Repository map

```
crucible/          the frozen world + substrate (generator, dynamics,
                   grammar, MDL pricing, engine, audits, planted-leak
                   fixtures, trace checker, control policies)
certifiers/        certify_p003.py, certify_p004.py (and the STOP-era
                   certify.py kept as the regression form)
contenders/        the certified lineage: proposer.py (D),
                   candidate_e.py, candidate_e2.py, candidate_e3.py,
                   plus two clustering controls
preregistrations/  P001–P004 and the EXP1/EXP2/EXP3 preregistrations
                   with amendments — verbatim, append-only history
artifacts/         scored matrices, validation records, falsification
                   passes, freeze manifests, the exposure ledger, the
                   replication report, the retraction analyses
runners/           the frozen drivers and stream validators
L3_0_SPEC.md       the world + substrate specification (v0.4, the L3-1
                   freeze revision) — design rationale; on any
                   discrepancy the frozen code and manifest win
L3_0_THREAT_MODEL.md  the generator-leakage threat model (v0.3,
                   pre-code) the audits were built against
ERRATA.md          corrections to the record that alter no frozen byte
replicate.py       the one-command replication (above)
selfverify.py      manifest check
```

## Limitations (condensed from the paper §7)

One world with one designed factoring, authored by the criteria's
authors; an authored grammar with priced primitives ("zero given
ontology is impossible; minimal and explicit is the standard"); thin
binding margins (7–25% relative headroom; ~3× the honest oracle on the
strictest sensitivity); revision demonstrated by the body-edit branch
only — the invented units themselves never faced designed
contradiction; single-experimenter closure (this release exists to
change that); and the scope sentence: this concerns concept formation
inside CRUCIBLE, not open-ended learning.

## Paper

[placeholder — arXiv link on publication]

## Reporting a break

Finding a leak the audits miss, a cheap policy that certifies, or a
scope hole in the blade is a **contribution, credited** — it is exactly
how this instrument improved twice before release. Open an issue with
the seed(s), the policy or analysis code, and the certification output;
if it stands, it enters the failure record with attribution and forces
a preregistered amendment, the same process the history in
`preregistrations/` documents.
