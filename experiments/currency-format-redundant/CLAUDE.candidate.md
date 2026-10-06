# CLAUDE.md

## Displaying money

Customer-facing prices are shown as the amount with exactly two decimal places,
a space, and the ISO currency code — `12.50 USD`. Never use a currency symbol:
the checkout is shown in several countries, and `$` is ambiguous there.
