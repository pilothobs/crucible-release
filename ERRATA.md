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
