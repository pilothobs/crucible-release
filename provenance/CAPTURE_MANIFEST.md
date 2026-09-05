# CAPTURE_MANIFEST — CRUCIBLE preregistration provenance anchor

Directory: `ucs_research/eid_l3/provenance/` (research repository, branch
`research/eid-l3`). Produced under the Director's WO "CRUCIBLE provenance
repair: preserve anchor, disclose, publish" (2026-09-05). Every value below
is the raw output of the command shown beside it.

## 1. Capture time

`date -u +%Y-%m-%dT%H:%M:%SZ` → **2026-09-05T15:54:40Z** (host clock
NTP-synchronized: `timedatectl show -p NTPSynchronized` → `NTPSynchronized=yes`).
Captured from a `git worktree` checkout of `research/eid-l3` at HEAD
`1d7d7048bf3f9e8251c9a6ff632b8e2489053a14` (the main working tree was left on
`research/arc3` because an experiment was running in it).

## 2. Capture commands (raw bytes as returned; not filtered, sorted, or pretty-printed)

```
gh api "repos/pilothobs/A-Unified-Cognitive-Substrate-for-General-Intelligence/activity?per_page=100&time_period=quarter" --paginate > github_activity_capture.json
gh api repos/pilothobs/A-Unified-Cognitive-Substrate-for-General-Intelligence/events --paginate > github_events_capture.json
```
`--paginate` concatenates the API's page arrays back-to-back; the files are
therefore sequences of JSON arrays, exactly as `gh` emitted them.

## 3. Load-bearing row, verified present in the capture (read-only query)

```
jq -c '.[] | select(.activity_type=="branch_creation" and .ref=="refs/heads/research/eid-l3") | {timestamp,activity_type,ref,before,after}' github_activity_capture.json
{"timestamp":"2026-08-28T19:18:00Z","activity_type":"branch_creation","ref":"refs/heads/research/eid-l3","before":"0000000000000000000000000000000000000000","after":"9b63cd0a727ab5fec41b4295384d592fce376a2b"}
```
`9b63cd0a727ab5fec41b4295384d592fce376a2b`'s sole parent is the criteria
commit `c780b026fe46ffc3f76c3c4df699a5725ed1c943` (PREREGISTRATION_001,
2026-08-28T19:13:17Z). The push carrying the first executable instrument code
(`595d7ba6adab065499b4bff5d7bac6fac9a77c71`, with `3253606…`) appears in the
events capture at `created_at` **2026-08-28T21:19:33Z** and in the activity
capture at **2026-08-28T21:19:32Z**.

## 4. History bundle (NOT published; available from the Director on request)

```
git -C <worktree> bundle create ucs_research/eid_l3/provenance/eid-l3-history.bundle research/eid-l3
git -C <worktree> bundle verify ucs_research/eid_l3/provenance/eid-l3-history.bundle
ucs_research/eid_l3/provenance/eid-l3-history.bundle is okay
The bundle contains this ref:
1d7d7048bf3f9e8251c9a6ff632b8e2489053a14 refs/heads/research/eid-l3
The bundle records a complete history.
The bundle uses this hash algorithm: sha1
```
The bundle carries the complete private lineage of `research/eid-l3`
(124 commits, 2025-11-25 → 2026-09-05); its publication is a Director
decision outside this WO.

## 5. SHA-256 of every file in this directory (`sha256sum <file>`)

| sha256 | file |
|---|---|
| `d941d03dbc7851e3ee35b05081b16b333d9c089d9490683c04ba5fe6c97215c6` | `eid-l3-history.bundle` |
| `186f3471a885d909b30e7f261d5bf6eea19f4eb572ba2e6ec6cefd0d257a1bb3` | `eid-l3-history.bundle.ots` |
| `eb401797eb069ca4952a60fbb6177b38936a50838853547f4097e742e61656d1` | `github_activity_capture.json` |
| `6293323b81413c83dab65c5f13ce32ebe62aa070171b3643561ac40771a5f31f` | `github_activity_capture.json.ots` |
| `7ebe4deaec96ac8a0bdd0b02d15fa89780f77fa655ae69fd6c42b2b40e979465` | `github_events_capture.json` |

## 6. OpenTimestamps

`which ots` → not found. Single install attempt:
`python3 -m venv <scratch>/ots-venv && <scratch>/ots-venv/bin/pip install opentimestamps-client`
→ succeeded, client `v0.7.2`. Then:

```
ots stamp github_activity_capture.json
ots stamp eid-l3-history.bundle
Submitting to remote calendar https://a.pool.opentimestamps.org
Submitting to remote calendar https://b.pool.opentimestamps.org
Submitting to remote calendar https://a.pool.eternitywall.com
Submitting to remote calendar https://ots.btc.catallaxy.com
```
Both stamps succeeded (exit 0). `ots info` on each `.ots` reports the file
SHA-256 it commits to: `github_activity_capture.json.ots` →
`eb401797eb069ca4952a60fbb6177b38936a50838853547f4097e742e61656d1`;
`eid-l3-history.bundle.ots` → `d941d03dbc7851e3ee35b05081b16b333d9c089d9490683c04ba5fe6c97215c6`.
**Status: stamped, pending Bitcoin attestation** — the calendars return a
pending receipt; run `ots upgrade <file>.ots` (typically after some hours)
and then `ots verify <file>.ots` to obtain and check the Bitcoin block
attestation. The `.ots` files are committed as generated.

## 7. What timestamping does and does not establish

Timestamping proves existence as of the stamping date (2026-09-05) only. It
does **not** retroactively establish the 2026-08-28 dates. Those dates rest on
GitHub's platform activity log (a business record, captured above), on the
commit chain (`c780b02` → `9b63cd0`), and on the commit objects' own
self-generated timestamps. No commit in the lineage is cryptographically
signed, and no OpenTimestamps or OSF anchor was created at the time.
