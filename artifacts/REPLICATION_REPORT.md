# WO-EID-L3-6 Replication Report — clean-environment reproduction of the
# SUMMIT verdict artifacts

**Result: EXACT MATCH on every compared artifact. No divergence.**

## Environment

| | Original (Axiom) | Replication |
|---|---|---|
| Execution | host, /mnt/raid (md0 raid) | Docker container, `--network none` |
| Filesystem | /mnt/raid/Eidolon | container overlayfs; clone staged on the root LVM (/dev/mapper/ubuntu--vg), a different physical filesystem |
| Python | system 3.12.3 (Ubuntu) | image `python:3.12-slim` (id sha256:09f7da3bc104…), CPython **3.12.14**, GCC 14.2.0 — independently installed |
| Source | working checkout | `git clone` of the repo, checked out at the **closure commit 0af3a88** |
| Network | n/a | **disabled** for the replication run |

Dependencies: the entire CRUCIBLE/contender/certifier stack is Python
stdlib only (verified by import scan); nothing was installed into the
image.

## What was re-run and compared

1. **Corpus fingerprints** — sha256 over the canonical serialization of
   `generate_corpus(s)` for all ten programme streams
   (23/29/31, 997/998/999, 1009/1013/1019, 1021), computed independently
   on host and in the container: **10/10 identical.**
2. **EXP2 scored matrix** (`l3_5/run_exp2.py`, frozen E.2 digest
   asserted in-run): container output **byte-identical** to the
   committed `l3_5/scored_runs_exp2.json`
   (sha256 `be0c56b40cd1269b51e850cadeac62582469a9c6e36b33e2896403cc8078c235`).
   Endpoint reproduced: PRIMARY-MET 5/5 seeds.
3. **P004 replay of Candidate E** (`l3_5/recertify_p004.py`, frozen E
   and certify_p004 digests asserted): **byte-identical** to
   `l3_5/scored_runs_p004.json`
   (sha256 `a4f451532a0723441e628d80bbf09421026cfa5eee6a427d59793a2dd9e0df17`).
   Endpoint reproduced: marker 0/15, PRIMARY-NOT-MET-UNDER-P004.
4. **EXP3 scored matrix + prediction evaluation**: **byte-identical** to
   `l3_5/scored_runs_exp3.json`
   (sha256 `62ff7a01f5753f577bb294521566cf4805365097bb042ca511722abbbec4d9f0`).
   Verdict reproduced: E3-CONFIRMED (P1 5/5+5/5, P2 met, P3 5/5).

Certification outputs are embedded in artifacts 2–4 (per-unit criteria
records, marker decisions); byte-identity of the files is byte-identity
of the certification outputs.

## Findings

1. **No divergence.** Different filesystem, independently installed
   interpreter (3.12.14 vs 3.12.3), no network, clone at the closure
   commit: every fingerprint, scored row, and certification output
   reproduced exactly.
2. **Record repair, disclosed:** the EXP3 driver used at verdict time
   was not committed at closure (it ran from an inline script). It was
   reconstructed as `l3_5/run_exp3.py`, verified on the original host to
   reproduce the committed artifact byte-identically, committed at
   `00741bf`, and injected into the clone for the replication (it is the
   one file the container ran that is not inside 0af3a88; it touches no
   frozen artifact, and the artifact it regenerates matched byte-for-
   byte).

## Scope

This is a same-machine, different-environment replication (fresh
container, isolated network, different filesystem and interpreter). It
is not an independent-hardware or independent-operator replication;
single-experimenter closure remains on the Director's permanent
residual list.
