#!/usr/bin/env python3
"""Mechanical checks for a test plan against its spec. No model, no judgment.

Usage: python3 validate_plan.py SPEC.md PLAN.md

Checks:
  1. Every rule ID a test cites exists in the spec.
  2. The "N tests, M rules" line at the top matches the real counts.
  3. A step is one action or one check (at most one block tag, no 'then').
  3b. Every test has all labeled lines and at least 3 numbered steps.
  4. At most 25 percent of tests are High, and every High can run now.
  5. Tests marked "Can I run it now: Yes" do not mention NEEDS HOW.
  6. Test IDs are unique and in order.
Exit code 0 when all pass, 1 otherwise.
"""
import re
import sys

LABELS = ["Importance:", "Checks:", "Done via:", "Can I run it now:",
          "Before you start:", "Steps:", "Expected:"]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def spec_ids(text):
    rules = set(re.findall(r"^- (R\d+[a-z]?)\.", text, flags=re.M))
    questions = set(re.findall(r"^- (Q\d+)\.", text, flags=re.M))
    return rules, questions


def split_tests(text):
    body = text.split("## Appendix")[0]
    parts = re.split(r"^\*\*(T\d+) - ", body, flags=re.M)
    tests = []
    for i in range(1, len(parts), 2):
        tests.append((parts[i], parts[i + 1]))
    return body, tests


def main(spec_path, plan_path):
    spec = read(spec_path)
    plan = read(plan_path)
    rules, questions = spec_ids(spec)
    body, tests = split_tests(plan)
    problems = []

    first = plan.strip().splitlines()[0]
    m = re.match(r"(\d+) tests?, (\d+) rules", first)
    if not m:
        problems.append("Top line is not in the form 'N tests, M rules'.")
    else:
        if int(m.group(1)) != len(tests):
            problems.append(f"Top line says {m.group(1)} tests, found {len(tests)}.")
        if int(m.group(2)) != len(rules):
            problems.append(f"Top line says {m.group(2)} rules, spec has {len(rules)}.")

    ids = [t[0] for t in tests]
    expected = [f"T{n:02d}" for n in range(1, len(tests) + 1)]
    if ids != expected:
        problems.append("Test IDs are not unique and in order.")

    high = 0
    for tid, block in tests:
        for label in LABELS:
            if label not in block:
                problems.append(f"{tid}: missing line '{label}'")
        steps = block.split("Steps:")[-1].split("Expected:")[0] if "Steps:" in block else ""
        n_steps = len(re.findall(r"^\d+\.", steps, flags=re.M))
        for line in re.findall(r"^\d+\..*$", steps, flags=re.M):
            tags = re.findall(r"\((?:A|V|P)\d+[a-z]?\)", line)
            if len(tags) > 1 or re.search(r"\bthen\b", line, flags=re.I):
                problems.append(f"{tid}: a step does more than one thing: '{line[:50]}'")
        if n_steps < 3:
            problems.append(f"{tid}: {n_steps} numbered steps, needs 3 or more.")
        checks = re.search(r"^Checks:(.*)$", block, flags=re.M)
        if checks:
            cited_r = re.findall(r"\bR\d+[a-z]?\b", checks.group(1))
            cited_q = re.findall(r"\bQ\d+\b", checks.group(1))
            for r in cited_r:
                if r not in rules:
                    problems.append(f"{tid}: cites {r}, which is not in the spec.")
            for q in cited_q:
                if q not in questions:
                    problems.append(f"{tid}: cites {q}, which is not in the spec.")
        imp = re.search(r"^Importance:\s*(\w+)", block, flags=re.M)
        run = re.search(r"^Can I run it now:\s*(\w+)", block, flags=re.M)
        if imp and imp.group(1) == "High":
            high += 1
            if run and run.group(1) != "Yes":
                problems.append(f"{tid}: High importance but cannot run now.")
        if run and run.group(1) == "Yes" and "NEEDS HOW" in block:
            problems.append(f"{tid}: marked 'Yes' but mentions NEEDS HOW.")

    if tests and high / len(tests) > 0.25:
        problems.append(f"{high} of {len(tests)} tests are High, limit is 25 percent.")

    print(f"Spec rules: {len(rules)}   Tests: {len(tests)}   High: {high}")
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
