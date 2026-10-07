from utils.stats import Stats
from utils.traits.trait_manager import TraitManager

class Character:
    def __init__(self, name: str, stats: Stats) -> None:
        self._name = name
        self._stats = stats
        self.__trait_manager: TraitManager = TraitManager()

    @property
    def name(self) -> str:
        return self._name

    @property
    def stats(self) -> Stats:
        return self._stats

    @property
    def trait_manager(self) -> TraitManager:
        return self.__trait_manager

    def get_info(self) -> str:
        return f"Name: {self.name}"



    
