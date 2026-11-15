29 tests, 51 rules in the spec.

## How to read this
- P = preparation, A = action, V = view.
- The commands are defined once in the spec. A test only names them with values.
- "Before you start" is what you do first. Amounts are in the smallest currency unit (2000 = 20.00 USD).

---

**T01 - Full refund when no amount is given**
Importance: Medium
Checks: A refund with no amount returns the whole charge (R3a, R1a).
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 that succeeded: do P1 with N = 2000. Write down the charge ID and the PaymentIntent ID.
Steps:
1. Ask for a refund on the charge and leave the amount out, so it is a full refund: A1 [charge = the charge ID, no amount].
2. Look at the refund that came back: V2 [refund ID from step 1].
3. Look at the charge to see what the refund did to it: V1 [charge ID].
Expected: The refund has status `succeeded` and amount 2000. The charge shows `amount_refunded` 2000 and `refunded` true. ASSUMPTION: status is `succeeded` at once for this card (E7).

**T02 - Partial refund when an amount is given**
Importance: Medium
Checks: A refund with an amount returns only that part, and the amount is in the smallest unit (R3b, R3c).
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 that succeeded: do P1 with N = 2000. Write down the charge ID.
Steps:
1. Ask for a refund of 500 (5.00 USD), so it is a partial refund: A1 [charge = the charge ID, amount = 500].
2. Look at the refund: V2 [refund ID].
3. Look at the charge: V1 [charge ID].
Expected: The refund amount is 500. The charge shows `amount_refunded` 500 and `refunded` false.

**T03 - Refunding by PaymentIntent is the same as refunding the charge**
Importance: Medium
Checks: A refund made with the PaymentIntent ID lands on the underlying charge (R2).
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 that succeeded: do P1 with N = 2000. Write down the charge ID and the PaymentIntent ID.
Steps:
1. Ask for a refund of 700 using the PaymentIntent ID instead of the charge ID: A1 [payment_intent = the PaymentIntent ID, amount = 700].
2. Look at the refund and check which charge it points to: V2 [refund ID].
3. Look at the charge: V1 [charge ID].
Expected: The refund shows the same charge ID you wrote down. The charge shows `amount_refunded` 700.

**T04 - A refund request with no charge and no PaymentIntent**
Importance: Medium
Checks: You must give a charge ID or a PaymentIntent ID (R1b).
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 that succeeded: do P1 with N = 2000. Write down the charge ID. You will not use it in the request, only to check that nothing changed.
Steps:
1. Ask for a refund with no charge ID and no PaymentIntent ID, only an amount of 500: A1 [leave out charge and payment_intent, amount = 500].
2. Read the answer.
3. Look at the charge to make sure no refund was made: V1 [charge ID].
Expected: The request is refused with an error. ASSUMPTION: the error type and message are not in the spec. The charge shows `amount_refunded` 0.

**T05 - Several refunds on one charge**
Importance: Medium
Checks: More than one refund can be made on the same charge, and they add up (R4).
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 that succeeded: do P1 with N = 2000. Write down the charge ID.
Steps:
1. Refund 500 (5.00 USD): A1 [charge = the charge ID, amount = 500].
2. Refund another 700 (7.00 USD) on the same charge: A1 [charge = the charge ID, amount = 700].
3. List the refunds of the charge: V4 [charge ID].
4. Look at the charge: V1 [charge ID].
Expected: Two refunds are listed, 500 and 700. The charge shows `amount_refunded` 1200 and `refunded` false.

**T06 - Refunds cannot add up to more than the charge**
Importance: High - money would be returned that was never paid.
Checks: The total of all refunds on a charge cannot be more than the charge (R5).
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 that succeeded: do P1 with N = 2000. Write down the charge ID. Then refund 1500 (A1 [amount = 1500]), so 500 is left to refund.
Steps:
1. Ask for 600, which is 100 more than what is left (1500 + 600 = 2100, charge is 2000): A1 [charge = the charge ID, amount = 600].
2. Read the answer.
3. Look at the charge: V1 [charge ID].
Expected: The request is refused with an error. ASSUMPTION: the exact error is not in the spec. The charge still shows `amount_refunded` 1500.

