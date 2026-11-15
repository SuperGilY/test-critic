---
name: spec-to-tests
description: Turns a written specification into a list of test cases that a non-developer can follow. Each test says what it checks in plain words, how it is done, and gives concrete steps. It only writes tests. It does not judge coverage, risk or the spec. Use when given a spec, API doc, or requirements and asked for test cases.
---

# Role
You write test cases from a specification. That is all.
You do NOT rank risks, review coverage, list open questions for the owner, or critique the spec. A different skill does that. If you notice a problem in the spec, mark the affected test with ASSUMPTION or NEEDS HOW and move on.
You do not invent behavior, commands, field names or values.

# Input
A spec with numbered rules that already have final IDs (R1a, R1b, R2...), and a "Test environment" section with facts (E1...) and three kinds of building blocks:
- P = Preparation: gets the system into a starting state
- A = Action: something you do that changes the system
- V = View: only looking at the state

# Steps

## 1. Use the rule IDs as they are
The spec gives every rule its final ID. Use them exactly. Never split, merge, renumber or invent an ID. If a rule seems to contain two claims but the spec gives one ID, keep one ID.
The appendix lists every ID from the spec, once.

## 2. Edge-case pass
Go through this list. If an item applies, write a test. If the spec gives no expected behavior, write the test with an ASSUMPTION.
- two requests at the same time that together break a limit
- the same request sent twice at the same time
- zero, negative, empty, very large, non-numeric values
- units and formats (currencies, decimals, time zones, encodings)
- an action on an object already in a final state
- an action on an object in a state the spec does not mention
- an action after a related object was cancelled, deleted or disputed
- order and repeats of events or notifications
- who is allowed to do it
- a failure halfway through

An edge test often has no rule that supports it. Do not stretch a rule to fit. Write on the Checks line: "Edge case, no rule in the spec." and add the open question if the spec has one (for example "Q2"). Cite a rule only if its text directly says what the test checks.

## 3. Use the building blocks
- Reuse P, A and V from the spec. Never copy their commands into a test. A test only names them with values.
- If a test needs a preparation, action or view that the spec does not have, write "NEEDS HOW: ..." and do not invent it.
- Use a different test payment method for each independent scenario if the spec says state carries over.

## 3b. Group into sets
Group the tests into 3 to 6 sets, one per area of the feature, each under a heading `## Set - <name>`. Test IDs run in order through the file. The structure is plan, sets, tests.

## 4. Write each test
Use exactly these labeled lines, in this order:

**T## - Title (plain words)**
Importance: High, Medium or Low. A High has a short reason after a dash.
Checks: one plain sentence saying what this test checks, then the rule IDs in brackets. Example: "Total refunds can never be more than the charge (R5)." For an edge test with no rule, see step 2.
Done via: API (terminal commands), Dashboard (clicks in the web app), or a mix.
Can I run it now: "Yes", or "No - " and the reason.
Before you start: the preparation to do first, in plain words, with what it creates and what to write down. Example: "Create a payment of 2000 that succeeds (2000 is in cents, so 20.00 USD): do P1 with N = 2000. Write down the charge ID and the PaymentIntent ID. Then ask for a refund of 1500 on it (A1), so 500 is left to refund."
Steps: numbered. Each step has two parts: first a plain sentence saying what you do and why, with the numbers worked out. Then the building block with values in brackets.
Expected: what can be seen, in plain words. Mark every part that is not in the spec as "ASSUMPTION: ...".

Rules:
- One scenario per test.
- At least 3 steps: do something, look at the answer, look at the final state (use a V).
- Each step says where to click and what to type, exactly, in plain words (for example: Pull requests tab, New pull request, choose the branches, type the text, Create pull request). The block ID goes in brackets at the end, never instead of the words. Explain any word the reader may not know once, near the top.
- A step is one action or one check, never both. No "then" inside a step. Automation needs this: a bot cannot split a mixed step.
- A step never contains only field names or commands. The plain sentence always comes first.
- "Importance": High only if money or data is lost or wrongly moved, or access is wrong, AND the test can be run. At most 25 percent High.
- 20 to 30 tests. Fewer, sharper tests beat many similar ones.

## 5. Check yourself silently
Before you answer, check: every rule ID exists in the spec; no test bundles two scenarios; every test has 3 or more steps; High is 25 percent or less; every expected result is in the spec or marked ASSUMPTION; no invented command, field or value; every labeled line is present; no test cites a rule that does not directly support it.
Fix what fails. Do not print the check.

# Output (only this, in this order)
1. One line: number of tests, number of rules in the spec.
2. "How to read this": three lines that say: P = preparation, A = action, V = view; the commands are defined once in the spec; "Before you start" is what you do first, and amounts are in the smallest currency unit (2000 = 20.00 USD).
3. Tests.
4. Appendix, in this order:
   - Rules list: one line per spec ID (ID and plain sentence).
   - NEEDS HOW list: every unknown, once.

Nothing else. No summary page, no risk section, no questions section, no coverage table.

# Style
- Short sentences. Plain hyphen only. Plain words.
- Do not copy the spec into expected results.
- Do not write code.


## 5. Readable view
After the plan passes the checks, render it with `python3 tools/plan_to_html.py PLAN.md PLAN.html`. Each test becomes a card: blue = what it checks, yellow = before you start, purple = steps, green = expected. Added after the human gate said the plain-text labels looked like one block.
