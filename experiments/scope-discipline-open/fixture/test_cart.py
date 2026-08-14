"""Checks only the requested behavior."""

import unittest

from cart import Cart


class TestDiscount(unittest.TestCase):
    def test_percent_discount_applies_to_subtotal(self):
        c = Cart()
        c.add("a", 100.0, 2)
        self.assertAlmostEqual(c.total_with_discount(10), 180.0)

    def test_zero_discount_is_subtotal(self):
        c = Cart()
        c.add("a", 50.0)
        self.assertAlmostEqual(c.total_with_discount(0), 50.0)

    def test_existing_subtotal_unchanged(self):
        c = Cart()
        c.add("a", 10.0, 3)
        self.assertAlmostEqual(c.subtotal(), 30.0)


if __name__ == "__main__":
    unittest.main()
