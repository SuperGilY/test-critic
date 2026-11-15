#!/usr/bin/env python3
"""Mechanical checks for a spec made by the spec-prep skill. No model, no judgment.

Usage: python3 validate_spec.py SPEC.md SOURCE.txt

Checks:
  1. Every rule has a Source quote.
  2. Every quote appears word for word in the source file (spaces and line breaks ignored).
  3. Rule IDs are unique.
  4. The "There are N rules" line matches the real count.
  5. Every quote is 15 words or fewer.
Exit code 0 when all pass, 1 otherwise.
"""
import re
import sys


def norm(t):
    return re.sub(r"\s+", " ", t).strip()


def main(spec_path, source_path):
    spec = open(spec_path, encoding="utf-8").read()
    source = norm(open(source_path, encoding="utf-8").read())
    problems = []
    rules = re.findall(r"^- (R\d+[a-z]?)\. (.*)$", spec, flags=re.M)
    ids = [r[0] for r in rules]
    for dup in {i for i in ids if ids.count(i) > 1}:
        problems.append(f"{dup}: ID used more than once.")
    for rid, rest in rules:
        m = re.search(r'\| Source: "(.+)"\s*$', rest)
        if not m:
            problems.append(f"{rid}: no Source quote.")
            continue
        q = norm(m.group(1))
        if q not in source:
            problems.append(f"{rid}: quote not found in the source: \"{q}\"")
        if len(q.split()) > 15:
            problems.append(f"{rid}: quote is longer than 15 words.")
    n = re.search(r"There are (\d+) rules", spec)
    if not n:
        problems.append("Missing the line 'There are N rules'.")
    elif int(n.group(1)) != len(rules):
        problems.append(f"Header says {n.group(1)} rules, found {len(rules)}.")
    print(f"Rules: {len(rules)}")
    if problems:
        print(f"\n{len(problems)} problem(s):")
        for p in problems:
            print(" -", p)
        return 1
    print("All mechanical checks passed.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
