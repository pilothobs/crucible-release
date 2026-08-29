# EID-L3 Phase L3-0 — World and Substrate Specification (v0.4, at the L3-1 freeze)

**Status:** v0.4 is the L3-1 freeze revision: it consolidates the build-phase amendments
that the audits forced, each declared in §0 with the measurement or arithmetic that forced
it, all before any contender exists. The frozen truth is `l3_1/MANIFEST.json` + the code
it certifies; this document is the design rationale, and on any discrepancy the manifest
wins and the discrepancy is a finding. History: v0.1 REVISION REQUIRED (R1–R6, §0c);
v0.2 revision; v0.3 cleared to L3-1 with the E_C condition plus two pre-code findings
(§0b). The full text of every version goes in the gate package for diff against its
change log.

**Governing preregistration:** `PREREGISTRATION_001_CONCEPT_CRITERIA.md`, committed at
`c780b02` before any spec text was written. The five criteria (a)–(e) and the Level 3
marker are frozen; this document supplies their operationalizations (§5), which freeze at
the L3-1 gate. The preregistration file is append-only and is untouched by this revision.

**Design law, inherited from the CPL programme:** structure defines what is legal; learning
decides what to do. Properties that are theorems about the system go in the substrate; only
judgment is learned.

---

## 0a. v0.4 change log (L3-1 build-phase amendments, each forced by an audit)

Every entry follows the same pattern: the audit machinery fired or a measured number was
wrong, the design was repaired **by construction**, and the audit re-run in full. The
detailed evidence trail is `L3_1_REPORT.md` §Defect-log.

| # | Amendment | Forced by |
|---|---|---|
| D1 | **P7 rank privilege removed** — all non-default rules share one rank; P7 becomes a genuine decoy (strictly dominated by cond_pattern masks). §2.6's repair table updated: the P7 shadow now *conflicts* (unresolved) instead of shadowing. | A16 check 1: with the privilege, the CondClass shadow (≈31 bits) beat the designed body-edit (≈36 bits) — (d)'s REVISE branch was again not optimal |
| D2 | **T = 32 steps** (20 learner + 4 ambient + 8 scored; was 24 = 12/6/6) | A16 check 4: at T=24 honest per-object rent ≈ +0.4 bits (noise); at 32 ≈ +6.35 bits. A7: more than ~4 ambient steps saturates the targets and the confound drowns in nulls |
| D3 | **tap reads (α1, α2) with four outcomes**; cracked-tap outcomes swapped so every kind still differs at E_C | A2: α1-only tap concentrated outcome marginals and majority-guessing compressed the identification margin to 0.119 |
| D4 | **soaked is transient** (tap dries; heat already dried) | A7: the world's steady state under exploration was "everything is wet"; the confound and the transfer stratum both drowned in trivial nulls |
| D5 | **holdout selected by rule from a literal seed** (gate-hold check 3, T12): eligibility constraints H1 connectivity, H2 no-beacon (T8), H3 outcome balance (≤ 2 of 4 cells share an outcome), H4 split-family contact (≥ 1 cell contains k_old), stated first; canonical ordering; choice = eligible[SEED_HOLDOUT mod 57]. Derived set **{A-B, B-C, B-E, D-E}** (2× fuse, 2× crumble) — *different* from the interim hand-pick, accepted as drawn. The F2 region map duplicated for the rule is asserted against the real dynamics cell-for-cell at import | A1: the first hand-drafted holdout had 3/4 fuse cells — a majority-guess control hit 0.833 on the transfer stratum (post-fix: that control scores 0.000 on fc_unseen). The rule replaces hand-picking so the fix is a construction, not a search |
| D6 | **post-E_R kind weights marginal-matched** to the measured pre-E_R rejection marginals under the derived holdout (A .3009, B .0330, C .3007, D .1985, E .1669; B sits in three held-out cells), frozen as literals | A6: naive uniform post weights made the K0 marginal jump at E_R — a real side channel (rejection sampling skews marginals hard) |
| D7 | **hypothetical transfer queries** (§6.1): held-out-cell grind queries under stated pristine conditions, scored against the generator outcome, never executed, never revealed, no state change; stratum = fc_unseen (cell never ground this run, policy-dependent n, always reported) vs fc_seen | two executed designs failed with evidence: at step 3 the stratum measured identification (oracle-with-identification 0.083); at step 19 it collapsed to soaked-null (cheap control 0.75) and executing handed the memorizer the withheld datum |
| D8 | **A6 statistic**: permutation test on pre/post centroid distance over per-action unary outcome conditionals (side channels); grind channel scoped to Shift-T pricing | leave-one-out nearest-centroid anti-predicted at n=10 (returned 0.1 on identical distributions); joint frequencies were distorted by the audit's own exclusions |
| D9 | **A9 probes late-step rows**; the PL3 fixture is **structural** — the kind-excess *magnitude* cannot separate the declared confound from a planted label (measured differential 0.045 on matched windows: silent), so the fixture fires on the cross-type targeting-overlap rate: real draft-heat and rain-soak target different attribute sets (overlap only on rare B, measured rate ≈ 0.21), a planted single-kind label targets one kind for both (measured 0.775); fire iff Δ > 0.15 | the early-row probe diluted the planted leak into silence (T15); then the magnitude-differential fixture was itself measured silent — two iterations of the same lesson: a fixture must be shown to fire, not assumed to |

Gate outcome at this revision: **A1–A16 all PASS, all five planted leaks FIRE**,
manifest self-verifies. Thresholds ⟨L3-1⟩ are frozen in
`PREREGISTRATION_002_L3_1_FREEZE.md` §3.

## 0b. v0.3 change log (post-clearance condition + pre-code findings)

