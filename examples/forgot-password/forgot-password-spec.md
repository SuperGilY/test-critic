# Spec: Forgot password (input for the test-writer skill) - v1

Source: OWASP Forgot Password Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html
Licence: CC BY-SA 4.0. Date read: 2026-11-15.
The source text is a condensed version returned by a fetch tool (see source-owasp-forgot-password.txt). It is not the full page.
There are 30 rules. The IDs are final.

## Rules
- R1. The reset request gives the same message for accounts that exist and accounts that do not. | Source: "Return a consistent message for both existent and non-existent accounts."
- R2. The reset request takes the same time for both. | Source: "keep response timing uniform"
- R3. The reset method is delivered through a separate channel. | Source: "use a side channel to deliver the reset method"
- R4a. Tokens or codes are cryptographically random. | Source: "Tokens or codes should be cryptographically random"
- R4b. Tokens or codes are long enough. | Source: "long enough"
- R4c. Tokens or codes are stored securely. | Source: "stored securely"
- R4d. Tokens or codes can be used once. | Source: "single-use"
- R4e. Tokens or codes expire. | Source: "time-limited"
- R5. A token is bound to one user. | Source: "Bind tokens to users"
- R6. Nothing changes on the account (for example a lockout) until a valid token is presented. | Source: "Make no account changes (such as lockouts) until a valid token is presented."
- R7. Requests are limited per account, or a CAPTCHA is required. | Source: "Rate-limit per account or require a CAPTCHA to prevent flooding."
- R8. Input is validated. | Source: "Apply standard input validation and SQL injection defenses."
- R9. The user's identity is checked with the token or code. | Source: "Verify identity via the token or code."
- R10. The new password is entered twice. | Source: "Require the password to be entered twice"
- R11. The new password must meet the application's password policy. | Source: "enforce the application's standard password policy"
- R12. The new password is stored securely. | Source: "Store it securely"
- R13. An email notice is sent after the reset, and it does not contain the password. | Source: "email a notice without the password"
- R14. The user is not logged in automatically after the reset. | Source: "Don't log the user in automatically."
- R15. The user is offered to end existing sessions. | Source: "Offer to invalidate existing sessions."
- R16. The reset link is not built from the Host header of the request. | Source: "Don't trust the Host header when building reset URLs"
- R17. Reset links use HTTPS. | Source: "Use HTTPS."
- R18. The reset page sends a no-referrer Referrer-Policy. | Source: "Set a no-referrer Referrer-Policy on the reset page."
- R19. Guessing of tokens is rate-limited. | Source: "Rate-limit guessing."
- R20. A PIN has 6 to 12 digits. | Source: "6 to 12 digits"
- R21. Entering a PIN with the username opens a session that can only reset the password. | Source: "creates a restricted session limited to resetting the password"
- R22. Security questions are never the only way to reset. | Source: "Never the sole reset mechanism"
- R23. Accounts are not locked because of forgotten-password attempts. | Source: "Don't lock accounts in response to forgotten-password attacks"
- R24. After a suspected compromise, sessions and open reset links are ended. | Source: "Invalidate sessions and outstanding reset links."
- R25. After a suspected compromise, the user is notified through all applicable channels. | Source: "Notify the user through all applicable channels"
- R26. Replaced contact details are not restored automatically. | Source: "Don't automatically restore replaced contacts."

## Open questions
- Q1. How long is "long enough"? Example: is a 6-character token allowed, or does it need 32 or more? (R4b)
- Q2. How long is "time-limited"? Example: a link made at 10:00 is still valid at 10:40, yes or no? (R4e)
- Q3. What is the limit for requests? Example: is the 6th request in one hour for the same account refused? (R7, R19)
- Q4. What is "the application's password policy"? Example: is "abc12345" accepted? (R11)
- Q5. What exact message is shown for R1? Same text only, or also the same page and status code? (R1, R2)
- Q6. How much time difference counts as "the same time"? Example: 200 ms for an existing account and 250 ms for a missing one. (R2)
- Q7. If the PIN session cannot do anything except reset, how long does it last? (R21)
- Q8. Which channels count as "applicable" in R25? Example: email only, or email and SMS? (R25)
- Q9. What happens to a token that was used once and is presented again? Error text? (R4d)
- Q10. If the user declines to end other sessions (R15), do those sessions stay open? (R15)

## Test environment
Not provided. The source describes advice for builders and has no system to test.
Needed before tests can run:
- P: a test account with a known email, and a way to read the email it receives.
- A: open the reset page, send a reset request for an email, open a reset link, submit a new password.
- V: read the email received, read the response of the request, check whether a session is open.
- A way to see response timing and response headers (for R2, R16, R18).
- A way to make the token expire without waiting (for R4e).
