# PROVENANCE — preregistration timeline evidence (added post-release, 2026-09-05)

This file and the `provenance/` directory were added after the release
(see `ERRATA.md`, E3 and E5). They alter no frozen byte: no preregistration or
verdict artifact was modified. `MANIFEST.json` — the release's non-frozen
file index (see ERRATA E1) — was regenerated in the same commit to list
them, as it was for every earlier non-frozen edit.

## Disclosure (verbatim as carried in the paper, §2.1)

Preregistration provenance. The criteria document (PREREGISTRATION_001) was committed at 2026-08-28T19:13:17Z and is byte-identical to its first commit (SHA-256 702994301924dda574df73a91a5895f7cde6079c8c04e57708a28dca32229455). Its existence at that time is witnessed by a third party: GitHub recorded creation of branch research/eid-l3 at 2026-08-28T19:18:00Z pointing at commit 9b63cd0, whose sole parent is the criteria commit c780b02. The first executable instrument code reached the same server at 2026-08-28T21:19:32Z, and no contender existed until 2026-08-29T00:21:24Z. We note the limits of this evidence: no commit in the lineage is cryptographically signed, no OpenTimestamps or OSF anchor was created at the time, and a platform activity log is a business record rather than a proof. We further disclose that PREREGISTRATION_002 — the L3-1 freeze specification, distinct from the criteria — was revised in place 40 minutes after it was committed: the holdout set was replaced with a rule-derived set, two reported fc_unseen measurements were updated, the A9 planted-leak margin analysis was rewritten, and two scoring conventions were added. The frozen decision thresholds (δ_b, δ_e, θ_ev, f_d, τ_d, α) were not among the changes. That revision predates any contender code. The criteria themselves were never modified; Appendix G gives the complete diff.

On the date labels in this record. Several documents in this release — certain freeze manifests, analysis artifacts, and preregistrations other than PREREGISTRATION_001 — carry an internal date of 2026-08-30, while the commit record and the third-party log above place the work on 2026-08-28/29 UTC. These are authoring errors in the written date labels, recorded as ERRATUM E1; the frozen files were left unedited and only MANIFEST.json was corrected. Two points bear on how a reader should weigh this. First, PREREGISTRATION_001 — the criteria document on which the certification rests — carries no date in its text at all; its binding statement is that it was committed before any world, substrate, generator, or contender code existed, and that ordering is what the external anchor establishes. Second, every affected label is forward-dated: the documents claim to be later than they are, not earlier. A record altered to strengthen a priority claim would be dated earlier, not two days after the events it precedes.