**T07 - Two refund requests at the same moment that together are too much**
Importance: High - two requests could together return more money than was paid.
Checks: The total cannot go over the charge even when two requests arrive at the same time (R5). The spec does not say how simultaneous requests are handled.
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 that succeeded: do P1 with N = 2000. Write down the charge ID.
Steps:
1. Send two refund requests of 1500 each at the same moment (together 3000, charge is 2000): A5 with A1 [charge = the charge ID, amount = 1500], twice.
2. Read both answers.
3. Look at the charge: V1 [charge ID].
Expected: ASSUMPTION: one request succeeds and the other is refused. The charge shows `amount_refunded` 1500, never 3000.

**T08 - Refund amount of zero or below**
Importance: Low
Checks: Edge case, no rule in the spec. Open question Q2.
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 that succeeded: do P1 with N = 2000. Write down the charge ID.
Steps:
1. Ask for a refund of 0: A1 [charge = the charge ID, amount = 0]. Read the answer.
2. Ask for a refund of -100: A1 [charge = the charge ID, amount = -100]. Read the answer.
3. Look at the charge: V1 [charge ID].
Expected: ASSUMPTION: both requests are refused. The charge shows `amount_refunded` 0.

**T09 - Refund on a charge that is already fully refunded**
Importance: Medium
Checks: Nothing more can be refunded after the whole charge was refunded (R5). Open question Q5 about the exact error.
Done via: API
Can I run it now: Yes
Before you start: Create a fully refunded payment of 2000: do P7 with N = 2000. Write down the charge ID.
Steps:
1. Ask for another refund of 100 on the same charge: A1 [charge = the charge ID, amount = 100].
2. Read the answer.
3. Look at the charge: V1 [charge ID].
Expected: ASSUMPTION: the request is refused with an error. The charge still shows `amount_refunded` 2000.

**T10 - A valid reason is saved**
Importance: Low
Checks: A reason from the allowed list is accepted (R6).
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 that succeeded: do P1 with N = 2000. Write down the charge ID.
Steps:
1. Ask for a refund of 500 with the reason `requested_by_customer`: A1 [charge = the charge ID, amount = 500, reason = requested_by_customer].
2. Look at the refund: V2 [refund ID].
3. Look at the charge: V1 [charge ID].
Expected: The refund shows `reason` = `requested_by_customer`. The charge shows `amount_refunded` 500.

**T11 - A reason that is not on the list**
Importance: Low
Checks: Only `duplicate`, `fraudulent` and `requested_by_customer` are allowed as a reason (R6).
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 that succeeded: do P1 with N = 2000. Write down the charge ID.
Steps:
1. Ask for a refund of 500 with the reason `changed_my_mind`, which is not on the list: A1 [charge = the charge ID, amount = 500, reason = changed_my_mind].
2. Read the answer.
3. Look at the charge: V1 [charge ID].
Expected: ASSUMPTION: the request is refused with an error. The charge shows `amount_refunded` 0.

**T12 - Metadata can be added and then removed**
Importance: Low
Checks: Metadata is optional, and a key is removed by sending an empty value (R7a, R7b).
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 that succeeded: do P1 with N = 2000. Write down the charge ID. Ask for a refund of 500 with metadata `order_id` = `A-1`: A1 [amount = 500, metadata order_id = A-1]. Write down the refund ID.
Steps:
1. Look at the refund to see the metadata: V2 [refund ID].
2. Remove the key by sending an empty value: A7 [refund ID, order_id = empty].
3. Look at the refund again: V2 [refund ID].
Expected: First view shows `order_id` = `A-1`. Second view shows no `order_id` key.

**T13 - A payment on hold cannot be refunded**
Importance: Medium
Checks: A PaymentIntent in status `requires_capture` cannot be refunded directly (R10).
Done via: API
Can I run it now: Yes
Before you start: Create a payment on hold of 2000: do P5 with N = 2000. Write down the PaymentIntent ID. Its status must be `requires_capture`.
Steps:
1. Ask for a refund on the PaymentIntent: A1 [payment_intent = the PaymentIntent ID, amount = 500].
2. Read the answer.
3. Look at the PaymentIntent: V3 [PaymentIntent ID].
Expected: The request is refused with an error. ASSUMPTION: the error is not in the spec. The status is still `requires_capture`.

