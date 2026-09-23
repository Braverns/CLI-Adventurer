from utils.stats import Stats

class Profession:
    def __init__(self, name: str, stats: Stats) -> None:
        self.name = name
        self.stats = stats

    @classmethod
    def create_default(cls, name: str):
        return cls(name, Stats(0, 0, 0, 0, 0))