from characters.character import Character
from utils.stats import Stats

class Monster(Character):
    def __init__(self, name: str, stats: Stats, rarity: str = "Common", monster_type: str = "Physical",
                 exp_reward: int = 10, gold_reward: int = 15, max_health: int = 60) -> None:
        super().__init__(name, stats)
        self.rarity = rarity
        self.monster_type = monster_type
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.max_health = max_health

    def get_info(self) -> str:
        return f"Monster: {self.name} | Rarity: {self.rarity} | Type: {self.monster_type}"