**T14 - A payment on hold is cancelled instead**
Importance: Medium
Checks: A PaymentIntent in `requires_capture` can be cancelled (R10, R27a).
Done via: API
Can I run it now: Yes
Before you start: Create a payment on hold of 2000: do P5 with N = 2000. Write down the PaymentIntent ID.
Steps:
1. Cancel the PaymentIntent: A3 [PaymentIntent ID].
2. Read the answer.
3. Look at the PaymentIntent: V3 [PaymentIntent ID].
Expected: The status is `canceled`.

**T15 - A payment that already succeeded cannot be cancelled**
Importance: Medium
Checks: A PaymentIntent cannot be cancelled after it succeeded (R27b).
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 that succeeded: do P1 with N = 2000. Write down the PaymentIntent ID.
Steps:
1. Try to cancel the PaymentIntent: A3 [PaymentIntent ID].
2. Read the answer.
3. Look at the PaymentIntent: V3 [PaymentIntent ID].
Expected: The request is refused with an error. ASSUMPTION: the error text is not in the spec. The status is still `succeeded`.

**T16 - A pending refund later becomes succeeded**
Importance: Medium
Checks: With the test card for pending refunds, the refund starts `pending` and later becomes `succeeded` (R17, R32, E4).
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 with the pending-refund card: do P2 with N = 2000. Write down the charge ID.
Steps:
1. Ask for a full refund: A1 [charge = the charge ID, no amount]. Write down the refund ID.
2. Look at the refund right away: V2 [refund ID].
3. Wait a few minutes, then look again: V2 [refund ID]. The spec does not say how long it takes.
4. Look for the update event: V5 [type = refund.updated].
Expected: First view shows `pending`. Later view shows `succeeded`. ASSUMPTION: "a few minutes" is enough. The event list shows a `refund.updated` for this refund.

**T17 - A refund that succeeds first and then fails**
Importance: Medium
Checks: With the test card for failing refunds, the refund becomes `failed` and has a reason (R18b, R19, E5).
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 with the failing-refund card: do P3 with N = 2000. Write down the charge ID.
Steps:
1. Ask for a full refund: A1 [charge = the charge ID, no amount]. Write down the refund ID.
2. Look at the refund right away: V2 [refund ID].
3. Wait a few minutes, then look again: V2 [refund ID].
4. Look for the failure event: V5 [type = refund.failed].
Expected: First view shows `succeeded`. Later view shows `failed`, with `failure_reason` and `failure_balance_transaction`. ASSUMPTION: the reason is one of the values in R19. The event list shows `refund.failed`.

**T18 - A dispute while a refund is pending**
Importance: Medium
Checks: If a customer disputes while a refund is pending, the refund fails with `charge_for_pending_refund_disputed` (R20).
Done via: API
Can I run it now: No - no test card gives a pending refund and a dispute at the same time (P9 is NEEDS HOW).
Before you start: Create a charge with a pending refund and a dispute at the same time: NEEDS HOW (P9).
Steps:
1. Ask for a full refund: A1 [charge = the charge ID, no amount].
2. Wait for the dispute to appear.
3. Look at the refund: V2 [refund ID].
Expected: The refund has status `failed` and `failure_reason` = `charge_for_pending_refund_disputed`.

**T19 - Refund on a charge that is already disputed**
Importance: Medium
Checks: Edge case, no rule in the spec.
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 that gets a dispute: do P4 with N = 2000. Wait a minute. Write down the charge ID.
Steps:
1. Check the charge is disputed: V1 [charge ID]. `disputed` should be true.
2. Ask for a full refund: A1 [charge = the charge ID, no amount]. Read the answer.
3. Look at the charge again: V1 [charge ID].
Expected: ASSUMPTION: not in the spec. Write down what happens (refund made or refused) and see if it matches what R20 and R21 suggest.

**T20 - A card refund cannot be cancelled through the API**
Importance: Low
Checks: For cards, cancelling is only possible in the Dashboard (R24a).
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 that succeeded: do P1 with N = 2000. Ask for a refund of 500 (A1 [amount = 500]). Write down the refund ID.
Steps:
1. Try to cancel the refund through the API: A6 [refund ID].
2. Read the answer.
3. Look at the refund: V2 [refund ID].
Expected: The request is refused. ASSUMPTION: the error text is not in the spec. The refund status is unchanged.

