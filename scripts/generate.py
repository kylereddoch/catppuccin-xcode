#!/usr/bin/env python3
"""Generate Xcode 27 workspace themes from the vendored Catppuccin palette."""

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLAVORS = ("latte", "frappe", "macchiato", "mocha")


def to_oklch(hex_color):
    """Convert an sRGB hex color to Xcode's exact OKLCH representation."""
    value = hex_color.removeprefix("#")
    rgb = [int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    r, g, b = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb]
    l = (.4122214708 * r + .5363325363 * g + .0514459929 * b) ** (1 / 3)
    m = (.2119034982 * r + .6806995451 * g + .1073969566 * b) ** (1 / 3)
    s = (.0883024619 * r + .2817188376 * g + .6299787005 * b) ** (1 / 3)
    lightness = .2104542553 * l + .793617785 * m - .0040720468 * s
    a = 1.9779984951 * l - 2.428592205 * m + .4505937099 * s
    b = .0259040371 * l + .7827717662 * m - .808675766 * s
    return {
        # Normalize libm's trailing-bit differences across macOS and Linux.
        # Twelve decimals preserve every 8-bit sRGB palette value exactly.
        "chroma": {"exact": round(math.hypot(a, b), 12)},
        "gamut": "sRGB",
        "hue": {"radians": round(math.atan2(b, a) % (2 * math.pi), 12)},
        "lightness": {"exact": round(lightness, 12)},
        "opacity": 1,
    }


def build_theme(flavor):
    palette = json.loads((ROOT / "palettes/catppuccin.json").read_text())[flavor]
    mapping = json.loads((ROOT / "palettes/mapping.json").read_text())

    def color(name):
        return to_oklch(palette["colors"][name]["hex"])

    translucent_roles = {"selectedTextBackgroundColor", "currentLineHighlight"}
    overrides = {
        role: {"colorWithOpacity" if role in translucent_roles else "color": color(name)}
        for role, name in mapping.items()
    }
    return {
        "fileVersion": 1,
        "recipe": {
            "background": {"customColor": color("base")},
            "colorScheme": "dark" if palette["dark"] else "light",
            "palette": {
                "colorOverrides": overrides,
                "primary": {"custom": color("lavender")},
                "secondary": {"custom": color("base")},
            },
        },
    }


def theme_path(flavor):
    palette = json.loads((ROOT / "palettes/catppuccin.json").read_text())[flavor]
    return ROOT / "themes" / f"Catppuccin {palette['name']}.xcworkspacecolortheme"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--flavor", choices=FLAVORS, help="Generate just one flavor.")
    parser.add_argument("--check", action="store_true", help="Fail if committed themes differ; write nothing.")
    args = parser.parse_args()
    stale = []
    for flavor in (args.flavor,) if args.flavor else FLAVORS:
        path = theme_path(flavor)
        expected = json.dumps(build_theme(flavor), indent=2) + "\n"
        if args.check:
            if not path.exists() or path.read_text() != expected:
                stale.append(path.name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected)
            print(f"Generated {path.name}")
    if stale:
        parser.exit(1, "Themes need regeneration: " + ", ".join(stale) + "\n")
    if args.check:
        print("Generated themes are current.")


if __name__ == "__main__":
    main()
