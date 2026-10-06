<h1 align="center">contexttest-findings</h1>

<p align="center"><strong>Measured results for instruction-file rules — <code>CLAUDE.md</code> and <code>AGENTS.md</code>.</strong><br>
Real agent runs, pre-registered predictions, published data, null results and corrections included.</p>

<p align="center">
  <img alt="MIT license" src="https://img.shields.io/badge/license-MIT-101828">
  <img alt="70 valid live agent trials" src="https://img.shields.io/badge/live_trials-70_valid-6b21a8">
  <img alt="2 agents" src="https://img.shields.io/badge/agents-Claude_Code_%C2%B7_Codex-174ea6">
  <img alt="pre-registered" src="https://img.shields.io/badge/predictions-pre--registered-08775c">
</p>

---

Instruction files are full of rules everyone copies and nobody measures. This
repository runs those rules as experiments with
[contexttest](https://github.com/erickdronski/contexttest) and publishes what
came back. Every number below came from a real agent run, and the raw reports
are committed next to the experiments that produced them.

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

### Finding 1 — a rule that carries information works, on both agents

The fixture is a small checkout module. The task asks for a `format_price(cents)`
function "for the display string shown to customers at checkout." The rule says
house prices render as `12.50 USD`, never with a symbol. Nothing in the code,
the tests, or the prompt mentions presentation; the convention exists only in
the instruction file.

Without the rule, Claude Code wrote `$12.50` in 9 of 10 attempts (the tenth
wrote a bare `12.50`). With it, all 10 matched the house format. Codex, given
the same rule through `AGENTS.md`, went from 0 of 5 to 5 of 5.

The rule also made the work cheaper. Across the Claude Code arms:

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

The practical reading: a convention that matters should be written down, even
when the code already demonstrates it somewhere nearby. "The agent will pick it
up from the codebase" held only 3 times in 10.

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
- **Shell commands were denied.** Trials ran with Claude Code's `acceptEdits`
  permission mode, which in non-interactive runs approves file edits and refuses
  shell commands. Agents could read and edit, not run their own tests. Both
  arms ran under the same restriction.
- **Delivery was proven by behaviour, not by tokens.** contexttest's passive
  delivery check compares input tokens across arms. For rules this short, trial
  to trial variation (about ±1,200 tokens) is larger than the rule itself
  (about 67), so the check correctly reports `unknown`. Delivery is shown
  instead by the rule arms following the rule in 25 of 25 attempts.
- **The positive control proves the harness, not the rule genre.** A rule
  carrying a fact the agent cannot infer will always look effective. The useful
  result is the contrast with the rules that restate defaults.

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

`doctor` confirms how the instructions will reach the agent before anything is
spent. Every Claude Code trial in this round cost **$13.85 in total**, about
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
