"""Behavior check for the requested change, and nothing more."""

import unittest

from inventory import Inventory


class TestRemoveGuard(unittest.TestCase):
    def test_removing_more_than_held_raises(self):
        inv = Inventory()
        inv.add("widget", 3)
        with self.assertRaises(ValueError):
            inv.remove("widget", 5)

    def test_valid_remove_still_works(self):
        inv = Inventory()
        inv.add("widget", 3)
        inv.remove("widget", 2)
        self.assertEqual(inv.count("widget"), 1)

    def test_add_unchanged(self):
        inv = Inventory()
        inv.add("bolt", 4)
        inv.add("bolt", 1)
        self.assertEqual(inv.count("bolt"), 5)


if __name__ == "__main__":
    unittest.main()
