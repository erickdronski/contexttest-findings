# Retracted — the treatment was never delivered

These reports were published on 2026-08-14 as a null result for a
scope-discipline rule. They are kept for the record, not as evidence.

The rule was written to `AGENTS.md`. Claude Code does not load `AGENTS.md` — it
loads `CLAUDE.md` — so neither arm received the rule, and the two arms were the
same experiment run twice. A tie was the only possible outcome.

The reports themselves show it. Each trial's total input tokens (uncached +
cache creation + cache read, across its three requests):

| arm | attempt 1 | attempt 2 | attempt 3 |
|---|---|---|---|
| no-scope-rule | 51,747 | 51,177 | 51,177 |
| scope-rule | 51,202 | 51,202 | 51,199 |

A delivered rule of this length adds roughly 120 tokens to every request, about
360 per trial. The observed difference is about 25 tokens per trial — the size
of a file listing, not of the rule.

The same check was reproduced on 2026-10-06 with Claude Code 2.1.272: a canary
instruction in `AGENTS.md` was ignored; the identical instruction in `CLAUDE.md`
was followed.

The experiment was re-run with the rule delivered through `CLAUDE.md`. See
`../2026-10-06/` and the README.
