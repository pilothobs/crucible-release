"""Recompute SHA-256 for every file in MANIFEST.json and report
OK / ALTERED / MISSING per file; exit 0 iff all OK."""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    man = json.load(open(os.path.join(HERE, "MANIFEST.json")))
    bad = 0
    for path, want in sorted(man["files"].items()):
        full = os.path.join(HERE, path)
        if not os.path.exists(full):
            print("MISSING ", path)
            bad += 1
            continue
        got = hashlib.sha256(open(full, "rb").read()).hexdigest()
        if got != want:
            print("ALTERED ", path)
            bad += 1
    print("%d files, %d problems -> %s"
          % (len(man["files"]), bad, "OK" if not bad else "FAIL"))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
