class Choice:
    def __init__(self, choice_id: str, label: str, enabled: bool = True, disabled_reason: str = "") -> None:
        self.choice_id = choice_id
        self.label = label
        self.enabled = enabled
        self.disabled_reason = disabled_reason

    def describe(self) -> str:
        return self.label


class ConditionalChoice:
    def __init__(self, choice_id: str, label: str, required_stat: str, difficulty: int,
                 enabled: bool = True, disabled_reason: str = "") -> None:
        self.choice_id = choice_id
        self.label = label
        self.required_stat = required_stat
        self.difficulty = difficulty
        self.enabled = enabled
        self.disabled_reason = disabled_reason

    def describe(self) -> str:
        return f"{self.label} [{self.required_stat.upper()}, kesulitan {self.difficulty}]"


class EventResult:
    def __init__(self, messages = None, completed: bool = False, outcome_id: str = "",
                 battle_request = None, granted_items = None, ending_id: str = "") -> None:
        self.messages = []
        self.granted_items = []

        if messages is not None:
            self.messages = list(messages)

        if granted_items is not None:
            self.granted_items = list(granted_items)

        self.completed = completed
        self.outcome_id = outcome_id
        self.battle_request = battle_request
        self.ending_id = ending_id


class BattleResult:
    def __init__(self, winner, loser) -> None:
        self.winner = winner
        self.loser = loser


class EndingResult:
    def __init__(self, ending_id: str, title: str, text: str, remaining_lives: int, level: int,
                 gold: int, quest_status: str, reputation: tuple) -> None:
        self.ending_id = ending_id
        self.title = title
        self.text = text
        self.remaining_lives = remaining_lives
        self.level = level
        self.gold = gold
        self.quest_status = quest_status
        self.reputation = reputation
