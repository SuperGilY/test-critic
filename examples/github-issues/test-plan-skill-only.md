27 tests, 17 rules in the spec.

## How to read this
- P = preparation, A = action, V = view. The letters in brackets point to the building blocks in the spec.
- Every test starts with P1b: a new branch named after the test (t01 for T01), made from main, with one file edited and committed. The test lines only give the branch name.
- N is the number of the open issue you create in P2. M is the number of a second open issue (P2b). Write the number down.
- Default branch: the main branch of the repository. Here it is main. The other branch is called other.
- Keyword: a word like Closes or Fixes written before an issue number. It links a pull request to an issue.
- Linked: the issue shows the pull request in its side panel, and the pull request lists the issue as "may close".
- Merge: put the branch of a pull request into the target branch.
- Triage permission: a permission level that lets a person manage issues without writing code.
- Reason for closing: the choice in the dropdown next to the Close issue button.
- Second account and second repository (P3) are not set up. Tests that need them say NEEDS HOW.

## Set - Linking a pull request

**T01 - A keyword in the description links the pull request**
Importance: Medium
Checks: A keyword in the pull request description links the pull request to the issue (R1).
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t01 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t01 → description: Closes #N → Create pull request. (A2)
2. Check the PR: Pull requests tab → the new PR. Look at: open, merged or closed, and issues listed as "may close". (V2)
3. Check the issue: Issues tab → #N. Look at: Open/Closed. (V1)
Expected: The pull request is open. Issue N is listed as "may close". ASSUMPTION: Issue N is still open, because it closes only after the merge.

**T02 - Link a pull request to an issue by hand**
Importance: Low
Checks: A pull request can be linked to an issue by hand (R1).
Done via: A website (clicks).
Can I run it now: No - the spec has no way to link by hand.
Before you start: New branch t02 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t02 → description: Linked by hand → Create pull request. (A2)
2. Link the PR by hand: NEEDS HOW: link the pull request to issue N without a keyword.
3. Check the issue: Issues tab → #N. Look at: Open/Closed, linked pull request in the side panel. (V1)
Expected: ASSUMPTION: The pull request shows in the side panel of issue N. ASSUMPTION: Issue N is still open.

**T03 - A linked pull request can be seen on the issue**
Importance: Low
Checks: When a pull request is linked, others can see on the issue that someone is working on it (R14).
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t03 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t03 → description: Closes #N → Create pull request. (A2)
2. Check the issue: Issues tab → #N. Look at: linked pull request in the side panel. (V1)
3. Check the PR: Pull requests tab → the new PR. Look at: open, merged or closed. (V2)
Expected: The side panel of issue N shows the pull request. The pull request is open. ASSUMPTION: Looking at it with the same account is enough to stand in for a collaborator.

**T04 - A keyword is ignored when the pull request targets another branch**
Importance: High - an issue could be closed by mistake.
Checks: A keyword in a pull request into a branch other than the default branch does nothing and makes no link (R3, R4).
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t04 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR into other: Pull requests tab → New pull request → base: other, compare: t04 → description: Closes #N → Create pull request. (A3)
2. Check the PR: Pull requests tab → the new PR. Look at: issues listed as "may close". (V2)
3. Merge the PR: Pull requests tab → the PR → Merge pull request → Confirm merge. (A5)
4. Check the issue: Issues tab → #N. Look at: Open/Closed, linked pull request in the side panel. (V1)
Expected: The pull request does not list issue N as "may close". After the merge, issue N is still open. Issue N shows no linked pull request.

**T05 - A keyword in a comment instead of the description**
Importance: Low
Checks: Edge case, no rule in the spec. Q1.
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t05 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t05 → description: No keyword here → Create pull request. (A2)
2. Add a comment: Pull requests tab → the PR → comment box → type: Closes #N → Comment. (A9)
3. Check the PR: Pull requests tab → the PR. Look at: issues listed as "may close". (V2)
4. Check the issue: Issues tab → #N. Look at: Open/Closed, linked pull request in the side panel. (V1)
Expected: ASSUMPTION: The pull request does not list issue N as "may close". ASSUMPTION: Issue N shows no linked pull request and is open.

## Set - Writing the keyword

