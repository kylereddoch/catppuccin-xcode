# Official port compatibility and Xcode 27 coverage

## Does the official theme work in Xcode 27?

**Yes, through the classic-theme importer.** All four official `.xccolortheme` files were imported and selected successfully in **Xcode 27.1 (27A9269), macOS 27.2 (26B5091g), on 2026-09-23**. This was a color import test: fonts/line spacing and cursor shape were unchecked. It does not establish that every older setting survives import.

The reference is [catppuccin/xcode at e3816a6](https://github.com/catppuccin/xcode/tree/e3816a60caaf9889b81866924fd6ef0a4e2ad571). The existing [upstream Xcode 27 issue #22](https://github.com/catppuccin/xcode/issues/22) also reports that Mocha imports successfully.

In this build, Xcode converted the legacy files to native workspace recipes with **33 explicit color overrides**. The resulting colors differed from the original palette. Our native files encode the intended sRGB colors directly and include **38 explicit overrides**.

| Flavor | Official source background | Converted legacy background | Official source text | Imported UI text | Our native UI text |
| --- | --- | --- | --- | --- | --- |
| Latte | `#EFF1F5` | `#F2F4F7` | `#4C4F69` | `#5E637C` | `#4C4F69` |
| Frappé | `#303446` | `#3F4458` | `#C6D0F5` | `#D0DAF7` | `#C6D0F5` |
| Macchiato | `#24273A` | `#30354B` | `#CAD3F5` | `#D4DCF7` | `#CAD3F5` |
| Mocha | `#1E1E2E` | `#28293C` | `#CDD6F4` | `#D6DFF6` | `#CDD6F4` |

Converted background values above are decoded from Xcode's saved OKLCH recipes. Text values were also checked in Appearance's hex controls. The exact cause of the import conversion has not been isolated; these results do not prove the same behavior in every Xcode/macOS build. All measured role values are recorded in [upstream-import-results.json](upstream-import-results.json).

## What this native adaptation preserves

The shared mapping now follows the official source for the directly corresponding colors in all four flavors:

| Element | Catppuccin color |
| --- | --- |
| Plain text, member declarations, project/external variables | Text |
| Comments and documentation comments, including emphasis | Overlay 2 |
| Keywords | Mauve |
| Attributes and preprocessor directives | Teal |
| Strings and character literals | Green |
| Regular expressions | Pink |
| Numbers and project/external constants | Peach |
| Functions, macros, system macros, source links | Blue |
| Type declarations, project/external classes and types | Yellow |
| Background, current line, selection, invisibles | Base, Surface 0, Surface 1, Surface 2 |
| Editor insertion point | Subtext 0 |

The broader project/external type and member fallbacks follow Xcode's converted recipe: Yellow for types, Blue for members. The native debugger role uses the official console prompt's Green as a design approximation. Diff additions and deletions explicitly use Green and Red. The Foreground seed remains Lavender and the Background seed Base; Xcode derives additional interface treatments from those seeds.

This changes the initial native prototype's attributes, character literals, links, preprocessors/macros, member declarations, external variables, member fallbacks, emphasized comments, cursor, and debugger assignments. The four flavor guides are regenerated from these mappings.

## Coverage boundaries

The [coverage manifest](../palettes/upstream-coverage.json) accounts for **all 104 leaf settings** in each pinned official theme. Tests fail if a reference setting is left unclassified. Counts describe source settings, not the number of visible UI controls.

| Disposition | Count | Meaning |
| --- | ---: | --- |
| Direct color mapping | 31 | 26 syntax colors plus 5 editor surfaces. Native RGB values match the official source in every flavor. This checks assigned values, not every language's token classification. |
| Merged regex categories | 4 | Capture names, character names, regex numbers and other regex tokens have no separately exposed equivalent in the tested native controls; the recipe has one Regex role. |
| Approximation | 1 | Legacy console prompt Green supplies the native Debugger role; separate prompt/output parity is not claimed. |
| Separate typography settings | 40 | Editor, console and markup fonts. The native color files intentionally leave fonts, weights and sizes unchanged. |
| No direct native control verified | 27 | Seven remaining console colors, ten rendered-markup colors, seven scrollbar marker colors, block dimming, MARK tokens and inline documentation code. |
| Format metadata | 1 | Legacy version field, replaced by native `fileVersion`. |

In particular, rendered documentation/markup is different from source documentation comments. Likewise, native diff colors do not promise exact scrollbar marker colors. No unsupported legacy keys have been inserted into the native JSON to give the appearance of complete coverage.

**This is coverage of the verified native controls, not complete one-to-one parity with every legacy setting.** Further runtime work is needed on console output, rendered documentation, diagnostics, navigation, search, inactive windows, and language-specific token classification. Fonts can be configured separately in Appearance; the classic import dialog offers a fonts/line-spacing option, but that option was not tested in this session.

## Reproduce the checks

1. Download the four legacy files at the pinned upstream revision. Their byte-identical test copies, SHA-256 hashes, original paths and MIT license are under [tests/fixtures/upstream](../tests/fixtures/upstream/).
2. Back up existing themes and note the current appearance selection. Use distinct filenames to avoid replacing your themes.
3. Open **Settings → Appearance → Theme → Choose… → Import…**. Import one legacy file with colors enabled and fonts/cursor shape disabled. Explicitly choose the imported theme if it is not selected automatically; this was necessary for the accented Frappé test name.
4. Read the displayed text/comment hex values and inspect the newly saved `.xcworkspacecolortheme` file under `~/Library/Developer/Xcode/UserData/FontAndColorThemes/`.
5. Copy our native theme into that folder directly. Choose Latte in Light appearance or the other flavors in Dark. In the tested 27.1 build, newly copied files appeared without restarting. Restart when convenient if they are not listed.
6. Compare the exact palette assignments with `python3 -m unittest discover -s tests -v`. The tests use local fixtures and temporary installer folders, never your real Xcode preferences.
7. Restore your original selection and remove temporary test files from the active theme folder.

All four native files loaded and their Plain Text and Debugger hex controls matched the intended palette. Latte's visible keyword, attribute, string, regex, number, character, link, preprocessor, macro and type-declaration controls also matched. This was an Appearance preview and control check, not a full visual certification of every workspace surface. Original selections, fonts, cursor preferences and installed Mocha were restored after testing.

## Upstream contribution

The natural target is **[catppuccin/xcode](https://github.com/catppuccin/xcode)**, adding Xcode 27 support alongside its existing legacy files. The central Catppuccin repository already points to an Xcode port; a second listing would not implement support in that port.

[PR #24: native Xcode 27 workspace themes](https://github.com/catppuccin/xcode/pull/24) is open against the official port, referencing issue #22 and this project. It adds the four tested native files, generation based on the existing legacy files, native validation, and compatibility documentation.

The contribution scope is:

- Reference [issue #22](https://github.com/catppuccin/xcode/issues/22), including the precise tested builds and importer results.
- Add native workspace files for all four flavors while retaining the existing `.xccolortheme` files for older Xcode versions.
- Integrate reproducible native generation with the port's existing `xcode.tera` / Whiskers workflow, or agree on the generator with maintainers.
- Add separate installation instructions for legacy and native themes, palette/coverage checks, and real Xcode previews after reviewing the remaining surfaces.
- Preserve upstream licensing and project conventions. See the [organization's contribution guidelines](https://github.com/catppuccin/.github/blob/main/CONTRIBUTING.md).

This repository contains the comparison, native mappings and regression tests supporting the PR. The submission explicitly discloses the remaining visual checks. Local checks pass; at submission time, the upstream workflows required maintainer approval to run.
