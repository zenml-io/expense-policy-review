# Expense policy review

A single LangGraph agent reviews one employee expense against a fictional company policy and records the run in Langfuse. There is no Kitaru code in this repo. All policy text, employees, merchants, and amounts are synthetic.

The agent looks up the expense, searches the policy, checks the amount against that category's primary cap, and answers with `approve`, `flag_for_review`, or `deny`, plus a short reason and the policy section ids it used. If the policy is ambiguous or required information is missing, it is supposed to flag the expense for a person instead of guessing.

## Setup

Python 3.11 or newer and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
cp .env.example .env
```

Fill in `.env`. The file is gitignored.

- `OPENAI_API_KEY`
- `OPENAI_MODEL` (optional, default `gpt-5-nano`)
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_HOST`

The Langfuse Python SDK (5.2.0 here) prefers `LANGFUSE_BASE_URL` and still reads `LANGFUSE_HOST` when the base URL is unset. Set one of them. If both are set, `LANGFUSE_BASE_URL` wins.

## Run

`scripts/run_queries.py` sends every line of `queries.jsonl` through the agent and flushes a Langfuse trace. It calls the model. It does not read `labels.jsonl`.

```bash
uv run python scripts/run_queries.py
uv run python scripts/run_queries.py --repeats 3
uv run python scripts/run_queries.py --limit 2
```

`--repeats` defaults to 1. `--limit` runs only the first N queries. Each trace is tagged with the query id and the run number. Those values are also stored as trace metadata (`query_id`, `run_number`). The trace name is `expense-policy-review`.

## Traces

`scripts/run_queries.py` passes `langfuse.langchain.CallbackHandler` on each `agent.invoke`. The handler maps LangChain runs onto Langfuse observations: a chain whose name or class path contains "agent" becomes an `agent` span, other chains become `chain` spans, chat-model runs become `generation` spans, and tools become `tool` spans.

The graph from `create_agent` has two nodes, `model` and `tools`. A scripted review that called `get_expense_details` and `search_policy` together, then `check_amount_limit`, then `recommend_decision`, then answered, produced **17** spans. Nothing was sent to OpenAI or to a Langfuse server; the handler wrote into an in-memory exporter. The tree was:

```text
expense-policy-review          chain        user request; trace name, tags, and metadata
  model                        chain
    ScriptedModel              generation
  tools                        chain
    get_expense_details        tool
  tools                        chain        parallel calls become sibling chains
    search_policy              tool
  model                        chain
    ScriptedModel              generation
  tools                        chain
    check_amount_limit         tool
  model                        chain
    ScriptedModel              generation
  tools                        chain
    recommend_decision         tool
  model                        chain
    ScriptedModel              generation   final decision and reason
```

The probe used a scripted chat model, so each generation is named `ScriptedModel`. A real run names that span `ChatOpenAI`. The root span is type `chain`, not `agent`, because the graph name `expense-policy-review` does not contain "agent". Trace tags were `q01` and `run-1`. Trace metadata held `query_id` and `run_number`. A live model that takes another turn, or that also calls `flag_for_review`, adds another model chain, another generation, and another tools chain plus tool span. That is more than a flat list of five tool steps. The handler does not collapse the LangGraph node wrappers.

## Layout

- `expense_review/policy.py` and top-level `policy.md` — synthetic Lumenfield Analytics policy, ten section ids. `policy.md` is the rendered text of `policy.py`.
- `expense_review/expenses.py` — in-memory expenses keyed by `expense_id`
- `expense_review/agent.py` — one `create_agent` graph and the system prompt
- `queries.jsonl` — 15 employee messages
- `labels.jsonl` — expected decision, expected section ids, and difficulty, kept out of the queries file
- `scripts/run_queries.py` — traced runs

## Tests

No model calls and no network:

```bash
uv run pytest
```

## Synthetic data

Lumenfield Analytics, its policy, and every expense in this repo are fictional demo data.
