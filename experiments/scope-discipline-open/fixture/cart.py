"""A shopping cart."""


class Cart:
    def __init__(self):
        self.lines = []

    def add(self, sku, price, quantity=1):
        self.lines.append({"sku": sku, "price": price, "quantity": quantity})

    def subtotal(self):
        return sum(l["price"] * l["quantity"] for l in self.lines)