| Item | Disposition | Where |
|---|---|---|
| **C1 — E_C/E_R decoupling** (the gate condition) | **Done.** Weathered arrivals begin at their own preregistered episode **E_C (default 300)**, distinct from **E_R (default 400)** where k_new enters and the co-occurrence holdout opens. A6's invisibility claim is scoped to E_R; the condition novelty at E_C is inherent-and-declared, priced by T7/A10's novelty-flag measurement rather than pretended invisible. Criterion (d) is now tested twice on different branches — body-edit at E_C, split at E_R — strictly stronger evidence than one compound event. | §2.6, §3, §6.4 (A6), §8; threat model T8/A10/A16 |
| **C2 — admission semantics: genesis deadlock found by arithmetic, declared pre-code** | Working confirmation 2's membership-evidence arithmetic before building exposed a structural defect in v0.2's strict-decrease admission: **the empty library is an MDL local minimum.** Objects are episode-scoped, so hypothetical replay can never credit a new class's rules against past episodes' expired objects (no historical memberships exist to carry them); a genesis batch (class + rules + memberships ≈ 90 bits at §4.5 prices) can recoup at most ≈ 48 bits from current-episode evidence at §8 scale. Strict-decrease admission therefore rejects **every** first concept, and the library can never grow — the same family of composed-interface defect as R2. **Fix, introducing no tunable constant (T11-clean):** admission gates are grammar-legality and proposal budget only; batch ΔMDL is computed by replay, returned to the learner (R3), and recorded in the admission record — **accounting, never a gate**. "Paid for" lives entirely in criterion (c)'s lifetime prequential rent check, which was always the forward-looking, binding test. Consequences accepted and declared: the v0.2 "guessing never enters" corollary is retired — wrong assertions now *enter and are punished* (≈ 13.3 bits per contradiction, violations logged, retraction available), which is the honest mechanism; junk admission is bounded by the op budget and fails (c). A rejected-batch overdraft constant was considered and discarded as a tunable that T11 would then have to police. | §4.5, §5.3, §9.4; threat model A16 |
| **C3 — batch op limit 16 → 96** (from confirmation 1's arithmetic) | The full class→attribute factoring transition at §8 scale is ≈ 84 operations (3 `Attr` + ~18 attributions + ~17 `AURule`/`APRule` + ~46 retires). v0.2's 16-op batches made it unreachable in one atomic batch — exactly the failure mode the verdict told A16 to catch. Budget is now **4 batches × ≤ 96 ops per boundary**; batches remain atomic (evaluated and applied as a unit, never transiting a conflicted intermediate library). A16 gains the explicit check that the transition fits one batch at frozen sizes. Membership ops are also confirmed legal *inside* structural batches (splits move members). | §4.7, §8; threat model A16 |

Both C2 and C3 are products of the arithmetic the clearance verdict asked A16 to verify;
they are declared here, before any code exists, rather than discovered mid-build. The full
v0.3 text accompanies the L3-1 gate package for line-diff against this log.

## 0c. v0.2 change log (gate revision round 1)

| Item | Disposition | Where |
|---|---|---|
| **R1** revision reachability (blocking; subsumes gap 1) | **Done.** (a) Split semantics formalized: `REVISE(C_old, move-members)` + `NEW(C_new)` in one batch is a revision *of C_old*; C_old keeps name, admission record and prequential clock, C_new gets a fresh admission. (b) Condition-revelation element added: `cracked` is producible by no transition — arrival-only, scheduled post-E_R — and §4.4's rank semantics are changed so cond_pattern narrowness confers no rank, making narrow-the-existing-rule (a body-edit REVISE) the arithmetically optimal repair. Audit A16 added: ΔMDL dominance of both designed repairs verified before any contender exists. **Adaptation, declared:** the Director's example cell (heat on charred volatile) is learner-reachable pre-E_R, since charring is learner-producible and the learner acts freely; scheduling alone cannot hold it out. The arrival-only-condition mechanism preserves the requirement (unreachable pre-E_R by scheduling, no change to F or determinism, no restriction on learner freedom). | §2.6, §3, §4.4, §5.4, threat model A16 |
| **R2** unresolvable-world interface bug (blocking) | **Done.** Interface split: structural ops at episode boundaries; membership assertion/retraction for current-episode objects allowed per-step, MDL-charged, logged identically. Composition verified in-text: §5.4 membership-move logging unchanged; §6.1 fresh-object stratum now reported as pre-identification and post-identification sub-strata. Admission semantics for assertions clarified (replay rule, §4.5): a pre-evidence assertion has no retrospective coding benefit and is rejected by arithmetic — guessing never enters. | §4.5, §4.7, §5.4, §6.1 |
| **R3** interface law (gaps 2, 3, 7) | **Done.** Law adopted: anything derivable in principle from published rules plus the learner's own observations may be exposed; nothing else is. Proposal return = {accepted \| rejected, batch ΔMDL}. Read path added: violations attributed to any concept (id, query, predicted, observed, resolution path) — contradiction detection at E_R is now a lookup. Both declared in §7's given table. | §4.6, §4.7, §7 |
| **R4** decoy kinds (gaps 6, 9) | **Done.** F2 declared symmetric; holdout unordered. Pair rules carry a spelled order-mode {sym, ord}; ord is expressible and never pays — first decoy. Two decoy families added: P9 history-conditioned rules (world is memoryless given condition) and P10 count-based classes (dynamics never read counts). T10's counting argument repaired at the kind level; A5/A12 extended to the decoys. | §2.3, §2.5, §4.3, threat model T10/A5/A12 |
| **R5** MDL formulas now, constants at L3-1 (gaps 4, 5) | **Done.** §4.5 states the integer code (Elias gamma), per-assertion formulas, per-production spelling computation, and edit-delta pricing with the edit-<-respell invariant. §8b works the arithmetic at planned scale. The v0.1 defaults were shown **thin** (≈ +0.6 bits/object for class concepts) and, per the review's instruction, the world is grown now: 5 objects × 24 steps (≈ +3 bits/object, ≈ +9k bits over the run). Preregistered vacuity floors added to A3. | §4.5, §8, §8b |
| **R6** step accounting | **Done.** One sentence in §2.4; §8 row updated: scored queries are dedicated steps inside T, not extras. | §2.4, §8 |

Gap mapping: gap 1 → R1; gaps 2, 3, 7 → R3; gap 4, 5 → R5; gap 6, 9 → R4; gap 8 accepted
as-is (E_R numbers ride the L3-1 preregistration addendum). Protected items carried
unchanged: §4.1 (no prediction channel), the declared-confound-plus-interventional-scoring
design with A7, T15's planted-leak fixtures, §5.6's (d)-untested-never-(d)-passed
semantics, A2's oracle-with-identification, and append-only change control on the
preregistration.

One consequential side-effect of R1, declared: under the new §4.4 rank semantics, P7
(`CondClass`) stops being redundant — it becomes the *costlier live alternative* to
narrowing a cond_pattern, which strengthens the decoy/alternative structure rather than
weakening it (§2.6, §4.3).

---

## 1. Scope and phase mapping

This spec covers:

| Section | Content | Freezes at |
|---|---|---|
| §2 | The world: CRUCIBLE v0.1 (generator design) | L3-1 gate (by manifest) |
| §3 | Preregistered distribution shifts | now (structure); L3-1 (episode numbers) |
| §4 | The substrate: what it owns, the concept library, the meta-grammar, MDL | L3-1 gate |
| §5 | Operationalization of criteria (a)–(e) and the Level 3 marker | L3-1 gate |
| §6 | Evaluation protocol, controls, vacuity gate | L3-1 gate |
| §7 | The exhaustive given/learned declaration | now |
| §8, §8b | Default parameters and worked MDL arithmetic | L3-1 gate |
| §9 | Open design risks surfaced for gate review | — |
| §10 | Verification and self-verify plan | L3-1 gate |

Phase L3-1 builds this and audits it; L3-2 runs the cheap contenders that must fail; L3-3
runs one real contender. Nothing here touches the parked proof-search track or any frozen
CPL-009 artifact.

---

## 2. The world: CRUCIBLE v0.1

A deterministic, oracle-decidable object-interaction world. The name is a working label,
nothing more. Design goals, in the charter's order: hidden compositional structure;
interventions so prediction is causal; a planned shift that forces a concept split — and,
since v0.2, a planned revelation that forces a genuine body-edit (§2.6).

### 2.1 Observable sorts and alphabets (all given, all declared)

| Sort | Alphabet | Notes |
|---|---|---|
| Object token | `o0`…`oN` per episode | opaque; episode-scoped; assigned by random permutation per episode (threat T1) |
| Appearance | 3 features, each in {0..4} | drawn iid uniform, **independent of kind by construction** — a pure nuisance channel (CPL-008 lesson); carries zero information about anything |
| Condition | {pristine, charred, soaked, cracked} | observable, mutable. Objects arrive pristine pre-E_R; `cracked` is **arrival-only** (§2.6) — no action or ambient event ever produces it |
| Action (unary) | {tap, heat, soak} | applied to one object |
| Action (binary) | {grind} | applied to a pair of objects; **F2 is symmetric** (§2.3), so the pair is unordered in the world; the *grammar* can still spell ordered rules (§4.3, decoy) |
| Outcome | 11 symbols: {thud, ring, crumble, melt, ignite, hiss, fuse, repel, shatter, dissolve, null} | fixed alphabet, declared up front; not all reachable pre-shift (threat T8) |
| Ambient event | {draft-heat, rain-soak} | generator-applied actions, observed passively (§2.4) |

The learner-facing observation at each step is: the set of objects with (token, appearance,
condition), the event that just occurred (who acted, which action, which object(s), which
outcome), and nothing else. **No episode index, no global step counter, no kind, no
attribute, no generator state is ever observable** (threat T6).

### 2.2 Latent structure (generator-internal, never observed)

- **Attributes.** Three hidden binary attributes α = (α1, α2, α3). Working gloss only (the
  learner never sees these names): α1 ~ hardness, α2 ~ volatility, α3 ~ solubility.
- **Kinds.** A kind is a distinct attribute vector. Pre-shift kind set K0 = 5 of the 8
  possible vectors, chosen so that (i) no attribute is constant across K0, (ii) no two
  attributes are perfectly correlated across K0, (iii) the three held-out vectors leave
  room for the shift family and for genuinely novel post-shift structure. The exact 5
  vectors are fixed at L3-1 freeze from a literal seed.
- **Kind assignment.** Each episode's objects draw kinds iid from a fixed categorical
  distribution, subject pre-E_R to holdout rejection (§2.5). **v0.4 D6:** rejection
  skews the *effective* pre-E_R marginals (kinds in more holdout cells are rejected
  more), so the post-E_R weights are frozen as literals matched to the **measured**
  pre-E_R marginals scaled by the non-k_new share — the K0 marginal is continuous at E_R
  and carries no beacon. Kind is sampled independently of appearance, token order, and
  position (threats T1–T3).

### 2.3 Dynamics (deterministic, attribute-factored, symmetric pairs)

All outcomes are deterministic functions of attributes and condition — never of kind
identity directly, never of appearance, never of object token, never of history beyond the
current condition (**the world is memoryless given condition** — this is what makes P9 a
decoy, and it is audited, A5-ext):

- **Unary:** `F1(α, condition, action) → (outcome, condition′)`. Structure constraints,
  fixed now: `tap` and `heat` read only (α1, α2); `soak` reads only α3. Condition
  transitions are sparse (e.g. heat on a volatile pristine object → ignite + charred; soak
  on a soluble object → dissolve-class outcomes + soaked). **No F1 transition produces
  `cracked`** (§2.6). The full F1 table is written at L3-1, frozen by manifest, and
  dual-implemented (§10).
- **Binary:** `F2(α_i, α_j, condition_i, condition_j) → outcome`, **symmetric by
  declaration**: `F2(x, y) = F2(y, x)` for every argument pair. F2 depends on the pair only
  through a small set of symmetric attribute comparisons (e.g. α1∧α1′, α3⊕α3′), so it is
  **compositional by construction**: an agent that has identified per-object attributes
  from unary interactions and learned the comparison rules from *some* pairs can predict
  pairs it has **never observed**. This is the structure that makes criterion (e) testable
  and makes the Level 3 marker (§5.7) worth money under MDL. Order-sensitive pair rules
  remain *expressible* in the grammar and never pay — the first decoy (§4.3, R4).
- **Determinism and the ε-floor.** The world is deterministic. The substrate's coding
  distribution assigns each predicted outcome probability 1−ε with ε shared uniformly over
  the remaining 10 symbols (ε fixed at L3-1, order 1e-3), so contradictions cost finitely
  many bits and are logged rather than fatal.

Why deterministic: every audit standard inherited from CPL-009 (byte-exact regeneration,
oracle decidability, decision-level probes) is strictly easier to enforce, and expressive
machinery must earn its inclusion. Stochastic outcomes are a versioned extension, not v0.1.

### 2.4 Episodes, interaction, and the declared confound

An episode: N_obj fresh objects (default 5), T steps (default 32, grown twice by
audit arithmetic — §0a D2). Each step is one of three kinds, interleaved by the
substrate's schedule: a **learner-chosen action** (any action on any object/pair; every
action is always legal — there is no legality to learn), an **ambient event**
(generator-chosen, observed passively), or a **scored query** (§6.1). Scored queries are
dedicated steps *inside* T, not extras (R6): the frozen mix is 20 learner + 4 ambient +
8 scored. Ambient targeting prefers not-yet-targeted attribute-positive objects, so the
declared confound stays sharp instead of saturating (D2/D4; measured A7 gap +0.134).

