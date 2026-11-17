# Test Critic

Two Claude skills that turn a written spec into a test plan, then review that plan with a separate pass that did not write it. The review ends in a one-page report a manager can read in 30 seconds.

Built by Gil Yagen, QA Engineering Lead.

## The question it answers

A manager asks: "How well is this feature covered?" The answer should take one second and have no fluff. For the example feature, the answer is:

> Refunds: 19 of 51 rules clearly covered, 8 partly, 24 not. No tests run yet. Biggest gap: balance and fees have no test at all.

Open [`dashboard/index.html`](dashboard/index.html) in a browser to see that answer per area of the feature.

## How it works

1. **Spec in.** Every rule in the spec has a fixed ID (R1a, R5, R38b). The spec also defines the setup steps once (P), the actions (A) and the views (V).
2. **Skill 1, `spec-to-tests`, writes the plan.** Plain-language tests a non-developer can follow. It marks every guess as ASSUMPTION and every unknown as NEEDS HOW. It does not judge its own work.
3. **Human gate.** A person reads a few tests and writes two lines before the review starts.
4. **Skill 2, `test-plan-critic`, reviews.** It reads the spec first, writes its own must-test list, and only then reads the plan. It fills a fixed HTML template, so every report looks the same.

Why two skills: a writer that checks its own work misses its own mistakes.

## What is here

| Path | What |
|---|---|
| `skills/spec-to-tests/` | Skill 1, the writer |
| `skills/spec-prep/` | Skill 0, turns messy requirements into a numbered spec where every rule quotes its source |
| `skills/test-plan-critic/` | Skill 2, the critic, with the report template |
| `examples/forgot-password/` | A second domain: the OWASP forgot-password guidance turned into 30 rules by `spec-prep` |
| `examples/github-issues/` | A third domain: GitHub Docs on linking and closing issues. 17 rules, 19 tests, critic report, and a colour HTML view of the plan |
| `examples/refunds/` | The spec (Stripe refunds, public docs), the 29-test plan, the critic's report |
| `dashboard/index.html` | The coverage answer board, one self-contained file |
| `tools/validate_spec.py` | Checks that every rule's quote appears word for word in the source |
| `tools/validate_plan.py` | Mechanical checks, no model: rule IDs exist, counts add up, High share, required lines |
| `tools/plan_to_html.py` | Turns a plan into colour cards, one per test, grouped by set |
| `tools/plan_to_automation.py` | Turns a plan into an automation view: one row per step, action or check, as JSON and a table |
| `evaluation/` | The 11 known defects used to check the critic |

## Results so far

- The critic was checked against 11 defects found by hand in an earlier plan. Critic v3 found 8 clearly. Critic v4 found 9 clearly and 2 partly.
- Stable rule IDs fixed a real problem: the earlier plan counted 51 claims against 38 rules in the spec. Now the plan and the spec agree on 51.
- First real run (2026-11-15): one test from the GitHub issues plan (merge closes the linked issue) was run by hand by a tester who does not know GitHub. It passed. It exposed a gap: the steps did not explain what a pull request is or how to make the branch. Both were added to the plan. One test passed once; it does not prove the rest.
- Clean-context check (2026-11-15): a fresh agent given only the writer skill and the GitHub spec wrote a plan that passed the mechanical checks. Run 1 exposed refund-specific wording and conflicting format rules in the skill. After fixing them, run 2 followed the format, wrote 27 tests, and covered one rule (link by hand) that the hand-edited plan had missed. See `examples/github-issues/test-plan-skill-only.md`. `test-plan-v6.md` in the same folder is the version shaped by a human gate.
- On the current plan, the critic's top finding is that 27 of 29 tests depend on one setup step nobody has run.

## Limits

- Only one test has been run so far (see Results). "Covered" means the plan has a test for the rule, not that the test passed.
- Two example features. The second (forgot password) has a spec but no test plan or review yet. It comes from a condensed copy of the source, and its test environment is "not provided".
- The review of plan v8 was done in the same session that wrote the plan, so it is not an independent check.
- The 11 known defects were found by the author, on one plan.
- Parts of the spec come from public docs, and some setup steps are marked unverified.

## Check a plan without a model

```
python3 tools/validate_plan.py examples/refunds/refunds-spec.md examples/refunds/test-plan-v8.md
```

A model checking its own work missed a bundled test in an earlier run. These checks are plain code, so they do not tire or agree with the writer.

The same idea checks the spec: `python3 tools/validate_spec.py examples/forgot-password/forgot-password-spec.md examples/forgot-password/source-owasp-forgot-password.txt`. On its first run it caught a misquoted rule and a wrong rule count in the spec written by the skill.

## Use it

Add the two `SKILL.md` files as skills in Claude. Send the spec to the critic first, then the plan. Keep the spec in the same ID format as `examples/refunds/refunds-spec.md`.
