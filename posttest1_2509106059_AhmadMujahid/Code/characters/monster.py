from utils.stats import Stats

class Monster:
    def __init__(self, name: str, rarity: str, monster_type: str, health: float | int, stats: Stats):
        self.name = name
        self.rarity = rarity
        self.monster_type = monster_type
        self.health = health
        self.stats = stats

    def take_damage(self, damage: float | int) -> None:
        self.health -= damage

    def is_alive(self) -> bool:
        return self.health > 0
    
    @property
    def health(self) -> float | int:
        return self.__health

    @health.setter
    def health(self, amount: float | int) -> None:
        if amount < 0:
            self.__health = 0
        else:
            self.__health = amount

    def attack(self, target) -> None:
        target.take_damage(self.stats.strength)