# currency-format — hypothesis, written before the run

**Role: positive control.** A null result elsewhere in this repository only
means something if the harness can detect an effect when one exists. This
experiment is built so that one should exist.

**The rule** states a house convention — prices render as `12.50 USD`, never
with a symbol — that appears nowhere in the fixture. The code, the tests, and
the prompt are all silent on presentation. The only place the convention exists
is the instruction file.

**The task** asks for a `format_price(cents)` function for the checkout page.
The visible tests check only that the result contains `12.50`. A hidden
assertion, stored in the experiment config (which the trial worktree does not
contain), checks the exact house format for three amounts.

**Prediction.** Without the rule, the agent writes the conventional `$12.50`
and fails the hidden check in most attempts. With the rule, it passes in most
attempts.

**What counts as the rule working:** with-rule success exceeds no-rule success
by at least 60 percentage points across five paired attempts.

**What would falsify the harness rather than the rule:** if both arms fail or
both arms pass at similar rates, either the rule did not reach the model or the
hidden check leaked. Per-request input tokens are compared across arms to
distinguish the two.