**T06 - A keyword followed by a colon**
Importance: Medium
Checks: A keyword followed by a colon still works (R5).
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t06 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t06 → description: Closes: #N → Create pull request. (A2)
2. Check the PR: Pull requests tab → the new PR. Look at: issues listed as "may close". (V2)
3. Merge the PR: Pull requests tab → the PR → Merge pull request → Confirm merge. (A5)
4. Check the issue: Issues tab → #N. Look at: Open/Closed. (V1)
Expected: Issue N is listed as "may close". After the merge, issue N is closed.

**T07 - A keyword in uppercase**
Importance: Medium
Checks: A keyword in uppercase still works (R5).
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t07 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t07 → description: CLOSES #N → Create pull request. (A2)
2. Check the PR: Pull requests tab → the new PR. Look at: issues listed as "may close". (V2)
3. Merge the PR: Pull requests tab → the PR → Merge pull request → Confirm merge. (A5)
4. Check the issue: Issues tab → #N. Look at: Open/Closed. (V1)
Expected: Issue N is listed as "may close". After the merge, issue N is closed.

**T08 - The short form for an issue in the same repository**
Importance: Medium
Checks: The form KEYWORD #ISSUE-NUMBER links an issue in the same repository (R6).
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t08 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t08 → description: Fixes #N → Create pull request. (A2)
2. Check the PR: Pull requests tab → the new PR. Look at: issues listed as "may close". (V2)
3. Merge the PR: Pull requests tab → the PR → Merge pull request → Confirm merge. (A5)
4. Check the issue: Issues tab → #N. Look at: Open/Closed. (V1)
Expected: Issue N is listed as "may close". After the merge, issue N is closed.

**T09 - The form for an issue in a different repository**
Importance: Medium
Checks: The form KEYWORD OWNER/REPOSITORY#ISSUE-NUMBER links an issue in another repository (R7).
Done via: A website (clicks).
Can I run it now: No - needs the second repository and second account (P3), which are not set up.
Before you start: New branch t09 (P1b). NEEDS HOW: second repository with an open issue, write down its number K (P3).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t09 → description: Closes OWNER/REPOSITORY#K, with the real owner, repository and number of the second repository → Create pull request. (A2)
2. Merge the PR: Pull requests tab → the PR → Merge pull request → Confirm merge. (A5)
3. Check the issue in the second repository: NEEDS HOW: open issue K in the second repository. Look at: Open/Closed. (V1)
Expected: ASSUMPTION: Issue K in the second repository is closed after the merge.

**T10 - Two issues, each with its own keyword**
Importance: Medium
Checks: To close several issues, each one gets its own keyword (R8).
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t10 (P1b). Open issues, write down N and M (P2, P2b).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t10 → description: Closes #N and Closes #M → Create pull request. (A2)
2. Merge the PR: Pull requests tab → the PR → Merge pull request → Confirm merge. (A5)
3. Check issue N: Issues tab → #N. Look at: Open/Closed. (V1)
4. Check issue M: Issues tab → #M. Look at: Open/Closed. (V1)
Expected: Issue N is closed. Issue M is closed.

**T11 - Two issues, one keyword only**
Importance: Low
Checks: Several issues after one keyword are not all closed, each needs its own keyword (R8).
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t11 (P1b). Open issues, write down N and M (P2, P2b).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t11 → description: Closes #N, #M → Create pull request. (A2)
2. Merge the PR: Pull requests tab → the PR → Merge pull request → Confirm merge. (A5)
3. Check issue N: Issues tab → #N. Look at: Open/Closed. (V1)
4. Check issue M: Issues tab → #M. Look at: Open/Closed. (V1)
Expected: Issue N is closed. ASSUMPTION: Issue M is still open.

**T12 - A word that is not a keyword**
Importance: Low
Checks: Edge case, no rule in the spec. Q5.
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t12 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t12 → description: Closing #N → Create pull request. (A2)
2. Check the PR: Pull requests tab → the new PR. Look at: issues listed as "may close". (V2)
3. Merge the PR: Pull requests tab → the PR → Merge pull request → Confirm merge. (A5)
4. Check the issue: Issues tab → #N. Look at: Open/Closed. (V1)
Expected: ASSUMPTION: The word is ignored. ASSUMPTION: Issue N is not listed as "may close" and is still open after the merge.

