"""Run synthetic expense reviews and send traces to Langfuse.

This script calls the model. It does not read labels.jsonl.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

from expense_review.agent import build_agent  # noqa: E402


def _load_jsonl(path: Path) -> list[dict]:
    rows = []
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path.name}:{line_number} is not valid JSON: {exc}") from exc
    return rows


def _require_env() -> None:
    import os

    missing = [
        name
        for name in ("OPENAI_API_KEY", "LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY")
        if not os.getenv(name)
    ]
    if not (os.getenv("LANGFUSE_BASE_URL") or os.getenv("LANGFUSE_HOST")):
        missing.append("LANGFUSE_HOST or LANGFUSE_BASE_URL")
    if missing:
        joined = ", ".join(missing)
        raise SystemExit(f"Missing environment variables: {joined}")


def _final_text(result: dict) -> str:
    for message in reversed(result.get("messages", [])):
        content = getattr(message, "content", "")
        if not isinstance(content, str) or not content.strip():
            continue
        if getattr(message, "tool_calls", None):
            continue
        message_type = getattr(message, "type", "")
        if message_type in {"ai", "assistant"}:
            return content.strip()
    return ""


def run(repeats: int, limit: int | None) -> None:
    _require_env()
    from langfuse import get_client
    from langfuse.langchain import CallbackHandler

    queries = _load_jsonl(ROOT / "queries.jsonl")
    if limit is not None:
        queries = queries[:limit]

    agent, review_log = build_agent()
    langfuse = get_client()

    for query in queries:
        query_id = str(query["id"])
        message = str(query["message"])
        for run_number in range(1, repeats + 1):
            review_log.clear()
            handler = CallbackHandler()
            result = agent.invoke(
                {"messages": [{"role": "user", "content": message}]},
                config={
                    "callbacks": [handler],
                    "run_name": "expense-policy-review",
                    "metadata": {
                        "query_id": query_id,
                        "run_number": run_number,
                        "langfuse_tags": [query_id, f"run-{run_number}"],
                        "langfuse_trace_name": "expense-policy-review",
                    },
                },
            )
            langfuse.flush()
            recorded = review_log.decisions[-1]["decision"] if review_log.decisions else "none"
            print(
                f"{query_id} run {run_number} "
                f"trace_id={handler.last_trace_id} recorded={recorded}"
            )
            print(_final_text(result))
            print("---")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Review each synthetic expense query and trace the run in Langfuse."
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=1,
        help="How many times to run each query (default: 1).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Run only the first N queries.",
    )
    args = parser.parse_args(argv)
    if args.repeats < 1:
        raise SystemExit("--repeats must be at least 1")
    if args.limit is not None and args.limit < 0:
        raise SystemExit("--limit must be zero or positive")
    run(args.repeats, args.limit)


if __name__ == "__main__":
    main(sys.argv[1:])
