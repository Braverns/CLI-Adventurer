from __future__ import annotations

from functools import partial
from content.balance import sell_price
from core.models import Choice, EventResult
from events.event import Event

class MerchantEvent(Event):
    def __init__(self, stock: list) -> None:
        super().__init__("opening_merchant", "Pedagang Fernley", "Pedagang menawarkan perlengkapan perjalanan.")
        self.stock = list(stock)

    def _actions(self, session) -> dict:
        player = session.player
        actions = {"leave": (Choice("leave", "Lanjutkan perjalanan"), self._leave)}
        for index, item in enumerate(self.stock):
            enabled = player.gold >= item.price and player.inventory.check_slot()
            choice = Choice(f"buy:{index}", f"Beli {item.name}: {item.price} gold", enabled,
                            "Gold tidak cukup atau inventory penuh")
            actions[choice.choice_id] = (choice, partial(self._buy, index))
        for index, item in enumerate(player.inventory.items):
            if item is not None:
                choice = Choice(f"sell:{index}", f"Jual slot {index}: {item.name}, {sell_price(item)} gold")
                actions[choice.choice_id] = (choice, partial(self._sell, index))
        return actions

    def get_choices(self, session) -> list:
        return [choice for choice, action in self._actions(session).values()]

    def resolve(self, session, choice_id: str, payload=None) -> EventResult:
        self.validate_choice(session, choice_id)
        return self._actions(session)[choice_id][1](session)

    def _buy(self, index: int, session) -> EventResult:
        item = self.stock[index]
        player = session.player
        if player.gold < item.price or not player.inventory.check_slot():
            raise ValueError("Transaksi tidak memenuhi syarat")
        player.inventory.add_item(item)
        player.spend_gold(item.price)
        self.stock.pop(index)
        return EventResult([f"Membeli {item.name} seharga {item.price} gold."])

    def _sell(self, slot: int, session) -> EventResult:
        item = session.player.inventory.get_item(slot)
        price = sell_price(item)
        session.player.inventory.remove_item(slot)
        session.player.gain_gold(price)
        self.stock.append(item)
        return EventResult([f"Menjual {item.name} seharga {price} gold."])

    def _leave(self, session) -> EventResult:
        return EventResult(["Kamu meninggalkan pedagang."], completed=True, outcome_id="done")
