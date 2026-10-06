"""Money helpers for the checkout service.

All amounts are integer cents. Floats never touch money in this module.
"""


def add(*amounts):
    """Sum any number of amounts."""
    return sum(amounts)


def apply_percent_off(amount, percent):
    """Reduce an amount by a whole-number percentage, rounding down to the cent."""
    return amount - amount * percent // 100


def format_receipt_total(amount):
    """Render the order total for the emailed receipt, e.g. 12.50 USD."""
    return "%d.%02d USD" % (amount // 100, amount % 100)
