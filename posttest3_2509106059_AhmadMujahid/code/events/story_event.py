from core.models import EventResult
from events.event import Event


class StoryNode:
    def __init__(self, node_id: str, text: str, choices: list, actions: dict) -> None:
        self.node_id = node_id
        self.text = text
        self.choices = choices
        self.actions = actions


class StoryEvent(Event):
    def __init__(self, event_id: str, title: str, nodes: dict, first_node: str, battle_handler = None) -> None:
        super().__init__(event_id, title, "")

        self.nodes = nodes
        self.current_node_id = first_node
        self.battle_handler = battle_handler
        self._battle_started = False

    def get_info(self) -> str:
        node = self.nodes[self.current_node_id]

        return f"{self.title}\n{node.text}"

    def get_choices(self, session) -> list:
        if self._battle_started:
            return []

        node = self.nodes[self.current_node_id]

        return node.choices

    def resolve(self, session, choice_id: str, payload = None) -> EventResult:
        self.validate_choice(session, choice_id)

        node = self.nodes[self.current_node_id]
        action = node.actions[choice_id]
        result = action(session)

        if result.battle_request is not None:
            self._battle_started = True

        return result

    def on_battle_finished(self, session, result) -> EventResult:
        if self.battle_handler is None:
            return super().on_battle_finished(session, result)

        return self.battle_handler(session, result)
