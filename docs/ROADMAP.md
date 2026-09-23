# Roadmap

## Foundation

- [x] Native Xcode 27 Mocha workspace theme.
- [x] Reproducible generator using a pinned Catppuccin palette.
- [x] Initial Latte, Frappé, and Macchiato themes with correct light/dark metadata.
- [x] Selective installer with backups and automated checks.
- [x] MIT license and upstream attribution.
- [x] Import all four official legacy themes in Xcode 27.1 and compare converted colors.
- [x] Align direct native color mappings with the official port; account for every legacy setting.
- [x] Load all four revised native themes and spot-check Appearance color controls.

## Before a stable release

- [ ] Review all four flavors in real Xcode workspaces, including light Latte contrast.
- [ ] Check console, navigation, project settings, search, diff, and diagnostic treatments.
- [ ] Check automatic light/dark switching and per-workspace selection.
- [ ] Capture real screenshots for each flavor and document tested Xcode/macOS versions.
- [ ] Refine per-flavor mappings where readability requires it.
- [ ] Test install/update/uninstall on a clean user profile.
- [ ] Publish a versioned downloadable release with licenses and installation instructions.

## Possible later work

- Optional accent variants if Xcode's generated interface colors warrant them.
- A separate legacy-format export if there is demand for Xcode 26 support.
- Review and refine [upstream PR #24](https://github.com/catppuccin/xcode/pull/24), which adds native themes and references [issue #22](https://github.com/catppuccin/xcode/issues/22). See the [compatibility report](UPSTREAM-COMPATIBILITY.md).
