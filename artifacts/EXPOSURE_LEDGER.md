# Exposure ledger — every generator seed ever used in the programme

Extracted from PREREGISTRATION_L35_EXP2 section 3 (committed before the
EXP2 verdict streams existed) and extended by the EXP3 draw. Verdict-
bearing streams are drawn by preregistered rule from this ledger; a
contender claiming fresh-stream results must extend it the same way.

| Seed(s) | Role |
|---|---|
| 17 | Candidate D-era eval stream; also exposed in D development; used with leak variants in the audit/planted-fixture runs |
| 18, 19 | D-era eval streams (D scoring, controls, D falsification pass) |
| 23, 29, 31 | EXP1 verdict streams (Candidate E scoring, H2 analyses, P004 validation and replay) — burned |
| 997, 998, 999 | development streams (never verdict-bearing) |
| 1009, 1013, 1019 | EXP2 verdict streams (rule: three smallest primes > 1000 not in the ledger at draw time) — burned |
| 1021 | EXP3 fresh stream (same rule, drawn after 1009/1013/1019 entered the ledger) — burned |
| 731001–731006 | named internal RNG stream constants (offset by corpus seed; not corpus seeds) |
| 731007 | SEED_HOLDOUT (holdout-pair draw under the preregistered rule) |

Draw rule for new verdict streams: the smallest primes greater than 1000
not appearing above, committed to a preregistration before any stream is
generated, each stream validated two-sidedly (both oracles certify the
marker at composite level; every control certifies nothing; the cluster
regression form holds) before any contender exposure.
