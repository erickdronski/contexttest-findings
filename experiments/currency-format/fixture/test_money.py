"""Tests for the money helpers."""

import unittest

from money import add, apply_percent_off, format_price


class TestMoney(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(100, 250, 5), 355)

    def test_percent_off_rounds_down_to_the_cent(self):
        self.assertEqual(apply_percent_off(999, 10), 900)

    def test_format_price_shows_two_decimals(self):
        self.assertIn("12.50", format_price(1250))


if __name__ == "__main__":
    unittest.main()
