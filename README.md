<h1 align="center">contexttest-findings</h1>

<p align="center"><strong>Measured results for common <code>AGENTS.md</code> rules.</strong><br>
Real agent runs, published data, null results included.</p>

<p align="center">
  <img alt="MIT license" src="https://img.shields.io/badge/license-MIT-101828">
  <img alt="12 live agent trials" src="https://img.shields.io/badge/live_trials-12-6b21a8">
  <img alt="reproducible" src="https://img.shields.io/badge/reproducible-yes-08775c">
</p>

---

Instruction files are full of rules everyone copies and nobody measures. This
repository runs those rules as experiments with
[contexttest](https://github.com/erickdronski/contexttest) and publishes what
came back — including when the answer is "no measurable difference," which is
most of what has been found so far.

Every number below came from a real agent run. Nothing here is estimated,
simulated, or reasoned about. The raw reports are committed.

## Finding 1 — a scope-discipline rule changed nothing measurable

**The rule under test**, a compressed version of one that appears in a great
many public `AGENTS.md` files:

> Deliver exactly what was asked, and nothing beyond it. Do not add features,
> abstractions, or helpers the task did not request. Do not refactor
> surrounding code that already works. Do not add error handling for cases the
> task did not name.

Two tasks, three paired attempts each, Claude Code as the agent.

| | task success | median diff lines | median changed files | median cost |
|---|---|---|---|---|
| **Task A — add a guard** | | | | |
| no rule | 100% (3/3) | 5 | 1 | $0.0741 |
| with rule | 100% (3/3) | 5 | 1 | $0.0741 |
| **Task B — open-ended feature** | | | | |
| no rule | 100% (3/3) | 3 | 1 | $0.0736 |
| with rule | 100% (3/3) | 3 | 1 | $0.0739 |

**Verdict: tie, both tasks.** Identical success, identical diff size, identical
file count. Exact paired p = 1.000; 3 of 3 pairs passed on both sides.

The interesting part is Task B. It was written specifically to *invite* scope
creep — "add a `total_with_discount(percent)` method" is the kind of request
that tempts a model into input validation, currency rounding policy, a coupon
abstraction, and a docstring essay. The rule was supposed to suppress that.

It had nothing to suppress. **The model produced a 3-line change without the
rule.** On this model and at this task size, the instruction was dead weight —
it cost tokens in every request and bought nothing measurable.

### What this does not show

Stating the limits plainly, because the result is easy to over-read:

- **It is underpowered.** Three pairs per task. With `n=3`, only an enormous
  effect could reach significance, and a real 10–20% effect would be invisible
  here. `p = 1.000` means "no signal at this sample size," not "proven equal."
- **Both tasks were small** — single-file, well-specified, one obvious answer.
  A rule against gold-plating plausibly earns its place on multi-file work,
  vague requests, or long autonomous runs. None of that was tested.
- **One model, one harness.** Results may differ on other models, and almost
  certainly differ on older ones — the rule was probably written *for* a model
  that needed it.
- **Diff size is a proxy for scope creep, not scope creep itself.** A model can
  stay small and still do the wrong thing.

The honest summary: **on small well-specified tasks with a current model, this
popular rule bought nothing.** That is a narrow claim, and it is the one the
data supports.

## Why publish a null result

Because the alternative is a repository that only reports wins, which is how
you end up with instruction files full of rules that survived selection bias
rather than measurement. A rule that does nothing is worth knowing about: it
occupies context in every single request, and context is the scarcest thing an
agent has.

## Reproduce it

```bash
git clone https://github.com/erickdronski/contexttest-findings
cd contexttest-findings
npx github:erickdronski/contexttest run --config experiments/scope-discipline-open/contexttest.json
```

Each experiment is a config, a fixture repository, a candidate instruction
file, and assertions. Trials run in detached git worktrees from the same
commit, so the only thing differing between variants is the instruction
treatment.

Total cost of every trial in this repository: **about $0.89.** Reproducing it
is affordable, which is rather the point — these questions have been unmeasured
because measuring them felt expensive, not because it is.

```
experiments/<name>/
  contexttest.json      the experiment
  AGENTS.candidate.md   the rule being tested
  fixture/              the repository the agent works in, plus its tests
results/<name>/
  report.json           full evidence, every trial
  report.html           standalone readable report
```

## Contributing an experiment

The bar is that a result must be *falsifiable and reproducible*, not that it
must be interesting. Null results are welcome and currently outnumber the
alternatives.

A good experiment isolates one rule, uses a task where the rule could plausibly
matter, and states up front what outcome would count as the rule working. If
you cannot say in advance what "it worked" looks like, the experiment will not
answer anything.

Open an issue with the rule you want tested and the task you think would
discriminate.

## License

MIT.
