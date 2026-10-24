from dataclasses import dataclass
from core.models import EventResult
from events.event import Event

@dataclass
class StoryNode:
    node_id: str
    text: str
    choices: list
    actions: dict

class StoryEvent(Event):
    def __init__(self, event_id: str, title: str, nodes: dict, first_node: str, battle_handler=None) -> None:
        super().__init__(event_id, title, "")
        self.nodes = nodes
        self.current_node_id = first_node
        self.battle_handler = battle_handler
        self._battle_started = False

    def get_info(self) -> str:
        return f"{self.title}\n{self.nodes[self.current_node_id].text}"

    def get_choices(self, session) -> list:
        if self._battle_started:
            return []
        return self.nodes[self.current_node_id].choices

    def resolve(self, session, choice_id: str, payload=None) -> EventResult:
        self.validate_choice(session, choice_id)
        result = self.nodes[self.current_node_id].actions[choice_id](session)
        if result.battle_request is not None:
            self._battle_started = True
        return result

    def on_battle_finished(self, session, result) -> EventResult:
        if self.battle_handler is None:
            return super().on_battle_finished(session, result)
        return self.battle_handler(session, result)