**T13 - A keyword for an issue number that does not exist**
Importance: Low
Checks: Edge case, no rule in the spec. Q4.
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t13 (P1b).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t13 → description: Closes #9999 → Create pull request. (A2)
2. Check the PR: Pull requests tab → the new PR. Look at: issues listed as "may close". (V2)
3. Merge the PR: Pull requests tab → the PR → Merge pull request → Confirm merge. (A5)
4. Check the PR again: Pull requests tab → the PR. Look at: open, merged or closed. (V2)
Expected: ASSUMPTION: The pull request can be created and merged. ASSUMPTION: No issue is listed as "may close" and no error stops the merge.

## Set - Closing by merge or commit

**T14 - Merging a linked pull request closes the issue**
Importance: Medium
Checks: Merging a linked pull request into the default branch closes the issue by itself (R2).
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t14 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t14 → description: Closes #N → Create pull request. (A2)
2. Check the PR: Pull requests tab → the new PR. Look at: issues listed as "may close". (V2)
3. Merge the PR: Pull requests tab → the PR → Merge pull request → Confirm merge. (A5)
4. Check the issue: Issues tab → #N. Look at: Open/Closed. (V1)
Expected: Issue N is open before the merge. Issue N is closed after the merge, with no other action.

**T15 - A keyword in a commit message closes the issue on merge**
Importance: Medium
Checks: A keyword in a commit message closes the issue when the commit is merged into the default branch (R9).
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t15 (P1b). Open issue, write down N (P2).
Steps:
1. Commit an edit: Code tab → branch t15 → open a file → edit → Commit changes → message: Fixes #N. (A7)
2. Open a PR: Pull requests tab → New pull request → base: main, compare: t15 → description: No keyword here → Create pull request. (A2)
3. Check the issue before the merge: Issues tab → #N. Look at: Open/Closed. (V1)
4. Merge the PR: Pull requests tab → the PR → Merge pull request → Confirm merge. (A5)
5. Check the issue after the merge: Issues tab → #N. Look at: Open/Closed. (V1)
Expected: Issue N is open before the merge. Issue N is closed after the merge.

**T16 - A keyword only in a commit message is not a linked pull request**
Importance: Low
Checks: A pull request that has the keyword only in a commit message is not shown as a linked pull request (R10).
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t16 (P1b). Open issue, write down N (P2).
Steps:
1. Commit an edit: Code tab → branch t16 → open a file → edit → Commit changes → message: Fixes #N. (A7)
2. Open a PR: Pull requests tab → New pull request → base: main, compare: t16 → description: No keyword here → Create pull request. (A2)
3. Check the PR: Pull requests tab → the new PR. Look at: issues listed as "may close". (V2)
4. Check the issue: Issues tab → #N. Look at: linked pull request in the side panel. (V1)
Expected: The pull request does not list issue N as "may close". ASSUMPTION: The side panel of issue N shows no linked pull request. The spec says this is not yet confirmed.

**T17 - A pull request closed without merging**
Importance: Medium
Checks: Edge case, no rule in the spec. Q3.
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t17 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t17 → description: Closes #N → Create pull request. (A2)
2. Close the PR: Pull requests tab → the PR → Close pull request. (A8)
3. Check the PR: Pull requests tab → Closed → the PR. Look at: open, merged or closed. (V2)
4. Check the issue: Issues tab → #N. Look at: Open/Closed. (V1)
Expected: The pull request is closed, not merged. ASSUMPTION: Issue N stays open.

**T18 - The issue is already closed when the pull request is merged**
Importance: Low
Checks: Edge case, no rule in the spec. Q2.
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t18 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t18 → description: Closes #N → Create pull request. (A2)
2. Close the issue: Issues tab → #N → Close issue. (A6)
3. Merge the PR: Pull requests tab → the PR → Merge pull request → Confirm merge. (A5)
4. Check the issue: Issues tab → #N. Look at: Open/Closed, the reason, linked pull request in the side panel. (V1)
5. Check the PR: Pull requests tab → the PR. Look at: open, merged or closed. (V2)
Expected: The pull request is merged. ASSUMPTION: Issue N stays closed and the merge shows no error.

