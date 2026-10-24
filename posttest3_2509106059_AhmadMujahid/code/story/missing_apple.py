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
        choices = [
            Choice("attack", "Langsung serang goblin"),
            ConditionalChoice("cha", "Bujuk goblin untuk bicara", "charisma", INTERROGATION_DIFFICULTY),
            ConditionalChoice("int", "Jebak percakapannya dengan pertanyaan", "intelligence", INTERROGATION_DIFFICULTY),
            ConditionalChoice("str", "Intimidasi goblin", "strength", INTERROGATION_DIFFICULTY),
        ]
        actions = {
            "attack": self._attack_goblin,
            "cha": self._interrogate_cha,
            "int": self._interrogate_int,
            "str": self._interrogate_str,
        }
        text = (f"{self.description}\nQuest diterima. Malam pertama, kamu berjaga di ladang. "
                "Seekor goblin membawa apel sambil bergumam tentang persembahan kepada-Nya.")
        node = StoryNode("goblin", text, choices, actions)
        nodes = {"goblin": node}

        return StoryEvent("apple_goblin", self.name, nodes, "goblin", self._goblin_result)

    def _attack_goblin(self, session) -> EventResult:
        monster = create_goblin()

        return EventResult(["Goblin bersiap melawanmu."], battle_request = monster)

    def _interrogate_cha(self, session) -> EventResult:
        return self._interrogate(session.player.stats.charisma, session)

    def _interrogate_int(self, session) -> EventResult:
        return self._interrogate(session.player.stats.intelligence, session)

    def _interrogate_str(self, session) -> EventResult:
        return self._interrogate(session.player.stats.strength, session)

    def _interrogate(self, stat_value: int, session) -> EventResult:
        success = check_success(stat_value, INTERROGATION_DIFFICULTY, session.rng)
        self.knows_orachulm = success

        if success:
            text = "Goblin menyebut Orachulm dan tempatnya di dalam hutan."
        else:
            text = "Goblin menolak membocorkan rahasianya."

        monster = create_goblin()

        return EventResult([text, "Goblin menyerang!"], battle_request = monster)

    def _goblin_result(self, session, result) -> EventResult:
        if result.winner.owner is not session.player:
            self.fail()

            return EventResult(["Kamu gagal menghentikan goblin. Quest gagal."], True,
                               "failed", ending_id = "APPLE_FAILED")

        if self.knows_orachulm:
            outcome = "informed"
            self.stage = "travel"
        else:
            outcome = "uninformed"
            self.stage = "report"

        return EventResult(["Goblin berhasil dikalahkan."], True, outcome)

    def create_orachulm_event(self) -> StoryEvent:
        self.stage = "orachulm"
        text = ("Malam hari kedua. Di tempat yang disebut goblin, kamu menemukan sosok hijau "
                "besar dengan taring bawah: orc bernama Orachulm.")
        choices = [
            Choice("report", "Kembali dan laporkan hasil penyelidikan"),
            Choice("fight", "Lawan Orachulm"),
        ]
        actions = {
            "report": self._return,
            "fight": self._fight_orachulm,
        }
        node = StoryNode("orachulm", text, choices, actions)
        nodes = {"orachulm": node}

        return StoryEvent("apple_orachulm", "Orachulm", nodes, "orachulm", self._orachulm_result)

    def _return(self, session) -> EventResult:
        self.orachulm_outcome = "reported"

        return EventResult(["Kamu membawa informasi kembali kepada Pak Warrey."], True, "done")

    def _fight_orachulm(self, session) -> EventResult:
        monster = create_orachulm()

        return EventResult(battle_request = monster)

    def _orachulm_result(self, session, result) -> EventResult:
        if result.winner.owner is session.player:
            self.orachulm_outcome = "slayer"

            session.player.reputation.add("Orc Slayer")

            sword = GreatSword()

            return EventResult(["Orachulm tumbang. Kamu dikenal sebagai Orc Slayer."],
                               True, "done", granted_items = [sword])

        self.orachulm_outcome = "escaped"

        return EventResult(["Kamu berhasil kabur dan tetap dapat melaporkan hasil penyelidikan."],
                           True, "done")

    def create_report_event(self) -> StoryEvent:
        choices = [Choice("report", "Laporkan hasil penyelidikan")]
        actions = {"report": self._report}
        node = StoryNode("report", "Pak Warrey menunggu hasil penyelidikanmu.", choices, actions)
        nodes = {"report": node}

        return StoryEvent("apple_report", "Laporan kepada Pak Warrey", nodes, "report")

    def _report(self, session) -> EventResult:
        self.complete()

        self.stage = "finished"

        session.player.gain_gold(QUEST_GOLD)

        levels = session.player.gain_experience(QUEST_EXP)
        endings = {
            "not_met": "APPLE_GOBLIN_RESOLVED",
            "reported": "APPLE_ORC_REPORTED",
            "escaped": "APPLE_ORC_ESCAPED",
            "slayer": "APPLE_ORC_SLAYER",
        }
        messages = [f"Quest berhasil. Hadiah {QUEST_GOLD} gold dan {QUEST_EXP} EXP."]

        if levels > 0:
            messages.append(f"Naik {levels} level, memperoleh {levels * 5} poin stat.")

        ending_id = endings[self.orachulm_outcome]

        return EventResult(messages, True, "reported", ending_id = ending_id)
