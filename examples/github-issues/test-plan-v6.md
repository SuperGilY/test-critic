19 tests, 17 rules in the spec.

## How to read this
- **Keyword** = a word GitHub reads as "close this issue on merge": Closes, Fixes. Write it like this: Closes #7
- **N** = the number of your issue (shown next to its title, e.g. #7)
- **PR** (pull request) = a request to bring the changes of one branch into another, here into main. It is what GitHub reads to link and close issues
- **Branch** = a separate copy of the files where you can change things without touching main
- **Merge** = bring the branch changes into main
- **Set** = a group of tests for one area
- **P1** = once: new test repo with branches main and other
- **P1b** = before every test: Code tab → branch menu (says main) → type the name, e.g. t07 → Create branch → open README.md → pencil icon → add a word → Commit changes → Commit changes. Without this edit GitHub will not let you open a PR
- **P2** = new issue: Issues tab → New issue → any title → Submit new issue
- Letters in brackets at the end of a step (A5, V1) = building block in the spec. Ignore them.

---

## Set - Keywords and linking

---

**T01 - A keyword in the description links the pull request to the issue**
Importance: Medium
Checks: A keyword in the description links the pull request to the issue, and others can see that work is in progress (R1, R6, R14).
Done via: Website (clicks in GitHub)
Can I run it now: Yes
Before you start: New branch t01 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t01 → Create pull request → description: Closes #N (real number) → Create pull request. (A2)
2. Check the PR: Pull requests tab → open it. Look at: Open/Merged/Closed, issue it will close. (V2)
3. Check the issue: Issues tab → #N. Look at: Open/Closed, side panel (linked PR). (V1)
Expected: The pull request page lists issue N as one it may close. The issue's side panel shows the pull request. ASSUMPTION: the exact wording on the screen is not in the spec.

---

**T02 - Uppercase keyword with a colon works**
Importance: Low
Checks: Keywords can be followed by a colon and written in uppercase (R5).
Done via: Website (clicks in GitHub)
Can I run it now: Yes
Before you start: New branch t04 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t04 → Create pull request → description: CLOSES: #N (capital letters, a colon, the real number instead of N) → Create pull request. (A2)
2. Merge it: open the PR → Merge pull request → Confirm merge. (A5)
3. Check the issue: Issues tab → #N. Look at: Open/Closed, side panel (linked PR). (V1)
Expected: The issue is Closed.

---

**T03 - A word that is not on the keyword list**
Importance: Low
Checks: Edge case. The spec lists the keywords but does not say what happens with other words (Q5).
Done via: Website (clicks in GitHub)
Can I run it now: Yes
Before you start: New branch t15 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t15 → Create pull request → description: Closing #N (real number) → Create pull request. (A2)
2. Merge it: open the PR → Merge pull request → Confirm merge. (A5)
3. Check the issue: Issues tab → #N. Look at: Open/Closed, side panel (linked PR). (V1)
Expected: The issue is still Open. ASSUMPTION: the word Closing is not a keyword.

---

**T04 - A keyword written in a comment, not in the description**
Importance: Medium
Checks: Edge case. The spec says the keyword goes in the pull request description and does not mention comments (Q1).
Done via: Website (clicks in GitHub)
Can I run it now: Yes
Before you start: New branch t16 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t16 → Create pull request → description: plain text (no keyword) → Create pull request. (A2)
2. Add a comment: open the PR → comment box at the bottom → type: Closes #N (real number) → Comment. (A9)
3. Merge it: open the PR → Merge pull request → Confirm merge. (A5)
4. Check the issue: Issues tab → #N. Look at: Open/Closed, side panel (linked PR). (V1)
Expected: ASSUMPTION: the issue is still Open.

---

**T05 - A keyword on a pull request into another branch does nothing**
Importance: Medium
Checks: If the pull request does not go into the main branch, keywords are ignored and no link is made (R3, R4).
Done via: Website (clicks in GitHub)
Can I run it now: Yes
Before you start: New branch t03 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: other, compare: t03 → Create pull request → description: Closes #N (real number) → Create pull request. (A3)
2. Check the issue: Issues tab → #N. Look at: Open/Closed, side panel (linked PR). (V1)
3. Merge it: open the PR → Merge pull request → Confirm merge. (A5)
4. Check the issue: Issues tab → #N. Look at: Open/Closed, side panel (linked PR). (V1)
Expected: The issue shows no linked pull request, and after the merge it is still Open.

---

**T06 - Removing the keyword unlinks the issue**
Importance: Medium
Checks: A keyword link is removed by editing the description and deleting the keyword (R12).
Done via: Website (clicks in GitHub)
Can I run it now: Yes
Before you start: New branch t07 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t07 → Create pull request → description: Closes #N (real number) → Create pull request. (A2)
2. Check the issue: Issues tab → #N. Look at: Open/Closed, side panel (linked PR). (V1)
3. Edit the description: open the PR → three dots on the description → Edit → delete the text, type "no keyword" → Update comment. (A4)
4. Check the issue: Issues tab → #N. Look at: Open/Closed, side panel (linked PR). (V1)
5. Merge it: open the PR → Merge pull request → Confirm merge. (A5)
6. Check the issue: Issues tab → #N. Look at: Open/Closed, side panel (linked PR). (V1)
Expected: After the edit the issue shows no linked pull request. After the merge the issue is still Open.

---

## Set - Closing by merge

---

**T07 - Merging the linked pull request closes the issue**
Importance: High - an issue closes without anyone closing it, so work can be marked done by mistake.
Checks: Merging a linked pull request into the main branch closes the issue by itself (R2).
Done via: Website (clicks in GitHub)
Can I run it now: Yes
Before you start: New branch t02 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t02 → Create pull request → description: Closes #N (real number) → Create pull request. (A2)
2. Merge it: open the PR → Merge pull request → Confirm merge. (A5)
3. Check the issue: Issues tab → #N. Look at: Open/Closed, side panel (linked PR). (V1)
Expected: The issue is Closed.

---

**T08 - Two issues, each with its own keyword, both close**
Importance: Medium
Checks: To close two issues, each one needs its own keyword (R8).
Done via: Website (clicks in GitHub)
Can I run it now: Yes
Before you start: New branch t05 (P1b). Create two open issues: do P2 twice. Write down both numbers (N and M).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t05 → Create pull request → description: Closes #N, closes #M (the real numbers) → Create pull request. (A2)
2. Merge it: open the PR → Merge pull request → Confirm merge. (A5)
3. Check issue N: Issues tab → #N. Look at: Open/Closed. (V1)
4. Check issue M: Issues tab → #M. Look at: Open/Closed. (V1)
Expected: Both issues are Closed.

---

**T09 - One keyword for two issues closes only the first**
Importance: Medium
Checks: Each issue needs its own keyword, so a second number with no keyword should not close it (R8). The spec does not say what happens to the bare second number.
Done via: Website (clicks in GitHub)
Can I run it now: Yes
Before you start: New branch t06 (P1b). Create two open issues: do P2 twice. Write down both numbers (N and M).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t06 → Create pull request → description: Closes #N, #M (one keyword, two real numbers) → Create pull request. (A2)
2. Merge it: open the PR → Merge pull request → Confirm merge. (A5)
3. Check issue N: Issues tab → #N. Look at: Open/Closed. (V1)
4. Check issue M: Issues tab → #M. Look at: Open/Closed. (V1)
Expected: Issue N is Closed. ASSUMPTION: issue M stays Open.

---

**T10 - A merge that mentions an issue that is already closed**
Importance: Medium
Checks: Edge case, no rule in the spec. Open question Q2.
Done via: Website (clicks in GitHub)
Can I run it now: Yes
Before you start: New branch t12 (P1b). Open issue, write down N (P2). Close it: open the issue → Close issue. (A6)
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t12 → Create pull request → description: Closes #N (the real number of the closed issue) → Create pull request. (A2)
2. Merge it: open the PR → Merge pull request → Confirm merge. (A5)
3. Check the issue: Issues tab → #N. Look at: Open/Closed, side panel (linked PR). (V1)
Expected: ASSUMPTION: the merge works, the issue stays Closed and no error is shown. The test fails if the merge fails or the issue opens again.

---

**T11 - Closing the pull request without merging leaves the issue open**
Importance: Medium
Checks: Edge case, no rule in the spec. Open question Q3. R2 says the issue closes on merge.
Done via: Website (clicks in GitHub)
Can I run it now: Yes
Before you start: New branch t13 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t13 → Create pull request → description: Closes #N (real number) → Create pull request. (A2)
2. Close the PR without merging: open it → Close pull request (bottom of the page). (A8)
3. Check the issue: Issues tab → #N. Look at: Open/Closed, side panel (linked PR). (V1)
Expected: The issue is still Open. ASSUMPTION: not stated in the spec.

---

**T12 - A keyword for an issue number that does not exist**
Importance: Low
Checks: Edge case, no rule in the spec. Open question Q4.
Done via: Website (clicks in GitHub)
Can I run it now: Yes
Before you start: New branch t14 (P1b). You do not need an issue. Pick a number much higher than the number of issues you have, for example 9999.
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t14 → Create pull request → description: Closes #9999 → Create pull request. (A2)
2. Merge it: open the PR → Merge pull request → Confirm merge. (A5)
3. Check the PR: Pull requests tab → open it. Look at: Open/Merged/Closed, issue it will close. (V2)
Expected: ASSUMPTION: the pull request is created and merged, and no issue is changed. The test fails if creating or merging gives an error.

---

## Set - Keyword in a commit message

---

**T13 - A keyword in a commit message closes the issue on merge**
Importance: Medium
Checks: A keyword in a commit message closes the issue when that commit is merged into the main branch (R9).
Done via: Website (clicks in GitHub)
Can I run it now: Yes
Before you start: New branch t08 (P1b). Open issue, write down N (P2).
Steps:
1. Commit with a keyword: Code tab → branch t08 → open a file → pencil icon → change one word → Commit changes → message: Fixes #N (real number) → Commit changes. (A7)
2. Open a PR: Pull requests tab → New pull request → base: main, compare: t08 → Create pull request → description: plain text (no keyword) → Create pull request. (A2)
3. Merge it: open the PR → Merge pull request → Confirm merge. (A5)
4. Check the issue: Issues tab → #N. Look at: Open/Closed, side panel (linked PR). (V1)
Expected: The issue is Closed. ASSUMPTION: GitHub reads the keyword from the commit message when the pull request is merged.

---

**T14 - A commit-message keyword does not show the pull request as linked**
Importance: Low
Checks: A pull request that has the keyword only in a commit message is not shown as a linked pull request (R10).
Done via: Website (clicks in GitHub)
Can I run it now: Yes
Before you start: New branch t09 (P1b). Open issue, write down N (P2).
Steps:
1. Commit with a keyword: Code tab → branch t09 → open a file → pencil icon → change one word → Commit changes → message: Fixes #N (real number) → Commit changes. (A7)
2. Open a PR: Pull requests tab → New pull request → base: main, compare: t09 → Create pull request → description: plain text (no keyword) → Create pull request. (A2)
3. Check the issue: Issues tab → #N. Look at: Open/Closed, side panel (linked PR). (V1)
4. Check the PR: Pull requests tab → open it. Look at: Open/Merged/Closed, issue it will close. (V2)
Expected: The issue does not list the pull request as linked. The pull request page lists no issue it may close. ASSUMPTION: the second part is not stated in the spec.

---

## Set - Other repositories and pull requests

---

**T15 - Closing an issue in another repository**
Importance: Medium
Checks: For an issue in a different repository the syntax is KEYWORD OWNER/REPOSITORY#NUMBER (R7).
Done via: Website (clicks in GitHub)
Can I run it now: No - needs a second test repository (P3, NEEDS HOW).
Before you start: New branch t17 (P1b). Create an open issue in the second repository and write down its number. NEEDS HOW: the second repository.
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t17 → Create pull request → description: Fixes OWNER/REPOSITORY#NUMBER (the real owner name, repository name and number of the issue in the second repository) → Create pull request. (A2)
2. Merge it: open the PR → Merge pull request → Confirm merge. (A5)
3. Check the issue in the second repository: Issues tab → its number. (V1)
Expected: The issue in the second repository is Closed.

---

**T16 - A keyword that points to a pull request comment**
Importance: Low
Checks: A keyword that points to a comment in another pull request links them, and merging the first closes the second (R13).
Done via: Website (clicks in GitHub)
Can I run it now: No - NEEDS HOW: how to copy the link of a comment, and a second pull request on its own branch.
Before you start: New branch t19 (P1b). Open a second pull request on its own branch. NEEDS HOW.
Steps:
1. In the second pull request, copy the link of one comment. NEEDS HOW.
2. Open a PR: Pull requests tab → New pull request → base: main, compare: t19 → Create pull request → description: Fixes (the link of the comment) → Create pull request. (A2)
3. Merge it: open the PR → Merge pull request → Confirm merge. (A5)
4. Check the second PR: Pull requests tab → open it. (V2)
Expected: The second pull request is Closed.

---

## Set - Who can close an issue, and why

---

**T17 - The person who opened an issue can close it**
Importance: Low
Checks: Anyone can close an issue they opened (R15).
Done via: Website (clicks in GitHub)
Can I run it now: No - needs a second GitHub account, so that the closer is not the repository owner (P3, NEEDS HOW).
Before you start: New branch t10 (P1b). Log in with the second account and create an open issue in the test repository. Write down its number (N).
Steps:
1. Check the issue as the second account: log in → Issues tab → #N. (V1)
2. Close the issue: open it → Close issue (bottom of the page). (A6)
3. Check the issue: Issues tab → #N. Look at: Open/Closed, side panel (linked PR). (V1)
Expected: The issue is Closed.

---

**T18 - Who can close an issue opened by someone else**
Importance: Medium
Checks: People with triage permission or more can close issues opened by others (R16). The spec does not say what happens for people with less access.
Done via: Website (clicks in GitHub)
Can I run it now: No - needs a second account (P3, NEEDS HOW).
Before you start: New branch t18 (P1b). Log in with the second account and create an open issue in the test repository. Write down its number (N). Your own account owns the repository, so it has triage permission or more.
Steps:
1. Check the issue the second account created: Issues tab → #N. (V1)
2. Close the issue: open it → Close issue (bottom of the page). (A6)
3. Check the issue: Issues tab → #N. Look at: Open/Closed, side panel (linked PR). (V1)
Expected: The issue is Closed.

---

**T19 - The reason for closing is saved**
Importance: Low
Checks: The reason chosen when closing an issue is saved (R17). The spec does not list the reasons (Q9).
Done via: Website (clicks in GitHub)
Can I run it now: No - the list of reasons is not in the spec (Q9). Look at the dropdown first and write the list down.
Before you start: New branch t11 (P1b). Open issue, write down N (P2).
Steps:
1. Read the closing reasons: open the issue → small arrow next to Close issue → write down the list. (A6)
2. Close with another reason: arrow next to Close issue → pick a reason that is not the first → Close issue. NEEDS HOW: which reason. (A6)
3. Check the issue: Issues tab → #N. Look at: Open/Closed, side panel (linked PR). (V1)
Expected: The issue is Closed and shows the reason you chose. ASSUMPTION: the reason is shown on the issue.

---

## Appendix

### Rules list
R1 link by hand or with a keyword. R2 merge into main closes the issue. R3 keywords work only on the main branch. R4 other branches ignore keywords. R5 colon and uppercase allowed. R6 same-repository syntax. R7 other-repository syntax. R8 one keyword per issue. R9 keyword in commit message closes on merge. R10 commit-message-only pull request not shown as linked. R11 only manual links can be unlinked by hand. R12 keyword link removed by editing the description. R13 pull request comment reference links and closes. R14 collaborators see linked pull request. R15 anyone can close own issue. R16 triage permission can close others' issues. R17 reason for closing can be chosen.

### NEEDS HOW list
- A second test repository (T15).
- A second GitHub account (T17, T18).
- The list of closing reasons (T19).
- Copying the link of a pull request comment, and a second pull request on its own branch (T16).
