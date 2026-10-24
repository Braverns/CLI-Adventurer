from __future__ import annotations
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from cli.console import render_box

class CliTests(unittest.TestCase):
    def play(self, commands):
        result = subprocess.run(
            [sys.executable, "-X", "utf8", str(ROOT / "code/main.py"), "--seed", "7", "--name", "Bravern"],
            input=commands, text=True, encoding="utf-8", capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def test_real_cli_short_ending(self):
        output = self.play("1\n1\n1\n1\n")
        self.assertIn("Penutup: APPLE_GOBLIN_RESOLVED", output)
        self.assertIn("Mendapat 5 poin stat", output)

    def test_real_cli_slayer_with_shop_equipment_and_allocated_points(self):
        output = self.play("1\n4\nequip 0\n1\n4\nstat strength 5\n1\n1\n2\n1\n")
        self.assertIn("Penutup: APPLE_ORC_SLAYER", output)
        self.assertIn("Mendapat Great Sword", output)
        self.assertNotIn("AKSI DITOLAK", output)

    def test_unknown_command_and_eof_are_handled(self):
        output = self.play("tidak_ada\n")
        self.assertIn("AKSI DITOLAK", output)
        self.assertIn("SESI DITUTUP", output)

    def test_boxes_wrap_and_have_equal_width_without_dash_rules(self):
        box = render_box("Judul", ["a" * 200, "", "Dua\nbaris"])
        lengths = {len(line) for line in box.splitlines()}
        self.assertEqual(len(lengths), 1)
        self.assertTrue(box.splitlines()[0].strip().startswith("_"))
        self.assertTrue(box.splitlines()[-1].startswith("|_"))
        self.assertNotIn("---", box)
