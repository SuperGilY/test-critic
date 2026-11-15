# Spec: Refunds (input for the test-writer skill) - v2, stable IDs

Source: Stripe public docs, read 2026-11-03.
- Refunds guide: https://docs.stripe.com/refunds
- Idempotent requests: https://docs.stripe.com/idempotency
- Create refund params: from a Rust client mirror of the API (docs.rs async-stripe-core CreateRefund). The official reference page was not reachable, so parameter constraints are only what is listed here.

Each rule has a fixed ID so tests can cite it. There are 51 rules. The IDs are final: do not split, merge, renumber or invent IDs. A rule that is a sentence inside a longer paragraph already has its own letter (R3a, R3b, R3c).

## Creating a refund
- R1a. A refund is made by creating a refund with a charge ID or a PaymentIntent ID.
- R1b. You must specify one of them.
- R2. Refunding a PaymentIntent is the same as refunding its underlying charge.
- R3a. `amount` is optional. Without it, the refund is full.
- R3b. With `amount`, the refund is partial.
- R3c. `amount` is an integer in the smallest currency unit (for example cents).
- R4. More than one refund can be issued against one charge.
- R5. The total of all refunds on a charge cannot exceed the original charge amount.
- R6. `reason`, if set, is one of: `duplicate`, `fraudulent`, `requested_by_customer`.
- R7a. `metadata` is optional key-value pairs.
- R7b. A metadata key can be unset by posting an empty value.
- R8. `instructions_email` is for payment methods without native refund support.
- R9a. `refund_application_fee` and `reverse_transfer` are booleans.
- R9b. A transfer can be reversed only by the application that created the charge.
- R10. A PaymentIntent with status `requires_capture` cannot be refunded directly (the charge is uncaptured). It must be cancelled instead.
- R11. Refunds can only go back to the original payment method. A different destination is not possible.
- R12. Dashboard bulk refund supports full refunds only. Partial refunds are issued one by one.
- R13. Dashboard: choosing reason "Other" requires a note.

## Balance and fees
- R14. Refunds use the available Stripe balance (not pending amounts).
- R15a. If the available balance is not enough, card refunds are held as pending until the balance is sufficient.
- R15b. If the available balance is not enough, refunds for other payment method types fail.
- R16. Stripe's processing fees from the original transaction are not returned.

## Statuses and failures
- R17. Refund statuses mentioned: `pending`, `succeeded`, `failed`, `canceled`, `requires_action`.
- R18a. A refund can fail if the bank or issuer cannot process it (closed account, card problem).
- R18b. A failed refund has status `failed` with `failure_reason` and `failure_balance_transaction`.
- R18c. After a failure the amount returns to the Stripe balance, which can take up to 30 days from the post date.
- R19. `failure_reason` values: `charge_for_pending_refund_disputed`, `declined`, `expired_or_canceled_card`, `insufficient_funds`, `lost_or_stolen_card`, `merchant_request`, `unknown`.
- R20. If a customer disputes a charge while a refund is pending, the refund fails with `charge_for_pending_refund_disputed`. Stripe recommends handling the dispute instead of refunding.
- R21. For bank debit methods (SEPA, Bacs, ACH, and others) there is a risk of a double refund if a refund and a dispute both happen.
- R22. Some payment methods (for example Konbini, PromptPay, Boleto, bank transfers) enter `requires_action` and the customer is emailed for bank details. `next_action` holds the email info and an `expires_at`.
- R23. `requires_action` transitions: customer submits details -> `pending`; refund arrives -> `succeeded`; bank returns the funds -> back to `requires_action`; customer does not respond before expiry -> `failed`; cancelled while in `requires_action` -> `canceled`.

## Cancelling
- R24a. For cards, only Dashboard cancellation is supported (not API).
- R24b. Some card refunds can be cancelled for a short time, only if not already processed as a reversal.
- R25. A refund in `requires_action` can be cancelled by API or Dashboard.
- R26. A cancelled refund moves to `canceled` and includes `failure_reason` and `failure_balance_transaction`.
- R27a. A PaymentIntent can be cancelled only in: `requires_payment_method`, `requires_capture`, `requires_confirmation`, `requires_action`, `processing` (US bank account only).
- R27b. A PaymentIntent cannot be cancelled after it succeeded.
- R27c. A cancelled PaymentIntent fails any further operation.

## Reversal
- R28. A refund issued shortly after the charge can appear as a reversal: the original charge disappears from the customer's statement and no separate credit is issued. Via API: `destination_details[card][type] = 'reversal'`.

