from characters.character import Character

class Combatant:
    def __init__(self, owner: Character, max_health: float | int) -> None:
        self.owner = owner
        self.health = max_health
        self.max_health = max_health
        self.statuses = []

    @property
    def health(self) -> float | int:
        return self.__health

    @health.setter
    def health(self, amount: float | int) -> None:
        if amount <= 0:
            self.__health = 0
        else:
            self.__health = amount

    def is_alive(self) -> bool:
        return self.health > 0

    def take_damage(self, damage: float | int) -> None:
        self.health -= damage

    def attack(self, target: Combatant) -> None:
        target.take_damage(self.owner.stats.strength)

    def add_status(self, new_status) -> None:
        for status in self.statuses:
            if type(status) == type(new_status):
                status.extend_duration(new_status.duration)
                return

        self.statuses.append(new_status)

    def process_statuses(self) -> None:
        active_statuses = []

        for status in self.statuses:
            status.on_turn(self)

            if status.is_active():
                active_statuses.append(status)

        self.statuses = active_statuses

