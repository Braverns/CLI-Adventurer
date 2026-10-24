class Stats:
    def __init__(self, strength: int, agility: int, defense: int, intelligence: int, charisma: int) -> None:
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

    def __str__(self) -> str:
        return (f"strength: {self.strength} | "
                f"agility: {self.agility} | "
                f"defense: {self.defense} | "
                f"intelligence: {self.intelligence} | "
                f"charisma: {self.charisma}")
