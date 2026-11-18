# Agent guide

Instructions for coding agents working in this repo. `README.md` covers setup, the runner, and the Langfuse span tree in more detail.

## What this is

A single LangGraph agent reviews one employee expense against a fictional company policy and answers `approve`, `flag_for_review`, or `deny`. Each run is traced to Langfuse. The company (Lumenfield Analytics), the policy, the employees, and the expenses are all synthetic. Keep it that way: never add real names, companies, or amounts.

## Why it exists

This repo is the stand-in for a production agent in ZenML's content on agent evals: an agent that is already running, with traces already flowing into Langfuse, and no evals yet. `scripts/run_queries.py --repeats N` simulates the traffic. The evals are then built from those traces with Kitaru, outside this repo.

The traces are meant to support four eval angles:

- **Retrieval:** did `search_policy` return the right section?
- **Decision:** does the decision match the label?
- **Citation groundedness:** was every cited section actually retrieved?
- **Ambiguity:** did the agent flag an unclear case instead of guessing?

## The baseline is frozen

Do not edit the system prompt in `agent.py` or the tool behavior in `tools.py` unless the task says so explicitly. The author's baseline run matched the labels on roughly 90% of queries, so some traces are wrong on purpose, and those failures are the material the evals are built on. A "fix" here silently changes every trace generated afterwards. Tagged versions (`v1`, `v1.1`) mark the baselines; a behavior change belongs in a new tag.

## Commands

```bash
uv sync                                          # install
uv run pytest                                    # tests: no model calls, no network
uv run python scripts/run_queries.py --limit 2   # live run: calls OpenAI and Langfuse
```

Run `uv run pytest` after every change. Do not run `scripts/run_queries.py` unless asked: it needs a filled-in `.env`, spends model tokens, and writes traces to a real Langfuse project.

## Layout

- `expense_review/policy.py` — the policy: section text, `CATEGORY_LIMITS`, `RECEIPT_THRESHOLD`, and the other caps. Source of truth.
- `policy.md` — rendered output of `render_policy_markdown()` in `policy.py`.
- `expense_review/expenses.py` — in-memory expense records keyed by `expense_id`.
- `expense_review/tools.py` — the five deterministic tools. None calls a model.
- `expense_review/agent.py` — the `create_agent` graph, tool wrappers, and system prompt.
- `expense_review/expected.py` — labeling helper for clear-cut decisions.
- `scripts/run_queries.py` — sends `queries.jsonl` through the agent with a Langfuse callback.
- `queries.jsonl` — 42 employee messages. `labels.jsonl` — the expected decision, sections, and difficulty for each.
- `queries_pending.jsonl` — q43–q45, parked because the policy does not clearly decide them.
- `label_notes.md` — the reasoning behind the labels for q16–q45.
- `tests/test_tools.py` — tool behavior plus the invariants below.

## Invariants the tests enforce

- **`policy.md` must equal `render_policy_markdown()` byte for byte.** Change policy text in `policy.py`, then regenerate:
  ```bash
  uv run python -c "from expense_review.policy import render_policy_markdown as r; open('policy.md','w').write(r())"
  ```
- **Labels stay out of the agent's path.** `agent.py`, `tools.py`, and `scripts/run_queries.py` must not import `expense_review.expected` or read `labels.jsonl`, `label_notes.md`, or `queries_pending.jsonl`. The check is a string match on the source, so even a comment naming those files can fail it. The runner mentions `labels.jsonl` exactly once, in its docstring.
- **Queries and labels are separate files.** Expected answers never go in `queries.jsonl`.
- **Existing expenses are pinned.** Several records (`EXP-1001`, `EXP-1002`, `EXP-1005`, `EXP-1014`, `EXP-1015`) are asserted field by field, and the total is asserted to be 45. Adding an expense means updating that count and the dataset tests.

## Things that look like bugs but are intended

- `search_policy` matches exact tokens with no stemming and returns at most three sections, so it can miss the right one.
- `check_amount_limit` compares the submitted total with the category's primary cap. It does not divide by nights, attendees, or miles, and it knows nothing about exceptions.
- `EXP-1015` is filed under `meals` with a software memo.

These gaps are part of the frozen baseline above. If a task does ask you to change one, say so in the PR.

## Conventions

- Money is `Decimal`, quantized to two places, and stored as strings in the expense records. Do not introduce floats.
- A total exactly at a cap is within the limit. An amount exactly at the receipt threshold does not need a receipt.
- When the policy is ambiguous or required information is missing, the correct decision is `flag_for_review`, not `deny`.
- A new query needs a line in `queries.jsonl`, a line in `labels.jsonl`, a record in `expenses.py`, and an entry in `label_notes.md`. If the policy does not clearly decide it, park it in `queries_pending.jsonl` instead of labeling it.
- Never commit `.env`. New environment variables go in `.env.example` with an empty value.
