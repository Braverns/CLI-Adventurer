from content.balance import require_integer

class Item:
    def __init__(self, name: str, price: int = 0, description: str = "", item_id: str = "") -> None:
        require_integer(price, "Harga")
        self.name = name
        self.price = price
        self.description = description
        self.item_id = item_id or name.lower().replace(" ", "_")

    def __str__(self) -> str:
        return f"{self.name} | Harga: {self.price} | {self.description}"
