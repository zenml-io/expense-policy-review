"""Deterministic tools for the synthetic expense review.

None of these functions call a model.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Any

from expense_review.expenses import EXPENSES
from expense_review.policy import CATEGORY_LIMITS, RECEIPT_THRESHOLD, SECTIONS

DECISIONS = ("approve", "flag_for_review", "deny")

_STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "for",
        "from",
        "if",
        "in",
        "is",
        "it",
        "of",
        "on",
        "or",
        "per",
        "that",
        "the",
        "this",
        "to",
        "up",
        "usd",
        "when",
        "with",
    }
)
_TOKEN = re.compile(r"[a-z0-9]+")


@dataclass
class ReviewLog:
    """In-memory record of decisions and human-review routes for one agent."""

    decisions: list[dict[str, Any]] = field(default_factory=list)
    flags: list[dict[str, Any]] = field(default_factory=list)

    def clear(self) -> None:
        self.decisions.clear()
        self.flags.clear()


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in _TOKEN.findall(text.lower())
        if len(token) >= 3 and token not in _STOPWORDS
    }


def search_policy(query: str) -> list[dict[str, str]]:
    """Return up to three policy sections by keyword overlap.

    Scoring is exact tokens only, with no stemming. A query can miss the
    section a person would have picked.
    """
    query_tokens = _tokens(query)
    if not query_tokens:
        return []

    ranked: list[tuple[int, str, dict[str, str]]] = []
    for section in SECTIONS:
        title_tokens = _tokens(section.title)
        id_tokens = _tokens(section.id.replace("-", " "))
        body_tokens = _tokens(section.text)
        score = 0
        for token in query_tokens:
            if token in title_tokens or token in id_tokens:
                score += 3
            elif token in body_tokens:
                score += 1
        if score > 0:
            ranked.append(
                (
                    score,
                    section.id,
                    {"id": section.id, "title": section.title, "text": section.text},
                )
            )

    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [item[2] for item in ranked[:3]]


def get_expense_details(expense_id: str) -> dict[str, Any]:
    """Return one synthetic expense, or a not-found record."""
    record = EXPENSES.get(expense_id)
    if record is None:
        return {"found": False, "expense_id": expense_id}
    return {"found": True, **record}


def _money(amount: Any) -> Decimal:
    try:
        value = Decimal(str(amount))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"amount is not a number: {amount!r}") from exc
    if value < 0:
        raise ValueError("amount must be zero or positive")
    return value.quantize(Decimal("0.01"))


def _normalize_category(category: str) -> str:
    return category.strip().lower().replace("-", "_").replace(" ", "_")


def check_amount_limit(category: str, amount: Any, has_receipt: bool) -> dict[str, Any]:
    """Compare a submitted total with the category's primary unit cap.

    ``within_limit`` is true when the total is less than or equal to that cap.
    The cap is not divided by nights, attendees, or miles. Receipts are
    required only when the amount is above the policy threshold. An unknown
    category returns ``limit`` null and ``within_limit`` false.
    """
    if not isinstance(has_receipt, bool):
        raise TypeError("has_receipt must be a bool")

    value = _money(amount)
    receipt_required = value > RECEIPT_THRESHOLD
    receipt_ok = (not receipt_required) or has_receipt
    normalized = _normalize_category(category)
    limit = CATEGORY_LIMITS.get(normalized)
    if limit is None:
        return {
            "within_limit": False,
            "limit": None,
            "receipt_required": receipt_required,
            "receipt_ok": receipt_ok,
        }

    return {
        "within_limit": value <= limit,
        "limit": f"{limit:.2f}",
        "receipt_required": receipt_required,
        "receipt_ok": receipt_ok,
    }


def _section_ids(cited_sections: list[str] | str) -> list[str]:
    if isinstance(cited_sections, str):
        parts = cited_sections.split(",")
    else:
        parts = [str(part) for part in cited_sections]
    return [part.strip() for part in parts if part.strip()]


def recommend_decision(
    expense_id: str,
    decision: str,
    reason: str,
    cited_sections: list[str] | str,
    log: ReviewLog | None = None,
) -> dict[str, Any]:
    """Record the final decision. Does not change the decision."""
    if decision not in DECISIONS:
        allowed = ", ".join(DECISIONS)
        raise ValueError(f"decision must be one of: {allowed}")
    if not reason or not str(reason).strip():
        raise ValueError("reason is required")

    record = {
        "expense_id": expense_id,
        "decision": decision,
        "reason": str(reason).strip(),
        "cited_sections": _section_ids(cited_sections),
    }
    if log is not None:
        log.decisions.append(dict(record))
    return record


def flag_for_review(
    expense_id: str,
    reason: str,
    log: ReviewLog | None = None,
) -> dict[str, Any]:
    """Route an expense to a person. Does not decide approve or deny."""
    if not reason or not str(reason).strip():
        raise ValueError("reason is required")

    record = {
        "expense_id": expense_id,
        "reason": str(reason).strip(),
        "routed_to": "human_review",
    }
    if log is not None:
        log.flags.append(dict(record))
    return record
