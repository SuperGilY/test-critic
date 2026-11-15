# Critic baseline: 11 known defects in test plan v6

Written 2026-11-03. Found by hand after reading the plan. Do not show this file to the critic during a run. The v6 plan itself is not in this repository.

1. T09 bundles two scenarios (refund refused, then cancel accepted). The writer's silent self-check said no test bundles.
2. T17 has Importance High but no pass/fail expected result ("write down what happened"). It is exploration, not a test.
3. T17 cites R20 and R21 for a test they do not support. R20 is about a refund that is pending when the dispute arrives. R21 is about bank debit, and the test uses a card.
4. T13 says "Can I run it now: Yes" but depends on A7, which is unverified. Same for tests using V4 and V5.
5. No test for R34 (key length 255 / 256), although it is easy to run.
6. No test for an invalid `reason` value (R6). Only the valid reason is tested.
7. R16 (fees not returned), R14 and R15 (balance) have no test. All three depend on NEEDS HOW items, and the plan does not say so next to the claim.
8. Claim IDs changed between runs (for example R18b meant the 30-day return in one version and the failed status in another). Comparing runs by claim ID is not safe.
9. T19 and T20 say "wait a few minutes". The spec only says "some time later". The number is invented.
10. No test for who is allowed to refund (permissions or restricted keys). The spec is silent, so the critic should raise it as a question.
11. Many tests use the same preparation (P1) with the same unverified part. One wrong detail blocks about 25 tests.

## Results

- Critic v3: 8 of 11 clear, #7 and #8 partial, #10 missed.
- Critic v4 (clean chat, edge-case list one by one): 9 of 11 clear, #7 and #8 partial, #10 found.
- #7 and #8 cannot be seen by a one-run critic.
