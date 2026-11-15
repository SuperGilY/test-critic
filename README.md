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
| `skills/test-plan-critic/` | Skill 2, the critic, with the report template |
| `examples/refunds/` | The spec (Stripe refunds, public docs), the 29-test plan, the critic's report |
| `dashboard/index.html` | The coverage answer board, one self-contained file |
| `tools/validate_plan.py` | Mechanical checks, no model: rule IDs exist, counts add up, High share, required lines |
| `evaluation/` | The 11 known defects used to check the critic |

## Results so far

- The critic was checked against 11 defects found by hand in an earlier plan. Critic v3 found 8 clearly. Critic v4 found 9 clearly and 2 partly.
- Stable rule IDs fixed a real problem: the earlier plan counted 51 claims against 38 rules in the spec. Now the plan and the spec agree on 51.
- On the current plan, the critic's top finding is that 27 of 29 tests depend on one setup step nobody has run.

## Limits

- No test has been run. "Covered" means the plan has a test for the rule, not that the test passed.
- One example feature. A second spec has not been tried yet.
- The review of plan v8 was done in the same session that wrote the plan, so it is not an independent check.
- The 11 known defects were found by the author, on one plan.
- Parts of the spec come from public docs, and some setup steps are marked unverified.

## Check a plan without a model

```
python3 tools/validate_plan.py examples/refunds/refunds-spec.md examples/refunds/test-plan-v8.md
```

A model checking its own work missed a bundled test in an earlier run. These checks are plain code, so they do not tire or agree with the writer.

## Use it

Add the two `SKILL.md` files as skills in Claude. Send the spec to the critic first, then the plan. Keep the spec in the same ID format as `examples/refunds/refunds-spec.md`.
