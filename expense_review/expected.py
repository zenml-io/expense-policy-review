"""Label helper for clear-cut expense decisions.

Not used by the agent, the tools, or scripts/run_queries.py.

``expected_decision`` returns ``approve``, ``flag_for_review``, or ``deny``
only when that result follows ``CATEGORY_LIMITS`` and ``RECEIPT_THRESHOLD``
the same way ``check_amount_limit`` does. The submitted total is compared
with the primary cap. A receipt is required only when the amount is above
the threshold. A total exactly at the cap is within the limit. An amount
exactly at the receipt threshold does not need a receipt.

It returns ``needs_manual_label`` when the written policy sends the case to
a person, or when the decision depends on a unit or exception the limit
check does not apply. That includes a split meal, any alcohol claim, a
client total above the primary cap, missing client or attendee names,
airfare that is not a stated domestic economy fare booked at least 14 days
ahead, lodging that is not one night in a standard city, airport trips,
mileage, software that is annual, a team license, above the monthly cap, or
silent on the billing period, gifts that are cash, a gift card, for an
employee, or unnamed, home-office rent, decorations, internet, and furniture
above the Facilities approval line or without a receipt, an unknown
category, and a memo that describes a different kind of purchase than the
category.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from decimal import Decimal

from expense_review.policy import (
    BOOKING_LEAD_DAYS,
    CATEGORY_LIMITS,
    FURNITURE_APPROVAL_ABOVE,
    HIGH_COST_CITY,
    RECEIPT_THRESHOLD,
)

NEEDS_MANUAL_LABEL = "needs_manual_label"

_SIGNALS: dict[str, tuple[str, ...]] = {
    "meals": ("lunch", "dinner", "breakfast", "meal", "meals", "pasta"),
    "alcohol": ("beer", "wine", "whiskey", "cocktail", "alcohol"),
    "client_entertainment": ("attendee", "attendees", "client"),
    "airfare": ("airfare", "flight", "round trip", "cabin"),
    "lodging": ("night", "nights", "hotel", "lodging"),
    "ground_transport": ("rideshare", "taxi", "mileage", "miles"),
    "software": ("subscription", "software", "license"),
    "gifts": ("gift",),
    "home_office": ("desk", "chair", "lamp", "furniture", "internet", "rent", "decoration"),
}
_ALCOHOL_WORDS = _SIGNALS["alcohol"]
_FURNITURE_WORDS = ("desk", "chair", "lamp", "furniture")


def expected_decision(expense: Mapping[str, object]) -> str:
    """Return the clear-cut decision, or ``needs_manual_label``."""
    category = _normalize_category(str(expense["category"]))
    amount = Decimal(str(expense["amount"])).quantize(Decimal("0.01"))
    has_receipt = expense["has_receipt"]
    memo = str(expense["memo"])
    if not isinstance(has_receipt, bool) or amount < 0 or category not in CATEGORY_LIMITS:
        return NEEDS_MANUAL_LABEL
    if _needs_manual_label(category, amount, memo, has_receipt):
        return NEEDS_MANUAL_LABEL

    limit = CATEGORY_LIMITS[category]
    if amount > limit:
        return "deny"
    if amount > RECEIPT_THRESHOLD and not has_receipt:
        return "flag_for_review"
    return "approve"


def _normalize_category(category: str) -> str:
    return category.strip().lower().replace("-", "_").replace(" ", "_")


def _has_phrase(text: str, phrase: str) -> bool:
    return re.search(rf"\b{re.escape(phrase)}\b", text) is not None


def _scrub(memo: str) -> str:
    return re.sub(r"\bno alcohol\b", " ", memo.lower())


def _has_alcohol(memo: str) -> bool:
    scrubbed = _scrub(memo)
    return any(_has_phrase(scrubbed, word) for word in _ALCOHOL_WORDS)


def _mismatch(category: str, scrubbed: str) -> bool:
    own = _SIGNALS.get(category, ())
    if any(_has_phrase(scrubbed, phrase) for phrase in own):
        return False
    for other, phrases in _SIGNALS.items():
        if other == category:
            continue
        if any(_has_phrase(scrubbed, phrase) for phrase in phrases):
            return True
    return False


def _nights(text: str) -> int | None:
    if re.search(r"\bone\s+night\b", text):
        return 1
    match = re.search(r"\b(\d+)\s+nights?\b", text)
    if match is None:
        return None
    return int(match.group(1))


def _needs_manual_label(
    category: str,
    amount: Decimal,
    memo: str,
    has_receipt: bool,
) -> bool:
    lower = memo.lower()
    if _mismatch(category, _scrub(memo)):
        return True
    if category == "meals":
        return _meals_manual(memo)
    if category == "alcohol":
        return True
    if category == "client_entertainment":
        return _client_manual(memo, amount)
    if category == "airfare":
        return _airfare_manual(lower)
    if category == "lodging":
        return _lodging_manual(memo)
    if category == "ground_transport":
        return _ground_manual(lower)
    if category == "software":
        return _software_manual(lower, amount)
    if category == "gifts":
        return _gifts_manual(memo)
    if category == "home_office":
        return _home_manual(lower, amount, has_receipt)
    return True


def _meals_manual(memo: str) -> bool:
    scrubbed = _scrub(memo)
    if _has_phrase(scrubbed, "split") or "other part of the same" in scrubbed:
        return True
    if _has_alcohol(memo):
        return True
    per_diem = _has_phrase(scrubbed, "per-diem") or _has_phrase(scrubbed, "per diem")
    itemized = any(
        _has_phrase(scrubbed, word) for word in ("itemized", "lunch", "dinner", "breakfast")
    )
    return per_diem and itemized


def _client_manual(memo: str, amount: Decimal) -> bool:
    lower = memo.lower()
    if amount > CATEGORY_LIMITS["client_entertainment"]:
        return True
    if "attendees:" not in lower or " from " not in lower:
        return True
    if "no alcohol" not in lower or _has_alcohol(memo):
        return True
    return False


def _airfare_manual(lower: str) -> bool:
    if "international" in lower or "domestic" not in lower:
        return True
    if "economy" not in lower or "business" in lower or "first class" in lower:
        return True
    match = re.search(r"\bbooked\s+(\d+)\s+days\b", lower)
    if match is None:
        return True
    return int(match.group(1)) < BOOKING_LEAD_DAYS


def _lodging_manual(memo: str) -> bool:
    if HIGH_COST_CITY.lower() in memo.lower():
        return True
    if _nights(memo.lower()) != 1:
        return True
    return re.search(r"\bin [A-Z][a-z]+", memo) is None


def _ground_manual(lower: str) -> bool:
    if re.search(r"\bmiles?\b", lower) or "mileage" in lower:
        return True
    if "airport" in lower and "not an airport" not in lower and "not airport" not in lower:
        return True
    return not (_has_phrase(lower, "rideshare") or _has_phrase(lower, "taxi"))


def _software_manual(lower: str, amount: Decimal) -> bool:
    if any(_has_phrase(lower, word) for word in ("team", "annual", "manager")):
        return True
    if not (_has_phrase(lower, "monthly") or _has_phrase(lower, "per month")):
        return True
    return amount > CATEGORY_LIMITS["software"]


def _gifts_manual(memo: str) -> bool:
    lower = memo.lower()
    if "gift card" in lower or re.search(r"\bcash\b", lower):
        return True
    if re.search(r"\b(?:employee|coworker|colleague)\b", lower):
        return True
    return re.search(r"\bfor client [A-Z][a-z]+ [A-Z][a-z]+\b", memo) is None


def _home_manual(lower: str, amount: Decimal, has_receipt: bool) -> bool:
    if "rent" in lower or "decoration" in lower or "internet" in lower:
        return True
    furniture = any(_has_phrase(lower, word) for word in _FURNITURE_WORDS)
    if not furniture:
        return True
    if amount > FURNITURE_APPROVAL_ABOVE or not has_receipt:
        return True
    return False
