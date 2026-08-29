# EID-L3 Phase L3-0 — Generator Leakage Threat Model (v0.3, pre-code)

**Status:** companion to `L3_0_SPEC.md` v0.3. v0.3 changes (keyed to the clearance
condition and the spec's §0a): A6/T8 scoping and A10 scans re-anchored to the decoupled
events — weathered arrivals begin at **E_C**, the kind shift at **E_R**, and A6's
invisibility claim binds E_R only (C1); A16 extended with the batch-atomicity/fit check,
the genesis-reachability check, and the membership-evidence arithmetic (C2, C3); T11 notes
that the C2 admission amendment introduces **no** new tunable constant. v0.2 changes
(keyed to the gate verdict): T7 extended to weathered-arrival novelty flags (R1); T8
extended with the A6 side-channel scoping and the cracked-cell alphabet constraint (R1);
T10's counting argument repaired at the kind level with the decoy table (R4); A5 and A12
extended to the decoys (R4); **A16 added** — revision-reachability arithmetic (R1).
Everything else is unchanged from v0.1.

**Why this document exists.** The charter states it directly: this generator is a larger
leak surface than Horn clauses. CRUCIBLE has more channels than CPL-009's program graphs —
appearance, condition, ambient events, episode composition, co-occurrence scheduling, an
outcome alphabet, and a shift schedule — and every one of them is a place where the answer
can leak into a cue that a non-concept-forming policy reads off. The two reference cases
below cost this programme, respectively, a full phase's headline results and a full
benchmark version. Every threat here is written against them.

**Reference case 1 — CPL-007 (Phase I/II autopsy).** Leakage through *symbol spelling*:
lexicographically ordered indices correlated with the answer, and index-ordered scalar
channels encoded node identity; separately, a symmetrised adjacency made valid and invalid
inference byte-identical. Lesson: identity carriers (names, indices, orderings) leak unless
randomized per-instance, and a representation choice can silently destroy the distinction
under test.

**Reference case 2 — CPL-009 v0.1 (withdrawn benchmark).** Every whole-case surface
feature sat at exactly the 0.5000 majority baseline — and the benchmark was still solvable
by counting graph edges, because the audit was case-level while the exploit was
decision-level: at 12/12 on-spine decisions the correct successor was the unique
highest-in-degree sibling. Lesson: **a benchmark probed for leakage only at the label level
has not been probed.** Audit at the unit the policy acts on. Corollary (from the v1.0
redesign): make a cue impossible by construction, not merely weak by measurement — patching
one statistical cue re-exposes another.

**Standing posture.** Expect the apparatus to be the bug. Most major CPL findings were
defects in the investigator's own new machinery, caught because deterministic oracles had
to pass first. Every audit below is decision-level (the scored-query unit) unless stated.

---

## Threat register

Each entry: the leak, the reference failure it rhymes with, the construction-level
mitigation (impossible-by-construction where achievable), and the L3-1 audit that verifies
the construction. Audits A1–A7 are defined in `L3_0_SPEC.md` §6.4; audits A8+ are
introduced here and join the L3-1 gate.

### T1 — Object tokens encode kind
Token assignment order correlated with kind (e.g. kinds sampled in a fixed order, tokens
assigned sequentially) would make `o0`'s number informative. *Reference: CPL-007
lexicographic/index leaks.*
**Construction:** tokens are a fresh random permutation per episode, drawn from an RNG
stream independent of the kind-assignment stream.
**Audit A8:** decision-level probe: token index as predictor of kind and of scored-query
outcome, must sit at the declared chance floor across all strata.

### T2 — Appearance carries kind information
The obvious leak: any statistical dependence lets clustering-on-appearance impersonate
concept formation. *Reference: CPL-008's nuisance channel, inverted — there the channel had
to be ignored; here it must be information-free.*
**Construction:** appearance is drawn iid uniform from a stream independent of kind — MI is
zero by construction, not by tuning.
**Audit A4:** appearance-feature probes at exactly chance on every stratum, for outcome and
for kind; plus a generator unit test asserting stream independence (seed surgery: redraw
appearance, verify kinds and dynamics byte-identical).

### T3 — Positional and episode-composition leaks
Kind inferable from slot position in the object list, from episode composition (e.g. "every
episode has exactly one α3-object"), or from arrival order. *Reference: CPL-007 ordering
leaks.*
**Construction:** object list order is an independent random permutation; kind sampling is
iid per object (no per-episode quotas), subject only to the co-occurrence constraint (T7).
**Audit A8 (extended):** position and composition-count features probed at the scored-query
unit.

### T4 — Condition history as a kind fingerprint visible to static features
Condition is honest state, but a *static* predictor could read condition as a proxy for
kind (charred ⇒ was ignitable) without any concept formation. This is not a leak to
eliminate — condition dynamics are the world — but a cheap-control surface to measure.
**Construction:** none (it is legitimate structure).
**Audit:** the static condition/appearance learner is a named §6.3 cheap-ceiling contender;
criteria thresholds are set above its measured ceiling. The scored-query design includes
pristine fresh objects, where condition carries nothing.

### T5 — Ambient process leaks kind directly
The ambient process is kind-biased *by design* (the causal trap). The leak variant: the
learner observes which objects the ambient process targets and reads targeting as a kind
label without doing any causal work — ambient targeting becomes an oracle.
*Reference: v0.1's "the generator's own scheduling is a cue" family.*
**Construction:** ambient bias magnitudes are moderate (frozen at L3-1), so targeting is a
noisy cue, not a label; and scored queries include fresh objects never yet targeted.
**Audit A9:** ambient-targeting-count features join the decision-level probe set; the
ambient-correlational control (A7) measures exactly how far this cue carries, and criteria
thresholds must clear it.

### T6 — Global time / schedule leaks
Episode index or step counter would let a policy special-case the preregistered E_R without
detecting contradiction. *Reference: harness-neutralizing-the-bug, CPL-005 family.*
**Construction:** no episode index, no global counter, no schedule information in any
observation (§2.1). The learner can count episodes itself — that is memory, which is
legitimate — but nothing marks E_R.
**Audit A6:** shift invisibility (spec §6.4).

### T7 — Co-occurrence holdout leaks through its own absence
The held-out pair cells are detectable pre-shift: a learner can notice that kinds i and j
never share an episode. This cannot *predict* the held-out F2 outcome (which is the scored
quantity), but a control could use "never co-seen" as a novelty flag to hedge differently
on first-co-occurrence queries.
**Construction:** holdout is enforced by episode composition (learner constraint-free);
first-co-occurrence queries are scored identically for all policies, so hedging shifts the
floor for everyone or no one.
**Audit A10:** verify the enforcement (zero held-out co-occurrences pre-E_R across the full
generated corpus, by scan) and report the co-seen-count feature in the decision-level probe
set, so the size of the novelty-flag effect is measured rather than assumed away.
**Extended (v0.2, R1; re-anchored v0.3, C1):** the same treatment applies to the second
designed novelty channel, weathered arrivals (`cracked` objects, spec §2.6): verify by
scan that zero cracked arrivals occur **pre-E_C** (the events are decoupled — E_C default
300, E_R default 400), and add the condition-novelty flag ("first cracked object seen")
to the probe set so its hedging value is measured, not assumed away.

### T8 — Outcome-alphabet reachability signatures
If an outcome symbol is reachable only post-shift, or only for k_new, its first appearance
is a shift beacon and a family label. *Reference: spelling-derived leaks — identity carried
by vocabulary usage.*
**Construction:** F1/F2 tables are built under the constraint that k_new's outcomes are all
outcomes some K0 kind already produces (k_new is a new *combination*, not a new vocabulary),
and pre/post outcome marginals per action are matched within a declared tolerance.
**Extended (v0.2, R1):** the same constraint binds the condition-revelation cells — cracked
behavior draws only on outcomes the pre-shift world already produces.
**Audit A6 (extended in v0.2; scoped to E_R in v0.3, C1):** classifier probe on
outcome-frequency windows pre/post **E_R** must fail to locate the kind shift above
chance, excluding windows containing the prediction failures themselves. Scope, per spec
§3/§6.4: A6 targets the **side channels** (appearance, ambient rates, outcome
frequencies, episode shape) and binds **E_R only** — E_C is a declared, visible novelty
event by construction and A6 makes no claim about it. The designed novelty channels —
first co-occurrences, weathered arrivals at E_C, and k_new's own prediction failures —
*are* the test content, are necessarily observable, and are handled by T7/A10's
novelty-flag measurement instead, so their observability is priced rather than pretended
away.

### T9 — RNG stream coupling
One RNG feeding kinds, appearance, tokens and schedule couples channels that are
independent on paper — the classic silent correlation. *Reference: CPL-008B's index-ordered
scalars, an accidental coupling of identity and value.*
**Construction:** named, separately literal-seeded streams per channel (kind, appearance,
token-permutation, ambient, schedule, query design); `hash()` never used for seeds
(programme rule); `PYTHONHASHSEED` invariance measured at three values from day one.
**Audit A11:** seed-surgery tests — redraw any single stream, verify all others'
outputs byte-identical; regeneration byte-identity across interpreters.

### T10 — Meta-grammar smuggling (the L3-specific leak)
The experimenter writes both the generator and the grammar; P4–P6 exist because the
generator is attribute-factored. Worst case, the grammar is a keyhole shaped exactly like
the answer and "invention" is reading the keyhole. *Reference: none in CPL — this threat
class is new at Level 3 and is the biggest single risk in the programme.*
**Construction:** grammar frozen at L3-1 before any contender; expressible space large
relative to the true structure at the *instance* level (the L3-1 audit includes the
counting argument: the number of admissible attribute structures, refinements and rules the
grammar can spell vs. the one the generator uses) **and, since v0.2, at the *kind* level
(R4)** — the non-initial production space now contains both rewarded and unrewarded
structure:

| Non-initial kind | Rewarded by this generator? |
|---|---|
| P4 `Attr` / P5 `AURule` / P6 `APRule` (sym mode) | yes — the generator's own factoring |
| P7 `CondClass` | workable, strictly costlier than cond_pattern narrowing (spec §2.6) — live alternative |
| P3/P6 ord mode (order-sensitive pair rules) | never — F2 is symmetric (decoy) |
| P9 `HRule` (history-conditioned rules) | never — memoryless given condition (decoy) |
| P10 `CountClass` (interaction-count classes) | never — dynamics never read counts (decoy) |

The marker is defined over *any* non-initial production, not the intended one, and firing
it now requires selecting rewarded structure from a space that also offers generically
attractive dead ends.
**Audit A12 (extended in v0.2):** the L3-3 proposal mechanism's move-type inventory is
audited in writing before training, in both directions: for generator-shaped special cases
("propose a 3-bit attribute vector over classes" would be a smuggled answer; "propose any
grammar-legal term" is not), **and for a suspiciously-shaped inability to propose the decoy
kinds** — a proposer that cannot spell P9/P10/ord terms has been shaped by knowledge of
what doesn't pay, which is the same leak in reverse. Recorded as a standing review item at
every gate.

### T11 — MDL constants tuned toward the intended winner
Description-length prices chosen so the attribute factoring wins by construction rather
than by compression. *Reference: harness-neutralizes-the-bug family — the metric embeds
the conclusion.*
**Construction:** all costs derived mechanically from declared alphabet sizes (§4.5), no
per-production hand prices; frozen at L3-1 before contenders. The v0.3 admission amendment
(C2) deliberately introduces **no** overdraft or threshold constant — an admission
tolerance would have been exactly the kind of tunable this threat polices, and it was
considered and discarded for that reason (spec §0a).
**Audit A13:** sensitivity report — oracle-library vs. cheap-library MDL ordering must be
stable under ±2-bit perturbations per concept and under ε an order of magnitude either way.

### T12 — Scored-query design favors the intended concept structure
Query stratification (first-co-occurrence, fresh objects) is chosen because it is where
concepts pay; a hostile reading is that scoring is aimed where the intended winner shines.
**Construction:** the design is uniform-interventional within strata, identical for every
policy including all controls; strata are preregistered here, before any contender; all
strata are always reported (never merged — the 009B profile lesson).
**Audit:** the vacuity gate itself (A1–A3): if cheap policies clear criterion thresholds on
the full stratified stream, the task, not the controls, is declared wrong (charter L3-2
STOP semantics).

### T13 — Learner-driven exploration contaminates evaluation
A contender that explores adversarially could shape its own future scored stream (e.g.
grinding objects to change conditions before queries). *Reference: harness contamination,
CPL-006.*
**Construction:** scored queries are substrate-scheduled with pre-drawn designs; the
query's (object, action) draw is independent of history where the stratum permits, and
condition-at-query is recorded and reported per stratum. Controls and contenders face the
same scheduler with the same literal seeds.
**Audit A14:** replay determinism of the scored stream given the event log; cross-policy
diff of scored-stream designs must be empty at matched seeds and stated strata.

### T14 — Dual-use of the event log (training on the test)
All streams pass through one substrate; a bug could let proposal evaluation peek at future
events or at scored-query outcomes before prediction. *Reference: v0.1's audit
granularity — the exploit lived below the audited unit.*
**Construction:** prequential discipline is structural — the library that predicts step t
is the library as of t−1; admission replay uses only past events; the substrate API has no
read path to undisclosed future state.
**Audit A15:** substrate invariant tests: attempt-to-peek unit tests plus byte-replay of
the full MDL/score ledger from the event log alone (§10 replay identity).

### T15 — The verifier is the bug
The audits above are new machinery, and new machinery is where CPL found most of its
defects (the 009B kind-blind sentinel probe reported spurious 0.73–0.84 leakage before
being made kind-aware). *Reference: 009B §N, explicitly.*
**Construction/response:** dual implementation of dynamics with byte-agreement (§10);
probes written kind-aware from the start (features only probed where they apply to the
query type); every probe validated on planted-leak fixtures — a deliberately leaky
mini-generator variant where the probe *must* fire, so silent-pass probes are caught (a
probe that cannot detect a planted leak certifies nothing).

---

## A16 — Reachability arithmetic (new in v0.2, R1; extended in v0.3, C2/C3)

Not a leakage audit but a *reachability* audit, run at L3-1 before any contender exists:
verify by ΔMDL computation, at the frozen parameters and under the §4.5 pricing, that

1. **the body-edit branch is optimal where designed (site: E_C):** for each designated
   condition-revelation cell (spec §2.6), narrow-the-existing-rule-plus-add
   (`REVISE` + `NEW`) strictly beats every alternative repair — do-nothing, add-only,
   narrow-only, the P7 shadow route, and retire-and-respell — at the scheduled
   weathered-arrival frequency;
2. **the split-with-continuity branch is optimal where designed (site: E_R):** the
   formalized split (`REVISE(C_old, move-members)` + `NEW(C_new)`, spec §5.4) strictly
   beats retire-and-respell and do-nothing for the k_old-covering concept;
3. **the factoring transition fits one atomic batch (C3):** the complete class→attribute
   transition (Attrs + attributions + AU/APRules + retires) is counted in ops at the
   frozen library sizes and shown ≤ the per-batch op limit, so the marker's target
   structure is not unreachable for budget reasons;
4. **genesis is reachable (C2):** the class-genesis sequence from an empty library has a
   finite, computed MDL payback horizon at the frozen prices under the v0.3 admission
   semantics — i.e. the arithmetic that deadlocked v0.2's strict-decrease rule is shown
   resolved, not assumed resolved; and
5. **the membership-evidence arithmetic is a computed number:** the number of observed
   interactions after which a membership assertion's lifetime rent turns positive at the
   frozen prices (≈ ⌈assertion cost / log₂|O|⌉ events) is computed and reported, so the
   identification burden is a number, not a hope.

Failure of checks 1–4 fails the L3-1 freeze: each would mean a criterion is being graded
on a branch or a structure the world never makes reachable — the exact defect family the
gate review identified in v0.1 (R1). The computation is analytic (deterministic world,
declared pricing), so this audit has no measurement noise; it is arithmetic that either
holds or does not.

---

## Audit roll-up for the L3-1 gate

| Audit | Verifies | Threats |
|---|---|---|
| A1–A3 | headroom, identification, lookup-fails arithmetic with preregistered gap floors (vacuity) | T12, crux 9.1 |
| A4 | appearance null by construction | T2 |
| A5 | decision-level cheap-feature sweep at the scored-query unit; extended to history, count and pair-order features (decoys measured unrewarded) | T1–T5, T7, T10 |
| A6 | shift invisibility on side channels incl. outcome-marginal matching (designed novelty channels scoped out, priced under A10) | T6, T8 |
| A7 | causal trap has teeth (ambient-correlational gap) | T5, §2.4 |
| A8 | token/position/composition probes | T1, T3 |
| A9 | ambient-targeting features probed | T5 |
| A10 | holdout + weathered-arrival enforcement scans; co-seen-count and condition-novelty probes | T7 |
| A11 | RNG stream independence by seed surgery; interpreter invariance | T9 |
| A12 | proposal move-type inventory review, both directions incl. decoy proposability (standing, per gate) | T10 |
| A13 | MDL sensitivity | T11 |
| A14 | scored-stream determinism and cross-policy identity | T13 |
| A15 | prequential no-peek invariants; ledger byte-replay | T14 |
| A16 | reachability arithmetic: both (d) branches optimal at their sites (E_C, E_R); factoring fits one batch; genesis reachable; membership-evidence number computed | R1, C2, C3 (spec §2.6, §4.5, §4.7, §5.4) |
| — | planted-leak fixtures for every probe | T15 |

**Gate rule (inherited):** any audit failure after freeze is a stop condition — preserve
state, report, wait. Any cue found above floor is repaired by construction and the audit
re-run in full, never patched by measurement; superseded audit outputs are preserved and
relabelled, never deleted.
