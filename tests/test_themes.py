"""Check color fidelity, generation drift, and non-destructive installation."""
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("generate", ROOT / "scripts/generate.py")
generate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate)


def decode_hex(color):
    lightness = color["lightness"]["exact"]
    chroma = color["chroma"]["exact"]
    hue = color["hue"]["radians"]
    a, b = chroma * math.cos(hue), chroma * math.sin(hue)
    l = (lightness + .3963377774 * a + .2158037573 * b) ** 3
    m = (lightness - .1055613458 * a - .0638541728 * b) ** 3
    s = (lightness - .0894841775 * a - 1.291485548 * b) ** 3
    linear = [
        4.0767416621 * l - 3.3077115913 * m + .2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - .3413193965 * s,
        -.0041960863 * l - .7034186147 * m + 1.707614701 * s,
    ]
    rgb = [12.92 * v if v <= .0031308 else 1.055 * v ** (1 / 2.4) - .055 for v in linear]
    return "#" + "".join(f"{round(v * 255):02x}" for v in rgb)


class ThemeTests(unittest.TestCase):
    def test_all_palette_colors_round_trip(self):
        palettes = json.loads((ROOT / "palettes/catppuccin.json").read_text())
        for flavor in generate.FLAVORS:
            for name, entry in palettes[flavor]["colors"].items():
                with self.subTest(flavor=flavor, color=name):
                    self.assertEqual(decode_hex(generate.to_oklch(entry["hex"])), entry["hex"])

    def test_generated_themes_match_and_have_complete_coverage(self):
        expected_backgrounds = {"latte": "#eff1f5", "frappe": "#303446", "macchiato": "#24273a", "mocha": "#1e1e2e"}
        mapping = json.loads((ROOT / "palettes/mapping.json").read_text())
        for flavor in generate.FLAVORS:
            with self.subTest(flavor=flavor):
                theme = json.loads(generate.theme_path(flavor).read_text())
                self.assertEqual(theme, generate.build_theme(flavor))
                self.assertEqual(theme["fileVersion"], 1)
                recipe = theme["recipe"]
                self.assertEqual(recipe["colorScheme"], "light" if flavor == "latte" else "dark")
                self.assertEqual(decode_hex(recipe["background"]["customColor"]), expected_backgrounds[flavor])
                overrides = recipe["palette"]["colorOverrides"]
                self.assertEqual(len(overrides), 38)
                self.assertEqual(set(overrides), set(mapping))
                palette = json.loads((ROOT / "palettes/catppuccin.json").read_text())[flavor]["colors"]
                for role, entry in overrides.items():
                    self.assertEqual(len(entry), 1)
                    key = "colorWithOpacity" if role in ("selectedTextBackgroundColor", "currentLineHighlight") else "color"
                    self.assertEqual(decode_hex(entry[key]), palette[mapping[role]]["hex"])


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.destination = Path(self.temp.name) / "theme folder"

    def install(self, *args):
        return subprocess.run(
            ["sh", str(ROOT / "install.sh"), *args], capture_output=True, text=True,
            env={**os.environ, "XCODE_THEME_DIR": str(self.destination)},
        )

    def test_install_all_preserves_existing_and_is_repeatable(self):
        self.destination.mkdir()
        old = self.destination / "Catppuccin Mocha.xcworkspacecolortheme"
        old.write_text("user-customized-theme")
        unrelated = self.destination / "Another Theme.xcworkspacecolortheme"
        unrelated.write_text("keep")
        result = self.install("--all")
        self.assertEqual(result.returncode, 0, result.stderr)
        for flavor in generate.FLAVORS:
            source = generate.theme_path(flavor)
            self.assertEqual((self.destination / source.name).read_bytes(), source.read_bytes())
        backups = list((self.destination / "Backups").glob("*/*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "user-customized-theme")
        self.assertEqual(unrelated.read_text(), "keep")
        self.assertEqual(self.install("--all").returncode, 0)
        self.assertEqual(len(list((self.destination / "Backups").glob("*/*"))), 1)

    def test_invalid_choice_writes_nothing(self):
        self.assertNotEqual(self.install("unknown").returncode, 0)
        self.assertFalse(self.destination.exists())

    def test_default_installs_only_mocha(self):
        self.assertEqual(self.install().returncode, 0)
        self.assertEqual([p.name for p in self.destination.iterdir()], [generate.theme_path("mocha").name])


if __name__ == "__main__":
    unittest.main()
