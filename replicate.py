"""CRUCIBLE release — one-command replication of the verdict artifacts.

Stock Python 3.12, zero dependencies.  Stages the frozen code and freeze
manifests into a runtime tree matching the paths the frozen runners
expect (the runners are byte-identical to their certified digests and
open research-phase relative paths like `l3_5/FREEZE_EXP2.json`; the
staging step recreates that layout from this repository's taxonomy
without modifying any frozen file), then:

  1. regenerates all ten programme corpora from the ledger seeds and
     compares canonical fingerprints against the committed record;
  2. re-runs the Candidate E.2 scored matrix (5 seeds x 3 streams);
  3. re-runs the P004 replay of Candidate E (the retraction artifact);
  4. re-runs the Candidate E.3 matrix with its prediction evaluation;

byte-comparing each output against the committed artifact and ending
with one PASS/FAIL line per artifact plus the total runtime.  Expected
wall time: about 2–4 minutes on a modern CPU.  Exit code 0 iff all PASS.
"""
import filecmp
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(HERE, "_runtime")

STAGE = {
    "crucible": [("crucible/" + f, "crucible/" + f)
                 for f in os.listdir(os.path.join(HERE, "crucible"))
                 if f.endswith(".py")],
    "l3_2": [("certifiers/certify.py", "l3_2/certify.py"),
             ("certifiers/certify_p003.py", "l3_2/certify_p003.py"),
             ("certifiers/certify_p004.py", "l3_2/certify_p004.py"),
             ("contenders/contenders.py", "l3_2/contenders.py")],
    "l3_3": [("contenders/proposer.py", "l3_3/proposer.py")],
    "l3_5": [("contenders/candidate_e.py", "l3_5/candidate_e.py"),
             ("contenders/candidate_e2.py", "l3_5/candidate_e2.py"),
             ("contenders/candidate_e3.py", "l3_5/candidate_e3.py"),
             ("runners/run_exp2.py", "l3_5/run_exp2.py"),
             ("runners/run_exp3.py", "l3_5/run_exp3.py"),
             ("runners/recertify_p004.py", "l3_5/recertify_p004.py"),
             ("artifacts/FREEZE.json", "l3_5/FREEZE.json"),
             ("artifacts/FREEZE_P004.json", "l3_5/FREEZE_P004.json"),
             ("artifacts/FREEZE_EXP2.json", "l3_5/FREEZE_EXP2.json"),
             ("artifacts/FREEZE_EXP3.json", "l3_5/FREEZE_EXP3.json"),
             ("artifacts/scored_runs_exp2.json",
              "l3_5/scored_runs_exp2.json")],
}

COMPARE = [
    ("l3_5/scored_runs_exp2.json", "artifacts/scored_runs_exp2.json",
     "E.2 scored matrix"),
    ("l3_5/scored_runs_p004.json", "artifacts/scored_runs_p004.json",
     "P004 replay of Candidate E"),
    ("l3_5/scored_runs_exp3.json", "artifacts/scored_runs_exp3.json",
     "E.3 matrix + prediction"),
]


def stage():
    if os.path.exists(RUN):
        shutil.rmtree(RUN)
    for pkg, files in STAGE.items():
        os.makedirs(os.path.join(RUN, pkg), exist_ok=True)
        open(os.path.join(RUN, pkg, "__init__.py"), "w").close()
        for src, dst in files:
            shutil.copyfile(os.path.join(HERE, src),
                            os.path.join(RUN, dst))


def fingerprints():
    sys.path.insert(0, RUN)
    old = os.getcwd()
    os.chdir(RUN)
    try:
        from crucible.gen import generate_corpus
        got = {str(s): hashlib.sha256(
            repr(generate_corpus(s)).encode()).hexdigest()
            for s in (23, 29, 31, 997, 998, 999, 1009, 1013, 1019, 1021)}
    finally:
        os.chdir(old)
        sys.path.remove(RUN)
    want = json.load(open(os.path.join(HERE, "artifacts",
                                       "corpus_fingerprints.json")))
    return got == want, len(want)


def main():
    t0 = time.time()
    print("CRUCIBLE replication — staging runtime tree")
    stage()
    results = []
    ok, n = fingerprints()
    results.append(("corpus fingerprints (%d streams)" % n, ok))
    print("%-42s %s" % (results[-1][0], "PASS" if ok else "FAIL"))
    for script in ("l3_5/run_exp2.py", "l3_5/recertify_p004.py",
                   "l3_5/run_exp3.py"):
        print("running", script, "...")
        r = subprocess.run([sys.executable, script], cwd=RUN,
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-2000:])
            print(r.stderr[-2000:])
            results.append((script, False))
    for produced, committed, label in COMPARE:
        ok = filecmp.cmp(os.path.join(RUN, produced),
                         os.path.join(HERE, committed), shallow=False)
        results.append((label, ok))
        print("%-42s %s" % (label, "PASS" if ok else "FAIL"))
    dt = time.time() - t0
    allok = all(ok for _l, ok in results)
    print("-" * 60)
    for label, ok in results:
        print("%-42s %s" % (label, "PASS" if ok else "FAIL"))
    print("TOTAL: %s in %.0f s" % ("PASS" if allok else "FAIL", dt))
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
