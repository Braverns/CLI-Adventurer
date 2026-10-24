from collections import defaultdict
from utils.traits.trait_entry import TraitEntry

class TraitManager:
    def __init__(self) -> None:
        self.traits = {}

    def change_traits(self, removed, added, character) -> None:
        changes = defaultdict(int)
        examples = {}
        for entries, sign in ((removed, -1), (added, 1)):
            for entry in entries:
                changes[type(entry.trait)] += sign * entry.stack
                examples[type(entry.trait)] = entry.trait
        planned = {}
        for trait_type, delta in changes.items():
            existing = self.traits.get(trait_type)
            trait = existing.trait if existing else examples[trait_type]
            total = (existing.stack if existing else 0) + delta
            if not 0 <= total <= trait.max_stack:
                raise ValueError(f"Stack {trait.name} di luar batas")
            planned[trait_type] = (trait, total, delta)
        for trait_type, (trait, total, delta) in planned.items():
            if delta < 0:
                trait.on_remove(character, -delta)
            if delta > 0:
                trait.on_add(character, delta)
            if total:
                self.traits[trait_type] = TraitEntry(trait, total)
            else:
                self.traits.pop(trait_type, None)

    def add_trait(self, trait, character, amount: int) -> None:
        self.change_traits([], [TraitEntry(trait, amount)], character)

    def remove_trait(self, trait, character, amount: int) -> None:
        self.change_traits([TraitEntry(trait, amount)], [], character)

    def trigger_attack(self, attacker, target, rng=None) -> None:
        for entry in self.traits.values():
            method = getattr(entry.trait, "on_attack", None)
            if callable(method):
                method(attacker, target, entry.stack, rng)

    def trigger_reward(self, character) -> None:
        for entry in self.traits.values():
            method = getattr(entry.trait, "on_reward", None)
            if callable(method):
                method(character, entry.stack)
