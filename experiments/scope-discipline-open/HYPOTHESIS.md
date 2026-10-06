# scope-discipline-open — hypothesis, written before the re-run

**History.** First published on 2026-08-14 as a null result, now retracted for
the same reason as `scope-discipline`: the rule was written to `AGENTS.md`,
which Claude Code does not load, so neither arm received it.

**This run** delivers the rule through `CLAUDE.md`, strips the answer key from
the worktree, isolates the agent from user-level configuration, pins the model,
and uses five paired attempts.

**The task** — add `total_with_discount(percent)` to a cart — deliberately
leaves room for scope creep: validation of the percentage, rounding policy,
helper abstractions, docstrings.

**Prediction.** A small effect at most. Current models tend to answer this
prompt with a short change unprompted, which would leave a scope rule little to
suppress.

**What counts as the rule working:** with the rule, median diff lines fall by at
least a third, or the share of attempts that add unrequested validation falls by
at least 40 percentage points.