**The ambient process is a deliberately declared confound.** Ambient `draft-heat`
preferentially targets high-α2 objects and `rain-soak` preferentially targets high-α3
objects (exact biases frozen at L3-1). Consequently, in passively observed data, actions
are correlated with kinds, and a correlational predictor of P(outcome | action, features)
fitted on the ambient stream inherits the confound. The learner's own chosen actions and
the substrate's scored queries (§6.1) are interventions — `do(action)` on a uniformly
scheduled (object, action) design — so **prediction is scored causally and correlational
shortcuts are burned by construction**. L3-1 must measure that this trap has teeth: a
history-correlational control must show a measured, materially nonzero gap between ambient
and interventional prediction (§6.4, audit A7).

### 2.5 Co-occurrence control (the transfer holdout)

The **unordered** kind-pair alphabet over K0 has 15 cells (F2 is symmetric, §2.3, so
unordered is the world's own granularity); the 10 cross-kind cells are the holdout
candidates. **v0.4 D5:** the holdout set H of 4 cells is selected **by rule from a
literal seed** — eligibility constraints H1 (connectivity: every F2 region keeps a
visible cell), H2 (no-beacon: held-out outcomes all visible pre-shift, T8), H3 (outcome
balance: ≤ 2 of 4 cells share an outcome), H4 (≥ 1 cell contains k_old) are stated
first, eligible subsets ordered canonically, and the choice is
`eligible[SEED_HOLDOUT mod N]` (N = 57 measured), accepting whatever the draw returns.
H is **never instantiated pre-shift**: the generator never places two objects whose
kinds form a held-out pair in the same episode.
The learner therefore cannot grind a held-out pair no matter what it chooses — the holdout
is enforced by construction, not by policing the learner (threat T7). Post-shift, held-out
pairs appear and are probed by scored queries on **first** co-occurrence, before any
experience with that pair exists. This is the unseen-combination test that criterion (e)
and the compositionality claim rest on.

### 2.6 Condition revelation (new in v0.2 — the designed body-edit, R1b)

The element that makes criterion (d)'s REVISE branch demonstrably reachable:

- **`cracked` is arrival-only.** No F1 transition and no ambient event produces `cracked`
  (constraint on the F1 table, fixed now, before the table is written). It can exist only
  as an object's *initial* condition.
- **Weathered arrivals are scheduled post-E_C only (decoupled from E_R in v0.3, C1).**
  Pre-E_C, every object arrives pristine, so every (kind, action, cracked) cell is
  **unreachable pre-E_C by scheduling alone** — no learner behavior can reach it, because
  the condition cannot be manufactured. From E_C on (default episode 300, §8), a scheduled
  fraction of objects (default 20%) arrive cracked. E_C precedes E_R (default 400), so the
  body-edit test and the split test are separate events on separate branches of (d).
- **Cracked behavior differs.** For designated cells (≥ 2 K0 kinds × ≥ 1 action; exact
  cells at L3-1), F1 on a cracked object differs from the same (kind, action) on other
  conditions, with outcomes drawn from the existing alphabet (T8 constraint).
- **Why the optimal repair is a body-edit.** The MDL-optimal pre-E_C library provably
  spells the affected rules with wildcard cond_patterns — cracked never occurs, so a
  narrower pattern buys nothing and costs bits (§4.5). Post-E_C those rules mispredict on
  cracked cells. Under §4.4's rank semantics (cond_pattern narrowness confers no rank),
  the repair options are exactly:

  | Repair | Model cost | Cracked-cell data cost per event | Measured bits (A16, per run) |
  |---|---|---|---|
  | do nothing | 0 | ≈ 13.3 bits (contradiction at ε = 1e-3) | 1462 |
  | add cracked rule only | full rule spelling | ≈ 3.46 bits (same-rank conflict → unresolved) | 402 |
  | narrow existing rule only (`REVISE`) | edit-delta | ≈ 3.46 bits (unresolved, no cracked rule) | 396 |
  | **narrow + add (`REVISE` + `NEW`)** | **edit-delta + rule spelling** | **≈ 0 bits** | **37** |
  | P7 shadow route (`CondClass` + rule) | P7 + rule spelling | ≈ 3.46 bits (same-rank conflict — v0.4 D1: P7 confers no rank) | 413 |
  | retire + respell both rules | 2 × rule spelling | ≈ 0 bits | 52 |

  Narrow+add strictly dominates every alternative (v0.4: verified by A16 at the frozen
  prices — the v0.2/v0.3 claim that it dominated *with* a rank-privileged P7 was wrong by
  ≈ 5 bits, which is exactly what A16 check 1 exists to catch; the privilege was removed,
  D1). The winning repair **contains a genuine body-edit to a persistent, previously
  certified rule concept** — the REVISE branch of criterion (d) is exercised by
  arithmetic, not by hope.
- **Audit A16** (threat model) computes these ΔMDL comparisons for the designed cells at
  the frozen parameters, before any contender exists, and fails the freeze if narrow+add
  is not strictly optimal. It likewise verifies that at Shift-R the
  split-with-continuity repair beats retire-and-respell, so **both** branches of (d) —
  membership-move (split) and body-edit (narrow) — are demonstrably reachable.

---

## 3. Preregistered distribution events (decoupled in v0.3, C1)

Three preregistered events, in fixed order, at episode numbers preregistered at the L3-1
freeze (defaults §8; the L3-1 preregistration addendum carries the numbers, per the
accepted disposition of gap 8):

- **E_C — condition revelation (default episode 300).** Weathered (cracked) arrivals
  begin (§2.6), forcing the designed **body-edit** repair on affected rule concepts. The
  first cracked object is a visible novelty; that is inherent-and-declared, not a leak —
  what matters is that it is *the test content itself*, and its hedging value is measured
  by T7/A10's novelty-flag probes rather than assumed away.
- **E_R — family shift (default episode 400).** A new kind k_new enters the sampling
  distribution: an attribute vector from outside K0 that **matches some K0 kind k_old on
  (α1, α2) and differs on α3**. By §2.3's action-attribute separation, k_new is
  byte-identical to k_old under `tap`, `heat`, and every F2 comparison that reads only
  (α1, α2) — and contradicts it under `soak` and the α3-reading part of `grind`. Any
  concept that adequately covered k_old now silently covers k_new and **mispredicts**.
  This is the event that forces a concept **split**: the charter's "new family sharing
  part of an old family's behavior."
- **Shift-T — reuse/transfer (episodes ≥ E_R).** The held-out co-occurrence cells H open
  up, including cells involving k_new. Scored queries probe first co-occurrences.
  Criterion (e) is evaluated here: concepts formed pre-shift must carry their predictive
  advantage onto a stream whose pair distribution the learner never trained on.

**A6's invisibility claim is scoped to E_R** (v0.3): the *kind* shift must be
undetectable in every observable side channel — appearance, episode length, object count,
ambient rates, outcome-alphabet usage frequencies — except through prediction failure
itself, and the residue is audited (threat T8). E_C is a declared, visible novelty event
by construction; A6 makes no claim about it. Criterion (d) is thereby tested **twice on
different branches** — body-edit at E_C, split at E_R — which is strictly stronger
evidence than one compound event.

The event boundaries also split the MDL/prediction record: all criteria are evaluated
with pre-E_C, E_C–E_R, and post-E_R accounting kept separate (§5, §6).

---

## 4. The substrate

Invariant-first. The substrate owns everything that is a theorem about the experiment;
the learner owns only judgment. Concretely the substrate owns: observation encoding,
prediction scoring, consistency checking, MDL accounting, the concept-library data
structure, revision bookkeeping, query scheduling, and ablation replay. **The learner
proposes distinctions and revisions. It does nothing else.**

### 4.1 The load-bearing design decision: predictions come from the library

The single most important structural choice in this spec (protected through revision,
unchanged from v0.1):

> **The predictor is the substrate's deterministic interpretation of the concept library.
> The learner has no prediction channel.**

The learner cannot emit a prediction, only library operations. Every scored prediction is
computed by the substrate by applying the library's rules to the query (§4.4). This makes
the criteria structural rather than aspirational: (a) holds because the library *is* the
predictor, so there is nowhere for load-bearing knowledge to hide in weights; (b) is
computable by replaying frozen streams with a concept removed; (c) is computable because
both code lengths live in one place; (d) is enforceable because every library mutation
passes through logged, grammar-checked operations. A contender whose internal machinery is
neural can only cash its knowledge out as library content. This is the CPL-009 move —
soundness was removed from the learnable surface there; *bookkeeping integrity* is removed
from it here.

### 4.2 Concept library data structure

A library L is a set of named concepts. Each concept is a typed term of the meta-grammar
(§4.3) with: a name (opaque, system-assigned, stable across revisions — identity continuity
is what criterion (d) measures); a kind tag (which grammar production built it); a body;
an admission record (episode, ΔMDL at admission); a revision history (append-only list of
logged edits with their triggering contradictions); and violation counters. Rules (P2, P3,
P5, P6, P8, P9) are concepts in their own right and carry all of the same records.

### 4.3 Meta-grammar (given, declared, closed)

Sorts: object variables, class symbols, attribute symbols, action constants, outcome
constants, condition constants, booleans, small integers (P10 thresholds).

Productions (the complete list — nothing else is expressible):

| # | Production | Reading | Rewarded by this generator? |
|---|---|---|---|
| P1 | `Class(name)` + membership assertions `member(o, C)` | extensional object class; membership asserted per object (episode-scoped objects; persistent classes) | yes |
| P2 | `URule(C, cond_pattern, action) → outcome [, cond′]` | unary response rule for a class | yes |
| P3 | `PRule(C, C′, cond_pattern; mode) → outcome` for `grind`, mode ∈ {sym, ord} | pairwise interaction rule between classes; `sym` covers both orders, `ord` binds one order | sym: yes; **ord: never** (F2 symmetric) — decoy |
| P4 | `Attr(name)` + attribution assertions `has(C, A)` / `¬has(C, A)` | **a predicate over class symbols** — second-order structure | yes (F1/F2 are attribute-factored) |
| P5 | `AURule(attr_expr, cond_pattern, action) → outcome [, cond′]` | unary rule over attribute expressions instead of class identity | yes |
| P6 | `APRule(attr_expr_i ⊗ attr_expr_j, cond_pattern; mode) → outcome`, ⊗ ∈ {∧, ∨, ⊕, =}, mode ∈ {sym, ord} | pair rule over attribute comparisons | sym: yes; **ord: never** — decoy |
| P7 | `CondClass(C, condition)` | a class refined by condition; rules attached to it share the ordinary rule rank (v0.4 D1) | **never** — strictly dominated by cond_pattern masks once it confers no rank — decoy |
| P8 | `Default(action) → outcome` | class-free default rule | weakly (floor compression) |
| P9 | `HRule(prev_event_pattern, C \| attr_expr, action) → outcome` | history-conditioned rule: outcome depends on the previous event on the object | **never** — the world is memoryless given condition (§2.3) — decoy |
| P10 | `CountClass(action, θ)` + rules attached to it | objects grouped by interaction-count threshold ("tapped ≥ θ times") | **never** — dynamics never read counts — decoy |

**Initial concept kinds** (the declared set, for the Level 3 marker): **{P1, P2, P3, P8}**.
**Expressible but not initial:** {P4, P5, P6, P7, P9, P10}. The marker (§5.7) requires a
certified structure whose top production is outside the initial set. Because certification
demands (b) load-bearing, (c) paid-for, and (e) reused, the decoy kinds (P9, P10, and the
ord modes) are marker-eligible in principle and cannot pass in fact unless the world is not
as declared — which is precisely what the A5 extension measures. The marker is therefore a
selection among live alternatives, not a keyhole (R4; T10).

Honesty note, stated here and in the threat model (T10): the grammar is written by the same
experimenter who writes the generator, and P4–P6 exist because the generator is
attribute-factored. That is the experiment, not a leak — the question is whether the
learner *finds and pays for* the factoring, not whether it is expressible. The mitigations
are (i) the grammar is frozen before any contender exists, (ii) the expressible space now
contains, at the kind level, both rewarded structure and generically attractive unrewarded
structure (P9, P10, ord modes; counting argument in the L3-1 audit), and (iii) the L3-3
proposal mechanism must be generic over the grammar, with its move-type inventory audited
both for a hand-shaped "propose exactly the true factoring" move and for a
suspiciously-shaped *inability* to propose decoys (A12, extended).

### 4.4 Library-induced predictor (deterministic semantics; rank rules revised in v0.2)

For a query `(state, action, object(s))`:

1. Collect applicable rules: rules whose class (via current membership assertions),
   attribute expression (via current attributions), condition pattern, and (for P9)
   history pattern match the query.
2. **Rank levels (v0.4 D1, frozen):** level B — **all** non-default rules (P2/P3/P5/P6/
   P9 and P7- or P10-attached alike) at one shared rank; level C — P8 defaults. The
   highest non-empty level decides. **Neither cond_pattern narrowness nor P7 refinement
   confers rank** (the v0.1 narrowness privilege and the v0.2 P7 privilege each made a
   shadow cheaper than the designed body-edit; both removed, each with the arithmetic
   that caught it — R1, D1). Conflicting outcomes among applicable rules in the deciding
   level → the query is **unresolved**.
3. Resolved query → coding distribution (1−ε on the ruled outcome); unresolved → uniform
   over the 11 outcomes. New objects with no membership assertion are unresolved until the
   learner asserts membership (identification-by-interaction is part of the task; per-step
   membership ops, §4.7).
4. The predicted outcome, the applicable-rule set, and the resolution path are logged per
   scored query — this is what makes decision-level audits (§6.4) and ablation replay
   (§5.2) possible.

### 4.5 MDL accounting (formulas fixed now; numeric constants frozen at L3-1 — R5)

Two-part, substrate-computed.

**Code construction, fixed now:**

- **Integer code:** Elias gamma for unbounded positive integers. Bounded choices cost
  log₂(alphabet size), the alphabet being the one declared at the point of use.
- **Operation code:** each library operation begins with log₂(N_ops) bits over the declared
  operation set (§4.6).
- **Concept spelling:** production choice log₂(N_productions = 10); then per-argument:
  class/attribute references cost log₂(current symbol-table size) (minimum 1 bit); action
  log₂ 4; outcome log₂ 11; condition log₂ 4; cond_pattern 1 bit (wildcard) or 1 + 4 bits
  (explicit condition mask); mode flags 1 bit; attr_expr recursively (operator log₂ 4 +
  operand references); P10 thresholds by Elias gamma.
- **Assertions:** `member(o, C)` = op code + log₂(N_obj) + class reference.
  `has/¬has(C, A)` = op code + class reference + attribute reference + 1 bit sign.
- **Edit-delta (`REVISE`):** op code + concept reference + slot selector
  (log₂ of that production's slot count) + spelling of the new value for that slot alone.
  **Invariant, holds by construction: a single-slot edit is strictly cheaper than
  respelling the same concept.** (This is what §2.6's dominance argument rests on.)
- **Data cost L(D | L):** prequential — every observed event (learner-chosen, ambient, and
  scored) is coded under the library-induced distribution *as of that step*, −log₂ p.
  Resolved-correct ≈ 0.0014 bits (ε = 1e-3); resolved-wrong = log₂(10/ε) ≈ 13.29 bits;
  unresolved = log₂ 11 ≈ 3.46 bits. Yesterday's library codes today's data; the running
  ledger is never recoded.
- **Admission rule (amended in v0.3, C2 — genesis deadlock).** Admission gates are
  **grammar-legality and proposal budget only.** Batch ΔMDL is computed by *hypothetical
  replay* of the retained stream under the candidate library (the ledger itself is never
  rewritten), **returned to the learner (R3), and recorded in the admission record — it is
  accounting, never a gate.** Rationale, by arithmetic: objects are episode-scoped, so
  replay can never credit a new class's rules against past episodes' expired objects; a
  genesis batch (class + rules + memberships ≈ 90 bits at these prices) recoups at most
  ≈ 48 bits from current-episode evidence at §8 scale, so v0.2's strict-decrease rule made
  the empty library an MDL local minimum from which no concept could ever be admitted.
  "Paid for" is criterion (c)'s lifetime prequential rent check (§5.3), which is
  forward-looking and was always the binding test. Wrong or speculative assertions now
  enter and are *punished* — ≈ 13.3 bits per contradiction, violations logged against
  them, retraction available — which is the honest mechanism; junk admission is bounded by
  the op budget and fails (c). No overdraft or threshold constant is introduced (T11).
- **Why a lookup table fails by arithmetic:** objects are episode-scoped and fresh forever,
  so per-object memorization buys compression only within one episode and pays description
  cost every episode; class/attribute structure amortizes across all future episodes. The
  arithmetic at planned scale is worked in §8b; L3-2 verifies it empirically with an
  explicit lookup contender.

All numeric constants that fall out of these formulas (symbol-table sizes as they evolve,
N_ops, slot counts) are computed and frozen in the L3-1 manifest; the formulas above do not
change without a versioned spec revision.

### 4.6 Consistency checking and revision bookkeeping

- Every scored or observed event that contradicts a resolved prediction is a **violation**,
  logged against the exact rule(s) and concept(s) on the resolution path.
- Library operations (the declared op set, N_ops = 6): `NEW(term)`, `REVISE(name, edit)`,
  `RETIRE(name)`, `assert-member(o, C)`, `retract-member(o, C)`,
  `assert/retract-attribution(C, A, sign)` (one op code with a sign bit). Edits are
  grammar-typed deltas (change an outcome, narrow a condition pattern, move members,
  add/remove an attribution), not free rewrites.
- The revision log is append-only and substrate-owned. Per-operation it records: episode,
  operation, concept identity, edit delta, the violation IDs that triggered it (proposals
  may cite violations; citations are checked to be real), and the library-wide **edit
  footprint** — which other concepts changed in the same batch. Criterion (d)'s locality
  test (§5.4) reads this log; it is not reconstructible any other way, which is why the
  substrate owns it.
- **Violation read path (R3):** the learner may query, at any step, the violations
  attributed to any concept: (violation id, the query, predicted outcome, observed
  outcome, resolution path). This is derivable in principle from the published predictor
  semantics plus the learner's own observations, so exposing it opens no information
  channel (§4.7 interface law); it makes contradiction detection a lookup rather than an
  unstated obligation.

### 4.7 Learner interface (complete; split in v0.2 — R2, R3)

**Interface law (R3), governing every read path:** anything derivable in principle from
the published rules (§7's given table) plus the learner's own observation history may be
exposed by the substrate; anything not so derivable stays unexposed. Every exposure below
is justified under this law.

- **Per step:** receive the observation; then either the learner's chosen action executes,
  or the scheduled ambient event / scored query does. **Membership operations
  (`assert-member` / `retract-member` for current-episode objects) may be submitted at any
  step** — MDL-charged per §4.5, admitted under the same v0.3 semantics (legality gate,
  ΔMDL recorded), logged identically to boundary operations (R2). The violation read path
  (§4.6) is available at any step.
- **Per episode boundary:** submit at most B_prop structural proposal batches
  (`NEW` / `REVISE` / `RETIRE` / attribution ops, and membership ops where a structural
  change moves members — splits need them), each a bounded set of operations
  (**≤ 96 ops per batch since v0.3, C3** — sized so the full class→attribute factoring
  transition, ≈ 84 ops at §8 scale, fits in **one atomic batch**; batches are evaluated
  and applied as a unit and never transit a conflicted intermediate library; A16 checks
  the fit explicitly).
- **Proposal return (R3):** for every batch, the substrate returns
  `{accepted | rejected, batch ΔMDL}`. Nothing else is returned.
- The learner never sees kinds, attributes, F-tables, episode indices, MDL internals
  beyond the published construction rules and the returned ΔMDL values, or anything
  generator-internal. Contenders and cheap controls (L3-2/L3-3) all sit behind this same
  interface, which is what makes them comparable.

**Composition check for R2, recorded:** with per-step membership ops, an object probed at
step t can be asserted into a class at step t+1 and resolves from then on — so
oracle-with-identification (A2) and every honest contender can resolve current-episode
objects, while scored queries scheduled *before* first interaction remain unresolved for
every policy alike and measure the identification burden (§6.1 sub-strata). §5.4's
membership-move logging is unaffected: membership ops were always logged; only their
timing constraint changed.

---

## 5. Operationalization of the preregistered criteria

Criteria text is frozen in `PREREGISTRATION_001`. Operationalizations below freeze at the
L3-1 gate; thresholds marked ⟨L3-1⟩ are set during the L3-1 audit **before any contender
exists** and are frozen in the manifest.

### 5.1 (a) Named and inspectable

Satisfied structurally by §4.1–§4.2: a structure counts only if it is an admitted library
concept. There is no other way to influence predictions, so nothing load-bearing can be a
pattern in weights. Verified by the substrate invariant tests (§10), not by measurement.

### 5.2 (b) Load-bearing

Ablation replay: on the frozen post-hoc evaluation stream, the substrate recomputes every
scored query with concept c removed (memberships/attributions referencing c removed with
it; the rest of the library untouched). c is load-bearing iff prediction degrades by at
least δ_b ⟨L3-1⟩ on top-1 accuracy over the scored queries, with a paired test at the query
level (McNemar, the CPL-009 machinery). Replay determinism makes this exact, not sampled.

### 5.3 (c) Paid for (amended in v0.3, C2)

One binding check, one recorded description:
- **Prequential lifetime check (binding):** from admission to evaluation point, cumulative
  data-bits saved (prequential code with c vs. the same history replayed without c) ≥
  description bits spent on c and its assertions, including c's share of batch overhead.
  Computed by the substrate by replay. This is the entire "paid for" gate: a concept that
  never pays rent fails (c) no matter how it entered.
- **Admission ΔMDL (recorded, not a gate):** the batch ΔMDL at admission is kept in the
  admission record and reported with every certification, so reviewers can see whether a
  concept entered as an investment (positive ΔMDL, repaid later) or as an immediate
  compression. v0.2's strict-decrease admission gate was removed by the C2 genesis-deadlock
  arithmetic (§0a, §4.5).

### 5.4 (d) Revised, not replaced (split semantics formalized in v0.2 — R1a)

**Split semantics, fixed now:** a split — `REVISE(C_old, move-members / narrow membership
discipline)` together with `NEW(C_new)` in the same batch — **counts as a revision of
C_old**. C_old keeps its name, its admission record, and its prequential clock; C_new
receives a fresh admission record and a fresh clock. A `RETIRE(C_old)` + `NEW` + `NEW`
respelling is **replacement**, not revision, and fails identity continuity below.

**The two designed contradiction streams, and which branch each exercises (decoupled in
v0.3, C1):** the family shift at **E_R** (the k_new split) exercises the membership-move
branch; the condition revelation at **E_C** exercises the body-edit branch on rule
concepts. A16 proves both branches are the arithmetically optimal repair for their
designed case, at their designed sites, before any contender exists (R1b). Because the
events are separate episodes, (d) is tested twice on different branches with independent
contradiction records.

On a contradiction stream, all of the following must hold for the concept c under test:
- **Identity continuity:** the same concept name survives; the edit is a logged
  `REVISE` on c (membership-move, cond_pattern narrowing, or another grammar-typed delta),
  possibly plus admission of new concepts in the same batch, not `RETIRE(c)` + `NEW`.
- **Locality:** the edit footprint outside c and newly admitted concepts is ≤ f_d ⟨L3-1⟩
  (a small fraction of the library, target order ≤ 10% of concepts touched).
- **Restoration:** post-revision, violations attributed to c on the triggering query type
  fall to the ε-floor, while c's pre-shift predictive performance (5.2's ablation margin on
  pre-shift-style queries) is retained within τ_d ⟨L3-1⟩.
- **Bookkeeping:** the revision log entry exists, cites real violations, and the claimed
  trigger precedes the edit. Substrate-logged, so this is a lookup, not an argument.

A pipeline that re-derives its library from scratch after contradiction generically fails
locality and identity continuity; §9.1 discusses the known arms race here and L3-2 tests it.

### 5.5 (e) Reused

On Shift-T queries (first co-occurrence of held-out pairs; fresh objects of familiar kinds;
post-E_R stream generally): the ablation margin of c (5.2's paired test) on the
**post-shift scored stream** must be ≥ δ_e ⟨L3-1⟩. The stream conditions were never
trained on: held-out pairs never co-occurred, fresh objects never existed, k_new never
appeared. For pair-mediating concepts the decisive cell is first-co-occurrence queries —
a concept whose advantage exists only on experienced pairs fails (e) there by arithmetic,
because no experience with those pairs exists to memorize.

### 5.6 Per-concept certification

A structure is certified as an invented concept iff (a) structural + (b), (c), (e) pass at
the preregistered thresholds and — for concepts that faced contradiction — (d) passes on
its contradiction record. Concepts that never faced contradiction are reported as
(d)-untested, never as (d)-passed; the Shift-R design guarantees that the concepts the
headline rests on *do* face contradiction.

### 5.7 The Level 3 marker

The marker fires iff a concept whose top production is outside the initial set {P1, P2,
P3, P8} — e.g. an `Attr` with its attributions and at least one `AURule`/`APRule`, or a
`CondClass` refinement — is admitted by the learner's own proposals and certified per §5.6,
including surviving Shift-R with (d) and carrying (e) across Shift-T. The intended-by-design
instance is the attribute factoring (P4–P6), because F2 makes it worth paying for; the
marker is defined over *any* non-initial production so that the learner is not graded on
matching the experimenter's imagination — and since v0.2 the non-initial space contains
genuinely unrewarded kinds (P9, P10, ord modes), so firing the marker requires selecting
the structure the world actually rewards, not merely leaving the initial set (R4).
Negative result semantics: a run that forms and certifies P1/P2/P3 concepts but never a
non-initial kind is L3-PARTIAL, not L3-POSITIVE.

---

## 6. Evaluation protocol

### 6.1 Scored queries (hypothetical form added in v0.4, D7)

The substrate schedules 8 scored-query steps per episode (of T = 32, §2.4/§8) from a
uniform interventional design over (object, action) — including grind pairs — stratified
to cover: fresh objects (identification burden), familiar-kind objects, and (post-shift)
k_new objects, weathered arrivals, and held-out-cell pairs. The fresh-object stratum is
reported as two sub-strata (R2 composition): **pre-identification** (query fires before
the learner's first interaction with the object — unresolved for every policy, measuring
the shared burden) and **post-identification**. Scored queries are predictions under
`do(action)`: the substrate asks for the library's prediction, then executes the action
and scores. Exploration actions are never scored; controls and contenders face
**identical scored streams** (same literal seeds), so exploration-policy differences
cannot confound scoring.

**Hypothetical scored queries (D7).** For the transfer stratum, the substrate issues
queries it does not execute: "grind(o_i, o_j) under stated pristine conditions" — the
library's prediction is recorded and scored against the generator-computed outcome; the
outcome is never revealed to any policy, no state changes, and nothing is coded into the
prequential ledger. Hypothetical queries are dry by construction and carry no information
channel, which is what makes the unseen-combination test clean: two executed designs
failed with evidence (identification confound at early steps; soaked-null collapse plus
datum-leak at late steps — §0a D7). Stratum semantics: **fc_unseen** iff no grind on that
kind-cell has occurred earlier in the run — policy-dependent by the honest meaning of
"never trained on", with per-policy n always reported — else **fc_seen**.

### 6.2 Metrics

**Unresolved-scoring convention, fixed now and applied uniformly (v0.4, gate-hold
check 2):** on the top-1 accuracy surface, **an unresolved query scores 0** — the
library declined to predict, and declining is not a hit. No realized uniform draw, no
tie-break. The uniform-chance reference 1/11 lives on the *coding* surface, where an
unresolved query costs exactly log₂ 11 ≈ 3.46 bits (§4.5); the two surfaces are never
mixed. One code path in the engine applies this to every policy and every stratum.
Consequence: null-empty scores **0.000** top-1 by construction (all queries unresolved)
while coding at exactly the uniform-chance bit rate — which is the sense in which it
"ties with chance by construction" (§6.3, corrected in v0.4).

Primary: top-1 outcome accuracy on scored queries, reported per stratum (never merged:
pre-shift, post-shift-familiar, k_new, weathered, first-co-occurrence, and the
identification sub-strata) — the CPL-009B lesson that the profile is the result.
Secondary: prequential bits/event; library size trajectory; violation rates; revision-log
statistics. Verdict endpoints for L3-3 are preregistered in the L3-3 WO, not here, but the
charter fixes the shape: the primary endpoint is the post-shift strata.

### 6.3 Reference policies (the ladder for this world)

Run under the identical interface:
- **oracle** — a substrate-side policy that writes the true structure into the library
  (kinds as classes, true attribute factoring, true rules); ceiling ≈ 1 − ε effects. Its
  library also fixes the target MDL: the compression that exists to be found.
- **null-empty** — empty library: all queries unresolved. Under the §6.2 convention it
  scores **0.000 top-1 by construction** and codes at exactly the uniform-chance rate
  (log₂ 11 bits/event) — the "ties with chance" property lives on the coding surface,
  the CPL-009 null-control standard. (v0.4 correction: the v0.2–v0.3 text said
  "1/11 top-1", which was wrong under the unresolved-scores-zero convention — caught at
  the L3-1 gate hold, check 2.)
- **null-default** — P8 defaults only (majority outcome per action): the honest
  deterministic floor, the "0.13-not-0.06" lesson from 009B applied here in advance.
- **Cheap ceiling (measured in L3-1, before contenders):** per-object lookup;
  clustering-plus-relabelling on interaction histories; static appearance/condition
  learner; ambient-correlational predictor (trained on the passive stream, burned on
  interventional queries — audit A7). These are the L3-2 failure-table contenders; L3-1
  measures them to fix the criteria thresholds ⟨L3-1⟩ at values the cheap ceiling fails.

### 6.4 The vacuity gate (CPL-008 confluence lesson: prove non-vacuity before competition)

The world is discarded or redesigned unless L3-1 measures **all** of:
- **A1 headroom:** oracle minus best §6.3 cheap policy ≥ a material margin on every primary
  stratum, largest on first-co-occurrence (compositional headroom is the point).
- **A2 identification is doable:** oracle-with-identification (true rules, but must infer
  each object's class from interactions like everyone else) still ≫ cheap ceiling —
  otherwise the task is secretly "identification is impossible" and concepts can't matter.
- **A3 the lookup fails by arithmetic, and the gaps clear the preregistered floors (R5):**
  measured MDL of the lookup contender diverges; the class-library-vs-empty gap is
  ≥ 5,000 bits and the factored-vs-class-library model+transfer gap is ≥ 300 bits at the
  frozen parameters (§8b). If either floor fails, the world is grown **before** freeze —
  never after.
- **A4 nuisance null:** appearance-feature probes at exactly chance on every stratum
  (they are independent by construction; the audit confirms the construction).
- **A5 decision-level leakage:** at the scored-query unit, every cheap observable feature
  (appearance, token, position, condition-history counts, co-occurrence counts) is probed
  as a predictor of the outcome and of the latent kind; anything above the declared floor
  is a stop condition (v0.1's edge-counting lesson: audit the unit acted on). **Extended
  (R4):** the probe set includes previous-event features, interaction-count features, and
  pair-order asymmetry — verifying by measurement that the world is memoryless given
  condition, count-blind, and F2-symmetric, i.e. that the decoys are in fact unrewarded.
- **A6 shift invisibility (scoped to E_R in v0.3, C1; statistic fixed in v0.4, D8):**
  a permutation test on the pre/post-E_R centroid distance over **per-action unary
  outcome conditionals** (k_new events excluded) must return p ≥ 0.05 — the kind shift
  is undetectable in the side channels (appearance, ambient rates, unary outcome
  conditionals, episode shape) except through prediction failure itself. The grind
  channel's pair-mix change at E_R *is* Shift-T (the holdout opening), designed and
  priced under T7, not a side channel. E_C is a declared visible novelty event and A6
  makes no claim about it; its channels (weathered arrivals) and the other designed
  novelty channels are priced by T7/A10's novelty-flag measurement instead (threat T8).
  Measured at the freeze: p = 0.975.
- **A7 the causal trap has teeth:** the ambient-correlational control's interventional
  score is materially below its passive-stream fit — the measured gap is reported.
- **A16 revision reachability (R1):** the §2.6 ΔMDL dominance computations, plus the
  Shift-R split-vs-respell comparison (defined in the threat model).

---

## 7. What is given — the exhaustive declaration

**Given (declared, frozen):** the observation alphabets (§2.1); the action set and its
always-legal semantics; the outcome alphabet; the ambient process's existence and
observability (its kind-bias magnitudes are generator-internal); the meta-grammar §4.3 in
full, including P4–P10 and the mode flags; the initial concept-kind set {P1, P2, P3, P8};
the library operation set, the per-step/boundary split, and proposal budgets (§4.7); the
MDL code construction rules of §4.5 including the Elias gamma choice, the edit-delta
invariant, and **the v0.3 admission semantics (legality + budget gate; ΔMDL recorded and
returned, never gating)**; the ε-floor; the library-induced predictor semantics including
the §4.4 rank levels; the scoring protocol and strata existence; **the proposal return
channel {accepted | rejected, batch ΔMDL} and the violation read path (R3)**; the
interface law itself (§4.7); **the hypothetical-query mechanism (v0.4 D7) as a
substrate-owned instrument** — stated-condition prediction, scored-not-executed,
outcome never revealed, no state change, excluded from the prequential ledger, separate
strata in every report.

**Not given (the learner's problem):** the number of kinds; any kind assignment; the
existence, number or identity of useful attributes; F1 and F2, including F2's symmetry
(the sym/ord distinction is spellable and its worth is learnable); the memorylessness and
count-blindness of the dynamics; which distinctions are worth paying for; when to split;
memberships and attributions; that a shift will occur, or when, or what shape; that
`cracked` exists only as an arrival condition; that attribute factoring is the intended
compression.

**Explicitly not learnable (substrate-owned invariants):** prediction from anything but
the library; unlogged library mutation; MDL arithmetic; violation attribution; the
scheduling of scored queries; identity of the revision log.

Zero given ontology is impossible; this table is the "minimal and explicit" standard the
charter demands. Anything later found to be given-but-undeclared is a stop condition.

---

## 8. Default parameters (all frozen at L3-1 by manifest, from literal seeds)

Frozen authoritative values live in `l3_1/MANIFEST.json`; this table mirrors them.

| Parameter | Frozen value | Notes |
|---|---|---|
| Kinds pre-shift / attributes | 5 / 3 binary | §2.2 |
| Objects per episode | 5 | |
| Steps per episode T | **32 = 20 learner + 4 ambient + 8 scored** | v0.4 D2 (was 24; grown by A16 rent arithmetic and the A7 saturation finding) |
| Episodes total / E_C / E_R | 600 / 300 / 400 | windows pre 1–299, mid 300–399, post 400–600; preregistered in `PREREGISTRATION_002` §1 |
| Weathered-arrival rate post-E_C | 20% of arrivals | §2.6 |
| Held-out pair cells | rule-derived from literal seed: {A-B, B-C, B-E, D-E} | v0.4 D5, §2.5; 57 eligible subsets under H1–H4 |
| Hypothetical transfer queries | ≤ 12 episodes per held-out cell, scored step 19 | v0.4 D7, §6.1 |
| Post-E_R kind weights | marginal-matched literals | v0.4 D6, §2.2 |
| ε (coding floor) | 1e-3 | §2.3, §4.5 |
| Proposal budget B_prop | 4 structural batches/episode boundary, ≤ 96 ops each (C3); membership ops per-step, unbatched, also legal inside structural batches | §4.7 |
| Training seeds (contender) | 5 | CPL-009B convention |
| Eval-stream seeds | 3, literal (17/18/19) | determinism-of-contender measured and stated, per 009B-V-001 lesson |

## 8b. Worked description-length arithmetic at planned scale (R5)

**v0.4 note:** the ballpark below was computed at the v0.3 defaults (T=24) and did its
job — it exposed the thin v0.1 gap and sized the v0.3 world. The frozen world is T=32
(D2) and the **measured** values at the freeze supersede the ballpark: empty 66,421 bits;
lookup 312,614 (**+246,193 — diverges**); class-library gap vs empty **42,786**
(floor 5,000); factored-vs-class model gap **474** (floor 300); genesis rent
**+6.35 bits/object**, payback ≈ 7.7 objects; membership evidence = **3 events**
(A3, A16 in `l3_1/audit_results.json`). Reading 3 below — the re-anchoring of the
marker's decisive evidence — is unchanged and is carried verbatim in
`PREREGISTRATION_002` §5.

Original v0.3 ballpark, retained: unit costs: op code 2.6 bits; production choice 3.3;
class ref ≈ 2.6; attr ref ≈ 1.6; action 2; outcome 3.46; cond_pattern 1–5; membership
assertion ≈ 8; rule spelling ≈ 18 (URule) / ≈ 20 (AURule/APRule); class or attr
declaration ≈ 7; attribution ≈ 10. Coding: resolved ≈ 0.0014 bits/event, unresolved
3.46, contradiction 13.29.

Scale (v0.3): 600 episodes × 5 objects = **3,000 objects**; 600 × 24 = **14,400 coded
events**; ≈ 4.8 events per object.

| Library | Model + assertion bits | Data bits | Total | vs empty |
|---|---|---|---|---|
| **empty** (null) | 0 | 14,400 × 3.46 ≈ 49,800 | ≈ 49,800 | — |
| **per-object lookup** | ≈ 54/object × 3,000 ≈ 162,000 | probes ≈ 31,100 + ≈ 0 | ≈ 193,000 | **+143,000 — diverges; A3 by arithmetic** |
| **class-only (Level-2 ceiling)** | rules ≈ 870 + memberships ≈ 24,000 | probes ≈ 15,600 + bleed ≈ 500 | ≈ 40,900 | **−8,900 (saves)** |
| **attribute-factored (oracle)** | rules+attrs ≈ 530 + memberships ≈ 24,000 | probes ≈ 15,600 − transfer/k_new savings ≈ 300–600 | ≈ 40,100–40,400 | −9,400 to −9,700 |

Readings, stated plainly:
1. **The lookup diverges by ≈ +143k bits** — criterion (c)'s "fails by arithmetic" is
   arithmetic, not argument.
2. **Class concepts clear the empty baseline by ≈ 9k bits** (≈ +3 bits per object net of
   identification and assertion costs). Under the v0.1 defaults (6 objects × 12 steps ≈
   2.7 events/object) this margin was ≈ **+0.6 bits/object — thin to the point of
   noise**, which is why the defaults were grown in this revision rather than after the
   harness exists (the Director's R5 instruction, applied).
3. **The factored library beats the class-only library by ≈ 500–900 bits** (rule-model
   compression ≈ 340, k_new spelling savings ≈ 80, held-out-cell transfer savings ≈
   100–500) — comfortably above single-concept spelling noise (~20 bits) but a thin
   fraction of total MDL. Consequence, preregistered here: **criterion (c) for the marker
   concept is satisfied by strict arithmetic, but the *decisive* marker evidence is the
   first-co-occurrence stratum accuracy plus ablation margins (b)/(e)** — MDL admission
   alone is not presented as the headline. The A3 floors (≥ 5,000 bits class-vs-empty,
   ≥ 300 bits factored-vs-class) make thinness a measured stop condition at L3-1.
4. Membership assertions dominate every non-trivial library's cost (≈ 24k bits). This is
   honest — identification effort is the price of concepts about hidden kinds — and it is
   shared by every policy that resolves anything, so it cancels in comparisons.

---

## 9. Open design risks surfaced for gate review (not resolved by fiat)

**9.1 The clusterability crux.** Any latent kind that determines behavior is recoverable
by clustering on sufficient interaction history — definitionally, since kinds *are*
behavioral equivalence classes. So concept-hood cannot rest on discovery being hard; it
rests on (c) rent-paying, (d) locality-under-contradiction, and (e) unseen-combination
transfer. The known arms race: a clustering wrapper that greedily maps new clusters onto
old names imitates (d)'s identity continuity. Current teeth: such a wrapper still fails
(e) on first co-occurrence for pair rules (nothing to memorize), and its refits generically
violate (d)-locality under Shift-R because re-clustering jitters memberships elsewhere.
If L3-2 shows those teeth insufficient, the charter's STOP applies and the
operationalizations get a versioned addendum. I flag now, honestly: **P1/P2 class concepts
formed by good clustering may pass (a)(b)(c) and untested-(d) — the criteria separate
Level 2 from Level 3 at (d), (e) and the marker, not at class formation.** The headline
claim is gated on the marker, which clustering cannot produce (its output vocabulary is
clusters, i.e. P1) — and which, since v0.2, requires selecting rewarded structure from a
kind space that also contains decoys (§4.3, §5.7).

**9.2 Meta-grammar smuggling (threat T10).** P4–P6 exist because the generator is
attribute-factored. Mitigations in §4.3, now including kind-level decoys (R4); residual
risk remains a named review item at every gate.

**9.3 MDL gaming.** Constants chosen post-hoc could make the intended concept win by
construction. Mitigation: formulas fixed in this spec (§4.5, R5), all remaining constants
frozen at L3-1 before contenders, plus the A13 sensitivity report (does the oracle library
still win under ±2 bits/concept perturbations?).

**9.4 Proposal-fishing.** ΔMDL computation is deterministic given data, so a learner can
search expression space by probing proposals; bounded by B_prop and fully logged. This is
legitimate library-learning search, but compute spent proposing is reported, so a
brute-force enumeration cannot masquerade as insight (the 009 compute-matching lesson,
applied to proposals; an explicit proposal-compute account is part of the L3-3 envelope).
The R3 proposal return (ΔMDL) lets the learner gradient-follow the accounting; recorded,
accepted — the information is derivable in principle (interface law), and the compute
account keeps the search visible. **Since v0.3 (C2) admission no longer gates on ΔMDL, so
spam *enters* rather than being rejected:** the exposure is bounded by the op budget, made
visible by the library-size trajectory (§6.2), and punished by criterion (c) — a spammed
library fails certification concept by concept. `RETIRE` exists for cleanup and is logged
like everything else.

**9.5 Single-experimenter closure.** The same agent writes generator, substrate, grammar
and (later) the contender. Standing mitigations: preregistration-by-commit, dual
implementation of dynamics (§10), the L3-1 audit as a distinct gated artifact, and the
programme's falsification-pass convention (an L3-3 result gets its own V-pass, as 009B did).

---

## 10. Verification and self-verify plan (built in L3-1, existing from day one)

- **Manifest + digests** for every frozen artifact (generator, substrate, F-tables, streams,
  audit outputs), with a self-verify routine present from the first commit — the
  V-001 lesson (no self-verifier existed) applied in advance.
- **Dual implementation:** F1/F2 and the episode driver implemented twice, independently
  (different modules, different styles); a trace cross-checker requires byte-agreement on
  full episode traces across literal seeds before anything else runs. Oracle disagreement
  is a hard stop (CPL rule 1.1).
- **Replay identity:** the substrate's MDL and scoring must reproduce byte-identically from
  the event log alone; ablation replay must be exact.
- **Environment identity:** literal seeds only, `PYTHONHASHSEED` invariance measured at
  three values (the 009B-V-001 closure, applied from the start), environment recorded per
  run, and a distinct `source_commit` field (the D1 lesson).
- **Frozen-material discipline:** nothing under `ucs_research/cpl009/` or the DNAR trees is
  ever touched; each gate report includes a zero-diff confirmation over the frozen roots.

---

*End of Phase L3-0 specification, v0.2. Companion document: `L3_0_THREAT_MODEL.md` (v0.2).
Gate: this revision returns to the same Director gate; no code until it clears.*
