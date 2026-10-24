import argparse
import shlex
from random import Random

from cli.console import describe_options, show_box
from content.catalog import create_player
from core.enums import EquipmentSlot, RunStatus
from core.game_session import GameSession

def show_inventory(session) -> None:
    player = session.player
    lines = [f"Terpakai: {len(player.inventory)}/{player.inventory.max_item}"]
    lines.extend(f"Slot {index}: {item}" for index, item in enumerate(player.inventory.items) if item is not None)
    lines.append("Equipment:")
    for slot in EquipmentSlot:
        item = player.equipment.get_equipped(slot)
        lines.append(f"{slot.value}: {item.name if item else 'kosong'}")
    lines.append("Trait aktif:")
    lines.extend(f"{entry.trait.name} x{entry.stack}" for entry in player.trait_manager.traits.values())
    show_box("INVENTORY & EQUIPMENT", lines)

def show_profile(session) -> None:
    show_box("KARAKTER", [session.player.get_info(), str(session.player.stats),
                         f"Quest: {session.quest.status.value}",
                         "Reputasi: " + (", ".join(sorted(session.player.reputation)) or "belum ada")])

def manage_equip(session, args) -> None:
    if len(args) not in (1, 2):
        raise ValueError("Gunakan equip SLOT_INVENTORY [SLOT_EQUIPMENT]")
    target = EquipmentSlot(args[1]) if len(args) == 2 else None
    session.equip(int(args[0]), target)
    show_box("EQUIPMENT", ["Item berhasil dipasang."])

def manage_unequip(session, args) -> None:
    if len(args) != 1:
        raise ValueError("Gunakan unequip SLOT_EQUIPMENT")
    session.unequip(EquipmentSlot(args[0]))
    show_box("EQUIPMENT", ["Item dikembalikan ke inventory."])

def manage_points(session, args) -> None:
    if len(args) != 2:
        raise ValueError("Gunakan stat NAMA_STAT JUMLAH")
    session.allocate_points(args[0], int(args[1]))
    show_box("ALOKASI STAT", [f"{args[1]} poin dialokasikan ke {args[0]}.", session.player.get_info()])

def show_help() -> None:
    show_box("BANTUAN", [
        "Masukkan nomor pilihan untuk melanjutkan event.",
        "profil | inventory | bantuan | keluar",
        "equip SLOT_INVENTORY [SLOT_EQUIPMENT]",
        "Contoh: equip 0 main_hand",
        "unequip SLOT_EQUIPMENT",
        "stat NAMA_STAT JUMLAH, contoh: stat strength 5",
        "Stat: strength, agility, defense, intelligence, charisma.",
        "Slot: head, chest, back, legs, boots, main_hand, off_hand.",
        "Kelola equipment dan poin di antara battle. Permainan belum memiliki save/load.",
    ])

def run_game(session) -> None:
    show_box("CLI ADVENTURE - FERNLEY", session.start())
    handlers = {
        "profil": lambda args: show_profile(session),
        "inventory": lambda args: show_inventory(session),
        "equip": lambda args: manage_equip(session, args),
        "unequip": lambda args: manage_unequip(session, args),
        "stat": lambda args: manage_points(session, args),
        "bantuan": lambda args: show_help(),
    }
    while session.status is RunStatus.ACTIVE:
        if session.active_battle is not None:
            logs = []
            while session.active_battle is not None and session.status is RunStatus.ACTIVE:
                logs.extend(session.step_battle())
            show_box("AUTO BATTLE", logs)
            continue
        event = session.active_event
        choices = session.get_choices()
        descriptions = describe_options(choices)
        lines = [session.player.get_info(),
                 f"Hari: {session.director.day} | Waktu: {session.director.time_phase}",
                 event.get_info()]
        if session.has_pending_reward:
            lines.append("Inventory penuh: pilih nasib hadiah.")
        for index, (choice, description) in enumerate(zip(choices, descriptions), 1):
            suffix = "" if choice.enabled else f" [TERKUNCI: {choice.disabled_reason}]"
            lines.append(f"{index}. {description}{suffix}")
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
                show_box("HASIL", session.choose(choices[index].choice_id))
                continue
            parts = shlex.split(command)
            if not parts or parts[0] not in handlers:
                raise ValueError("Perintah tidak dikenal. Ketik bantuan.")
            handlers[parts[0]](parts[1:])
        except (ValueError, IndexError) as error:
            show_box("AKSI DITOLAK", [str(error)])
    ending = session.ending
    show_box(ending.title.upper(), [
        ending.text, session.player.get_info(),
        f"Quest: {ending.quest_status}",
        "Reputasi: " + (", ".join(ending.reputation) or "belum ada"),
        f"Penutup: {ending.ending_id}",
        "Petualangan selesai.",
    ])

def main() -> None:
    parser = argparse.ArgumentParser(description="CLI Adventure - The Missing Apple")
    parser.add_argument("--seed", type=int, default=None, help="Seed untuk mengulangi pilihan event acak")
    parser.add_argument("--name", default=None, help="Nama karakter")
    args = parser.parse_args()
    try:
        name = args.name
        if name is None:
            show_box("SELAMAT DATANG", ["Masukkan nama petualang (kosong: Bravern)."])
            name = input("  > ").strip() or "Bravern"
        if not name.isprintable() or len(name) > 40:
            raise ValueError("Nama harus dapat dicetak dan maksimal 40 karakter")
        run_game(GameSession(create_player(name), Random(args.seed)))
    except (EOFError, KeyboardInterrupt):
        print()
        show_box("SESI DITUTUP", ["Permainan dihentikan."])
    except ValueError as error:
        show_box("DATA TIDAK VALID", [str(error)])

if __name__ == "__main__":
    main()
