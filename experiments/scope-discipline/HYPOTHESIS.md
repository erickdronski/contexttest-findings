# scope-discipline — hypothesis, written before the re-run

**History.** This experiment was first published on 2026-08-14 as a null
result. That result is retracted: the rule was written to `AGENTS.md`, which
Claude Code does not load, so neither arm received it. Per-request input tokens
differed by about 25 tokens across arms; a delivered rule of this length adds
roughly 120 per request.

**This run** puts the same rule in `CLAUDE.md`, strips the answer key from the
trial worktree, isolates the agent from user-level plugins and MCP servers, pins
the model, and uses five paired attempts instead of three.

**The task** — make `Inventory.remove` raise `ValueError` when removing more
than is held — is small, single-file, and explicit about scope ("Do not change
any other behavior").

**Prediction.** No measurable effect. The prompt already states the scope
constraint, so a rule restating it in general terms has little left to add.

**What counts as the rule working:** with the rule, median diff lines fall by at
least a third, or success rises by at least 40 percentage points.
