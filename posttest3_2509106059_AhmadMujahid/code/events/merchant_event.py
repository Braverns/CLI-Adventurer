from content.balance import sell_price
from core.models import Choice, EventResult
from events.event import Event


class MerchantEvent(Event):
    def __init__(self, stock: list) -> None:
        super().__init__("opening_merchant", "Pedagang Fernley", "Pedagang menawarkan perlengkapan perjalanan.")

        self.stock = list(stock)

    def get_choices(self, session) -> list:
        player = session.player
        choices = [Choice("leave", "Lanjutkan perjalanan")]

        for index, item in enumerate(self.stock):
            enabled = player.gold >= item.price and player.inventory.check_slot()
            choice = Choice(f"buy:{index}", f"Beli {item.name}: {item.price} gold", enabled,
                            "Gold tidak cukup atau inventory penuh")

            choices.append(choice)

        for index, item in enumerate(player.inventory.items):
            if item is not None:
                price = sell_price(item)
                choice = Choice(f"sell:{index}", f"Jual slot {index}: {item.name}, {price} gold")

                choices.append(choice)

        return choices

    def resolve(self, session, choice_id: str, payload = None) -> EventResult:
        self.validate_choice(session, choice_id)

        action, separator, index_text = choice_id.partition(":")
        index = None

        if separator:
            index = int(index_text)

        actions = {
            "buy": self._buy,
            "sell": self._sell,
            "leave": self._leave,
        }

        handler = actions[action]

        return handler(session, index)

    def _buy(self, session, index: int) -> EventResult:
        item = self.stock[index]
        player = session.player

        if player.gold < item.price or not player.inventory.check_slot():
            raise ValueError("Transaksi tidak memenuhi syarat")

        player.inventory.add_item(item)
        player.spend_gold(item.price)
        self.stock.pop(index)

        return EventResult([f"Membeli {item.name} seharga {item.price} gold."])

    def _sell(self, session, slot: int) -> EventResult:
        item = session.player.inventory.get_item(slot)
        price = sell_price(item)

        session.player.inventory.remove_item(slot)
        session.player.gain_gold(price)
        self.stock.append(item)

        return EventResult([f"Menjual {item.name} seharga {price} gold."])

    def _leave(self, session, index = None) -> EventResult:
        return EventResult(["Kamu meninggalkan pedagang."], completed = True, outcome_id = "done")
