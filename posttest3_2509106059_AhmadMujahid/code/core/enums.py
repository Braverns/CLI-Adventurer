from __future__ import annotations

from enum import Enum

class EquipmentSlot(Enum):
    HEAD = "head"
    CHEST = "chest"
    BACK = "back"
    LEGS = "legs"
    BOOTS = "boots"
    MAIN_HAND = "main_hand"
    OFF_HAND = "off_hand"

class FlowPhase(Enum):
    OPENING_ONE = "opening_one"
    OPENING_TWO = "opening_two"
    GOBLIN_STORY = "goblin_story"
    TRAVEL = "travel"
    ORACHULM_STORY = "orachulm_story"
    REPORT = "report"
    FINISHED = "finished"

class QuestStatus(Enum):
    NOT_STARTED = "not_started"
    ACTIVE = "active"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

class RunStatus(Enum):
    NOT_STARTED = "not_started"
    ACTIVE = "active"
    FINISHED = "finished"
