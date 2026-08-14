"""A tiny inventory ledger."""


class Inventory:
    def __init__(self):
        self._items = {}

    def add(self, sku, quantity):
        self._items[sku] = self._items.get(sku, 0) + quantity

    def remove(self, sku, quantity):
        self._items[sku] = self._items.get(sku, 0) - quantity

    def count(self, sku):
        return self._items.get(sku, 0)
