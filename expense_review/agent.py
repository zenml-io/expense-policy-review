"""LangGraph expense-policy review agent.

Traces are attached by the caller. This module does not talk to Langfuse.
Policy text and expenses are synthetic.
"""

from __future__ import annotations

import os
from typing import Any

from langchain.agents import create_agent
from langchain_core.tools import tool

import expense_review.tools as tool_impl
from expense_review.tools import ReviewLog

DEFAULT_MODEL = "gpt-5-nano"

SYSTEM_PROMPT = """You review one employee expense against the Lumenfield Analytics expense policy.
The policy and the expense records are synthetic demo data. Apply that written policy to the record.

Before you decide:
- Call get_expense_details for the expense id in the request. If it is not on file, flag it for review.
- Call search_policy at least once. Cite a section id only if that section was returned by search_policy. Never invent a section id. An id that merely appears inside another section's text does not count as retrieved.
- Call check_amount_limit with the expense category, amount, and has_receipt before you decide.

check_amount_limit compares the submitted total with the category's primary unit cap and applies the receipt threshold. It does not divide by nights, attendees, or miles, and it does not grant exceptions. Read the retrieved policy for the unit and for exceptions. A total inside the returned cap can still be denied. A total above that cap can still be allowed once you apply the unit written in the policy.

If the policy is ambiguous, or required information is missing, flag the expense for review. That includes a missing receipt above the threshold, a missing count the policy asks for, written approval the policy requires when it is not in the record, and a memo that describes a different kind of purchase than the category. Do not guess.

When the decision is flag_for_review, call flag_for_review and recommend_decision. For approve or deny, call recommend_decision only. Call recommend_decision exactly once.

Then answer in two short lines and nothing else:
Decision: approve or flag_for_review or deny
Reason: one or two sentences, including the cited section ids.
"""


def model_name() -> str:
    """Return the chat model id, defaulting to gpt-5-nano."""
    raw = os.getenv("OPENAI_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    if ":" in raw:
        return raw
    return f"openai:{raw}"


def build_tools(log: ReviewLog) -> list[Any]:
    """Bind the deterministic tools to one review log."""

    @tool
    def search_policy(query: str) -> list[dict[str, str]]:
        """Search the synthetic expense policy.

        Returns up to three sections with id, title, and text.
        Matching is keyword overlap with no stemming, so a query can miss.
        """
        return tool_impl.search_policy(query)

    @tool
    def get_expense_details(expense_id: str) -> dict[str, Any]:
        """Look up one synthetic expense by id.

        Returns found, employee, category, amount, merchant, date, has_receipt, and memo.
        found is false when the id is unknown.
        """
        return tool_impl.get_expense_details(expense_id)

    @tool
    def check_amount_limit(
        category: str, amount: float, has_receipt: bool
    ) -> dict[str, Any]:
        """Compare the submitted total with the category's primary unit cap.

        Returns within_limit, limit, receipt_required, and receipt_ok.
        The cap is applied to the total as submitted. This does not divide by
        nights, attendees, or miles, and it does not decide policy exceptions.
        Unknown categories return limit null and within_limit false.
        """
        return tool_impl.check_amount_limit(category, amount, has_receipt)

    @tool
    def recommend_decision(
        expense_id: str,
        decision: str,
        reason: str,
        cited_sections: list[str],
    ) -> dict[str, Any]:
        """Record the final decision for this expense.

        decision must be approve, flag_for_review, or deny.
        cited_sections must be section ids returned by search_policy.
        """
        return tool_impl.recommend_decision(
            expense_id,
            decision,
            reason,
            cited_sections,
            log=log,
        )

    @tool
    def flag_for_review(expense_id: str, reason: str) -> dict[str, Any]:
        """Route this expense to a person for review.

        Use this when the decision is flag_for_review. It does not approve or deny.
        """
        return tool_impl.flag_for_review(expense_id, reason, log=log)

    return [
        search_policy,
        get_expense_details,
        check_amount_limit,
        recommend_decision,
        flag_for_review,
    ]


def build_agent(log: ReviewLog | None = None) -> tuple[Any, ReviewLog]:
    """Create the single expense-review agent and the log its tools write to."""
    review_log = log or ReviewLog()
    agent = create_agent(
        model=model_name(),
        tools=build_tools(review_log),
        system_prompt=SYSTEM_PROMPT,
        name="expense-policy-review",
    )
    return agent, review_log
