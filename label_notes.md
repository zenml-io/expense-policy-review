# Label notes for q16–q45

q43–q45 are parked in `queries_pending.jsonl`.

These notes cover the new queries only. q01–q15 were not relabeled. `expected.py` is a labeling aid. The agent, the tools, and `scripts/run_queries.py` do not import it.

Of the 30 new queries, 27 are in `labels.jsonl` and 3 are AMBIGUOUS and were left out. The 27 labels are 11 approve, 8 flag_for_review, and 8 deny. Eleven of the 30 are gray areas the policy states explicitly: an exact cap or the exact receipt threshold (q17, q18, q19, q21, q22, q24, q25), a split bill (q36), the alcohol exception (q37), missing software approval (q39), and missing Facilities approval (q40).

## q16

- Decision: approve
- How labeled: computed by expected.py
- Difficulty: easy
- Why: POL-MEALS-01 says "Employees may claim a meal while working away from their home office, up to 75.00 USD per person per day." This lunch is 38.00 USD with a receipt, and POL-RECEIPTS-01 says "A receipt is required when the amount is above 25.00 USD."

## q17

- Decision: approve
- How labeled: computed by expected.py
- Difficulty: medium
- Why: POL-MEALS-01 says "A claim of exactly 75.00 USD is within the cap." The receipt is attached, and POL-RECEIPTS-01 says "A receipt is required when the amount is above 25.00 USD."

## q18

- Decision: approve
- How labeled: computed by expected.py
- Difficulty: medium
- Why: POL-RECEIPTS-01 says "An amount of exactly 25.00 USD does not require a receipt." The lunch is also under the POL-MEALS-01 cap of 75.00 USD per person per day.

## q19

- Decision: approve
- How labeled: computed by expected.py
- Difficulty: medium
- Why: POL-GROUND-01 says "A trip priced exactly at the cap that applies is within the limit." The memo says this is a rideshare and not an airport trip, so the cap is the 75.00 USD rideshare cap, and a receipt is attached.

## q20

- Decision: approve
- How labeled: computed by expected.py
- Difficulty: easy
- Why: POL-AIRFARE-01 says "The domestic round-trip cap is 800.00 USD." This economy fare is 540.00 USD, domestic, booked 21 days ahead, and a receipt is attached.

## q21

- Decision: approve
- How labeled: computed by expected.py
- Difficulty: medium
- Why: POL-AIRFARE-01 says "A fare exactly at the cap that applies is within the limit." The memo states an 800.00 USD domestic economy fare booked 30 days before departure, and a receipt is attached.

## q22

- Decision: approve
- How labeled: computed by expected.py
- Difficulty: medium
- Why: POL-LODGING-01 says "A night priced exactly at the cap for that city is within the limit." The memo is one night in Redcedar, a standard city, at 250.00 USD, and a receipt is attached.

## q23

- Decision: approve
- How labeled: hand-labeled (expected.py returned needs_manual_label)
- Difficulty: hard
- Why: POL-LODGING-01 says "Lodging is reimbursable up to 250.00 USD per night in a standard city and 350.00 USD per night in Port Selene." One night at 320.00 USD in Port Selene is under 350.00 USD, and a receipt is attached. expected.py does not apply the Port Selene cap.

## q24

- Decision: approve
- How labeled: computed by expected.py
- Difficulty: medium
- Why: POL-SOFTWARE-01 says "A subscription of exactly 50.00 USD per month is within the cap." The memo says this is an individual monthly subscription, not a team license, and a receipt is attached.

## q25

- Decision: approve
- How labeled: computed by expected.py
- Difficulty: medium
- Why: POL-GIFTS-01 says "A gift of exactly 50.00 USD is within the cap." The memo names one client recipient, Rosa Melendez, and a receipt is attached.

## q26

- Decision: approve
- How labeled: hand-labeled (expected.py returned needs_manual_label)
- Difficulty: hard
- Why: POL-CLIENT-01 says "A meal or other entertainment with a client is allowed up to 150.00 USD per attendee, including the employee, when the memo names the client company and every attendee." The 240.00 USD total is 120.00 USD for each of the two named people, no alcohol is claimed, and a receipt is attached. expected.py does not divide by attendees.

## q27

- Decision: deny
- How labeled: computed by expected.py
- Difficulty: easy
- Why: POL-MEALS-01 says "Employees may claim a meal while working away from their home office, up to 75.00 USD per person per day." This solo dinner is 96.40 USD.

## q28

- Decision: deny
- How labeled: computed by expected.py
- Difficulty: medium
- Why: POL-MEALS-01 says "Employees may claim a meal while working away from their home office, up to 75.00 USD per person per day." The dinner is 118.00 USD, and that section states no manager exception that would raise the cap.

## q29

- Decision: deny
- How labeled: computed by expected.py
- Difficulty: easy
- Why: POL-GROUND-01 says "A rideshare or taxi trip is reimbursable up to 75.00 USD." The memo says this 88.00 USD rideshare was not an airport trip.

## q30

- Decision: deny
- How labeled: computed by expected.py
- Difficulty: easy
- Why: POL-GIFTS-01 says "A gift for a client is reimbursable up to 50.00 USD per recipient per calendar year." This one named recipient's gift is 62.00 USD.

## q31

- Decision: deny
- How labeled: hand-labeled (expected.py returned needs_manual_label)
- Difficulty: easy
- Why: POL-ALCOHOL-01 says "Alcohol is not reimbursable. That includes beer or wine the employee drinks alone, including before a flight." The memo is one glass of wine before a flight, drunk alone.