**T21 - A card refund cancelled in the Dashboard**
Importance: Medium
Checks: A card refund can be cancelled in the Dashboard for a short time, and a cancelled refund shows a failure reason (R24b, R26, E8).
Done via: Dashboard
Can I run it now: Yes
Before you start: Create a payment of 2000 with the pending-refund card: do P2 with N = 2000. Ask for a full refund (A1, no amount). Write down the refund ID.
Steps:
1. Cancel the refund within 30 minutes: A4 [the payment].
2. Look at the refund: V2 [refund ID].
3. Look at the charge: V1 [charge ID].
Expected: ASSUMPTION: this pending card refund can be cancelled (the spec says only "some card refunds"). The refund has status `canceled`, with `failure_reason` and `failure_balance_transaction`. The charge shows `amount_refunded` 0.

**T22 - Sending the same refund twice with the same key**
Importance: High - a retry must never refund twice.
Checks: A retry with the same Idempotency-Key returns the saved answer (R33, R35).
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 that succeeded: do P1 with N = 2000. Write down the charge ID.
Steps:
1. Ask for a refund of 500 with the key `KEY-1`: A1 [charge = the charge ID, amount = 500, key = KEY-1]. Write down the refund ID.
2. Send exactly the same request again with the same key: A1 [same values, key = KEY-1].
3. List the refunds of the charge: V4 [charge ID].
4. Look at the charge: V1 [charge ID].
Expected: Both answers show the same refund ID. Only one refund is listed. The charge shows `amount_refunded` 500.

**T23 - Same key with different values**
Importance: Medium
Checks: A retry with the same key but different values gives an error (R37).
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 that succeeded: do P1 with N = 2000. Write down the charge ID.
Steps:
1. Ask for a refund of 500 with the key `KEY-2`: A1 [charge = the charge ID, amount = 500, key = KEY-2].
2. Ask again with the same key but 600: A1 [charge = the charge ID, amount = 600, key = KEY-2]. Read the answer.
3. Look at the charge: V1 [charge ID].
Expected: The second request gives an error. The charge shows `amount_refunded` 500.

**T24 - A request that failed validation can be retried with the same key**
Importance: Medium
Checks: If values fail validation, nothing is saved and the request can be retried (R38a).
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 that succeeded: do P1 with N = 2000. Write down the charge ID.
Steps:
1. Send an invalid request with the key `KEY-3` (amount -1): A1 [charge = the charge ID, amount = -1, key = KEY-3]. Read the answer.
2. Send a correct request with the same key: A1 [charge = the charge ID, amount = 500, key = KEY-3].
3. Look at the charge: V1 [charge ID].
Expected: Step 1 is refused. Step 2 succeeds. The charge shows `amount_refunded` 500. ASSUMPTION: step 1 fails at validation, so the key is free.

**T25 - Two requests with the same key at the same moment**
Importance: Medium
Checks: If a request conflicts with a concurrent one, nothing is saved and it can be retried (R38b).
Done via: API
Can I run it now: Yes
Before you start: Create a payment of 2000 that succeeded: do P1 with N = 2000. Write down the charge ID.
Steps:
1. Send two identical refund requests of 500 with the key `KEY-4` at the same moment: A5 with A1 [charge = the charge ID, amount = 500, key = KEY-4], twice. Read both answers.
2. If one was refused, send it again: A1 [same values, key = KEY-4].
3. List the refunds of the charge: V4 [charge ID].
Expected: ASSUMPTION: one request succeeds and one conflicts. After the retry only one refund is listed, 500.

**T26 - Who is allowed to refund**
Importance: Medium
Checks: Edge case, no rule in the spec.
Done via: API
Can I run it now: No - the spec has no way to create a key with fewer permissions (NEEDS HOW).
Before you start: Create a key that has no permission to refund: NEEDS HOW. Create a payment of 2000 that succeeded: do P1 with N = 2000.
Steps:
1. Ask for a refund with the limited key: A1 [charge = the charge ID, amount = 500, SECRET_KEY = the limited key].
2. Read the answer.
3. Look at the charge with the normal key: V1 [charge ID].
Expected: ASSUMPTION: the request is refused. The charge shows `amount_refunded` 0.

