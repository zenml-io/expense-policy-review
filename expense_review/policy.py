"""Synthetic Lumenfield Analytics expense policy.

Every figure and rule in this module is fictional. It is not a real
company's policy.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

# Primary unit cap applied by check_amount_limit to the submitted total.
# The policy text says what one unit is. The limit check does not divide
# by nights, attendees, or miles, and it does not apply exception rules.
CATEGORY_LIMITS: dict[str, Decimal] = {
    "meals": Decimal("75.00"),
    "client_entertainment": Decimal("150.00"),
    "alcohol": Decimal("40.00"),
    "airfare": Decimal("800.00"),
    "lodging": Decimal("250.00"),
    "ground_transport": Decimal("75.00"),
    "software": Decimal("50.00"),
    "gifts": Decimal("50.00"),
    "home_office": Decimal("300.00"),
}

RECEIPT_THRESHOLD = Decimal("25.00")

# Figures that live in the policy text. check_amount_limit does not apply them.
INTERNATIONAL_AIRFARE_CAP = Decimal("1800.00")
HIGH_COST_LODGING_CAP = Decimal("350.00")
AIRPORT_TRIP_CAP = Decimal("150.00")
MILEAGE_RATE_PER_MILE = Decimal("0.70")
MILEAGE_TRIP_CAP = Decimal("200.00")
INTERNET_MONTHLY_CAP = Decimal("50.00")
FURNITURE_APPROVAL_ABOVE = Decimal("150.00")
BOOKING_LEAD_DAYS = 14
HIGH_COST_CITY = "Port Selene"


@dataclass(frozen=True)
class PolicySection:
    """One labeled section of the synthetic policy."""

    id: str
    title: str
    text: str


def _usd(amount: Decimal) -> str:
    return f"{amount:.2f}"


def build_sections() -> tuple[PolicySection, ...]:
    """Return the synthetic policy sections in a stable order."""
    meals = _usd(CATEGORY_LIMITS["meals"])
    client = _usd(CATEGORY_LIMITS["client_entertainment"])
    alcohol = _usd(CATEGORY_LIMITS["alcohol"])
    airfare = _usd(CATEGORY_LIMITS["airfare"])
    international = _usd(INTERNATIONAL_AIRFARE_CAP)
    lodging = _usd(CATEGORY_LIMITS["lodging"])
    high_cost = _usd(HIGH_COST_LODGING_CAP)
    ground = _usd(CATEGORY_LIMITS["ground_transport"])
    airport = _usd(AIRPORT_TRIP_CAP)
    mileage_rate = _usd(MILEAGE_RATE_PER_MILE)
    mileage_cap = _usd(MILEAGE_TRIP_CAP)
    software = _usd(CATEGORY_LIMITS["software"])
    gifts = _usd(CATEGORY_LIMITS["gifts"])
    home = _usd(CATEGORY_LIMITS["home_office"])
    internet = _usd(INTERNET_MONTHLY_CAP)
    furniture = _usd(FURNITURE_APPROVAL_ABOVE)
    receipt = _usd(RECEIPT_THRESHOLD)

    return (
        PolicySection(
            id="POL-MEALS-01",
            title="Meals and per-diem",
            text=(
                f"Employees may claim a meal while working away from their home "
                f"office, up to {meals} USD per person per day. A claim of exactly "
                f"{meals} USD is within the cap. The cap applies to the total for "
                f"that person on that calendar day. "
                f"A per-diem of {meals} USD may be claimed instead of itemized "
                f"meals for a day with an overnight stay. Do not claim a per-diem "
                f"and an itemized meal for the same day. "
                f"Splitting one meal, one day, or one bill into more than one "
                f"submission so each part sits under {meals} USD is not allowed. "
                f"If the memo says the charge was split, or points at another "
                f"submission that is the other part of the same meal, flag the "
                f"expense for a person to review."
            ),
        ),
        PolicySection(
            id="POL-CLIENT-01",
            title="Client entertainment",
            text=(
                f"A meal or other entertainment with a client is allowed up to "
                f"{client} USD per attendee, including the employee, when the "
                f"memo names the client company and every attendee. A figure of "
                f"exactly {client} USD per attendee is within the cap. "
                f"If the memo does not name the client company or the attendees, "
                f"flag the expense for a person to review. Do not guess who "
                f"attended. This section does not allow alcohol. Alcohol follows "
                f"the alcohol section."
            ),
        ),
        PolicySection(
            id="POL-ALCOHOL-01",
            title="Alcohol",
            text=(
                "Alcohol is not reimbursable. That includes beer or wine the "
                "employee drinks alone, including before a flight. "
                f"Exception: beer or wine served at a client dinner may be claimed "
                f"up to {alcohol} USD per person, and only when Finance has already "
                f"approved that dinner in writing. A memo that says a manager "
                f"approved it is not written Finance approval. If the employee "
                f"claims the exception and the written approval is not in the "
                f"expense record, flag the expense for a person to review. Do not "
                f"approve the exception from the memo alone, and do not deny it "
                f"only because the memo is incomplete."
            ),
        ),
        PolicySection(
            id="POL-AIRFARE-01",
            title="Travel and airfare",
            text=(
                f"Airfare is reimbursable in an economy cabin only. The domestic "
                f"round-trip cap is {airfare} USD. The international round-trip cap "
                f"is {international} USD. A fare exactly at the cap that applies is "
                f"within the limit. Buy the ticket at least {BOOKING_LEAD_DAYS} days "
                f"before departure. If the memo does not say whether the trip is "
                f"domestic or international, or does not say how far ahead it was "
                f"booked, flag the expense for a person to review."
            ),
        ),
        PolicySection(
            id="POL-LODGING-01",
            title="Lodging",
            text=(
                f"Lodging is reimbursable up to {lodging} USD per night in a "
                f"standard city and {high_cost} USD per night in {HIGH_COST_CITY}. "
                f"A night priced exactly at the cap for that city is within the "
                f"limit. The cap is per night, not per stay. {HIGH_COST_CITY} is "
                f"the only high-cost city in this synthetic policy. Every other "
                f"city is standard. If the memo does not give the number of nights "
                f"or the city, flag the expense for a person to review instead of "
                f"treating the whole stay as one night."
            ),
        ),
        PolicySection(
            id="POL-GROUND-01",
            title="Ground transport and mileage",
            text=(
                f"A rideshare or taxi trip is reimbursable up to {ground} USD. A "
                f"trip to or from an airport is reimbursable up to {airport} USD. "
                f"A trip priced exactly at the cap that applies is within the "
                f"limit. Personal-car mileage is reimbursable at {mileage_rate} USD "
                f"per mile, up to {mileage_cap} USD per trip. The memo must state "
                f"the miles. If the miles are missing, flag the expense for a "
                f"person to review."
            ),
        ),
        PolicySection(
            id="POL-SOFTWARE-01",
            title="Software and subscriptions",
            text=(
                f"An individual software subscription is reimbursable up to "
                f"{software} USD per month. A subscription of exactly {software} USD "
                f"per month is within the cap. Divide an annual charge by 12 and "
                f"compare the result with {software} USD. If the memo does not say "
                f"whether the charge is monthly or annual, flag the expense for a "
                f"person to review. A team license, or any subscription above the "
                f"cap, needs a manager's written approval. If that approval is not "
                f"in the expense record, flag the expense for a person to review."
            ),
        ),
        PolicySection(
            id="POL-GIFTS-01",
            title="Gifts",
            text=(
                f"A gift for a client is reimbursable up to {gifts} USD per "
                f"recipient per calendar year. A gift of exactly {gifts} USD is "
                f"within the cap. Cash and gift cards are not reimbursable. A gift "
                f"for an employee is not reimbursable. If the memo does not name "
                f"the recipient, flag the expense for a person to review."
            ),
        ),
        PolicySection(
            id="POL-HOME-01",
            title="Home office",
            text=(
                f"A one-time home-office setup, such as a desk, chair, or lamp, is "
                f"reimbursable up to {home} USD when a receipt is attached. "
                f"Furniture priced above {furniture} USD also needs written "
                f"Facilities approval before purchase. If the employee says that "
                f"approval exists but it is not in the expense record, flag the "
                f"expense for a person to review. Home internet is reimbursable up "
                f"to {internet} USD per month. Rent and decorations are not "
                f"reimbursable."
            ),
        ),
        PolicySection(
            id="POL-RECEIPTS-01",
            title="Receipts",
            text=(
                f"A receipt is required when the amount is above {receipt} USD. An "
                f"amount of exactly {receipt} USD does not require a receipt. A "
                f"missing receipt above {receipt} USD is missing required "
                f"information: flag the expense for a person to review. Do not deny "
                f"an otherwise plausible expense only because the receipt is "
                f"missing, and do not approve it by assuming a receipt exists."
            ),
        ),
    )


SECTIONS: tuple[PolicySection, ...] = build_sections()
SECTIONS_BY_ID: dict[str, PolicySection] = {section.id: section for section in SECTIONS}


def render_policy_markdown() -> str:
    """Render the synthetic policy as markdown."""
    lines = [
        "# Lumenfield Analytics expense policy",
        "",
        "**Synthetic.** This document is fictional. It is not a real company's policy.",
        "",
        "Company: Lumenfield Analytics. Currency: USD. The figures below are demo data.",
        "",
    ]
    for section in SECTIONS:
        lines.append(f"## {section.id} — {section.title}")
        lines.append("")
        lines.append(section.text)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
