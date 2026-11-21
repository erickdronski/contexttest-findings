<h1 align="center">contexttest-findings</h1>

<p align="center"><strong>Measured results for instruction-file rules — <code>CLAUDE.md</code> and <code>AGENTS.md</code>.</strong><br>
Real agent runs, pre-registered predictions, published data, null results and corrections included.</p>

<p align="center">
  <a href="#results">Results</a> ·
  <a href="#first-a-correction">Correction</a> ·
  <a href="#what-these-results-do-not-show">Limitations</a> ·
  <a href="#reproduce-it">Reproduce</a>
</p>

<p align="center">
  <img alt="MIT license" src="https://img.shields.io/badge/license-MIT-101828">
  <img alt="80 valid live agent trials" src="https://img.shields.io/badge/live_trials-80_valid-6b21a8">
  <img alt="2 agents" src="https://img.shields.io/badge/agents-Claude_Code_%C2%B7_Codex-174ea6">
  <img alt="pre-registered" src="https://img.shields.io/badge/predictions-pre--registered-08775c">
</p>

---

This repository publishes controlled experiments on coding-agent instruction
files using [ContextTest](https://github.com/erickdronski/contexttest). Each
experiment includes its hypothesis, configuration, fixtures, and recorded
results so readers can inspect both the conclusion and the method.

The October study recorded **70 live trials across five experiments**. A
November 20 replication added **10 verified Codex trials**. Both rounds found
that giving Codex the checkout display format changed success from 0/5 to 5/5.
The four Claude experiments still await a verified rerun with shared memory disabled.

The useful business question is whether maintaining a rule improves the work
it governs. These experiments consider task success, change scope, duration,
and reported cost while retaining null results and corrections.

## First, a correction

**The first result published here was wrong.** In August this repository
reported that a popular scope-discipline rule "changed nothing measurable." The
rule had been written to `AGENTS.md`, while the Claude Code setup loaded
`CLAUDE.md`. Both arms therefore ran without the intended rule.

The reports said so on their own: total input tokens differed by about 25 per
trial across arms, where a delivered rule of that length adds about 120 per
request. A canary run reproduced it — the same instruction ignored in
`AGENTS.md`, followed in `CLAUDE.md`. The original reports are kept, unedited,
under [`results/*/2026-08-14-retracted/`](results/scope-discipline/2026-08-14-retracted/RETRACTED.md)
with a note explaining why they do not count.

ContextTest 0.3 added instruction-delivery records and a bridge for `AGENTS.md`
in Claude Code. The October Claude experiments also supplied the candidate
rule through a native `CLAUDE.md`.

## Results

### November 20, 2026 · pinned replication

| Codex currency-format result | October 6 · v0.3.0 | November 20 · v0.3.1 |
|---|---:|---:|
| Passed without the house rule | 0/5 | 0/5 |
| Passed with the house rule | 5/5 | 5/5 |
| Paired attempts favoring the rule | 5/5 | 5/5 |
| Exact two-sided paired p-value | 0.0625 | 0.0625 |
| Median changed lines, without / with rule | 7 / 7 | 7 / 7 |
| Median duration in seconds, without / with rule | 26.4 / 20.6 | 41.0 / 39.2 |

All ten November attempts completed, passed the fixture tests, and stayed
within the allowed paths. The hidden display check distinguished the arms.
All five untreated attempts returned `12.50` for 1,250 cents, while all five
treated attempts returned `12.50 USD`. In October, four untreated attempts
returned the bare amount and one added a dollar sign. The success result
replicated. The timing difference is descriptive given five attempts per arm.
[October report](results/currency-format-codex/2026-10-06/report.json) · [November report](results/currency-format-codex/2026-11-20/report.json) · [Rendered results](results/currency-format-codex/2026-11-20/report.html)

Both rounds used Codex CLI 0.156.1, `gpt-6-astra`, the same fixture commit,
prompts, assertions, and instruction variants. The harness recorded native
`AGENTS.md` delivery and rated its token-based delivery check `unknown` in both
rounds. The November run finished at 02:57 UTC on November 21 (November 20
Eastern). [Original fixture and hypotheses](https://github.com/erickdronski/contexttest-findings/tree/af742fce8090abdc83be08bfacc0a1cb41e7ee0a/experiments) · [Pinned harness](https://github.com/erickdronski/contexttest/tree/0c08733a767fdc0a9f17d811825ac2c8d46b4a80)

**Claude memory isolation remains untested in this replication.** The v0.3.1
change disables Claude Code's automatic memory between trials. On the first
Claude batch the provider rejected authentication before inference on all ten
invocations. Each exited with an error and zero model tokens. They contribute
zero observations. The other three Claude configurations and the second currency
batch were held. The 60 historical Claude observations remain labeled v0.3.0.
[Memory fix](https://github.com/erickdronski/contexttest/blob/0c08733a767fdc0a9f17d811825ac2c8d46b4a80/src/lib/adapters.mjs#L107-L125)

### October 6, 2026 · ContextTest 0.3.0

| Experiment | The question | Without the rule | With the rule | Paired evidence |
|---|---|---|---|---|
| [currency-format](experiments/currency-format/HYPOTHESIS.md) · positive control | Does a rule carrying a convention the code lacks change what the agent writes? | 1 / 10 | **10 / 10** | p = 0.004 · 10 pairs over 2 runs · strong |
| [currency-format-codex](experiments/currency-format-codex/HYPOTHESIS.md) | The same, on Codex reading `AGENTS.md` | 0 / 5 | **5 / 5** | p = 0.063 · 5 pairs · directional |
| [currency-format-redundant](experiments/currency-format-redundant/HYPOTHESIS.md) | Is the rule still needed when a neighbouring function already shows the convention? | 3 / 10 | **10 / 10** | p = 0.016 · 10 pairs over 2 runs · convincing |
| [scope-discipline](experiments/scope-discipline/HYPOTHESIS.md) | Does "deliver exactly what was asked" shrink a tightly scoped fix? | 5 / 5 | 5 / 5 | p = 1.000 · no effect on success |
| [scope-discipline-open](experiments/scope-discipline-open/HYPOTHESIS.md) | Does it shrink an open-ended addition? | 5 / 5 | 5 / 5 | p = 1.000 · identical in every trial |

Task success means every assertion passed: the fixture's tests, the allowed
paths, and — for the currency experiments — a hidden check of the exact output
format not included in the task prompt or fixture tests.

#### October finding 1 — both agents followed the explicit currency format

The fixture is a small checkout module. The task asks for a `format_price(cents)`
function "for the display string shown to customers at checkout." The rule says
house prices render as `12.50 USD`. The prompt and visible tests for this task
leave the exact format open. A neighboring experiment's fixture contains an
example that a search of the whole repository could find.

Without the rule, eight of the ten Claude Code attempts produced `$12.50`,
one produced a bare `12.50`, and one passed the exact house-format checks.
The original write-up miscounted the dollar-prefixed answers. The reported
success count stays at 1/10. All ten rule-arm attempts passed. Codex went
from 0/5 to 5/5 with the same rule in `AGENTS.md`. [Claude run 1](results/currency-format/2026-10-06/run-1/report.json) · [Claude run 2](results/currency-format/2026-10-06/run-2/report.json)

Reported cost and duration were also lower in the treated Claude Code arm.
These are descriptive results from this small sample:

| | without the rule | with the rule |
|---|---|---|
| median model requests | 11.5 | 8 |
| median duration | 64 s | 36 s |
| median cost | $0.37 | $0.25 |

This positive control tests whether the harness can detect an explicit
formatting instruction on this task.

#### October finding 2 — a nearby example alone gave inconsistent results

The prediction was that the rule would be redundant here. The fixture already
contains `format_receipt_total`, whose docstring and code both render
`12.50 USD`, in the same file the agent edits.

**That prediction failed.** Without the rule, the agent still wrote `$12.50` in
7 of 10 attempts. With the rule, 10 of 10 matched.

The practical implication for this task: an explicit rule was more reliable
than a nearby example. The untreated arm followed the convention in 3 of 10
attempts. Other repositories and task families need their own replication.

#### October finding 3 — scope-rule results fell short of the predicted thresholds

With the rule now reaching the model, both scope tasks were solved in every
attempt, in both arms.

- **The open-ended task** — "add a `total_with_discount(percent)` method" — was
  answered with the same 3-line change in all 10 attempts. No validation, no
  rounding policy, no helpers. There was no scope creep for the rule to
  suppress.
- **The tightly scoped fix** produced slightly smaller diffs with the rule: a
  median of 5 changed lines against 7, and every rule-arm attempt landed at 5.
  That is a 29% reduction — consistent, and below the one-third reduction
  pre-registered as "the rule working." It is reported as a small effect that
  missed its bar, not as a win.

The October scope rule showed little benefit on these two tasks.

## What these results do not show

- **October 6 models and tools.** The reports record Claude Code 2.1.272 with
  `claude-opus-5` and Codex CLI 0.156.1 with `gpt-6-astra`.
- **October Claude trials shared an auto-memory directory.** All sixty Claude
  trials used ContextTest 0.3.0. Because their worktrees belonged to the same
  Git repository, a memory written in one trial could have been read in another.
  The records do not establish whether this happened. Version 0.3.1 disables
  auto-memory in isolated Claude trials. A change between dates cannot by
  itself identify the memory fix as its cause. [Harness fix](https://github.com/erickdronski/contexttest/blob/0c08733a767fdc0a9f17d811825ac2c8d46b4a80/CHANGELOG.md#L13-L19)
- **Small, single-file tasks.** Rules about architecture, multi-file changes,
  or long autonomous runs were not tested.
- **Small samples.** Five to ten paired attempts per experiment. The paired
  test makes no assumption about the size of the effect, and the p-values above
  are exact, but a real 10–20% effect would be invisible at this scale.
- **Claude Code shell commands were denied.** The October trials used `acceptEdits`
  in non-interactive mode: Claude Code could read and edit, but could not run
  its own shell-based tests. Both Claude Code arms had the same restriction.
  Codex used its configured `workspace-write` sandbox; the agents did not
  share an identical permission model.
- **Token-based delivery checks vary by run.** ContextTest compares input
  tokens across arms, but short rules can be smaller than trial-to-trial usage
  variation. Some reports therefore mark delivery `unknown`; others mark it
  `consistent`. All 25 October currency trials in the rule arms produced
  the specified format.
- **The positive control checks whether the harness can detect an effect.**
  It supplies a convention absent from the fixture. Success on that control
  does not establish that every instruction of the same kind is effective.

## How the experiments are run

- **Predictions first.** Each experiment's `HYPOTHESIS.md` states what would
  count as the rule working, and was committed before any trial ran — commit
  `af742fc` contains every prediction and no result.
- **The setup removes the answer key.** Each trial starts in a disposable Git
  worktree. Setup removes the candidate instruction files, experiment configs,
  hypotheses, results, and this README. Sibling fixtures stay in place, including
  the neighboring receipt formatter. An agent with Git or network access
  could also consult history or the public repository. [Pinned setup](https://github.com/erickdronski/contexttest-findings/blob/af742fce8090abdc83be08bfacc0a1cb41e7ee0a/tools/sanitize_worktree.py) · [Neighboring fixture](https://github.com/erickdronski/contexttest-findings/blob/af742fce8090abdc83be08bfacc0a1cb41e7ee0a/experiments/currency-format-redundant/fixture/money.py)
- **Isolated agents.** Claude Code runs without the experimenter's user-level
  plugins, settings, or MCP servers (`--strict-mcp-config --setting-sources
  project,local`); Codex runs with `--ignore-user-config`. Models are pinned.
- **Paired and alternated.** Every attempt runs both arms from the same commit
  in fresh git worktrees, alternating which arm goes first.
- **Repeated runs are pooled, not merged.** The two currency experiments were
  run twice; `contexttest aggregate` pools them while keeping pairs inside their
  own run, so disagreement between runs stays visible in the pooled report.
- **November report export.** All ten Codex processes exited successfully with
  generated tokens. Before publication, each trial's assertions, pairing,
  changed files, and timing were checked against the original run. The public
  report omits the agent's process streams, which contain local diagnostics.
  The grader output and all measurements are retained. The export option is
  `--omit-agent-transcripts`. [Export tool](tools/publish_report.py)
- **Published without machine paths.** [`tools/publish_report.py`](tools/publish_report.py)
  replaces known local paths with placeholders and re-renders the HTML from the
  scrubbed JSON. It requires a new destination, checks for residual home paths,
  and publishes both files only after rendering succeeds. Review output for
  other identifying details before sharing; this is not a general secret scanner.

## Reproduce it

Use a fresh checkout of the original fixture and the pinned harness containing
the Claude memory fix. The example repeats the November currency test with a
signed-in Codex CLI. `doctor` inspects instruction delivery. The final command
starts ten live trials, five per arm.

```bash
git clone https://github.com/erickdronski/contexttest.git contexttest-harness
git -C contexttest-harness checkout --detach 0c08733a767fdc0a9f17d811825ac2c8d46b4a80

git clone https://github.com/erickdronski/contexttest-findings.git contexttest-fixture
cd contexttest-fixture
git checkout --detach af742fce8090abdc83be08bfacc0a1cb41e7ee0a
node ../contexttest-harness/src/cli.mjs doctor --config experiments/currency-format-codex/contexttest.json
node ../contexttest-harness/src/cli.mjs run --config experiments/currency-format-codex/contexttest.json
```

For the full five-experiment design, run `currency-format` and
`currency-format-redundant` twice each, then run `currency-format-codex`,
`scope-discipline`, and `scope-discipline-open` once each. Use the
corresponding config path for each run. Pool only repeat runs of the same
experiment and date. The four Claude experiments require a signed-in Claude Code CLI with access to the configured model.

The sixty October Claude Code trials reported **$13.85** in total, ranging from
$0.12 to $0.44 per trial. The ten October Codex trials used a subscription
with no per-trial cost reported.

```
experiments/<name>/
  contexttest.json        the experiment
  HYPOTHESIS.md           the prediction, committed before the run
  CLAUDE.candidate.md     the rule under test (AGENTS.candidate.md for Codex)
  fixture/                the code the agent works on, plus its visible tests
results/<name>/<date>/
  report.json, report.html          one run
  run-1/, run-2/, pooled/           repeated runs and their pooled analysis
```

## Contributing an experiment

The bar is that a result must be falsifiable and reproducible, not that it must
be interesting. Null results and failed predictions are welcome — this page has
both.

A good experiment isolates one rule, uses a task where the rule could plausibly
matter, and states up front what outcome would count as the rule working. If
you cannot say in advance what "it worked" looks like, the experiment will not
answer anything. Open an issue with the rule you want tested and the task you
think would discriminate.

## License

MIT.