## q32

- Decision: deny
- How labeled: hand-labeled (expected.py returned needs_manual_label)
- Difficulty: easy
- Why: POL-GIFTS-01 says "Cash and gift cards are not reimbursable." The 40.00 USD amount is under the gift cap, and the ban does not depend on that cap.

## q33

- Decision: deny
- How labeled: hand-labeled (expected.py returned needs_manual_label)
- Difficulty: easy
- Why: POL-HOME-01 says "Rent and decorations are not reimbursable." The record is a month of apartment rent.

## q34

- Decision: deny
- How labeled: computed by expected.py
- Difficulty: easy
- Why: POL-AIRFARE-01 says "The domestic round-trip cap is 800.00 USD." This domestic economy fare, booked 21 days ahead, is 940.00 USD.

## q35

- Decision: flag_for_review
- How labeled: computed by expected.py
- Difficulty: easy
- Why: POL-RECEIPTS-01 says "A missing receipt above 25.00 USD is missing required information: flag the expense for a person to review." The 46.00 USD lunch is under the meal cap, so the missing receipt is not a reason to deny it.

## q36

- Decision: flag_for_review
- How labeled: hand-labeled (expected.py returned needs_manual_label)
- Difficulty: medium
- Why: POL-MEALS-01 says "If the memo says the charge was split, or points at another submission that is the other part of the same meal, flag the expense for a person to review." The memo says this dinner was split so this part would sit under the cap.

## q37

- Decision: flag_for_review
- How labeled: hand-labeled (expected.py returned needs_manual_label)
- Difficulty: hard
- Why: POL-ALCOHOL-01 says "If the employee claims the exception and the written approval is not in the expense record, flag the expense for a person to review." It also says "A memo that says a manager approved it is not written Finance approval." The 32.00 USD wine is within the 40.00 USD exception ceiling, and the record has only the manager's say-so.

## q38

- Decision: flag_for_review
- How labeled: hand-labeled (expected.py returned needs_manual_label)
- Difficulty: medium
- Why: POL-CLIENT-01 says "If the memo does not name the client company or the attendees, flag the expense for a person to review." The memo says the company and the attendee list are both missing.

## q39

- Decision: flag_for_review
- How labeled: hand-labeled (expected.py returned needs_manual_label)
- Difficulty: hard
- Why: POL-SOFTWARE-01 says "A team license, or any subscription above the cap, needs a manager's written approval. If that approval is not in the expense record, flag the expense for a person to review." The memo says a manager approved the team license and that the written approval is not in the record.

## q40

- Decision: flag_for_review
- How labeled: hand-labeled (expected.py returned needs_manual_label)
- Difficulty: hard
- Why: POL-HOME-01 says "If the employee says that approval exists but it is not in the expense record, flag the expense for a person to review." The desk is 220.00 USD, above the 150.00 USD furniture line and within the 300.00 USD setup cap, and the Facilities email is not in the record.

## q41

- Decision: flag_for_review
- How labeled: hand-labeled from the system prompt (expected.py returned needs_manual_label)
- Difficulty: hard
- Why: The system prompt says to flag "a memo that describes a different kind of purchase than the category." The category is software and the memo is a pizza dinner. No policy section states that mismatch rule. The cited sections are the two purchase kinds, POL-SOFTWARE-01 and POL-MEALS-01. q14 and q15 were already labeled the same way and were not changed.

## q42

- Decision: flag_for_review
- How labeled: hand-labeled from the system prompt (expected.py returned needs_manual_label)
- Difficulty: hard
- Why: The system prompt says "Call get_expense_details for the expense id in the request. If it is not on file, flag it for review." The message cites EXP-1999, which is not on file, so expected_sections is empty. The stored row EXP-1042 is a different record (solo beer). If the message had cited EXP-1042, POL-ALCOHOL-01 would deny it because "Alcohol is not reimbursable. That includes beer or wine the employee drinks alone, including before a flight." That deny is not this label.

## q43 — AMBIGUOUS

- Decision: AMBIGUOUS
- How labeled: not added to labels.jsonl
- Question: The message asks for EXP-1043 and EXP-1016 together. The system prompt says "You review one employee expense" and does not say whether to flag, review both, or pick one. expected.py would approve EXP-1043 on its own, because that lunch is 29.00 USD with a receipt and POL-MEALS-01 allows "up to 75.00 USD per person per day."

## q44 — AMBIGUOUS

- Decision: AMBIGUOUS
- How labeled: not added to labels.jsonl
- Question: The message asks whether the Friday demo lunch moved. It names no expense. The prompt says to flag when required information is missing, and it also assumes there is one expense to look up and a retrieved section to cite. If the stored row EXP-1044 had been the request, POL-HOME-01 would deny it because "Rent and decorations are not reimbursable." That deny is not what the employee asked.

## q45 — AMBIGUOUS

- Decision: AMBIGUOUS
- How labeled: not added to labels.jsonl
- Question: POL-AIRFARE-01 says "Buy the ticket at least 14 days before departure." This domestic economy fare is 500.00 USD and was booked 6 days ahead, so the lead time is present and short. The same section says "If the memo does not say whether the trip is domestic or international, or does not say how far ahead it was booked, flag the expense for a person to review." It does not say whether a stated late booking is a deny or a flag. expected.py returned needs_manual_label.