**T19 - Two pull requests with the same keyword, the first is merged**
Importance: Low
Checks: Edge case, no rule in the spec. Q6.
Done via: A website (clicks).
Can I run it now: Yes
Before you start: Two new branches t19a and t19b (P1b, done twice). Open issue, write down N (P2).
Steps:
1. Open the first PR: Pull requests tab → New pull request → base: main, compare: t19a → description: Closes #N → Create pull request. (A2)
2. Open the second PR: Pull requests tab → New pull request → base: main, compare: t19b → description: Closes #N → Create pull request. (A2)
3. Merge the first PR: Pull requests tab → the first PR → Merge pull request → Confirm merge. (A5)
4. Check the second PR: Pull requests tab → the second PR. Look at: open, merged or closed, and issues listed as "may close". (V2)
5. Check the issue: Issues tab → #N. Look at: Open/Closed. (V1)
Expected: Issue N is closed. ASSUMPTION: The second pull request stays open. ASSUMPTION: It may or may not still list issue N, the spec does not say.

**T20 - A keyword that points to a comment in another pull request**
Importance: Low
Checks: A keyword that points to a pull request comment in another pull request links them, and merging the one with the keyword closes the other (R13).
Done via: A website (clicks).
Can I run it now: No - the spec does not say how to point a keyword at a comment.
Before you start: Two new branches t20a and t20b (P1b, done twice).
Steps:
1. Open the first PR: Pull requests tab → New pull request → base: main, compare: t20a → description: First pull request → Create pull request. (A2)
2. Add a comment: Pull requests tab → the first PR → comment box → type: A comment to point at → Comment. (A9)
3. Open the second PR: Pull requests tab → New pull request → base: main, compare: t20b → description: NEEDS HOW: a keyword that points to the comment in the first pull request → Create pull request. (A2)
4. Merge the second PR: Pull requests tab → the second PR → Merge pull request → Confirm merge. (A5)
5. Check the first PR: Pull requests tab → the first PR. Look at: open, merged or closed. (V2)
Expected: The first pull request is closed after the second one is merged.

## Set - Removing a link

**T21 - A keyword link cannot be unlinked by hand**
Importance: Low
Checks: Only a pull request linked by hand can be unlinked by hand (R11).
Done via: A website (clicks).
Can I run it now: No - the spec has no way to unlink by hand.
Before you start: New branch t21 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t21 → description: Closes #N → Create pull request. (A2)
2. Try to unlink by hand: NEEDS HOW: unlink issue N from the pull request without editing the description.
3. Check the PR: Pull requests tab → the PR. Look at: issues listed as "may close". (V2)
Expected: ASSUMPTION: There is no way to unlink by hand, or it does not work. Issue N is still listed as "may close".

**T22 - Deleting the keyword removes the link**
Importance: Medium
Checks: A keyword link is removed by editing the pull request description and deleting the keyword (R12).
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t22 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t22 → description: Closes #N → Create pull request. (A2)
2. Edit the description: Pull requests tab → the PR → three dots on the description → Edit → delete the text Closes #N → save. (A4)
3. Check the PR: Pull requests tab → the PR. Look at: issues listed as "may close". (V2)
4. Merge the PR: Pull requests tab → the PR → Merge pull request → Confirm merge. (A5)
5. Check the issue: Issues tab → #N. Look at: Open/Closed. (V1)
Expected: Issue N is no longer listed as "may close". ASSUMPTION: Issue N is still open after the merge.

**T23 - Deleting the keyword after the issue was closed by the merge**
Importance: Low
Checks: Edge case, no rule in the spec. Q8.
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t23 (P1b). Open issue, write down N (P2).
Steps:
1. Open a PR: Pull requests tab → New pull request → base: main, compare: t23 → description: Closes #N → Create pull request. (A2)
2. Merge the PR: Pull requests tab → the PR → Merge pull request → Confirm merge. (A5)
3. Check the issue: Issues tab → #N. Look at: Open/Closed. (V1)
4. Edit the description: Pull requests tab → Closed → the PR → three dots on the description → Edit → delete the text Closes #N → save. (A4)
5. Check the issue again: Issues tab → #N. Look at: Open/Closed. (V1)
Expected: Issue N is closed after the merge. ASSUMPTION: Issue N stays closed after the keyword is deleted.