## Timing and notifications
- R29. The customer sees a credit about 5-10 business days later, depending on the bank. Successful refunds can show in real time depending on network and issuer.
- R30a. The ARN reference can take up to 7 business days to arrive.
- R30b. No ARN for reversals.
- R31. Email to the customer is sent only if: the charge was created on a customer, the customer has a stored email, and "Email customers for refunds" is enabled.
- R32. Events: `refund.created`, `refund.updated`, `refund.failed`, `charge.refunded` (including partial), `charge.dispute.funds_reinstated`. Stripe recommends listening at least to `refund.created`.

## Idempotency (API v1)
- R33. All POST requests accept an `Idempotency-Key` header. GET and DELETE do not need it.
- R34. A key is up to 255 characters.
- R35. A retry with the same key returns the saved response of the first request, including 500 errors.
- R36. Keys can be pruned after at least 24 hours. After that a reused key starts a new request.
- R37. If a retry uses different parameters than the original, the API errors.
- R38a. The result is saved only after the endpoint starts executing. If parameters fail validation, nothing is saved and the request can be retried.
- R38b. If the request conflicts with a concurrent request, nothing is saved and the request can be retried.

## Not stated in the pages above (open questions)
- Q1. Is there a time limit after which a charge can no longer be refunded?
- Q2. Minimum refund amount? Rules for zero or negative amounts?
- Q3. Rules for zero-decimal and three-decimal currencies?
- Q4. How long can a refund stay pending for lack of balance (the "pending refund expiration window")?
- Q5. What happens on a refund request for an already fully refunded charge (error type and message)?
- Q6. Refund of a charge in a different currency than the account's?

## Test environment (how to set things up)

