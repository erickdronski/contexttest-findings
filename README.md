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
  <img alt="70 valid live agent trials" src="https://img.shields.io/badge/live_trials-70_valid-6b21a8">
  <img alt="2 agents" src="https://img.shields.io/badge/agents-Claude_Code_%C2%B7_Codex-174ea6">
  <img alt="pre-registered" src="https://img.shields.io/badge/predictions-pre--registered-08775c">
</p>

---

This repository publishes controlled experiments on coding-agent instruction
files using [ContextTest](https://github.com/erickdronski/contexttest). Each
experiment includes its hypothesis, configuration, fixtures, and recorded
results so readers can inspect both the conclusion and the method.

The current dataset contains **70 valid live trials across five experiments**,
run on **October 6, 2026**. It covers explicit formatting conventions and
scope-discipline rules on small tasks. These results are evidence for those
specific settings, not a general ranking of agents or instruction practices.

The useful business question is whether maintaining a rule improves the work
it governs. These experiments consider task success, change scope, duration,
and reported cost while retaining null results and corrections.

## First, a correction

**The first result published here was wrong.** In August this repository
reported that a popular scope-discipline rule "changed nothing measurable." The
rule had been written to `AGENTS.md`. Claude Code does not read `AGENTS.md` — it
reads `CLAUDE.md` — so neither arm ever received it, and a tie was the only
possible outcome.

The reports said so on their own: total input tokens differed by about 25 per
trial across arms, where a delivered rule of that length adds about 120 per
request. A canary run reproduced it — the same instruction ignored in
`AGENTS.md`, followed in `CLAUDE.md`. The original reports are kept, unedited,
under [`results/*/2026-08-14-retracted/`](results/scope-discipline/2026-08-14-retracted/RETRACTED.md)
with a note explaining why they do not count.

The fix went into the tool, not just this repository: contexttest 0.3 bridges
`AGENTS.md` into Claude Code, records how each arm's instructions were
delivered, and flags comparisons whose treatment probably never reached the
agent. Every experiment below was re-run or newly run after that fix.

## Results

| Experiment | The question | Without the rule | With the rule | Paired evidence |
|---|---|---|---|---|
| [currency-format](experiments/currency-format/HYPOTHESIS.md) · positive control | Does a rule carrying a convention the code lacks change what the agent writes? | 1 / 10 | **10 / 10** | p = 0.004 · 10 pairs over 2 runs · strong |
| [currency-format-codex](experiments/currency-format-codex/HYPOTHESIS.md) | The same, on Codex reading `AGENTS.md` | 0 / 5 | **5 / 5** | p = 0.063 · 5 pairs · directional |
| [currency-format-redundant](experiments/currency-format-redundant/HYPOTHESIS.md) | Is the rule still needed when a neighbouring function already shows the convention? | 3 / 10 | **10 / 10** | p = 0.016 · 10 pairs over 2 runs · convincing |
| [scope-discipline](experiments/scope-discipline/HYPOTHESIS.md) | Does "deliver exactly what was asked" shrink a tightly scoped fix? | 5 / 5 | 5 / 5 | p = 1.000 · no effect on success |
| [scope-discipline-open](experiments/scope-discipline-open/HYPOTHESIS.md) | Does it shrink an open-ended addition? | 5 / 5 | 5 / 5 | p = 1.000 · identical in every trial |

Task success means every assertion passed: the fixture's tests, the allowed
paths, and — for the currency experiments — a hidden check of the exact output
format the agent never got to see.

### Finding 1 — explicit formatting guidance improved these tasks on both agents

The fixture is a small checkout module. The task asks for a `format_price(cents)`
function "for the display string shown to customers at checkout." The rule says
house prices render as `12.50 USD`, never with a symbol. Nothing in the code,
the tests, or the prompt mentions presentation; the convention exists only in
the instruction file.

Without the rule, Claude Code wrote `$12.50` in 9 of 10 attempts (the tenth
wrote a bare `12.50`). With it, all 10 matched the house format. Codex, given
the same rule through `AGENTS.md`, went from 0 of 5 to 5 of 5.

Reported cost and duration were also lower in the treated Claude Code arm.
These are descriptive results from this small sample:

| | without the rule | with the rule |
|---|---|---|
| median turns | 11.5 | 8 |
| median duration | 64 s | 36 s |
| median cost | $0.37 | $0.25 |

Without it, agents spent turns looking for a convention to follow — attempting
more shell searches before settling on the symbol they would have used anyway.

This experiment was built to work. Its job is to show the harness can detect an
effect when one exists, which is what gives the null results below their
meaning.

### Finding 2 — agents did not generalize a convention from the next function over

The prediction was that the rule would be redundant here. The fixture already
contains `format_receipt_total`, whose docstring and code both render
`12.50 USD`, in the same file the agent edits.

**That prediction failed.** Without the rule, the agent still wrote `$12.50` in
7 of 10 attempts. It read the module, saw the receipt formatter, and treated
checkout as a different surface. With the rule, 10 of 10 matched.

The practical implication for this task: an explicit rule was more reliable
than a nearby example. The untreated arm followed the convention in 3 of 10
attempts. Other repositories and task families need their own replication.

### Finding 3 — the scope rule, actually delivered this time, still had little to do

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

On small, well-specified tasks with a current model, this rule bought little.
The claim stays that narrow.

## What these results do not show

- **One model per agent, at one point in time.** Claude Code 2.1.272 running
  `claude-opus-5`, and Codex CLI 0.156.1 running `gpt-6-astra`, on
  2026-10-06. Both are recorded in every report.
- **Small, single-file tasks.** Rules about architecture, multi-file changes,
  or long autonomous runs were not tested.
- **Small samples.** Five to ten paired attempts per experiment. The paired
  test makes no assumption about the size of the effect, and the p-values above
  are exact, but a real 10–20% effect would be invisible at this scale.
- **Claude Code shell commands were denied.** Those trials used `acceptEdits`
  in non-interactive mode: Claude Code could read and edit, but could not run
  its own shell-based tests. Both Claude Code arms had the same restriction.
  Codex used its configured `workspace-write` sandbox; the agents did not
  share an identical permission model.
- **Token-based delivery checks vary by run.** ContextTest compares input
  tokens across arms, but short rules can be smaller than trial-to-trial usage
  variation. Some reports therefore mark delivery `unknown`; others mark it
  `consistent`. Behaviour provides additional evidence: the treated currency
  arms followed the supplied format in 25 of 25 attempts. This supports
  treatment delivery without proving every internal step.
- **The positive control checks whether the harness can detect an effect.**
  It supplies a convention absent from the fixture. Success on that control
  does not establish that every instruction of the same kind is effective.

## How the experiments are run

- **Predictions first.** Each experiment's `HYPOTHESIS.md` states what would
  count as the rule working, and was committed before any trial ran — commit
  `af742fc` contains every prediction and no result.
- **The agent cannot see the answer key.** Trials run inside a checkout of this
  repository, so a setup step ([`tools/sanitize_worktree.py`](tools/sanitize_worktree.py))
  removes candidate rules, experiment configs, hypotheses, results, and this
  README from each trial worktree before the agent starts. CI verifies that it
  does.
- **Isolated agents.** Claude Code runs without the experimenter's user-level
  plugins, settings, or MCP servers (`--strict-mcp-config --setting-sources
  project,local`); Codex runs with `--ignore-user-config`. Models are pinned.
- **Paired and alternated.** Every attempt runs both arms from the same commit
  in fresh git worktrees, alternating which arm goes first.
- **Repeated runs are pooled, not merged.** The two currency experiments were
  run twice; `contexttest aggregate` pools them while keeping pairs inside their
  own run, so disagreement between runs stays visible in the pooled report.
- **Published without machine paths.** [`tools/publish_report.py`](tools/publish_report.py)
  copies a report into `results/`, replaces local paths with placeholders, and
  re-renders the HTML from the scrubbed JSON.

## Reproduce it

```bash
git clone https://github.com/erickdronski/contexttest-findings
cd contexttest-findings
npx github:erickdronski/contexttest doctor --config experiments/currency-format/contexttest.json
npx github:erickdronski/contexttest run    --config experiments/currency-format/contexttest.json
```

`doctor` inspects the configured instruction-delivery path before live trials
start. The Claude Code trials in this round reported **$13.85 in total**, about
$0.12 to $0.40 per trial; the Codex trials ran on a subscription and are not
priced.

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
