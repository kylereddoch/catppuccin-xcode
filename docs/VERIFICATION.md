# Verification record

## 2026-09-23 — official-port comparison and native loading checks

Tested Xcode **27.1 (27A9269)** on macOS **27.2 (26B5091g)**. All four official legacy themes imported through Appearance with colors enabled and fonts/cursor shape disabled. Xcode saved 33 color overrides per converted recipe; measured colors differed from the upstream palette. All four revised native files loaded by copying them directly into the theme folder and selecting them. Plain Text and Debugger hex values matched for each flavor; Latte's light syntax controls were additionally spot-checked. See the [full compatibility report](UPSTREAM-COMPATIBILITY.md) and [recorded values](upstream-import-results.json).

The native mapping now matches all 31 directly corresponding upstream color settings across four flavors. A coverage manifest accounts for every one of the 104 legacy settings, including typography and settings without a verified native equivalent. Eight automated tests pass. This does not establish complete console, markup, diagnostic, or per-language visual parity.

The user's original installed theme, light/dark selections, System appearance, fonts and cursor preferences were restored. Xcode was not restarted and its running project was left running. Newly copied native files appeared live in this build; the earlier 27.0 import finding below remains historical.

## 2026-09-22 — initial development version

**Mocha:** installed using the native theme folder and loaded in Xcode 27.0's Appearance settings. The displayed text color (`#CDD6F4`), background (`#1E1E2E`), and debugger color (`#94E2D5`) matched the intended values. The generator preserves the same palette assignments and exact 8-bit sRGB colors. Encoded OKLCH values are normalized to twelve decimal places so macOS and Linux generate identical files.

The settings preview area was collapsed, so this is a loading and color spot-check, not a complete visual review of a working project. Console, diagnostics, inactive windows, automatic switching, and all editor surfaces remain to be reviewed.

The Appearance **Import…** workflow misinterpreted the native file as a classic theme and produced default colors. Installing the actual `.xcworkspacecolortheme` file into `FontAndColorThemes` and reloading Xcode resolved that issue.

**Latte, Frappé, Macchiato at this initial checkpoint:** generated from their official palette values with the same 38 semantic assignments. Automated checks pass; no Xcode visual review has been completed yet.

**Automated coverage:** all palette colors round-trip through the sRGB/OKLCH conversion; each theme has the expected background, appearance, and 38 color assignments; generated output matches source; installation preserves an existing customized theme and unrelated themes; repeated installation does not create unnecessary backups; invalid flavor input writes nothing. Installer tests use temporary directories and do not modify real Xcode preferences.
