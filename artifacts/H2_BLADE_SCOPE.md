# H2 — Blade scope for the P4 marker units (reviewer hold, answered)

**Files:** analysis script `l3_5/h2_blade_scope.py`, raw output
`l3_5/h2_blade_scope.json` (same commit). No frozen file was changed;
this is verification-style analysis over fresh runs of the frozen
contender (digest per `l3_5/FREEZE.json`).

---

## 1. How the frozen certifier computed the blade's in-scope set for the marker units

Function: `_unit_scope`, `l3_2/certify_p003.py` **lines 82–113** (digest
`969c66b8…` — Candidate D freeze-2, unchanged through EXP1). Its
branches, by production:

- **lines 91–92:** `P1/P7/P10` → class-like; scope = surface queries
  whose views include a member-object of the unit.
- **lines 93–96:** `P2/P3/P9` → rules with a host: scope = surface
  queries matching the rule's action AND involving a member of the host
  class (`t.get("cls") or t.get("c1")`).
- **lines 97–98:** `P5/P6/P8` → `(action, None, None)`: scope = ALL
  surface queries matching the action (host filter vacuous —
  see §2).
- **P4 matches no branch.** A bare attribute contributes nothing to
  `class_like` or `rule_hosts`, so for the singleton P4 units
  (k47; k48/k49/k50; k52/k53) the loop at lines 100–112 returns
  **`scope = []`**.

Downstream (`evaluate_unit`, lines 287–300 and 300–306): empty scope →
`in_scope_ref = []` → `share = None` → `d_state = "out-of-scope"` →
`certifiable_d = True`. That is exactly the "out-of-scope" in the report
tables: **the blade never evaluated the bare P4 units because their
in-scope set is empty by construction.**

### Is that within the P003 text as written?

P003 Amendment 2 defines scope as *"shift-surface queries targeting c's
members … where an involved object is a member of c at query time; for
rules, where the query matches the rule's action and involves a member
of its host class; for composites, the union of member scopes"*, and
adds *"A unit with an empty in-scope reference-resolved set is
out-of-scope and follows the (d)-untested-correct path."* An attribute
has no object-members (objects are members of classes, not of
attributes), so a bare P4's scope is empty **as written**; the code
follows the text. The designed reach of the blade onto attributes is
the **composite unit** (P003 Condition 1: attribute + referencing
rules), and the composites WERE evaluated — on the marker runs they land
`uncertifiable-untested` at shares ≈ 0.60 while the bare P4 inside them
certifies.

### Do AURule/APRule units fall outside the scoping text?

No — but they are scoped **more broadly than the text**, not outside it.
P5/P6 rules have no host class (their expressions reference attributes),
so the text's "member of its host class" clause cannot apply; the frozen
code (lines 97–98, 105–110) scopes them **action-wide**: every
shift-surface query with a matching action is in scope. The blade did
bite them under that broader scoping — the P5/P6 singleton units show
shares 0.21–0.75 and land `uncertifiable-untested` throughout the scored
runs. The only production the blade cannot reach as a singleton is the
bare P4.

## 2. Sensitivity run — attributed-classes scoping

Recomputed per the hold: in-scope = shift-surface, reference-resolved
queries involving a member of any class carrying the unit's attributions
(taken from the substrate's authoritative `engine.lib.attributions`);
credit = resolved AND correct (the frozen definition); share =
1 − credit/|in-scope-ref|; θ_ev = 0.15. Every marker unit is attributed
on all 6 classes, so this scoping is effectively the entire
member-involving shift surface.

| Run | Unit | attributed classes | in-scope-ref | credit | share | ≤ θ_ev 0.15? |
|---|---|---|---|---|---|---|
| 201/23 | k47 | 6 | 692 | 448 | 0.3526 | **NO** |
| 202/23 | k47 | 6 | 692 | 423 | 0.3887 | **NO** |
| 203/23 | k47 | 6 | 692 | 420 | 0.3931 | **NO** |
| 204/23 | k47 | 6 | 692 | 425 | 0.3858 | **NO** |
| 205/23 | k47 | 6 | 692 | 447 | 0.3540 | **NO** |
| 203/29 | k49 | 6 | 751 | 470 | 0.3742 | **NO** |
| 203/29 | k50 | 6 | 751 | 470 | 0.3742 | **NO** |
| 204/29 | k48 | 6 | 749 | 454 | 0.3939 | **NO** |
| 204/29 | k49 | 6 | 749 | 454 | 0.3939 | **NO** |
| 205/29 | k48 | 6 | 749 | 452 | 0.3965 | **NO** |
| 205/29 | k49 | 6 | 749 | 452 | 0.3965 | **NO** |
| 201/31 | k52, k53 | 6 | 673 | 422 | 0.3730 | **NO** |
| 202/31 | k52, k53 | 6 | 673 | 432 | 0.3581 | **NO** |
| 203/31 | k52, k53 | 6 | 673 | 436 | 0.3522 | **NO** |
| 204/31 | k52, k53 | 6 | 673 | 423 | 0.3715 | **NO** |
| 205/31 | k52, k53 | 6 | 673 | 424 | 0.3700 | **NO** |

(201/29 and 202/29 fired no marker; nothing to evaluate there.)

**Reachability check, same scoping, same streams:** OracleIdent's
certified P4 attribute units score shares **0.0505 / 0.0556 / 0.0557**
(streams 23/29/31), in-scope-ref 790–863 — comfortably ≤ θ_ev. The
attributed-classes blade is therefore honest-reachable at the frozen
threshold; it is not a stricter-than-achievable test.

## 3. Conclusions, one line per unit

- **k47 (stream 23, all 5 seeds):** does NOT clear θ_ev under
  attributed-classes scoping (0.353–0.393 vs 0.15).
- **k48/k49/k50 (stream 29, seeds 203–205):** do NOT clear θ_ev
  (0.374–0.397 vs 0.15).
- **k52/k53 (stream 31, all 5 seeds):** do NOT clear θ_ev
  (0.352–0.373 vs 0.15).

## 4. Plain statement of what this means

Under the frozen, preregistered P003 scoping the marker certification
stands as reported: bare P4 units are out-of-scope for the blade by the
A2 text, the composites carry the blade and were reported
uncertifiable-untested alongside. Under the reviewer's
attributed-classes scoping, **no P4 marker unit would certify on any of
the 13 marker runs, and the marker would not fire** — while the honest
identification oracle clears the same blade at 0.05. The positive is
therefore **scoping-dependent**: Candidate E's ~37% shift-surface
abstention is a real deficiency that the frozen scoping does not test on
bare attributes. Whether this is (a) a named limitation the EXP1-
QUALIFIED verdict already carries, or (b) an operationalization defect
in the P003 scope text requiring an addendum and re-run under the L3-2
STOP semantics, is a criteria question — a Director ruling, per the
charter. The measurement itself is above, committed, deterministic.
