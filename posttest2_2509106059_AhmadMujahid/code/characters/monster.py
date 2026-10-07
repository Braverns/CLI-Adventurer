from utils.stats import Stats
from characters.character import Character

class Monster(Character):
    def __init__(self, name: str, stats: Stats, rarity: str, monster_type: str) -> None:
        super().__init__(name, stats)
        self.rarity = rarity
        self.monster_type = monster_type

    def get_info(self) -> str:
        return (f"Monster: {self.name} | " f"Rarity: {self.rarity} | " f"Type: {self.monster_type}")
        

    