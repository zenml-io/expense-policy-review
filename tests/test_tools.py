"""Tests for the deterministic expense tools. No model calls and no network."""

from __future__ import annotations

import json
from pathlib import Path

from expense_review.expenses import EXPENSES
from expense_review.policy import SECTIONS_BY_ID, render_policy_markdown
from expense_review.tools import check_amount_limit, get_expense_details, search_policy

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = {"approve", "flag_for_review", "deny"}
DIFFICULTIES = {"easy", "medium", "hard"}


def test_check_amount_limit_exact_meal_cap_with_receipt() -> None:
    result = check_amount_limit("meals", "75.00", True)
    assert result == {
        "within_limit": True,
        "limit": "75.00",
        "receipt_required": True,
        "receipt_ok": True,
    }


def test_check_amount_limit_over_cap_and_receipt_boundary() -> None:
    over = check_amount_limit("meals", "75.01", True)
    assert over["within_limit"] is False
    assert over["limit"] == "75.00"

    at_threshold = check_amount_limit("Meals", "25.00", False)
    assert at_threshold["within_limit"] is True
    assert at_threshold["receipt_required"] is False
    assert at_threshold["receipt_ok"] is True

    above_threshold = check_amount_limit("meals", "25.01", False)
    assert above_threshold["receipt_required"] is True
    assert above_threshold["receipt_ok"] is False


def test_check_amount_limit_uses_the_category_cap() -> None:
    gifts = check_amount_limit("gifts", "50.00", True)
    assert gifts["within_limit"] is True
    assert gifts["limit"] == "50.00"
    assert check_amount_limit("gifts", "50.01", True)["within_limit"] is False


def test_check_amount_limit_unknown_category() -> None:
    result = check_amount_limit("pet care", "40.00", False)
    assert result["within_limit"] is False
    assert result["limit"] is None
    assert result["receipt_required"] is True
    assert result["receipt_ok"] is False


def test_search_policy_mileage_hits_ground_section() -> None:
    hits = search_policy("personal car mileage rate")
    assert hits
    assert hits[0]["id"] == "POL-GROUND-01"
    assert "mileage" in hits[0]["text"]


def test_search_policy_returns_at_most_three_and_can_miss() -> None:
    broad = search_policy("meal alcohol gift lodging software mileage")
    assert len(broad) == 3
    assert search_policy("whiteboard") == []
    assert search_policy("uber lyft") == []


def test_get_expense_details_known_and_unknown() -> None:
    found = get_expense_details("EXP-1001")
    assert found["found"] is True
    assert found["employee"] == "Maya Ellison"
    assert found["category"] == "meals"
    assert found["amount"] == "42.50"
    assert found["has_receipt"] is True

    missing = get_expense_details("EXP-9999")
    assert missing == {"found": False, "expense_id": "EXP-9999"}
    assert "EXP-9999" not in EXPENSES


def test_policy_markdown_matches_source() -> None:
    assert (ROOT / "policy.md").read_text() == render_policy_markdown()
    for section_id in SECTIONS_BY_ID:
        assert section_id in (ROOT / "policy.md").read_text()


def test_queries_and_labels_stay_separate() -> None:
    queries = [
        json.loads(line)
        for line in (ROOT / "queries.jsonl").read_text().splitlines()
        if line.strip()
    ]
    labels = [
        json.loads(line)
        for line in (ROOT / "labels.jsonl").read_text().splitlines()
        if line.strip()
    ]
    assert len(queries) == 15
    assert [row["id"] for row in queries] == [row["id"] for row in labels]

    for query in queries:
        assert set(query) == {"id", "expense_id", "message"}
        assert query["expense_id"] in query["message"]
        assert query["expense_id"] in EXPENSES
        assert "expected_decision" not in query
        assert "expected_sections" not in query

    for label in labels:
        assert set(label) == {"id", "expected_decision", "expected_sections", "difficulty"}
        assert label["expected_decision"] in DECISIONS
        assert label["difficulty"] in DIFFICULTIES
        assert label["expected_sections"]
        for section_id in label["expected_sections"]:
            assert section_id in SECTIONS_BY_ID
