from utils.stats import Stats
from characters.classes.profession import Profession
from utils.trait import TraitsManajer

class Player:
    def __init__(self, name: str, level: int, health: float | int, profession: Profession, stats: Stats):
        self.name = name
        self.level = level
        self.health = health
        self.profession = profession
        self.stats = stats
        self.traits_manager: TraitsManajer = TraitsManajer()

        self.__apply_profession_stats()

    def __apply_profession_stats(self) -> None:
        self.stats.add(self.profession.stats)

    def take_damage(self, damage: float | int) -> None:
        self.health -= damage

    def is_alive(self) -> bool:
        return self.health > 0
    
    @property
    def health(self) -> float | int:
        return self.__health

    @health.setter
    def health(self, amount: float | int ) -> None:
        if amount < 0:
            self.__health = 0
        else:
            self.__health = amount

    def attack(self, target) -> None:
        target.take_damage(self.stats.strength)



