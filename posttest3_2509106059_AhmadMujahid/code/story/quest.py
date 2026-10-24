from core.enums import QuestStatus


class Quest:
    def __init__(self, quest_id: str, name: str, description: str, deadline_days: int = 3) -> None:
        self.quest_id = quest_id
        self.name = name
        self.description = description
        self.deadline_days = deadline_days
        self._status = QuestStatus.NOT_STARTED
        self.stage = "not_started"

    @property
    def status(self) -> QuestStatus:
        return self._status

    def start(self) -> None:
        if self._status is not QuestStatus.NOT_STARTED:
            raise ValueError("Quest sudah dimulai")

        self._status = QuestStatus.ACTIVE

    def complete(self) -> None:
        if self._status is not QuestStatus.ACTIVE:
            raise ValueError("Quest tidak aktif")

        self._status = QuestStatus.SUCCEEDED

    def fail(self) -> None:
        if self._status is not QuestStatus.ACTIVE:
            raise ValueError("Quest tidak aktif")

        self._status = QuestStatus.FAILED
