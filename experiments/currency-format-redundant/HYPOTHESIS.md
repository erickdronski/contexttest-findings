# currency-format-redundant — hypothesis, written before the run

**Role: the contrast to `currency-format`.** Same rule, same prompt, same hidden
check. One difference: the fixture already contains `format_receipt_total`,
which renders `12.50 USD`. The convention is now visible in the code.

**Prediction.** Without the rule, the agent reads the module, matches the
existing function's format, and passes most attempts. The rule restates what the
code already shows, so it adds little or nothing.

**What counts as the rule working:** with-rule success exceeds no-rule success
by at least 40 percentage points across five paired attempts. We expect it not
to.

**Why run it.** If `currency-format` shows a large effect and this shows none,
the pair says something more useful than either alone: an instruction earns its
place when it carries information the repository does not, and is dead weight
when it repeats what the code already demonstrates.

**What would complicate that reading:** a no-rule agent that writes `$12.50`
despite the neighbouring function — checkout and receipts are different
surfaces, and a model could reasonably treat them differently. If that happens
it is a finding about how far models generalize a local convention, and it is
reported as such.
