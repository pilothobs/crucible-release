# EID-L3 — Preregistration 003: Criteria-Operationalization Addendum
# (the L3-2 STOP resolution, as ruled by the Director 2026-08-29)

**Status:** binding versioned addendum, committed FIRST in the ruled sequence —
before any harness re-freeze code change, before the L3-2 re-run, before any
L3-3 WO exists. `PREREGISTRATION_001` (criteria text) remains untouched, as its
change control was built for: these are operationalization amendments only.
`PREREGISTRATION_002` remains in force except where a value is explicitly
superseded here; both stay append-only.

**Origin:** the L3-2 charter STOP (`l3_2/L3_2_REPORT.md`): ClusterRelabel
certified two Level-2 class concepts through the composition of two
operationalization defects — §5.6's untested-(d) path admits abstention-as-
evasion, and §5.5's whole-stream (e) let "survives the shift" degenerate into
"still works on what the shift didn't touch."

---

## Amendment 1 — (e) evaluates on the shift-introduced surface. APPROVED AS DRAFTED.

Criterion (e)'s ablation margin is computed over the **shift-introduced
scored surface**: queries that are k_new-involving, weathered-involving, or
hypothetical transfer queries, in the mid/post windows. "Carries its
predictive advantage across a generator shift" means carrying it **onto what
the shift introduced**. The whole-stream margin is still computed and
**reported as description**, never as the gate. Measured basis: the cheap
certifiers score −0.005 on this surface while true-structure concepts score
+0.04…+0.58 — the gap between looking like a concept and being one, which is
the surface certification now points at.

## Amendment 2 — the abstention blade (AS MODIFIED BY THE RULING).

The drafted "in-scope evasion by membership intersection" wounded the wrong
target: a tap/heat rule on a k_new-containing class is right on every query
it resolves (k_new matches k_old on (α1, α2)); it faces no contradiction
because there is none to face — that is not evasion. The decidable
distinction is **resolved-correct versus abstained**, all three states
substrate-computable from the resolution logs:

For a certification unit c (concept or declared composite), over the
shift-surface queries **targeting c's members** (its scope: shift-surface
queries where an involved object is a member of c at query time; for rules,
where the query matches the rule's action and involves a member of its host
class; for composites, the union of member scopes), restricted to queries the
**reference structure resolves** (computed from a reference true-structure
run on the byte-identical query stream — A14 guarantees alignment):

- **(d)-passed:** c revised after real violations, per §5.4 (with Amendment 3
  attribution) — certifiable.
- **(d)-untested-correct:** c's rules resolve its in-scope queries (their
  correctness is already policed by (b)/(e) and the violation machinery) and
  c's **abstention share** — the fraction of in-scope reference-resolved
  queries the run's library leaves unresolved — is ≤ the frozen threshold
  **θ_ev** — certifiable.
- **uncertifiable-untested:** abstention share > θ_ev — the concept
  systematically declines exactly where the reference structure resolves;
  abstention-as-evasion does not earn certification.

A unit with an empty in-scope reference-resolved set is **out-of-scope** and
follows the (d)-untested-correct path (nothing to abstain from). θ_ev is set
at the re-freeze under the Condition-1 protocol (a value the re-measured
cheap ceiling fails), before any contender exists, and frozen in the manifest.

## Amendment 3 — (d) attribution granularity. APPROVED AS DRAFTED.

Contradictions attached to a class via its hosted rules may be answered by
revisions to those rules **in the same batch citing the same violations**;
locality and restoration then run over the class-plus-hosted-rules cluster as
one unit.

## Amendment 4 — mandatory full L3-2 re-run. APPROVED AS DRAFTED.

L3-2 re-runs in full under these operationalizations before any L3-3 WO
exists.

---

## Condition 1 — thresholds re-derive under the original §6.3 protocol on the
new surface, before any contender

Changing the (e) surface changes every measured cheap ceiling. δ_e and θ_ev
are set at values the **re-measured** cheap ceiling fails, from the re-run's
control measurements, then frozen in the re-freeze manifest. The certification
unit is stated explicitly: **certification may be evaluated at the declared
composite level** — §5.7 already defines the marker instance as a composite
(an Attr with its attributions and at least one AURule/APRule), and composite
units (declared before certification: for each attribute, the attribute
concept plus the rules whose expressions reference it) are evaluated as one
unit for (b)/(c)/(d)/(e). "Individually thin rule concepts" is handled by the
unit definition, **not** by threshold erosion. **Class B at 0.044 stays
failed** — a rare-kind Level-2 class not certifying individually is the
criteria being honest, not a cost to engineer away.

## Condition 2 — preregistered two-sided acceptance conditions for the re-run

1. Cluster's two certifiers (the P1 classes for the two high-marginal kinds)
   flip to **uncertifiable-untested**.
2. The reference structure's concepts **still certify** under the same
   amended operationalizations (attribute composites and common-kind
   classes; rare-kind class B stays failed on (e) as ruled).
3. Every other control still fails.
4. **No control certifies by a new route.**

**ClusterRelabel is the standing regression fixture for the certification
logic from this addendum onward** — the T15 rule applied to the certifier
itself: every future change to certification machinery must show cluster's
certifiers still land uncertifiable-untested.

## Condition 3 — B-E power fix inside this re-freeze

Amendment 1's surface leans on the holdout cells, and B-E's 14 pooled queries
cannot carry a per-cell claim. The hypothetical-query schedule is equalized:
per-cell target raised to **24 per run**, with up to **3 hypothetical slots
per qualifying episode** (scored steps 19, 11, 23 in that priority) until the
cell reaches target. Legitimate exactly now — the harness re-freezes under
this addendum and no contender exists; impossible later. Declared caveat:
multiple hypothetical queries within one episode share the membership state's
evolution and are correlated trials; per-cell reporting carries episode
counts alongside query counts. The equalization ceiling for B-involving cells
remains bounded by B's co-occurrence rate (itself the honest price of the
rule-derived holdout); realized per-cell n is reported, not assumed.

## Condition 4 — sequence and delivery

Commit this addendum first; re-freeze the harness (new manifest, full A1–A16
audit re-run plus planted fixtures under the changed schedule); re-run L3-2;
then one gate package delivered **in-channel as text** with its full 64-hex
SHA-256: this addendum's final text, the re-run failure table with
acceptance-condition results, the updated manifest state, and the original
L3-1 package content.
