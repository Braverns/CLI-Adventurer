

class Stats:
    def __init__(self, strength: int, agility: int, defense: int, intelligence: int, charisma: int):
        self.strength = strength
        self.agility = agility
        self.defense = defense
        self.intelligence = intelligence
        self.charisma = charisma

    def add(self, bonus) -> None:
        self.strength += bonus.strength
        self.agility += bonus.agility
        self.defense += bonus.defense
        self.intelligence += bonus.intelligence
        self.charisma += bonus.charisma

    @staticmethod
    def is_valid_stat(value: int) -> bool:
        return value >= 0