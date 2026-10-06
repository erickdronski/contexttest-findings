# currency-format-codex — hypothesis, written before the run

**Role: cross-agent replication of the positive control.** Same fixture, same
prompt, same hidden check, and the same rule text as `currency-format` — but the
agent is Codex, which reads `AGENTS.md` natively, instead of Claude Code, which
reads `CLAUDE.md`.

**Prediction.** The effect replicates: without the rule Codex writes a
symbol-prefixed price and fails the hidden check; with it, Codex passes.

**What counts as replication:** with-rule success exceeds no-rule success by at
least 60 percentage points across five paired attempts, matching the direction
of `currency-format`.

**Why it matters.** Instruction files are increasingly shared across agents. A
rule that works for one agent and not another is worth knowing about before a
team assumes a single file serves both.
