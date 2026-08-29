# EID-L3 — Preregistration 001: Concept Criteria and the Level 3 Marker

**Status:** binding. Committed before any EID-L3 world code, substrate code, generator code,
or contender exists anywhere in this repository. The commit hash of this file is the freeze
point; everything in Phases L3-0 through L3-3 is gated by these criteria.

**Change control:** append-only programme rule inherited from CPL-009. These criteria may be
revised **only** by a versioned addendum (`PREREGISTRATION_002_…`, etc.) committed before any
further runs, and only under the Phase L3-2 STOP semantics (a cheap contender satisfying the
criteria proves the criteria wrong). The original text is never edited.

**Source:** EID-L3 charter (`Work_Orders/EID-L3.md`), Part 2, transcribed verbatim below.

---

## 1. Concept criteria (verbatim from the charter)

> A structure counts as an invented concept only if all of the following hold:
>
> (a) it is a named, inspectable object in the system's library, not a pattern in weights;
>
> (b) it is load-bearing — ablating it measurably degrades prediction;
>
> (c) it is paid for — it improves prediction per unit of description length, under an MDL
> accounting the substrate computes, so a lookup table fails by arithmetic, not argument;
>
> (d) it is revised, not replaced — after contradicting experience the system modifies that
> concept while the rest of the library stays intact, and the substrate logs the revision;
>
> (e) it is reused — it carries its predictive advantage across a generator shift it never
> trained on.

## 2. The Level 3 marker (verbatim from the charter)

> Also preregister the Level 3 marker: the appearance of a new concept kind (a type of
> structure not in the initial set) that satisfies (a)–(e).

## 3. Standing scope statement (verbatim from the charter)

> Level 3 in the honest form: the vocabulary and the set of concept kinds grow; the
> meta-grammar and primitives are given and declared. Zero given ontology is impossible;
> minimal and explicit is the standard.

---

## 4. Binding consequences, declared now

1. These five criteria and the marker **gate everything after**. No structure may be called
   a concept in any EID-L3 report unless the substrate's own accounting certifies (a)–(e).
2. The operationalization of each criterion (exact tests, thresholds, edit-distance and
   locality definitions, MDL code) is given in `L3_0_SPEC.md` §5 and freezes at the L3-1
   gate. The criteria themselves freeze **now**. If an operationalization is later shown to
   let a cheap control through, the operationalization is revised by addendum; the criteria
   text above is not.
3. The maximum claim at full success, verbatim from the charter, is:
   *"under a frozen synthetic world with substrate-guaranteed bookkeeping, a system
   invented, revised, and reused inspectable concepts satisfying preregistered criteria
   that cheap controls fail."*
   Nothing in this programme demonstrates AGI, general reasoning, or an LLM replacement,
   and no report may imply it.
4. Verdict vocabulary for Phase L3-3, inherited with CPL-009B semantics:
   L3-POSITIVE / L3-QUALIFIED / L3-PARTIAL / L3-NEGATIVE / APPARATUS-INVALID.
   A negative with a clean apparatus is a publishable finding.
