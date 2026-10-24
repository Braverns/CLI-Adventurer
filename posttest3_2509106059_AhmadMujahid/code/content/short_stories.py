from core.models import Choice, EventResult
from events.story_event import StoryEvent, StoryNode


def create_short_story() -> StoryEvent:
    def help_traveler(session):
        session.player.gain_gold(10)
        session.player.gain_experience(5)

        return EventResult(["Kamu mengembalikan surat yang tercecer. Sang pengelana memberi 10 gold dan 5 EXP."],
                           True, "done")

    def leave(session):
        return EventResult(["Pengelana melanjutkan pencariannya. Kamu kembali ke Fernley."], True, "done")

    node = StoryNode("bridge", "Di jembatan Fernley, seorang pengelana kehilangan surat untuk keluarganya. "
                     "Kamu melihat surat tersangkut di bawah bangku.",
                     [Choice("help", "Bantu mengambil dan mengembalikan surat"),
                      Choice("leave", "Lanjutkan perjalanan")],
                     {"help": help_traveler, "leave": leave})

    return StoryEvent("opening_letter", "Surat di Jembatan", {"bridge": node}, "bridge")
