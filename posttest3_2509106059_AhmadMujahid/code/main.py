import argparse
import shlex
from random import Random

from cli.console import describe_options, show_box
from content.catalog import create_player
from core.enums import EquipmentSlot, RunStatus
from core.game_session import GameSession


def show_inventory(session, args = None) -> None:
    player = session.player
    lines = [f"Terpakai: {len(player.inventory)}/{player.inventory.max_item}"]

    for index, item in enumerate(player.inventory.items):
        if item is not None:
            lines.append(f"Slot {index}: {item}")

    lines.append("Equipment:")

    for slot in EquipmentSlot:
        item = player.equipment.get_equipped(slot)
        item_name = "kosong"

        if item is not None:
            item_name = item.name

        lines.append(f"{slot.value}: {item_name}")

    lines.append("Trait aktif:")

    for entry in player.trait_manager.traits.values():
        lines.append(f"{entry.trait.name} x{entry.stack}")

    show_box("INVENTORY & EQUIPMENT", lines)


def show_profile(session, args = None) -> None:
    reputation = ", ".join(sorted(session.player.reputation))

    if not reputation:
        reputation = "belum ada"

    lines = [
        session.player.get_info(),
        str(session.player.stats),
        f"Quest: {session.quest.status.value}",
        f"Reputasi: {reputation}",
    ]

    show_box("KARAKTER", lines)


def manage_equip(session, args) -> None:
    if len(args) not in (1, 2):
        raise ValueError("Gunakan equip SLOT_INVENTORY [SLOT_EQUIPMENT]")

    inventory_slot = int(args[0])
    target_slot = None

    if len(args) == 2:
        target_slot = EquipmentSlot(args[1])

    session.equip(inventory_slot, target_slot)

    show_box("EQUIPMENT", ["Item berhasil dipasang."])


def manage_unequip(session, args) -> None:
    if len(args) != 1:
        raise ValueError("Gunakan unequip SLOT_EQUIPMENT")

    slot = EquipmentSlot(args[0])

    session.unequip(slot)

    show_box("EQUIPMENT", ["Item dikembalikan ke inventory."])


def manage_points(session, args) -> None:
    if len(args) != 2:
        raise ValueError("Gunakan stat NAMA_STAT JUMLAH")

    stat_name = args[0]
    amount = int(args[1])

    session.allocate_points(stat_name, amount)

    show_box("ALOKASI STAT", [f"{amount} poin dialokasikan ke {stat_name}.", session.player.get_info()])


def show_help(session = None, args = None) -> None:
    lines = [
        "Masukkan nomor pilihan untuk melanjutkan event.",
        "profil | inventory | bantuan | keluar",
        "equip SLOT_INVENTORY [SLOT_EQUIPMENT]",
        "Contoh: equip 0 main_hand",
        "unequip SLOT_EQUIPMENT",
        "stat NAMA_STAT JUMLAH, contoh: stat strength 5",
        "Stat: strength, agility, defense, intelligence, charisma.",
        "Slot: head, chest, back, legs, boots, main_hand, off_hand.",
        "Kelola equipment dan poin di antara battle. Permainan belum memiliki save/load.",
    ]

    show_box("BANTUAN", lines)


def run_game(session) -> None:
    opening_messages = session.start()

    show_box("CLI ADVENTURE - FERNLEY", opening_messages)

    handlers = {
        "profil": show_profile,
        "inventory": show_inventory,
        "equip": manage_equip,
        "unequip": manage_unequip,
        "stat": manage_points,
        "bantuan": show_help,
    }

    while session.status is RunStatus.ACTIVE:
        if session.active_battle is not None:
            logs = []

            while session.active_battle is not None and session.status is RunStatus.ACTIVE:
                battle_messages = session.step_battle()

                logs.extend(battle_messages)

            show_box("AUTO BATTLE", logs)

            continue

        event = session.active_event
        choices = session.get_choices()
        descriptions = describe_options(choices)
        lines = [
            session.player.get_info(),
            f"Hari: {session.director.day} | Waktu: {session.director.time_phase}",
            event.get_info(),
        ]

        if session.has_pending_reward:
            lines.append("Inventory penuh: pilih nasib hadiah.")

        for index, choice in enumerate(choices):
            description = descriptions[index]
            suffix = ""

            if not choice.enabled:
                suffix = f" [TERKUNCI: {choice.disabled_reason}]"

            lines.append(f"{index + 1}. {description}{suffix}")

        lines.append("Perintah: profil, inventory, equip, unequip, stat, bantuan, keluar")

        show_box("PETUALANGAN", lines)

        try:
            command = input("  > ").strip()

            if command == "keluar":
                show_box("SAMPAI JUMPA", ["Sesi dihentikan. Progres sesi ini tidak disimpan."])

                return

            if command.isdigit():
                index = int(command) - 1

                if index < 0 or index >= len(choices):
                    raise ValueError("Nomor pilihan tidak tersedia")

                choice_id = choices[index].choice_id
                messages = session.choose(choice_id)

                show_box("HASIL", messages)

                continue

            parts = shlex.split(command)

            if not parts or parts[0] not in handlers:
                raise ValueError("Perintah tidak dikenal. Ketik bantuan.")

            handler = handlers[parts[0]]
            arguments = parts[1:]

            handler(session, arguments)

        except (ValueError, IndexError) as error:
            show_box("AKSI DITOLAK", [str(error)])

    ending = session.ending
    reputation = ", ".join(ending.reputation)

    if not reputation:
        reputation = "belum ada"

    lines = [
        ending.text,
        session.player.get_info(),
        f"Quest: {ending.quest_status}",
        f"Reputasi: {reputation}",
        f"Penutup: {ending.ending_id}",
        "Petualangan selesai.",
    ]

    show_box(ending.title.upper(), lines)


def main() -> None:
    parser = argparse.ArgumentParser(description = "CLI Adventure - The Missing Apple")

    parser.add_argument("--seed", type = int, default = None, help = "Seed untuk mengulangi pilihan event acak")
    parser.add_argument("--name", default = None, help = "Nama karakter")

    args = parser.parse_args()

    try:
        name = args.name

        if name is None:
            show_box("SELAMAT DATANG", ["Masukkan nama petualang (kosong: Bravern)."])

            name = input("  > ").strip()

            if not name:
                name = "Bravern"

        if not name.isprintable() or len(name) > 40:
            raise ValueError("Nama harus dapat dicetak dan maksimal 40 karakter")

        player = create_player(name)
        rng = Random(args.seed)
        session = GameSession(player, rng)

        run_game(session)

    except (EOFError, KeyboardInterrupt):
        print()

        show_box("SESI DITUTUP", ["Permainan dihentikan."])

    except ValueError as error:
        show_box("DATA TIDAK VALID", [str(error)])


if __name__ == "__main__":
    main()
