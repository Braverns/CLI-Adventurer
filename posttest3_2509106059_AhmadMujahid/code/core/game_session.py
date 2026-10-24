from random import Random
from characters.combatant import Combatant
from combat.battle import Battle
from content.balance import COMBAT_MAX_HEALTH
from content.endings import ENDINGS
from core.enums import FlowPhase, RunStatus
from core.event_director import EventDirector
from core.models import Choice, EndingResult
from story.missing_apple import MissingAppleQuest

class GameSession:
    def __init__(self, player, rng=None) -> None:
        self.player = player
        self.rng = rng if rng is not None else Random()
        self.director = EventDirector()
        self.quest = MissingAppleQuest()
        self.status = RunStatus.NOT_STARTED
        self.active_event = None
        self.active_battle = None
        self.ending = None
        self._pending_result = None
        self._pending_items = []
        self._completed_events = set()

    def start(self) -> list[str]:
        if self.status is not RunStatus.NOT_STARTED:
            raise ValueError("Petualangan sudah dimulai")
        self.status = RunStatus.ACTIVE
        self.active_event = self.director.create_next_event(self)
        return ["Akhetaria telah menyatukan lima benua. Di Fernley, usia 15 tahun menandai kedewasaan.",
                "Kamu memilih menjadi petualang di satu-satunya guild kota ini."]

    def _require_active(self) -> None:
        if self.status is not RunStatus.ACTIVE:
            raise ValueError("Petualangan tidak aktif")

    @property
    def has_pending_reward(self) -> bool:
        return bool(self._pending_items)

    def get_choices(self) -> list:
        if self.status is not RunStatus.ACTIVE or self.active_battle is not None:
            return []
        if self._pending_items:
            choices = [Choice("skip_reward", "Tinggalkan hadiah")]
            choices.extend(Choice(f"replace_reward:{index}", f"Buang {item.name}, ambil hadiah")
                           for index, item in enumerate(self.player.inventory.items) if item is not None)
            return choices
        return self.active_event.get_choices(self)

    def choose(self, choice_id: str, payload=None) -> list[str]:
        self._require_active()
        if self.active_battle is not None:
            raise ValueError("Selesaikan battle terlebih dahulu")
        choices = {choice.choice_id: choice for choice in self.get_choices()}
        if choice_id not in choices or not choices[choice_id].enabled:
            raise ValueError("Pilihan tidak tersedia atau terkunci")
        if self._pending_items:
            return self._resolve_reward(choice_id)
        result = self.active_event.resolve(self, choice_id, payload)
        return self._apply_result(result)

    def _resolve_reward(self, choice_id: str) -> list[str]:
        item = self._pending_items.pop(0)
        if choice_id != "skip_reward":
            slot = int(choice_id.partition(":")[2])
            old = self.player.inventory.remove_item(slot)
            self.player.inventory.add_item(item)
            messages = [f"{old.name} dilepas. Mendapat {item.name}."]
        else:
            messages = [f"{item.name} ditinggalkan."]
        if not self._pending_items:
            result, self._pending_result = self._pending_result, None
            messages += self._complete_event(result)
        return messages

    def _apply_result(self, result) -> list[str]:
        messages = list(result.messages)
        if result.battle_request is not None:
            monster = result.battle_request
            self.active_battle = Battle(Combatant(self.player, COMBAT_MAX_HEALTH),
                                        Combatant(monster, monster.max_health), self.rng)
            return messages + [f"Battle dimulai: {monster.name}. HP combat dipulihkan penuh."]
        for item in result.granted_items:
            if self.player.inventory.check_slot():
                self.player.inventory.add_item(item)
                messages.append(f"Mendapat {item.name}.")
            else:
                self._pending_items.append(item)
        if self._pending_items:
            self._pending_result = result
            return messages + ["Inventory penuh. Pilih barang yang dibuang atau tinggalkan hadiah."]
        if result.completed:
            messages += self._complete_event(result)
        return messages

    def _complete_event(self, result) -> list[str]:
        event_id = self.active_event.event_id
        if event_id in self._completed_events:
            raise ValueError("Hasil event sudah diproses")
        self._completed_events.add(event_id)
        self.active_event._completed = True
        self.director.record_event_completion(result)
        if result.ending_id:
            self.finish_run(result.ending_id)
        else:
            self.active_event = self.director.create_next_event(self)
        return []

    def step_battle(self) -> list[str]:
        self._require_active()
        if self.active_battle is None:
            return []
        battle = self.active_battle
        messages = battle.step()
        if not battle.finished:
            return messages
        result = battle.get_result()
        self.active_battle = None
        if result.winner.owner is self.player:
            monster = result.loser.owner
            self.player.gain_gold(monster.gold_reward)
            levels = self.player.gain_experience(monster.exp_reward)
            self.player.trait_manager.trigger_reward(self.player)
            messages.append(f"Hadiah: {monster.gold_reward} gold dan {monster.exp_reward} EXP.")
            if levels:
                messages.append(f"Naik {levels} level. Mendapat {levels * 5} poin stat.")
        else:
            self.player.lose_life()
            messages.append(f"Kalah battle: kehilangan 1 nyawa. Sisa {self.player.lives}.")
            if self.player.lives == 0:
                self.finish_run("DEAD")
                return messages
        return messages + self._apply_result(self.active_event.on_battle_finished(self, result))

    def finish_run(self, ending_id: str) -> None:
        title, text = ENDINGS[ending_id]
        self.ending = EndingResult(ending_id, title, text, self.player.lives,
                                   self.player.level, self.player.gold, self.quest.status.value,
                                   tuple(sorted(self.player.reputation)))
        self.status = RunStatus.FINISHED
        self.director.phase = FlowPhase.FINISHED
        self.active_battle = None
        self.active_event = None

    def allocate_points(self, stat_name: str, amount: int) -> None:
        self._require_management()
        self.player.allocate_stat_points(stat_name, amount)

    def equip(self, inventory_slot: int, target_slot=None) -> None:
        self._require_management()
        self.player.equip_from_inventory(inventory_slot, target_slot)

    def unequip(self, slot) -> None:
        self._require_management()
        self.player.equipment.unequip_to_inventory(self.player, slot)

    def _require_management(self) -> None:
        self._require_active()
        if self.active_battle is not None or self.has_pending_reward:
            raise ValueError("Pengelolaan karakter tidak tersedia saat battle atau pemilihan hadiah")
