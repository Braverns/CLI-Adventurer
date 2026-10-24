from content.balance import TAVERN_COST
from core.models import Choice, EventResult
from events.event import Event


class TavernEvent(Event):
    def __init__(self, rest_cost: int = TAVERN_COST) -> None:
        super().__init__("opening_tavern", "Tavern Fernley", "Beristirahat dapat memulihkan satu nyawa.")

        self.rest_cost = rest_cost

    def get_choices(self, session) -> list:
        player = session.player
        enabled = player.lives < player.max_lives and player.gold >= self.rest_cost

        return [Choice("rest", f"Istirahat: {self.rest_cost} gold, pulihkan 1 nyawa", enabled, "Nyawa sudah penuh atau gold tidak cukup"), Choice("leave", "Pergi tanpa beristirahat")]

    def resolve(self, session, choice_id: str, payload = None) -> EventResult:
        self.validate_choice(session, choice_id)

        actions = {"rest": self._rest, "leave": self._leave}

        return actions[choice_id](session)

    def _rest(self, session) -> EventResult:
        session.player.spend_gold(self.rest_cost)
        session.player.recover_life()

        return EventResult(["Nyawa pulih satu. Kamu kembali melanjutkan perjalanan."], completed = True, outcome_id = "done")

    def _leave(self, session) -> EventResult:
        return EventResult(["Kamu memilih tidak beristirahat."], completed = True, outcome_id = "done")
