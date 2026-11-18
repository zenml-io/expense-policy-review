"""Tests for the deterministic expense tools. No model calls and no network."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from expense_review.expected import NEEDS_MANUAL_LABEL, expected_decision
from expense_review.expenses import EXPENSES
from expense_review.policy import SECTIONS_BY_ID, render_policy_markdown
from expense_review.tools import check_amount_limit, get_expense_details, search_policy

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = {"approve", "flag_for_review", "deny"}
DIFFICULTIES = {"easy", "medium", "hard"}
AMBIGUOUS_QUERY_IDS = {"q43", "q44", "q45"}
UNKNOWN_EXPENSE_ID = "EXP-1999"
ORIGINAL_QUERY_COUNT = 15


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


def _load_jsonl(name: str) -> list[dict]:
    return [
        json.loads(line)
        for line in (ROOT / name).read_text().splitlines()
        if line.strip()
    ]


def _expense(**fields: object) -> dict[str, object]:
    base: dict[str, object] = {
        "category": "meals",
        "amount": "40.00",
        "has_receipt": True,
        "memo": "Lunch while working away from the home office. No alcohol.",
    }
    base.update(fields)
    return base


def test_queries_and_labels_stay_separate() -> None:
    queries = _load_jsonl("queries.jsonl")
    labels = _load_jsonl("labels.jsonl")
    assert [row["id"] for row in queries[:ORIGINAL_QUERY_COUNT]] == [
        row["id"] for row in labels[:ORIGINAL_QUERY_COUNT]
    ]
    assert [row["id"] for row in queries[:ORIGINAL_QUERY_COUNT]] == [
        f"q{number:02d}" for number in range(1, ORIGINAL_QUERY_COUNT + 1)
    ]

    for query in queries:
        assert set(query) == {"id", "expense_id", "message"}
        assert query["expense_id"] in EXPENSES
        assert "expected_decision" not in query
        assert "expected_sections" not in query
        if query["id"] != "q42":
            assert query["expense_id"] in query["message"]

    labeled = {label["id"]: label for label in labels}
    for label in labels:
        assert set(label) == {"id", "expected_decision", "expected_sections", "difficulty"}
        assert label["expected_decision"] in DECISIONS
        assert label["difficulty"] in DIFFICULTIES
        if label["id"] == "q42":
            assert label["expected_sections"] == []
        else:
            assert label["expected_sections"]
        for section_id in label["expected_sections"]:
            assert section_id in SECTIONS_BY_ID
    assert labeled["q01"]["expected_decision"] == "approve"
    assert labeled["q15"]["expected_decision"] == "flag_for_review"


def test_dataset_ids_labels_and_expected_decisions() -> None:
    queries = _load_jsonl("queries.jsonl")
    pending = _load_jsonl("queries_pending.jsonl")
    labels = _load_jsonl("labels.jsonl")
    notes = (ROOT / "label_notes.md").read_text()
    ambiguous = set(re.findall(r"^## (q\d+) — AMBIGUOUS$", notes, re.M))
    headings = re.findall(r"^## (q\d+)\b", notes, re.M)

    assert ambiguous == AMBIGUOUS_QUERY_IDS
    assert headings == [f"q{number:02d}" for number in range(16, 46)]
    for query_id in ambiguous:
        section = notes.split(f"## {query_id} — AMBIGUOUS", 1)[1].split("\n## ", 1)[0]
        assert "Question:" in section
    assert "queries_pending.jsonl" in notes

    query_ids = [query["id"] for query in queries]
    pending_ids = [query["id"] for query in pending]
    label_ids = [label["id"] for label in labels]
    expense_ids = list(EXPENSES)
    assert len(query_ids) == len(set(query_ids)) == 42
    assert query_ids == label_ids
    assert len(label_ids) == len(set(label_ids))
    assert pending_ids == ["q43", "q44", "q45"]
    assert set(pending_ids).isdisjoint(label_ids)
    assert set(pending_ids) == ambiguous
    assert len(expense_ids) == len(set(expense_ids))
    assert query_ids == [f"q{number:02d}" for number in range(1, 43)]
    assert expense_ids == [f"EXP-{number}" for number in range(1001, 1046)]
    assert UNKNOWN_EXPENSE_ID not in EXPENSES

    for query in pending:
        assert set(query) == {"id", "expense_id", "message"}
        assert query["expense_id"] in EXPENSES
        assert "expected_decision" not in query

    labels_by_id = {label["id"]: label for label in labels}
    new_labels = [labels_by_id[f"q{number:02d}"] for number in range(16, 43)]
    decisions = [label["expected_decision"] for label in new_labels]
    assert decisions.count("approve") == 11
    assert decisions.count("flag_for_review") == 8
    assert decisions.count("deny") == 8
    section_counts: Counter[str] = Counter()
    for label in new_labels:
        section_counts.update(label["expected_sections"])
    for section_id in SECTIONS_BY_ID:
        assert section_counts[section_id] >= 2

    for query in pending:
        referenced = set(re.findall(r"EXP-\d+", query["message"]))
        if query["id"] == "q44":
            assert referenced == set()
            continue
        assert query["expense_id"] in referenced
        assert referenced <= set(EXPENSES)

    for query in queries:
        referenced = set(re.findall(r"EXP-\d+", query["message"]))
        if query["id"] == "q42":
            assert referenced == {UNKNOWN_EXPENSE_ID}
            continue
        assert query["expense_id"] in referenced
        assert referenced <= set(EXPENSES)

        decision = expected_decision(EXPENSES[query["expense_id"]])
        if decision != NEEDS_MANUAL_LABEL:
            assert labels_by_id[query["id"]]["expected_decision"] == decision
            limit_check = check_amount_limit(
                str(EXPENSES[query["expense_id"]]["category"]),
                EXPENSES[query["expense_id"]]["amount"],
                bool(EXPENSES[query["expense_id"]]["has_receipt"]),
            )
            if decision == "approve":
                assert limit_check["within_limit"] is True
                assert limit_check["receipt_ok"] is True
            elif decision == "deny":
                assert limit_check["within_limit"] is False
            else:
                assert limit_check["within_limit"] is True
                assert limit_check["receipt_ok"] is False


def test_expected_decision_matches_known_records() -> None:
    assert expected_decision(EXPENSES["EXP-1001"]) == "approve"
    assert expected_decision(EXPENSES["EXP-1002"]) == "deny"
    assert expected_decision(EXPENSES["EXP-1003"]) == "approve"
    assert expected_decision(EXPENSES["EXP-1004"]) == "flag_for_review"
    assert expected_decision(EXPENSES["EXP-1005"]) == NEEDS_MANUAL_LABEL
    assert expected_decision(EXPENSES["EXP-1008"]) == "approve"
    assert expected_decision(EXPENSES["EXP-1009"]) == "approve"
    assert expected_decision(EXPENSES["EXP-1010"]) == NEEDS_MANUAL_LABEL
    assert expected_decision(EXPENSES["EXP-1011"]) == "deny"
    assert expected_decision(EXPENSES["EXP-1013"]) == "deny"
    assert expected_decision(EXPENSES["EXP-1014"]) == NEEDS_MANUAL_LABEL
    assert expected_decision(EXPENSES["EXP-1015"]) == NEEDS_MANUAL_LABEL
    assert expected_decision(EXPENSES["EXP-1042"]) == NEEDS_MANUAL_LABEL
    assert expected_decision(EXPENSES["EXP-1043"]) == "approve"
    assert expected_decision(EXPENSES["EXP-1044"]) == NEEDS_MANUAL_LABEL
    assert expected_decision(EXPENSES["EXP-1045"]) == NEEDS_MANUAL_LABEL


def test_expected_decision_cap_and_receipt_rules() -> None:
    assert expected_decision(_expense(amount="75.00")) == "approve"
    assert expected_decision(_expense(amount="75.01")) == "deny"
    assert expected_decision(_expense(amount="25.00", has_receipt=False)) == "approve"
    assert expected_decision(_expense(amount="25.01", has_receipt=False)) == "flag_for_review"
    assert (
        expected_decision(_expense(memo="I split one dinner across two submissions."))
        == NEEDS_MANUAL_LABEL
    )
    assert expected_decision(_expense(category="pet care")) == NEEDS_MANUAL_LABEL
    assert (
        expected_decision(
            _expense(
                category="software",
                amount="80.00",
                memo="Individual monthly subscription for a notes app.",
            )
        )
        == NEEDS_MANUAL_LABEL
    )
    assert (
        expected_decision(
            _expense(
                category="alcohol",
                amount="10.00",
                memo="A glass of wine. I drank it alone. No clients.",
            )
        )
        == NEEDS_MANUAL_LABEL
    )


def test_runner_and_agent_do_not_read_labels_or_expected() -> None:
    agent = (ROOT / "expense_review" / "agent.py").read_text()
    tools = (ROOT / "expense_review" / "tools.py").read_text()
    runner = (ROOT / "scripts" / "run_queries.py").read_text()
    for source in (agent, tools, runner):
        assert "expense_review.expected" not in source
        assert "import expected" not in source
        assert "label_notes" not in source
    assert "labels.jsonl" not in agent
    assert "labels.jsonl" not in tools
    assert runner.count("labels.jsonl") == 1
    assert "does not read labels.jsonl" in runner
    assert 'ROOT / "queries.jsonl"' in runner
    assert "labels.jsonl" not in runner.replace("does not read labels.jsonl", "")


def test_runner_does_not_read_pending_queries() -> None:
    runner = (ROOT / "scripts" / "run_queries.py").read_text()
    assert "queries_pending.jsonl" not in runner
    assert 'ROOT / "queries.jsonl"' in runner


def test_original_expenses_are_unchanged() -> None:
    assert EXPENSES["EXP-1001"]["employee"] == "Maya Ellison"
    assert EXPENSES["EXP-1001"]["amount"] == "42.50"
    assert EXPENSES["EXP-1002"]["amount"] == "120.00"
    assert EXPENSES["EXP-1005"]["memo"] == (
        "Second submission for one dinner. I put the other part of the same "
        "bill on yesterday's expense so each submission stays under the daily cap."
    )
    assert EXPENSES["EXP-1014"]["category"] == "software"
    assert EXPENSES["EXP-1015"]["category"] == "meals"
    assert EXPENSES["EXP-1015"]["memo"] == (
        "Annual charge for a team whiteboard subscription, billed to my card."
    )
    assert len(EXPENSES) == 45
