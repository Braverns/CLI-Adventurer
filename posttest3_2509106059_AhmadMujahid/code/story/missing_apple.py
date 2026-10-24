from functools import partial
from content.balance import INTERROGATION_DIFFICULTY, QUEST_EXP, QUEST_GOLD, check_success
from content.catalog import create_goblin, create_orachulm
from core.models import Choice, ConditionalChoice, EventResult
from events.story_event import StoryEvent, StoryNode
from items.weapon import GreatSword
from story.quest import Quest

class MissingAppleQuest(Quest):
    def __init__(self) -> None:
        super().__init__("missing_apple", "The Missing Apple",
                         "Pak Warrey kehilangan apel dari panennya. Selidiki pencurian dalam tiga hari.")
        self.knows_orachulm = False
        self.orachulm_outcome = "not_met"

    def create_goblin_event(self) -> StoryEvent:
        self.start()
        self.stage = "goblin"
        choices = [Choice("attack", "Langsung serang goblin")]
        actions = {"attack": self._attack_goblin}
        approaches = {"cha": ("charisma", "Bujuk goblin untuk bicara"),
                      "int": ("intelligence", "Jebak percakapannya dengan pertanyaan"),
                      "str": ("strength", "Intimidasi goblin")}
        for key, (stat, label) in approaches.items():
            choices.append(ConditionalChoice(key, label, stat, INTERROGATION_DIFFICULTY))
            actions[key] = partial(self._interrogate, stat)
        node = StoryNode("goblin",
                         f"{self.description}\nQuest diterima. Malam pertama, kamu berjaga di ladang. "
                         "Seekor goblin membawa apel sambil bergumam tentang persembahan kepada-Nya.",
                         choices, actions)
        return StoryEvent("apple_goblin", self.name, {"goblin": node}, "goblin", self._goblin_result)

    def _attack_goblin(self, session) -> EventResult:
        return EventResult(["Goblin bersiap melawanmu."], battle_request=create_goblin())

    def _interrogate(self, stat: str, session) -> EventResult:
        success = check_success(getattr(session.player.stats, stat), INTERROGATION_DIFFICULTY, session.rng)
        self.knows_orachulm = success
        text = ("Goblin menyebut Orachulm dan tempatnya di dalam hutan."
                if success else "Goblin menolak membocorkan rahasianya.")
        return EventResult([text, "Goblin menyerang!"], battle_request=create_goblin())

    def _goblin_result(self, session, result) -> EventResult:
        if result.winner.owner is not session.player:
            self.fail()
            return EventResult(["Kamu gagal menghentikan goblin. Quest gagal."], True,
                               "failed", ending_id="APPLE_FAILED")
        outcome = "informed" if self.knows_orachulm else "uninformed"
        self.stage = "travel" if self.knows_orachulm else "report"
        return EventResult(["Goblin berhasil dikalahkan."], True, outcome)

    def create_orachulm_event(self) -> StoryEvent:
        self.stage = "orachulm"
        node = StoryNode("orachulm",
                         "Malam hari kedua. Di tempat yang disebut goblin, kamu menemukan sosok hijau "
                         "besar dengan taring bawah: orc bernama Orachulm.",
                         [Choice("report", "Kembali dan laporkan hasil penyelidikan"),
                          Choice("fight", "Lawan Orachulm")],
                         {"report": self._return, "fight": self._fight_orachulm})
        return StoryEvent("apple_orachulm", "Orachulm", {"orachulm": node},
                          "orachulm", self._orachulm_result)

    def _return(self, session) -> EventResult:
        self.orachulm_outcome = "reported"
        return EventResult(["Kamu membawa informasi kembali kepada Pak Warrey."], True, "done")

    def _fight_orachulm(self, session) -> EventResult:
        return EventResult(battle_request=create_orachulm())

    def _orachulm_result(self, session, result) -> EventResult:
        if result.winner.owner is session.player:
            self.orachulm_outcome = "slayer"
            session.player.reputation.add("Orc Slayer")
            return EventResult(["Orachulm tumbang. Kamu dikenal sebagai Orc Slayer."],
                               True, "done", granted_items=[GreatSword()])
        self.orachulm_outcome = "escaped"
        return EventResult(["Kamu berhasil kabur dan tetap dapat melaporkan hasil penyelidikan."],
                           True, "done")

    def create_report_event(self) -> StoryEvent:
        node = StoryNode("report", "Pak Warrey menunggu hasil penyelidikanmu.",
                         [Choice("report", "Laporkan hasil penyelidikan")], {"report": self._report})
        return StoryEvent("apple_report", "Laporan kepada Pak Warrey", {"report": node}, "report")

    def _report(self, session) -> EventResult:
        self.complete()
        self.stage = "finished"
        session.player.gain_gold(QUEST_GOLD)
        levels = session.player.gain_experience(QUEST_EXP)
        endings = {"not_met": "APPLE_GOBLIN_RESOLVED", "reported": "APPLE_ORC_REPORTED",
                   "escaped": "APPLE_ORC_ESCAPED", "slayer": "APPLE_ORC_SLAYER"}
        messages = [f"Quest berhasil. Hadiah {QUEST_GOLD} gold dan {QUEST_EXP} EXP."]
        if levels:
            messages.append(f"Naik {levels} level, memperoleh {levels * 5} poin stat.")
        return EventResult(messages, True, "reported", ending_id=endings[self.orachulm_outcome])
