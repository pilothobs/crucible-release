# EID-L3 — Preregistration 004: Composite-Mandatory Certification
# (the H2 blade-scope resolution, as ruled by the Director 2026-08-30)

**Status:** binding versioned addendum, committed FIRST in the ruled
sequence — before any certifier code for it exists, before the reference
measurement that fills in its threshold, before the EXP1 replay, before
any E.2 work. `PREREGISTRATION_001` (criteria text) untouched. P002 and
P003 remain in force except where a provision is explicitly superseded
here; all stay append-only. Ruling text: `l3_5/DIRECTOR_RULING_H2.md`
(verbatim).

**Origin:** the H2 blade-scope finding (`l3_5/H2_BLADE_SCOPE.md`, commit
3c7f514). The frozen `_unit_scope` gives bare P4 units an empty blade
scope (P4 matches no scoping branch; consistent with the P003 A2 text —
attributes have no object-members), so the EXP1 marker certified at a
granularity the abstention blade cannot reach, while the blade's designed
reach — the composite (P003 Condition 1) — failed it at ~0.60. Measured:
all 13 marker runs at attributed-classes shares 0.352–0.397 vs θ_ev
0.15 (2.3–2.6× exceedance); OracleIdent clears the identical blade at
0.050–0.056. Ruled an **operationalization defect** (abstention-as-
evasion through a scope hole, the defect class P003 Amendment 2 was
written to kill, recurring one unit-granularity down).

---

## Amendment 1 — attribute content certifies only as its declared composite

Certifiable units are: (i) all non-P4 singleton concepts, and (ii) for
each P4 attribute, its **declared composite** — the attribute, its
attributions, and every P5/P6 rule whose expression references it (the
existing `standard_units` composite construction, `certify_p003.py:60`).
**Bare P4 singletons are not certifiable units and are marker-
ineligible.** This aligns three texts that already agree: L3_0_SPEC §5.7
(the marker instance is a composite — "an Attr with its attributions and
at least one AURule/APRule"), P003 Condition 1 (certification may be
evaluated at the declared composite level; the composite is the blade's
designed reach onto attributes), and the ruling. Composite blade scope =
union of member scopes, per the existing P003 A2 text; the evaluation
arithmetic of `evaluate_unit` is unchanged — only the unit set and the
composite threshold below change.

## Amendment 2 — θ_comp, fixed by formula BEFORE the measurement exists

The abstention-blade threshold applied to composite units is **θ_comp**,
derived by this preregistered formula (Director approval, change 1) from
reference measurements taken by `l3_5/validate_p004.py` on the verdict
streams 23/29/31, before any contender replay:

> **θ_comp = min( 2 × S_or , (S_or + S_cc) / 2 )**
>
> where **S_or** = the maximum composite-unit abstention share of
> **OracleIdent** (the honest-reachability reference) across the three
> verdict streams, and **S_cc** = the minimum composite-unit abstention
> share across all eight control policies on those streams. If no
> control policy holds any P4 content (so no control composite share
> exists), the second leg is vacuous and **θ_comp = 2 × S_or**.

Singleton units keep θ_ev = 0.15 unchanged.

**Apparatus-stop conditions (a Director ruling, not a local
adjustment):** (i) oracle margin under 1.5× — θ_comp / S_or < 1.5;
(ii) θ_comp ≥ any existing control composite share; (iii) OracleFull's
composite units fail to clear θ_comp; (iv) any two-sided acceptance
condition below fails.

## Amendment 3 — two-sided acceptance conditions (before any replay)

On each verdict stream, under the P004 unit set and θ_comp:

1. OracleFull certifies with the marker at composite level.
2. OracleIdent certifies the marker at composite level (honest
   reachability).
3. ClusterRelabel and every other L3-2 control certify **nothing**.
4. The STOP-era cluster regression form holds (P003 Condition 2 — the
   standing fixture applies to every certification-machinery change,
   this one included).
5. No bare P4 appears in any certifiable set.

## Amendment 4 — mandatory replay re-certification and relabel

The 15 EXP1 scored runs are re-certified by **deterministic replay** of
the frozen Candidate E (digest per `l3_5/FREEZE.json`) on the same
seeds and streams — no new runs, no new streams — under the P004
machinery. The EXP1 verdict is then **relabelled** (never deleted): the
P003-era EXP1-QUALIFIED line stands as the record of what happened; the
P004 line is appended as **EXP1-NEGATIVE-UNDER-P004** if, as the ruling
anticipates from the measured composite shares (~0.60 vs an oracle at
≤ ~0.17), the marker does not fire. The relabel states the outcome
plainly, with per-run composite shares.

## Sequence

1. This addendum committed (this commit).
2. `l3_2/certify_p004.py` — a thin versioned wrapper reusing the frozen
   P003 evaluation functions; `certify_p003.py` is not edited.
3. `l3_5/validate_p004.py` — reference measurement → θ_comp by the
   formula → two-sided acceptance; θ_comp and the certifier digest
   frozen in `l3_5/FREEZE_P004.json`. Any stop condition → halt and
   report to the Director.
4. `l3_5/recertify_p004.py` — replay, run twice (determinism), plus the
   cross-scope consistency check (composite-scope shares ~0.60 vs the H2
   attributed-classes 0.35–0.40 — different scopes, both must
   reproduce).
5. Relabel in `l3_5/L3_5_REPORT.md` + DECISIONS.md; report in-channel.
6. Only then: EXP2 (Candidate E.2) preregistration, carrying the
   Director's approval changes 2 (exposure ledger + rule-drawn fresh
   verdict seeds) and 3 (identical budgets; exploration-distribution
   V-pass check).