Source: Stripe testing page (https://docs.stripe.com/testing), read 2026-11-03. The last ~4,300 characters of the page were not read. Lines marked [unverified] come from general knowledge of the API and were not in the pages read. Check them before running.

- E1. Use test-mode API keys for all calls.
- E2. Card-level state from one test can affect later tests that use the same card. Use a different test card (or a new payment method) for each independent scenario.
- E3. Card 4000000000000077 (`pm_card_bypassPending`): the charge succeeds and funds go straight to the available balance, bypassing pending. International version: 4000003720000278.
- E4. Card 4000000000007726 (`pm_card_pendingRefund`): a refund starts as `pending`, and "some time later" becomes `succeeded` and sends `refund.updated`. The delay is not stated.
- E5. Card 4000000000005126 (`pm_card_refundFail`): a refund starts as `succeeded`, and "some time later" becomes `failed` and sends `refund.failed`. The delay is not stated.
- E6. Dispute cards: 4061219946393810 (a fraudulent dispute is created shortly after the charge, listed as the card for most cases). 4000000000000259 (listed as creating a fraudulent dispute during the payment request, not confirmed). 4000008400000795: if the payment is partially refunded, a dispute is created for the unrefunded part (refund 3 of 10 = 7 disputed). A full refund does not trigger a dispute.
- E7. With all other test cards, refunds succeed immediately and never change status afterwards.
- E8. A card refund can be cancelled only in the Dashboard. In test environments, the cancel window is 30 minutes. (This gives a number for the R24b "short time" in test mode only.)
- E9. Test emails are documented only for ACH Direct Debit, with the address format `{username}+test_email@{domain}`. Whether card refund emails are sent in test mode is not stated.
- E10. Parallel requests need a client that can send two calls at the same moment (two terminals, or a short script).

### How to read the tests: three kinds of building blocks
Every test is made of building blocks that are defined once here.
- P = Preparation. Gets the system into a starting state (for example "a charge of 2000 that succeeded"). Done before the test.
- A = Action. Something you do that changes the system (ask for a refund, cancel something).
- V = View. Only looking at the current state. Changes nothing.

Replace SECRET_KEY with your test-mode secret key (E1). Sources: the Refunds, Idempotent requests, Retrieve a charge, Retrieve a refund and Create a PaymentIntent pages (read 2026-11-03). [unverified] marks what was not on those pages.

### Preparations (P)
- P1. A charge of N that succeeded, money available now. In a terminal:
  `curl https://api.stripe.com/v1/payment_intents -u "SECRET_KEY:" -d amount=N -d currency=usd -d payment_method=pm_card_bypassPending -d confirm=true -d "payment_method_types[]=card"`
  In the answer, write down two IDs: `id` (the PaymentIntent, starts with pi_) and `latest_charge` (the charge, starts with ch_). N must be at least 50 (the minimum charge is $0.50). [unverified: the `payment_method_types[]=card` form, needed so no redirect is asked for]
- P2. Same as P1, but with `payment_method=pm_card_pendingRefund`. A refund on this charge starts `pending` and later becomes `succeeded` (E4).
- P3. Same as P1, but with `payment_method=pm_card_refundFail`. A refund on this charge starts `succeeded` and later becomes `failed` (E5).
- P4. Same as P1, but with `payment_method=pm_card_createDispute`. A dispute appears "shortly" after the charge (E6).
- P5. A PaymentIntent on hold (`requires_capture`). Same as P1, with `-d capture_method=manual` added. The answer should show `status` = `requires_capture`. Write down the PaymentIntent ID.
- P6. A charge in a zero-decimal currency. Same as P1, with `currency=jpy` and N = 1000. NEEDS HOW: whether `pm_card_bypassPending` works with jpy.
- P7. A fully refunded charge. P1, then A1 with no amount.
- P8. A charge whose money is still pending, not available. NEEDS HOW: which test payment method leaves funds pending, and how to read the available balance.
- P9. A charge with a pending refund and a dispute at the same time. NEEDS HOW: no test card in the spec gives both.

### Actions (A)
- A1. Ask for a refund. In a terminal:
  `curl https://api.stripe.com/v1/refunds -u "SECRET_KEY:" -d charge=CHARGE_ID -d amount=AMOUNT`
  Leave out `-d amount=...` for a full refund. To refund by PaymentIntent use `-d payment_intent=PI_ID` instead of the charge. Add `-H "Idempotency-Key: KEY"` for an idempotent request. Add `-d reason=requested_by_customer` for a reason. Add `-d "metadata[order_id]=A-1"` for metadata [unverified syntax]. The answer is a refund object, or an error.
- A2. Ask for a refund in the Dashboard. Payments page -> find the payment -> the three dots -> "Refund payment" -> the default is a full refund; for a partial refund type another amount -> choose a reason ("Other" needs a note) -> "Refund".
- A3. Cancel a PaymentIntent. In a terminal:
  `curl -X POST https://api.stripe.com/v1/payment_intents/PI_ID/cancel -u "SECRET_KEY:"`
- A4. Cancel a refund in the Dashboard. Payments page -> find the payment -> the three dots -> "Cancel refund" -> if there are several partial refunds pick the right one -> "Yes, cancel refund".
- A5. Send two requests at the same moment. Option 1: open two terminal windows, paste one command in each, press Enter in both together. Option 2: in one terminal join the two commands with `&` and end with `wait`. [general shell knowledge]
- A6. Try to cancel a refund by API. `curl -X POST https://api.stripe.com/v1/refunds/REFUND_ID/cancel -u "SECRET_KEY:"` [unverified path]
- A7. Update a refund's metadata, for example to unset a key. `curl https://api.stripe.com/v1/refunds/REFUND_ID -u "SECRET_KEY:" -d "metadata[order_id]="` (an empty value unsets the key, per R7b). [unverified call]

### Views (V)
- V1. Look at a charge. `curl https://api.stripe.com/v1/charges/CHARGE_ID -u "SECRET_KEY:"`
  Useful fields: `amount` (the charge), `amount_refunded` (total refunded so far), `refunded` (true or false), `disputed` (true or false), `status`.
- V2. Look at a refund. `curl https://api.stripe.com/v1/refunds/REFUND_ID -u "SECRET_KEY:"`
  Useful fields: `status`, `amount`, `charge`, `payment_intent`, `destination_details`, `metadata`, `reason`. When a refund failed or was cancelled it also has `failure_reason` and `failure_balance_transaction` (R18b, R26).
- V3. Look at a PaymentIntent. `curl https://api.stripe.com/v1/payment_intents/PI_ID -u "SECRET_KEY:"`. Useful field: `status`. [same pattern as V1 and V2, page not opened]
- V4. List the refunds of a charge. `curl -G https://api.stripe.com/v1/refunds -u "SECRET_KEY:" -d charge=CHARGE_ID` [unverified]
- V5. See events (for example `refund.created`). `curl -G https://api.stripe.com/v1/events -u "SECRET_KEY:" -d type=refund.created -d limit=5` [unverified]
- V6. Read the available balance. NEEDS HOW.

### Still not found (a writer must mark these NEEDS HOW)
- A payment method that enters `requires_action` on refund (Konbini, PromptPay, bank transfer).
- Moving time forward (24-hour key pruning, 30-day failure return, `expires_at`).
- Forcing a 500 error.
- Creating a charge from a different application (Connect) and a transfer.
- Whether the Dashboard flows (R12, R13) can be tested in test mode.
- Whether a minimum or maximum for `amount` of a refund exists (only the PaymentIntent minimum of $0.50 was found).