("Appendix G" is the paper's appendix; the same complete diff is reproduced at the end of this file.)

## What is in `provenance/`

| sha256 | file |
|---|---|
| `eb401797eb069ca4952a60fbb6177b38936a50838853547f4097e742e61656d1` | `provenance/github_activity_capture.json` |
| `7ebe4deaec96ac8a0bdd0b02d15fa89780f77fa655ae69fd6c42b2b40e979465` | `provenance/github_events_capture.json` |
| `aa39ad20c5b477de30d1dcfb7c9863bd2cdc4e55c0c39ce7ae0ac2049bdb2766` | `provenance/CAPTURE_MANIFEST.md` |
| `6293323b81413c83dab65c5f13ce32ebe62aa070171b3643561ac40771a5f31f` | `provenance/github_activity_capture.json.ots` |
| `186f3471a885d909b30e7f261d5bf6eea19f4eb572ba2e6ec6cefd0d257a1bb3` | `provenance/eid-l3-history.bundle.ots` |

- `github_activity_capture.json` — raw, unmodified output of
  `gh api "repos/pilothobs/A-Unified-Cognitive-Substrate-for-General-Intelligence/activity?per_page=100&time_period=quarter" --paginate`,
  captured 2026-09-05T15:54:40Z. Contains the load-bearing row
  `{"timestamp":"2026-08-28T19:18:00Z","activity_type":"branch_creation","ref":"refs/heads/research/eid-l3","before":"0000000000000000000000000000000000000000","after":"9b63cd0a727ab5fec41b4295384d592fce376a2b"}`.
- `github_events_capture.json` — raw output of
  `gh api repos/pilothobs/A-Unified-Cognitive-Substrate-for-General-Intelligence/events --paginate`, same capture.
- `CAPTURE_MANIFEST.md` — capture time, exact commands, SHA-256 of every
  captured file, and the OpenTimestamps record.
- .ots files — OpenTimestamps calendar receipts, submitted 2026-09-05, pending Bitcoin attestation. These are not yet completed timestamp proofs; ots upgrade followed by ots verify is required once the attesting block is mined.

Once upgraded and verified, the `.ots` receipts will attest to the existence
of the stamped files as of the stamping date (2026-09-05) only; they do not
retroactively establish the 2026-08-28 dates, which rest on GitHub's platform
log captured above.

## Full-history bundle

A `git bundle` of the complete private lineage of `research/eid-l3`
(`eid-l3-history.bundle`, SHA-256
`d941d03dbc7851e3ee35b05081b16b333d9c089d9490683c04ba5fe6c97215c6`, ref
`1d7d7048bf3f9e8251c9a6ff632b8e2489053a14`) exists in the research
repository and is timestamped by `provenance/eid-l3-history.bundle.ots`.
It is **not published here**; it is available from the author on request.

## The PREREGISTRATION_002 in-place revision — complete diff

Commits `595d7ba6adab065499b4bff5d7bac6fac9a77c71` (file added, 2026-08-28T21:18:09Z; file SHA-256 98c20d07e1fef7dccc113332822b0fd0dd79307f58476a12fd104fdc1a60e4e2) → `f826d3e8fd30c833757f071b65b530b1b1d7a9e5` (revised, 2026-08-28T21:58:09Z; SHA-256 795379b73e28d59919b59210a2faee1202f2b8f7cf6babc4ae7ce82ac40f75db), research repository, branch research/eid-l3. First contender code: `4417ff3ce1768ec1711d5a559f2295b659b799d5`, 2026-08-29T00:21:24Z. The published `preregistrations/PREREGISTRATION_002_L3_1_FREEZE.md` is the revised (f826d3e) text, byte-frozen. Diff text SHA-256 58829d5c32598a70268aee92a0cf9bd20a206da7d800fb327758d391d0032b08, 66 lines:

```diff
diff --git a/ucs_research/eid_l3/PREREGISTRATION_002_L3_1_FREEZE.md b/ucs_research/eid_l3/PREREGISTRATION_002_L3_1_FREEZE.md
index 50ecce4..3fa15c2 100644
--- a/ucs_research/eid_l3/PREREGISTRATION_002_L3_1_FREEZE.md
+++ b/ucs_research/eid_l3/PREREGISTRATION_002_L3_1_FREEZE.md
@@ -23,10 +23,13 @@ committed before any further runs.
 
 Authoritative values in `l3_1/MANIFEST.json` `parameters`; headline: 5 objects
 × 32 steps (20 learner + 4 ambient + 8 scored), kinds K0 as listed with k_new
-= (0,0,1) splitting from k_old = (0,0,0) on α3; outcome-balanced holdout
-{A-B, A-D, B-C, C-E}; post-E_R kind weights **marginal-matched** to the
-measured pre-E_R rejection-sampling marginals (side-channel continuity at
-E_R); ε = 1e-3; proposal budget 4 × 96; membership ops per-step.
+= (0,0,1) splitting from k_old = (0,0,0) on α3; holdout **selected by rule
+from literal seed** (constraints H1–H4 stated first, spec §2.5 v0.4; 57
+eligible subsets; derived set {A-B, B-C, B-E, D-E}, 2× fuse / 2× crumble);
+post-E_R kind weights **marginal-matched** to the measured pre-E_R
+rejection-sampling marginals under that holdout (A .3009, B .0330, C .3007,
+D .1985, E .1669 — side-channel continuity at E_R); ε = 1e-3; proposal budget
+4 × 96; membership ops per-step.
 
 ## 3. Frozen criteria thresholds ⟨L3-1⟩ (spec §5), set from the L3-1
 measurements and frozen before any contender
@@ -62,10 +65,19 @@ memorizer the withheld datum) — the discard trail is in `L3_1_REPORT.md`.
 no grind event on that kind-cell has occurred earlier in the run — which is
 policy-dependent, because "never trained on" is a property of the run;
 per-policy n is therefore unequal and is always reported alongside.
-Remaining hypothetical queries are **fc_seen**. Measured at the gate:
-oracle 1.0 / oracle-with-identification 0.909 on fc_unseen, **every cheap
-control 0.000** — the compositional headroom exists and memorization cannot
-reach it.
+Remaining hypothetical queries are **fc_seen**. Measured at the freeze
+(rule-derived holdout): oracle 1.000 (n=12) and oracle-with-identification
+1.000 (n=12) on fc_unseen, **every cheap control 0.000** — the compositional
+headroom exists and memorization cannot reach it.
+
+**Scoring convention, fixed now (gate-hold check 2):** on the top-1 accuracy
+surface an **unresolved query scores 0** — declining to predict is not a
+hit; no realized uniform draw, no tie-break; one engine code path applies
+this to every policy and stratum. The uniform-chance reference 1/11 lives on
+the *coding* surface, where an unresolved query costs exactly log₂ 11 ≈ 3.46
+bits. Null-empty therefore scores 0.000 top-1 by construction while coding
+at exactly the uniform-chance bit rate — the corrected sense of "ties with
+chance by construction" (spec §6.2/§6.3 v0.4).
 
 ## 5. Verbatim re-anchoring of the marker's evidence (gate confirmation 3)
 
@@ -108,9 +120,16 @@ contender (each is in the spec v0.4 change log with its evidence)
   through its grind default and accepts a small violation stream there;
   reference-policy violations of this type are a modeling trade, not
   substrate unsoundness.
-- The A9 planted-leak discrimination margin is modest (normal kind-excess
-  0.04 vs fire threshold 0.06 vs planted 0.084); the probe fires on the
-  planted leak and is silent on the real generator, but the gap is not wide.
+- The ambient cue's kind excess is ≈ 0.10 under the rule-derived marginals —
+  by declaration (the causal-trap confound), priced by A9's outcome-excess
+  gate (measured 0.004, tol 0.06). The PL3 fixture is therefore
+  **differential**: it fires iff the planted excess exceeds the real
+  generator's measured excess by > 0.05 (measured: planted 0.19 vs real
+  0.10 → Δ ≈ 0.09, fires).
+- Under the rule-derived holdout, kind B's effective marginal is 0.033
+  pre-E_R (it sits in three held-out cells) — a declared consequence of
+  rejection enforcement; ≈ 99 B objects still occur pre-E_R, and A2/A1
+  margins clear their floors under this distribution.
 - `dissolve` is a declared outcome symbol that no reachable cell produces in
   v0.1; it is reserved, and its appearance anywhere is a stop condition.
 - Per-object memorization is *structurally* dead under this interface
```
