"""Synthetic employee expenses for the policy-review demo.

Every employee, merchant, and amount is fictional.
"""

from __future__ import annotations

EXPENSES: dict[str, dict[str, object]] = {
    "EXP-1001": {
        "expense_id": "EXP-1001",
        "employee": "Maya Ellison",
        "category": "meals",
        "amount": "42.50",
        "merchant": "Corner Deli",
        "date": "2026-03-04",
        "has_receipt": True,
        "memo": (
            "Lunch on a day away from the home office. No alcohol. "
            "No other meals claimed that day."
        ),
    },
    "EXP-1002": {
        "expense_id": "EXP-1002",
        "employee": "Chris Adelayo",
        "category": "meals",
        "amount": "120.00",
        "merchant": "The Oak Room",
        "date": "2026-03-05",
        "has_receipt": True,
        "memo": "Dinner while traveling. I ate alone. No other meals claimed that day.",
    },
    "EXP-1003": {
        "expense_id": "EXP-1003",
        "employee": "Priya Raman",
        "category": "meals",
        "amount": "75.00",
        "merchant": "Dayboard Cafe",
        "date": "2026-03-06",
        "has_receipt": True,
        "memo": (
            "Itemized meals for one day away from the home office. "
            "Total is the full day. No alcohol."
        ),
    },
    "EXP-1004": {
        "expense_id": "EXP-1004",
        "employee": "Jonah Peck",
        "category": "meals",
        "amount": "48.00",
        "merchant": "Noodle Bar",
        "date": "2026-03-07",
        "has_receipt": False,
        "memo": (
            "Dinner while traveling. I ate alone. The receipt was lost. "
            "No other meals claimed that day."
        ),
    },
    "EXP-1005": {
        "expense_id": "EXP-1005",
        "employee": "Elena Voss",
        "category": "meals",
        "amount": "70.00",
        "merchant": "Bistro Lane",
        "date": "2026-03-08",
        "has_receipt": True,
        "memo": (
            "Second submission for one dinner. I put the other part of the same "
            "bill on yesterday's expense so each submission stays under the daily cap."
        ),
    },
    "EXP-1006": {
        "expense_id": "EXP-1006",
        "employee": "Samir Qureshi",
        "category": "alcohol",
        "amount": "36.00",
        "merchant": "Harbor Wine",
        "date": "2026-03-09",
        "has_receipt": True,
        "memo": (
            "Wine during dinner with a client from Acme Robotics. "
            "My manager Dana said it was fine. Two people were there."
        ),
    },
    "EXP-1007": {
        "expense_id": "EXP-1007",
        "employee": "Nora Blake",
        "category": "alcohol",
        "amount": "22.00",
        "merchant": "Gatehouse Pub",
        "date": "2026-03-10",
        "has_receipt": True,
        "memo": "Two beers before a flight. No clients. I drank them alone.",
    },
    "EXP-1008": {
        "expense_id": "EXP-1008",
        "employee": "Theo Marchetti",
        "category": "client_entertainment",
        "amount": "140.00",
        "merchant": "Northwind Table",
        "date": "2026-03-11",
        "has_receipt": True,
        "memo": (
            "Dinner with Jordan Lee from Northwind Logistics. "
            "Attendees: Jordan Lee and me. No alcohol."
        ),
    },
    "EXP-1009": {
        "expense_id": "EXP-1009",
        "employee": "Helen Cho",
        "category": "airfare",
        "amount": "640.00",
        "merchant": "Northstar Air",
        "date": "2026-02-01",
        "has_receipt": True,
        "memo": (
            "Economy round trip from Redcedar to Halden. Domestic. "
            "Booked 21 days before departure."
        ),
    },
    "EXP-1010": {
        "expense_id": "EXP-1010",
        "employee": "Imani Brooks",
        "category": "lodging",
        "amount": "600.00",
        "merchant": "Redcedar Inn",
        "date": "2026-03-12",
        "has_receipt": True,
        "memo": "Three nights in Redcedar at 200.00 USD per night. Redcedar is not Port Selene.",
    },
    "EXP-1011": {
        "expense_id": "EXP-1011",
        "employee": "Felix Hart",
        "category": "ground_transport",
        "amount": "90.00",
        "merchant": "Cityloop Rides",
        "date": "2026-03-13",
        "has_receipt": True,
        "memo": "Rideshare across town to a client site. Not an airport trip.",
    },
    "EXP-1012": {
        "expense_id": "EXP-1012",
        "employee": "Grace Okada",
        "category": "home_office",
        "amount": "180.00",
        "merchant": "Desk World",
        "date": "2026-03-14",
        "has_receipt": True,
        "memo": (
            "Standing desk for my home office. I think Facilities approved it, "
            "but the approval email is not attached."
        ),
    },
    "EXP-1013": {
        "expense_id": "EXP-1013",
        "employee": "Luis Ferrer",
        "category": "gifts",
        "amount": "80.00",
        "merchant": "Gift Barn",
        "date": "2026-03-15",
        "has_receipt": True,
        "memo": "Gift basket for client Pat Okonkwo. One recipient.",
    },
    "EXP-1014": {
        "expense_id": "EXP-1014",
        "employee": "Wendy Cho",
        "category": "software",
        "amount": "42.00",
        "merchant": "Lumen Books",
        "date": "2026-03-16",
        "has_receipt": True,
        "memo": "Working dinner, pasta and sparkling water, while I read a manual. No alcohol.",
    },
    "EXP-1015": {
        "expense_id": "EXP-1015",
        "employee": "Omar Haddad",
        "category": "meals",
        "amount": "36.00",
        "merchant": "Northline Software",
        "date": "2026-03-17",
        "has_receipt": True,
        "memo": "Annual charge for a team whiteboard subscription, billed to my card.",
    },
}
