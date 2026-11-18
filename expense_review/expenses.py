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
    "EXP-1016": {
        "expense_id": "EXP-1016",
        "employee": "Adele Krantz",
        "category": "meals",
        "amount": "38.00",
        "merchant": "Pebble Soup",
        "date": "2026-03-18",
        "has_receipt": True,
        "memo": (
            "Lunch while working away from the home office. No alcohol. "
            "No other meals claimed that day."
        ),
    },
    "EXP-1017": {
        "expense_id": "EXP-1017",
        "employee": "Benito Salazar",
        "category": "meals",
        "amount": "75.00",
        "merchant": "Northpantry",
        "date": "2026-03-19",
        "has_receipt": True,
        "memo": (
            "Itemized meals for one day away from the home office. "
            "The total is the full day. No alcohol."
        ),
    },
    "EXP-1018": {
        "expense_id": "EXP-1018",
        "employee": "Camille Frost",
        "category": "meals",
        "amount": "25.00",
        "merchant": "Little Kettle",
        "date": "2026-03-20",
        "has_receipt": False,
        "memo": (
            "Lunch while working away from the home office. No alcohol. "
            "No other meals claimed that day."
        ),
    },
    "EXP-1019": {
        "expense_id": "EXP-1019",
        "employee": "Derek Nunez",
        "category": "ground_transport",
        "amount": "75.00",
        "merchant": "Harborline Rides",
        "date": "2026-03-21",
        "has_receipt": True,
        "memo": "Rideshare across town to a client site. Not an airport trip.",
    },
    "EXP-1020": {
        "expense_id": "EXP-1020",
        "employee": "Farah Siddiqui",
        "category": "airfare",
        "amount": "540.00",
        "merchant": "Redcedar Air",
        "date": "2026-03-22",
        "has_receipt": True,
        "memo": (
            "Economy round trip from Redcedar to Halden. Domestic. "
            "Booked 21 days before departure."
        ),
    },
    "EXP-1021": {
        "expense_id": "EXP-1021",
        "employee": "Gavin Holt",
        "category": "airfare",
        "amount": "800.00",
        "merchant": "Halden Air",
        "date": "2026-03-23",
        "has_receipt": True,
        "memo": (
            "Economy round trip from Redcedar to Halden. Domestic. "
            "Booked 30 days before departure."
        ),
    },
    "EXP-1022": {
        "expense_id": "EXP-1022",
        "employee": "Hanae Mori",
        "category": "lodging",
        "amount": "250.00",
        "merchant": "Redcedar House",
        "date": "2026-03-24",
        "has_receipt": True,
        "memo": "One night in Redcedar, a standard city.",
    },
    "EXP-1023": {
        "expense_id": "EXP-1023",
        "employee": "Ivan Petrescu",
        "category": "lodging",
        "amount": "320.00",
        "merchant": "Selene House",
        "date": "2026-03-25",
        "has_receipt": True,
        "memo": "One night in Port Selene at 320.00 USD.",
    },
    "EXP-1024": {
        "expense_id": "EXP-1024",
        "employee": "Jules Adebayo",
        "category": "software",
        "amount": "50.00",
        "merchant": "Noteleaf",
        "date": "2026-03-26",
        "has_receipt": True,
        "memo": "Individual monthly subscription for a note-taking app.",
    },
    "EXP-1025": {
        "expense_id": "EXP-1025",
        "employee": "Kira Lang",
        "category": "gifts",
        "amount": "50.00",
        "merchant": "Bindery Lane",
        "date": "2026-03-27",
        "has_receipt": True,
        "memo": "Gift of a book for client Rosa Melendez. One recipient.",
    },
    "EXP-1026": {
        "expense_id": "EXP-1026",
        "employee": "Mateo Solano",
        "category": "client_entertainment",
        "amount": "240.00",
        "merchant": "Bramble Table",
        "date": "2026-03-28",
        "has_receipt": True,
        "memo": (
            "Dinner with Priya Shah from Bramble Health. "
            "Attendees: Priya Shah and me. No alcohol."
        ),
    },
    "EXP-1027": {
        "expense_id": "EXP-1027",
        "employee": "Nia Brennan",
        "category": "meals",
        "amount": "96.40",
        "merchant": "Cedar Supper",
        "date": "2026-03-29",
        "has_receipt": True,
        "memo": "Dinner while traveling. I ate alone. No other meals claimed that day.",
    },
    "EXP-1028": {
        "expense_id": "EXP-1028",
        "employee": "Oscar Pell",
        "category": "meals",
        "amount": "118.00",
        "merchant": "Lateplate",
        "date": "2026-03-30",
        "has_receipt": True,
        "memo": "Dinner while traveling. I ate alone. No other meals claimed that day.",
    },
    "EXP-1029": {
        "expense_id": "EXP-1029",
        "employee": "Pauline Greer",
        "category": "ground_transport",
        "amount": "88.00",
        "merchant": "Southloop Rides",
        "date": "2026-03-31",
        "has_receipt": True,
        "memo": "Rideshare across town to a client site. Not an airport trip.",
    },
    "EXP-1030": {
        "expense_id": "EXP-1030",
        "employee": "Quentin Walsh",
        "category": "gifts",
        "amount": "62.00",
        "merchant": "Parcel and Twine",
        "date": "2026-04-01",
        "has_receipt": True,
        "memo": "Gift basket for client Lila Navarro. One recipient.",
    },
    "EXP-1031": {
        "expense_id": "EXP-1031",
        "employee": "Rosa Ibarra",
        "category": "alcohol",
        "amount": "18.00",
        "merchant": "Runway Bar",
        "date": "2026-04-02",
        "has_receipt": True,
        "memo": "A glass of wine before a flight. No clients. I drank it alone.",
    },
    "EXP-1032": {
        "expense_id": "EXP-1032",
        "employee": "Stefan Vogel",
        "category": "gifts",
        "amount": "40.00",
        "merchant": "Card Counter",
        "date": "2026-04-03",
        "has_receipt": True,
        "memo": "Gift card for client Nia Chen. One recipient.",
    },
    "EXP-1033": {
        "expense_id": "EXP-1033",
        "employee": "Talia Nguyen",
        "category": "home_office",
        "amount": "1400.00",
        "merchant": "Westlease Apartments",
        "date": "2026-04-04",
        "has_receipt": True,
        "memo": "Monthly apartment rent while I worked from home.",
    },
    "EXP-1034": {
        "expense_id": "EXP-1034",
        "employee": "Uma Deshpande",
        "category": "airfare",
        "amount": "940.00",
        "merchant": "Lumen Air",
        "date": "2026-04-05",
        "has_receipt": True,
        "memo": (
            "Economy round trip from Redcedar to Halden. Domestic. "
            "Booked 21 days before departure."
        ),
    },
    "EXP-1035": {
        "expense_id": "EXP-1035",
        "employee": "Victor Langston",
        "category": "meals",
        "amount": "46.00",
        "merchant": "Soup Window",
        "date": "2026-04-06",
        "has_receipt": False,
        "memo": (
            "Lunch while traveling. I ate alone. The receipt was lost. "
            "No other meals claimed that day."
        ),
    },
    "EXP-1036": {
        "expense_id": "EXP-1036",
        "employee": "Willa Park",
        "category": "meals",
        "amount": "55.00",
        "merchant": "Second Seating",
        "date": "2026-04-07",
        "has_receipt": True,
        "memo": (
            "Second submission for one dinner. I split the bill so this part "
            "sits under the daily cap."
        ),
    },
    "EXP-1037": {
        "expense_id": "EXP-1037",
        "employee": "Xavier Bloom",
        "category": "alcohol",
        "amount": "32.00",
        "merchant": "Clinic Table",
        "date": "2026-04-08",
        "has_receipt": True,
        "memo": (
            "Wine at a client dinner with Amos Reed from Hearthline Clinics. "
            "My manager Cole said it was fine. Attendees: Amos Reed and me. "
            "Finance approval is not in the expense record."
        ),
    },
    "EXP-1038": {
        "expense_id": "EXP-1038",
        "employee": "Yasmin Darwish",
        "category": "client_entertainment",
        "amount": "90.00",
        "merchant": "Unnamed Grill",
        "date": "2026-04-09",
        "has_receipt": True,
        "memo": (
            "Took a customer out for a conversation. I do not have the company "
            "name or the attendee list."
        ),
    },
    "EXP-1039": {
        "expense_id": "EXP-1039",
        "employee": "Zeke Holloway",
        "category": "software",
        "amount": "36.00",
        "merchant": "Stacklicense",
        "date": "2026-04-10",
        "has_receipt": True,
        "memo": (
            "Team license for a design tool, billed monthly. My manager said "
            "it was fine. Written approval is not in the expense record."
        ),
    },
    "EXP-1040": {
        "expense_id": "EXP-1040",
        "employee": "Anika Bose",
        "category": "home_office",
        "amount": "220.00",
        "merchant": "Upright Desk Co",
        "date": "2026-04-11",
        "has_receipt": True,
        "memo": (
            "Standing desk for my home office. Facilities approved it, but "
            "that email is not in the expense record."
        ),
    },
    "EXP-1041": {
        "expense_id": "EXP-1041",
        "employee": "Bruno Keller",
        "category": "software",
        "amount": "37.00",
        "merchant": "Slice Counter",
        "date": "2026-04-12",
        "has_receipt": True,
        "memo": "Pizza dinner while I was traveling. I ate alone. No alcohol.",
    },
    "EXP-1042": {
        "expense_id": "EXP-1042",
        "employee": "Celeste Marin",
        "category": "alcohol",
        "amount": "16.00",
        "merchant": "Hotel Tap",
        "date": "2026-04-13",
        "has_receipt": True,
        "memo": "A beer at the hotel bar. No clients. I drank it alone.",
    },
    "EXP-1043": {
        "expense_id": "EXP-1043",
        "employee": "Dario Esposito",
        "category": "meals",
        "amount": "29.00",
        "merchant": "Trail Lunch",
        "date": "2026-04-14",
        "has_receipt": True,
        "memo": (
            "Lunch while working away from the home office. No alcohol. "
            "No other meals claimed that day."
        ),
    },
    "EXP-1044": {
        "expense_id": "EXP-1044",
        "employee": "Esther Feldman",
        "category": "home_office",
        "amount": "45.00",
        "merchant": "Paper Lantern",
        "date": "2026-04-15",
        "has_receipt": True,
        "memo": "Wall decorations for my home office.",
    },
    "EXP-1045": {
        "expense_id": "EXP-1045",
        "employee": "Finn Gallagher",
        "category": "airfare",
        "amount": "500.00",
        "merchant": "Latefare Air",
        "date": "2026-04-16",
        "has_receipt": True,
        "memo": (
            "Economy round trip from Redcedar to Halden. Domestic. "
            "Booked 6 days before departure."
        ),
    },
}
