# ERRATA — corrections to the record that alter no frozen byte

Files under a freeze digest (the `FREEZE*.json` manifests, the
preregistration history, the verdict artifacts, the replication report)
are never edited after the fact. Corrections to the record are made
here instead. Ordering and integrity in this programme are carried by
commit hashes and SHA-256 digests, not by prose dates.

## E1 — one-day date-label error in late-SUMMIT documents

Several documents authored late in the SUMMIT session carry the date
**2026-08-30**:

- `artifacts/ANALYSIS_DEFECT_001.md` ("Found: 2026-08-30")
- `artifacts/FREEZE_EXP2.json`, `artifacts/FREEZE_EXP3.json`
  (`"frozen": "2026-08-30"`)
- `preregistrations/PREREGISTRATION_004_COMPOSITE_CERTIFICATION.md`
  (Director ruling date in the header)
- `preregistrations/PREREGISTRATION_L35_EXP2.md` (Amendment 1 date)
- `MANIFEST.json` prior to this correction (`"date": "2026-08-30"`)

The research repository's commit timestamps show all of this work was
committed **2026-08-28/29 UTC** — every file above landed 2026-08-29,
and the closure commit `0af3a88` is 2026-08-29 14:07 UTC. At release
scrub the host clock was verified NTP-synchronized (UTC); the 08-30
labels are an authoring error (the date was written one day ahead), not
a clock fault and not evidence of later work. No ordering claim depends
on a prose date. The mislabeled files are byte-frozen and remain
unedited; `MANIFEST.json` is the only non-frozen file affected and is
corrected in place.

## E2 — environment identifiers in the byte-frozen replication report

The environment table in `artifacts/REPLICATION_REPORT.md` names the
original execution host ("Axiom") and its filesystem paths (`/mnt/raid`,
`/mnt/raid/Eidolon`). The report is byte-frozen — its digest is part of
the replication record — and the identifiers carry no secret content;
they describe the environment the replication was run against, which is
the report's job. Ruled at release scrub: the lines stay.

## E3 — provenance evidence added post-release (2026-09-05)

`PROVENANCE.md` and `provenance/` were added on 2026-09-05, after the
release and after the Zenodo deposits. They carry a third-party
(GitHub platform-log) witness that the criteria document
(`preregistrations/PREREGISTRATION_001_CONCEPT_CRITERIA.md`, SHA-256
`702994301924dda574df73a91a5895f7cde6079c8c04e57708a28dca32229455`)
existed on 2026-08-28T19:18:00Z, before any instrument code reached the
server (2026-08-28T21:19:32Z), together with OpenTimestamps receipts made
on 2026-09-05. They also disclose that `PREREGISTRATION_002` — the L3-1
freeze specification, not the criteria — was revised in place 40 minutes
after it was first committed and before any contender code existed; the
committed file is byte-frozen and unedited here, and the literal delta is
given in the paper's Appendix G. No preregistration or verdict-artifact byte was
changed by this addition; `MANIFEST.json` (non-frozen, per E1) was
regenerated in the same commit to index the new files and this entry. Timestamps made on 2026-09-05 prove existence
as of that date only.