**T27 - Refund in a currency with no decimals**
Importance: Medium
Checks: Edge case, no rule in the spec. Open question Q3. R3c says only "smallest unit".
Done via: API
Can I run it now: No - NEEDS HOW: whether the test card works with jpy (P6).
Before you start: Create a payment of 1000 yen: do P6 with N = 1000.
Steps:
1. Ask for a refund of 500: A1 [charge = the charge ID, amount = 500].
2. Look at the refund: V2 [refund ID].
3. Look at the charge: V1 [charge ID].
Expected: ASSUMPTION: 500 means 500 yen, not 5.00. The charge shows `amount_refunded` 500.

**T28 - Not enough available balance**
Importance: Medium
Checks: With too little available balance, card refunds stay pending (R14, R15a).
Done via: API
Can I run it now: No - NEEDS HOW: a charge whose money is still pending (P8) and a way to read the balance (V6).
Before you start: Create a charge whose money is not yet available: NEEDS HOW (P8). Check the balance: NEEDS HOW (V6).
Steps:
1. Ask for a full refund: A1 [charge = the charge ID, no amount].
2. Look at the refund: V2 [refund ID].
3. Read the balance: NEEDS HOW (V6).
Expected: The refund has status `pending`. ASSUMPTION: it stays pending until the balance is enough.

**T29 - Reason "Other" needs a note in the Dashboard**
Importance: Low
Checks: In the Dashboard, the reason "Other" needs a note (R13).
Done via: Dashboard
Can I run it now: No - the spec does not say whether the Dashboard flow works in test mode.
Before you start: Create a payment of 2000 that succeeded: do P1 with N = 2000.
Steps:
1. Start a refund in the Dashboard, choose "Other" and leave the note empty: A2 [the payment, reason = Other, no note].
2. Read what the screen says.
3. Look at the charge: V1 [charge ID].
Expected: The refund cannot be sent without a note. The charge shows `amount_refunded` 0.

---

## Appendix

### Rules list
R1a refund made with a charge ID or PaymentIntent ID. R1b one of them is required. R2 refunding a PaymentIntent equals refunding its charge. R3a no amount means full refund. R3b amount means partial. R3c amount is an integer in the smallest unit. R4 several refunds on one charge. R5 total refunds cannot exceed the charge. R6 reason is one of three values. R7a metadata optional. R7b metadata key unset with empty value. R8 instructions_email for methods without native refund. R9a refund_application_fee and reverse_transfer are booleans. R9b only the creating application can reverse a transfer. R10 requires_capture cannot be refunded, must be cancelled. R11 refunds go only to the original payment method. R12 bulk refund in Dashboard is full only. R13 reason Other needs a note. R14 refunds use available balance. R15a card refunds pending if balance too low. R15b other methods fail if balance too low. R16 processing fees are not returned. R17 refund statuses. R18a refund can fail at the bank or issuer. R18b failed refund has failure fields. R18c failed amount returns to balance, up to 30 days. R19 failure_reason values. R20 dispute while pending fails the refund. R21 double refund risk for bank debits. R22 some methods enter requires_action. R23 requires_action transitions. R24a cards cancelled only in Dashboard. R24b some card refunds cancellable briefly. R25 requires_action refund cancellable by API or Dashboard. R26 cancelled refund has failure fields. R27a PaymentIntent cancellable only in listed states. R27b not cancellable after success. R27c cancelled PaymentIntent fails further operations. R28 reversal. R29 customer sees credit in 5-10 business days. R30a ARN up to 7 business days. R30b no ARN for reversals. R31 refund email conditions. R32 events. R33 POST accepts Idempotency-Key. R34 key up to 255 characters. R35 retry returns saved response. R36 keys pruned after 24 hours. R37 different parameters on retry give error. R38a validation failure saves nothing. R38b concurrent conflict saves nothing.

### NEEDS HOW list
- A charge with a pending refund and a dispute at once (P9).
- A charge whose money is still pending (P8).
- Reading the available balance (V6).
- A charge in a zero-decimal currency, jpy (P6).
- A key without permission to refund.
