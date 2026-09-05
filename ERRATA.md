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

## E4 — paper §7.5 overstated the split branch (mirrors the research log's ERRATUM E3)

The paper (draft v2; Zenodo v2, DOI 10.5281/zenodo.22177155) says in §7.5
that the split branch of criterion (d) "was never exercised" and that "no
contender in the programme ever needed the mis-join→split→remap pathway."
The L3-3 record contradicts the programme-wide form. Candidate D exercised
it: `artifacts/scored_runs_candidate_d.json` (SHA-256
0e376435a4a3fb614249d484c798bb4e91f93752ceb727ca669b9ae42e8d5c65) carries
`endpoints.d_split_seeds_of_5 = 4` — the preregistered rule counts a
training seed when split-revised units pass (d) on at least 2 of its 3
evaluation streams — and `artifacts/vpass_candidate_d.json` (SHA-256
21e11f8dc0e1b0699132035b7a7d7516f0386250de7d2362a6cf4b10bd6495da) records
14 (d)-passed units on stream 18 independently re-derived from the
operation and violation logs (`independent_agreement: true`), four of them
class (P1) units revised by membership-move splits. No attribute (P4) unit
passed (d) in Candidate D, and Candidate D certified nothing (verdict
L3-NEGATIVE). Corrected statement: the split branch was exercised once in
the programme, by a non-certifying contender on class units — never by a
certifying contender, and never on an adopted attribute unit. The §7.5
limitation (revision-under-contradiction of an adopted attribute has not
been demonstrated) stands. Corrected in the paper draft v2.1 on 2026-09-05
(research repository); the published PDF carries it at its next version.
No frozen byte changed.

## E5 — provenance wording corrections (2026-09-05)

Three corrections to the provenance record added under E3, made the same
day. (1) The description of the PREREGISTRATION_002 in-place revision is
corrected: it read "changing the holdout set and two gate thresholds"; the
revision replaced the holdout set with a rule-derived set, updated two
reported fc_unseen measurements, rewrote the A9 planted-leak margin
analysis, and added two scoring conventions, and left the frozen decision
thresholds (δ_b, δ_e, θ_ev, f_d, τ_d, α) untouched — the complete diff is
now reproduced in `PROVENANCE.md` and in the paper's Appendix G. (2) A
reconciliation of the E1 date labels with the commit record and the
third-party log is added to `PROVENANCE.md` and the paper's §2.1. (3) The
OpenTimestamps `.ots` files are now correctly characterized as calendar
receipts pending Bitcoin attestation, not completed timestamp proofs; E3's
closing sentence ("Timestamps made on 2026-09-05 prove existence as of that
date only") is to be read accordingly — once upgraded and verified they will
attest to existence as of that date only. `MANIFEST.json` regenerated
(authorized). No preregistration or verdict artifact modified.
