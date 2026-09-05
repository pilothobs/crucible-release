# Replications

This file records runs of the official CRUCIBLE replay. It is a **log of
claims**: entries marked *self-reported* were run by an outside operator and
have **not** been independently verified by the authors.

## How to run the official replay

```
git clone https://github.com/pilothobs/crucible-release
cd crucible-release
python3 selfverify.py      # recompute SHA-256 for every manifest file
python3 replicate.py       # official byte-exact replay
```

`selfverify.py` prints a summary line of the form
`76 files, 0 problems -> OK`. `replicate.py` regenerates the ten corpus streams
from the ledger and re-runs the scored artifacts, printing one PASS/FAIL line
per artifact plus the total; expected wall time is about 2–4 minutes on a
modern CPU, and the exit code is 0 iff all lines PASS:

```
corpus fingerprints (10 streams)           PASS
E.2 scored matrix                          PASS
P004 replay of Candidate E                 PASS
E.3 matrix + prediction                    PASS
TOTAL: PASS in ~120–200 s
```

## What a byte-exact PASS establishes — and what it does not

A `TOTAL: PASS` establishes **artifact integrity and determinism**: the released
files match their manifest hashes, and the scored matrices (E.2, the P004
Candidate-E retraction replay, and E.3 with its preregistered prediction)
regenerate **byte-for-byte** from the committed ledger on the operator's
machine. It does **not** establish **independent-operator validation**: the
official replay re-runs the paper's *own* pipeline in a fresh environment
(same-machine / different-container is exactly what the paper claims), so a PASS
confirms the release reproduces itself, not that a new operator with no shared
context, designing their own checks, reached the same scientific conclusion.
That independent step remains open.

## Replication log

| date | operator | environment | result | status |
|---|---|---|---|---|
| 2026-09-05 | third-party AI system (different vendor) | CPython 3.12.3, no extra packages, no network after clone | `TOTAL: PASS in 198 s`; selfverify 76 files / 0 problems | **self-reported, unverified** |
