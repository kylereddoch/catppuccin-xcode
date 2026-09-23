# Catppuccin for Xcode

Four pastel palettes for Xcode's Appearance settings, from light Latte to dark Mocha. Native workspace themes with solid backgrounds and 38 explicit color assignments for syntax, documentation, selections, cursors, diffs, and the debugger.

**Requires Xcode 27**, which introduced workspace-wide theming in Appearance settings. These themes use its native `.xcworkspacecolortheme` format; older Xcode versions are not supported.

An independent project by Kyle Reddoch, based on the [Catppuccin palette](https://github.com/catppuccin/palette). This is not an official Catppuccin port. The [official Xcode port](https://github.com/catppuccin/xcode) is a separate project. Its classic themes import into Xcode 27.1, but our testing found color changes during conversion. These native themes preserve the exact palette and align their shared syntax assignments with that port. See the [compatibility and coverage report](docs/UPSTREAM-COMPATIBILITY.md).

## Themes and status

Each flavor has a color guide with a syntax example, labeled swatches, and a complete table of what each color controls.

| Color guide | Appearance | Background | Theme file |
| --- | --- | --- | --- |
| [Latte](docs/themes/latte.md) | Light | `#EFF1F5` | [Download](themes/Catppuccin%20Latte.xcworkspacecolortheme) |
| [Frappé](docs/themes/frappe.md) | Dark | `#303446` | [Download](themes/Catppuccin%20Frapp%C3%A9.xcworkspacecolortheme) |
| [Macchiato](docs/themes/macchiato.md) | Dark | `#24273A` | [Download](themes/Catppuccin%20Macchiato.xcworkspacecolortheme) |
| [Mocha](docs/themes/mocha.md) | Dark | `#1E1E2E` | [Download](themes/Catppuccin%20Mocha.xcworkspacecolortheme) |

All four pass automated color and file checks. These checks do not replace reviewing real Xcode windows. This is an early development version; see the [roadmap](docs/ROADMAP.md) and [verification record](docs/VERIFICATION.md).

## Install

Requires macOS and **Xcode 27**. These `.xcworkspacecolortheme` files are not compatible with Xcode 26's legacy theme format.

Download this repository using **Code → Download ZIP** and unzip it, or clone it:

```sh
git clone https://github.com/kylereddoch/catppuccin-xcode.git
cd catppuccin-xcode
sh install.sh --all
```

To install one theme, use `sh install.sh mocha`, `latte`, `frappe`, or `macchiato`. With no argument, the installer selects Mocha. It backs up any different file with the same name before replacing it, and leaves other themes alone.

Restart Xcode when convenient. Open **Xcode → Settings → Appearance → Theme → Choose…**, then select your theme. Use Light appearance for Latte and Dark appearance for the other three. You can configure separate themes for light and dark appearances.

### Manual installation

Copy your chosen files from `themes/` into:

```text
~/Library/Developer/Xcode/UserData/FontAndColorThemes/
```

Create the folder if needed, then restart Xcode.

**Avoid the “Import…” button in the tested Xcode 27.0 build.** It treated the native file as a classic theme and substituted default colors. Copying the native file into the theme folder loaded the correct colors.

## What's themed

- Workspace and editor background, with a palette seed for generated interface colors.
- Text, comments, documentation, keywords, attributes, strings, regex, numbers, characters, and links.
- Preprocessors and macros; project and external types, functions, constants, and variables.
- Selection, cursor color, current line, invisibles, diff additions/deletions, and debugger color.

Xcode derives additional workspace surfaces, console colors, and status treatments from the recipe. Those derived colors are not independent exact palette overrides. System controls and the Settings window retain Apple's appearance treatment. Fonts, sizes, line spacing, and cursor shape are separate Xcode settings; installing these themes does not change them.

## Development

Python 3.9 or later, with no third-party dependencies:

```sh
python3 scripts/generate.py
python3 scripts/generate_guides.py
python3 scripts/generate.py --check
python3 scripts/generate_guides.py --check
python3 -m unittest discover -s tests -v
```

The source of truth is the pinned palette in `palettes/catppuccin.json` plus the semantic assignments in `palettes/mapping.json`. Edit the mapping and regenerate both the themes and guides; do not hand-edit generated files. `--flavor latte` limits theme generation to one flavor. The shared mapping follows the pinned official Xcode port for directly corresponding colors. The coverage manifest in `palettes/upstream-coverage.json` records every legacy setting and any native limitation.

The generator converts exact sRGB palette values to Xcode's OKLCH representation. Checks cover round-trip color fidelity, all 38 assignments, light/dark metadata, generated-file drift, and installer backups in a temporary directory. Additional tests compare native colors against byte-verified official fixtures for all four flavors and account for all 104 legacy settings.

See [CONTRIBUTING.md](CONTRIBUTING.md) for review guidance.

## Uninstall

Select a different theme, move the corresponding Catppuccin files out of the theme folder, then restart Xcode. Installer backups, when created, are under the theme folder's `Backups/` directory.

## Credits and license

- [Catppuccin](https://github.com/catppuccin/catppuccin) supplies the palette; its MIT notice is included in [palettes/LICENSE](palettes/LICENSE). The exact revision is recorded in [palettes/SOURCE.md](palettes/SOURCE.md).
- [Official Catppuccin Xcode port](https://github.com/catppuccin/xcode) supplies the reference syntax assignments and licensed test fixtures; see [fixture provenance](tests/fixtures/upstream/SOURCE.md).
- [Neon Glow](https://github.com/Angel5215/NeonGlow) was a reference for Xcode 27's native file structure and installation location. Its theme colors and implementation are not bundled here.
- [Apple's Xcode 27 overview](https://developer.apple.com/videos/play/wwdc2026/258/) describes workspace themes and separate font settings.

Project code and original mappings are available under the [MIT license](LICENSE).
