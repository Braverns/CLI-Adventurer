import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cli.console import describe_options, show_box
from characters.combatant import Combatant
from content.catalog import create_goblin, create_player, create_stock
from content.short_stories import create_short_story
from core.game_session import GameSession
from core.models import Choice, ConditionalChoice
from events.event import Event
from events.merchant_event import MerchantEvent
from events.monster_event import MonsterEvent
from events.tavern_event import TavernEvent
from inventory.inventory import Inventory
from items.item import Item

def demonstrate_abstraction() -> None:
    try:
        Event("abstract", "Event abstrak", "Tidak dapat dibuat langsung")
    except TypeError as error:
        show_box("1. BUKTI ABSTRAKSI", [type(error).__name__ + ": " + str(error),
                                     "Event wajib mengimplementasikan get_choices() dan resolve()."])
    else:
        raise AssertionError("ABC seharusnya tidak dapat diinstansiasi")

def demonstrate_polymorphism() -> None:
    session = GameSession(create_player())
    session.player.lose_life()
    events = [MonsterEvent("demo_monster", create_goblin()), TavernEvent(),
              MerchantEvent(create_stock()), create_short_story()]
    lines = []
    # Satu loop, objek subclass berbeda, method yang sama.
    for event in events:
        choices = event.get_choices(session)
        choice = next(option for option in choices if option.enabled)
        result = event.resolve(session, choice.choice_id)
        lines.append(f"{type(event).__name__}.get_choices(): {choice.describe()}")
        lines.append(f"resolve(): battle={result.battle_request is not None}, selesai={result.completed}")
        lines.extend(result.messages)
        lines.append("validate_choice() konkret dari Event dipakai sebelum resolusi.")
    show_box("2. POLIMORFISME VIA PEWARISAN", lines)

def demonstrate_duck_typing() -> None:
    normal = Choice("attack", "Serang langsung")
    checked = ConditionalChoice("cha", "Bujuk goblin", "charisma", 18)
    assert not issubclass(Choice, ConditionalChoice)
    assert not issubclass(ConditionalChoice, Choice)
    show_box("3. DUCK TYPING", [
        "Choice dan ConditionalChoice tidak saling mewarisi dan tidak memiliki parent aplikasi bersama.",
        "Keduanya dipanggil melalui describe_options(), yang hanya memakai describe().",
        *describe_options([normal, checked]),
    ])

def demonstrate_dunder_and_relationships() -> None:
    player = create_player()
    other = create_player("Arthur")
    item = Item("Apel", 4, "Contoh item mandiri")
    inventory = Inventory()
    inventory.add_item(item)
    count = len(inventory)
    inventory.remove_item(0)
    attacker, target = Combatant(player, 100), Combatant(create_goblin(), 100)
    damage = attacker.attack(target)
    show_box("4. MAGIC METHOD DAN RELASI", [
        f"str(Item): {item}",
        f"str(Stats): {player.stats}",
        f"len(Inventory): {count} sebelum dihapus, {len(inventory)} setelah dihapus.",
        f"Agregasi: item tetap ada sesudah dikeluarkan: {item.name}.",
        f"Asosiasi: Combatant.attack(target) menghasilkan {damage} damage.",
        f"Komposisi: inventory dua pemain berbeda: {player.inventory is not other.inventory}.",
        "Player membuat Inventory dan Equipment-nya sendiri di constructor.",
    ])

def demonstrate_level() -> None:
    player = create_player()
    levels = player.gain_experience(65)
    show_box("5. POIN STAT PER LEVEL", [
        f"65 EXP menghasilkan kenaikan {levels} level.",
        f"Level: {player.level} | Poin stat: {player.stat_points} | Sisa EXP: {player.experience}",
        "Setiap kenaikan level selalu memberi tepat 5 poin stat.",
    ])

def main() -> None:
    demonstrate_abstraction()
    demonstrate_polymorphism()
    demonstrate_duck_typing()
    demonstrate_dunder_and_relationships()
    demonstrate_level()

if __name__ == "__main__":
    main()
