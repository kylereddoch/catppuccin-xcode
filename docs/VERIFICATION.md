# Verification record

## 2026-09-22 — initial development version

**Mocha:** installed using the native theme folder and loaded in Xcode 27.0's Appearance settings. The displayed text color (`#CDD6F4`), background (`#1E1E2E`), and debugger color (`#94E2D5`) matched the intended values. The generator preserves the same palette assignments and exact 8-bit sRGB colors. Encoded OKLCH values are normalized to twelve decimal places so macOS and Linux generate identical files.

The settings preview area was collapsed, so this is a loading and color spot-check, not a complete visual review of a working project. Console, diagnostics, inactive windows, automatic switching, and all editor surfaces remain to be reviewed.

The Appearance **Import…** workflow misinterpreted the native file as a classic theme and produced default colors. Installing the actual `.xcworkspacecolortheme` file into `FontAndColorThemes` and reloading Xcode resolved that issue.

**Latte, Frappé, Macchiato:** generated from their official palette values with the same 38 semantic assignments. Automated checks pass; no Xcode visual review has been completed yet.

**Automated coverage:** all palette colors round-trip through the sRGB/OKLCH conversion; each theme has the expected background, appearance, and 38 color assignments; generated output matches source; installation preserves an existing customized theme and unrelated themes; repeated installation does not create unnecessary backups; invalid flavor input writes nothing. Installer tests use temporary directories and do not modify real Xcode preferences.
