# PROVENANCE — preregistration timeline evidence (added post-release, 2026-09-05)

This file and the `provenance/` directory were added after the release
(see `ERRATA.md`, E3). They alter no frozen byte: no preregistration or
verdict artifact was modified. `MANIFEST.json` — the release's non-frozen
file index (see ERRATA E1) — was regenerated in the same commit to list
them, as it was for every earlier non-frozen edit.

## Disclosure (verbatim as carried in the paper, §2.1)

Preregistration provenance. The criteria document (PREREGISTRATION_001) was committed at 2026-08-28T19:13:17Z and is byte-identical to its first commit (SHA-256 702994301924dda574df73a91a5895f7cde6079c8c04e57708a28dca32229455). Its existence at that time is witnessed by a third party: GitHub recorded creation of branch research/eid-l3 at 2026-08-28T19:18:00Z pointing at commit 9b63cd0, whose sole parent is the criteria commit c780b02. The first executable instrument code reached the same server at 2026-08-28T21:19:32Z, and no contender existed until 2026-08-29T00:21:24Z. We note the limits of this evidence: no commit in the lineage is cryptographically signed, no OpenTimestamps or OSF anchor was created at the time, and a platform activity log is a business record rather than a proof. We further disclose that PREREGISTRATION_002 — the L3-1 freeze specification, distinct from the criteria — was revised in place 40 minutes after it was committed, changing the holdout set and two gate thresholds; that revision predates any contender code. The criteria themselves were never modified.

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
- `github_activity_capture.json.ots`, `eid-l3-history.bundle.ots` —
  OpenTimestamps receipts (stamped 2026-09-05, pending Bitcoin attestation;
  `ots upgrade` then `ots verify` to complete).

The `.ots` receipts prove existence of the stamped files as of the
stamping date (2026-09-05) only; they do not retroactively establish the
2026-08-28 dates, which rest on GitHub's platform log captured above.

## Full-history bundle

A `git bundle` of the complete private lineage of `research/eid-l3`
(`eid-l3-history.bundle`, SHA-256
`d941d03dbc7851e3ee35b05081b16b333d9c089d9490683c04ba5fe6c97215c6`, ref
`1d7d7048bf3f9e8251c9a6ff632b8e2489053a14`) exists in the research
repository and is timestamped by `provenance/eid-l3-history.bundle.ots`.
It is **not published here**; it is available from the author on request.