## Set - Closing an issue by hand

**T24 - Close an issue you opened**
Importance: Low
Checks: Anyone can close an issue they opened (R15).
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t24 (P1b). Open issue, write down N (P2).
Steps:
1. Check the issue before: Issues tab → #N. Look at: Open/Closed. (V1)
2. Close the issue: Issues tab → #N → Close issue. (A6)
3. Check the issue after: Issues tab → Closed → #N. Look at: Open/Closed. (V1)
Expected: Issue N is open at first. Issue N is closed at the end.

**T25 - Close an issue opened by someone else, with triage permission**
Importance: Medium
Checks: On an organization repository, a person with triage permission or more can close issues opened by others (R16).
Done via: A website (clicks).
Can I run it now: No - needs an organization repository and a second account with triage permission (P3), not set up.
Before you start: New branch t25 (P1b). Open issue, write down N (P2).
Steps:
1. Sign in as the other person: NEEDS HOW: second account with triage permission on an organization repository.
2. Close the issue: Issues tab → #N → Close issue. (A6)
3. Check the issue: Issues tab → Closed → #N. Look at: Open/Closed. (V1)
Expected: Issue N is closed.

**T26 - A person without permission cannot close someone else's issue**
Importance: Medium
Checks: Edge case, no rule in the spec.
Done via: A website (clicks).
Can I run it now: No - needs a second account with limited permission (P3), not set up.
Before you start: New branch t26 (P1b). Open issue, write down N (P2).
Steps:
1. Sign in as the other person: NEEDS HOW: second account with no triage permission.
2. Try to close the issue: Issues tab → #N → look for Close issue. (A6)
3. Check the issue: Issues tab → #N. Look at: Open/Closed. (V1)
Expected: ASSUMPTION: The Close issue button is missing or fails. Issue N is still open.

**T27 - Choose a different reason when closing**
Importance: Low
Checks: The reason for closing an issue can be changed before closing (R17).
Done via: A website (clicks).
Can I run it now: Yes
Before you start: New branch t27 (P1b). Open issue, write down N (P2).
Steps:
1. Check the issue before: Issues tab → #N. Look at: Open/Closed. (V1)
2. Close with another reason: Issues tab → #N → dropdown next to Close issue → choose a reason other than the default → click the button. (A6)
3. Check the issue after: Issues tab → Closed → #N. Look at: Open/Closed, the reason. (V1)
Expected: Issue N is closed. ASSUMPTION: The reason shown is the one you chose, not the default. The spec does not list the reasons (Q9).

## Appendix

### Rules list
- R1. A pull request can be linked to an issue by hand or with a keyword in the description.
- R2. Merging a linked pull request into the default branch closes the issue by itself.
- R3. Keywords in the description work only when the pull request targets the default branch.
- R4. If the pull request targets another branch, keywords are ignored and no link is made.
- R5. Keywords can be followed by a colon and can be in uppercase.
- R6. For an issue in the same repository, the form is KEYWORD #ISSUE-NUMBER.
- R7. For an issue in another repository, the form is KEYWORD OWNER/REPOSITORY#ISSUE-NUMBER.
- R8. To close several issues, each issue needs its own keyword.
- R9. A keyword in a commit message closes the issue when the commit is merged into the default branch.
- R10. A pull request with the keyword only in a commit message is not shown as a linked pull request.
- R11. Only a pull request linked by hand can be unlinked by hand.
- R12. A keyword link is removed by editing the description and deleting the keyword.
- R13. A keyword pointing to a comment in another pull request links them, and merging the first closes the second.
- R14. When a pull request is linked, collaborators can see that someone is working on the issue.
- R15. Anyone can close an issue they opened.
- R16. On an organization repository, people with triage permission or more can close issues opened by others.
- R17. The reason for closing an issue can be changed before closing.

### NEEDS HOW list
- Link a pull request to an issue by hand (T02).
- Unlink a pull request from an issue by hand (T21).
- Second repository with an open issue (T09).
- Second account with triage permission on an organization repository (T25).
- Second account with no triage permission (T26).
- Write a keyword that points to a comment in another pull request (T20).
- Whether the side panel shows linked pull requests for keywords in commit messages (T16).
