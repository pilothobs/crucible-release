# ANALYSIS_DEFECT_001 — token→kind mapping ignored the display permutation

**Found:** 2026-08-30, during E.2 failure decomposition (an impossible
row — a cracked-condition view on a pristine-arrival object — was the
smoking gun; the world defines cracked as arrival-only).

**Defect.** The generator permutes display slots (`perm`: slot → latent
index; threat-PL2 mitigation). Token `oN` is display slot N; its kind is
`kinds[perm[N]]` and its arrival `arrival[perm[N]]`
(`crucible/engine.py::_episode`). Several ANALYSIS scripts mapped
`kinds[N]` / `arrival[N]` directly. Measured on dev 998: 340 of 6078
view-attributions mislabeled under the naive mapping; 0 under the
corrected one.

**Affected (analysis layer only; superseded, retained):**

1. `per_cell_all_runs.json` / `PER_CELL_TABLES.md` (commit 1618ee4; both
   gists) — kind-pair labels misattributed across cells. Superseded by
   `per_cell_all_runs_v2.json` / `PER_CELL_TABLES_v2.md`. Per-run totals
   and accuracies are unchanged; only labels move.
2. `vpass.json` `per_cell_stream23_seed201` — same defect; the v2 table
   for 201/23 supersedes it.
3. `vpass.json` / `vpass_exp1.py` `d_branches` — cracked-site
   classification used `arrival[N]`. Recounted with the correct mapping:
   **body-edit 5/5 seeds (3–12 cited events per run), split 0/5** — the
   committed conclusion stands unchanged.
4. **The D–E diagnostic line** (DECISIONS.md ruling entry; relabel §;
   review-bundle Part C "weakest cell" sentence; cited in the Director's
   H2 ruling). CORRECTED: under the true mapping the D–E cell
   ((0,1,0),(1,1,0)) resolves hypothetically at **0.542–0.625 over 24
   queries per run** — comparable to the other holdout cells
   (0.583–0.708 on 201/23) — not the 0.0/3 catastrophic failure v1
   showed. There is no confirmed D–E transfer failure. The A1.1(4)
   attribution-ambiguity observation from development stands as a dev
   observation, but the scored-run evidence attributed to it was a label
   artifact. E's real pair cells remain abstention-heavy across ALL
   cells (0.05–0.31), which is the true (and already-ruled-on) gap.

**Unaffected:** every certification and verdict (P003 and P004 machinery
never touch kind labels); all abstention shares (membership-based); the
H2 blade-scope finding and the P004 relabel; the cohort-correctness
checks (behavior-profile keyed, not index keyed); MDL, determinism,
controls, decoys, stream validation.

**Corrections committed alongside:** `percell_v2.py`,
`per_cell_all_runs_v2.json`, `PER_CELL_TABLES_v2.md`, and this note.
v1 artifacts retained (superseded, never deleted).
