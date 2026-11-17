# Spec: GitHub issues, linking and closing (input for the test-writer skill) - v1

Source: GitHub Docs, see source-github-docs.txt. Licence: CC BY 4.0. Date read: 2026-11-15.
The source text is an excerpt returned by a search tool. It is not the full pages.
There are 17 rules. The IDs are final.

## Rules
- R1. A pull request can be linked to an issue by hand, or with a keyword in the pull request description. | Source: "manually or using a supported keyword in the pull request description"
- R2. Merging a linked pull request into the default branch closes the linked issue by itself. | Source: "its linked issue is automatically closed"
- R3. Keywords in the description work only when the pull request targets the default branch. | Source: "interpreted only when the pull request targets the repository's default branch"
- R4. If the pull request targets another branch, keywords are ignored and no link is made. | Source: "then these keywords are ignored, no links are created"
- R5. Keywords can be followed by a colon, and can be in uppercase. | Source: "The keywords can be followed by colons or in uppercase."
- R6. For an issue in the same repository, the syntax is KEYWORD #ISSUE-NUMBER. | Source: "KEYWORD #ISSUE-NUMBER"
- R7. For an issue in a different repository, the syntax is KEYWORD OWNER/REPOSITORY#ISSUE-NUMBER. | Source: "KEYWORD OWNER/REPOSITORY#ISSUE-NUMBER"
- R8. To close several issues, each issue needs its own keyword. | Source: "Use full syntax for each issue"
- R9. A keyword in a commit message closes the issue when the commit is merged into the default branch. | Source: "The issue will be closed when you merge the commit into the default branch"
- R10. A pull request that only has the keyword in a commit message is not shown as a linked pull request. | Source: "will not be listed as a linked pull request"
- R11. Only a pull request linked by hand can be unlinked by hand. | Source: "Only manually linked pull requests can be manually unlinked."
- R12. A keyword link is removed by editing the pull request description and deleting the keyword. | Source: "you must edit the pull request description to remove the keyword"
- R13. A keyword that points to a pull request comment in another pull request links them, and merging the first one closes the second. | Source: "Merging the referencing pull request also closes the referenced pull request."
- R14. When a pull request is linked, collaborators can see that someone is working on the issue. | Source: "collaborators can see that someone is working on the issue"
- R15. Anyone can close an issue they opened. | Source: "Anyone can close an issue they opened."
- R16. On an organization repository, people with triage permission or more can close issues opened by others. | Source: "people with triage permissions or greater"
- R17. The reason for closing an issue can be changed before closing. | Source: "to change your reason for closing the issue"

## Open questions
- Q1. A keyword is written in a comment on the pull request, not in the description. Does it link? (R1)
- Q2. The issue is already closed when the pull request is merged. Is anything shown? (R2)
- Q3. The pull request is closed without merging. Does the issue stay open? (R2)
- Q4. The keyword points to issue #9999 and there is no such issue. What happens at creation and at merge? (R6)
- Q5. Which words count as keywords? The spec does not list them. Is "Closing #10" a keyword or ignored? (R5)
- Q6. Two pull requests both say "Closes #10". The first is merged. Does the second stay linked? (R2)
- Q7. A person without write access to the other repository writes "Fixes owner/repo#5". Does it close that issue? (R7)
- Q8. After the keyword is removed from the description, does the issue stay closed if it was already closed? (R12)
- Q9. Which reasons for closing exist, and what does each one show? (R17)
- Q10. If the default branch is renamed, do open pull requests keep their links? (R3)

## Test environment (written by the tester, not from the source. All of it is general knowledge of the GitHub website and is unverified.)
Use a new test repository that is not used for anything else. Nothing here should be run in a real project.

### Building blocks
- P = Preparation: gets the system into a starting state. A = Action: changes something. V = View: only looking.

### Preparations (P)
- P1. Done once. A test repository with a default branch `main` and a second branch `other`. Create the repository with a README, then create `other` from the branch menu.
- P1b. Done at the start of every test. A new branch for this test, named after the test (for example `t05`), created from `main`, with one file edited and committed. Each test gets its own branch, so a merge in one test never uses up the branch of another.
- P2. An open issue. Create it (A1) and write down its number N. P2b is a second open issue, number M.
- P3. A second test repository, and a second GitHub account with limited permission. NEEDS HOW: not set up.

### Actions (A)
- A1. Create an issue. Repository, Issues tab, "New issue", a title, "Create".
- A2. Create a pull request from the test branch into `main` with a description D. Repository, Pull requests tab, "New pull request", choose the two branches, write D, "Create pull request".
- A3. Create a pull request from the test branch into `other` with a description D. Same as A2 with another target branch.
- A4. Edit the description of a pull request. Open it, the three dots on the description, "Edit", save.
- A5. Merge a pull request. Open it, "Merge pull request", "Confirm merge".
- A6. Close an issue. Open it, "Close issue". The reason can be chosen in the dropdown next to the button.
- A7. Commit an edit to the test branch in the browser with a commit message M. Open a file on the test branch, edit, "Commit changes", write M.
- A8. Close a pull request without merging. Open it, "Close pull request".
- A9. Add a comment. Open the pull request, type the comment, "Comment".

### Views (V)
- V1. Look at an issue. Open it. Note: open or closed, the reason, and any linked pull request in the side panel.
- V2. Look at a pull request. Open it. Note: open, merged or closed, and any issue listed as "may close".

### Still not found
- A second account with limited permission (P3), and a second repository (for R7).
- Whether the side panel shows linked pull requests for commit-message keywords.
