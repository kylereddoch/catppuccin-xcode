# Contributing

Keep changes focused on Xcode 27's native Appearance themes. Use the official color names and palette values. Preserve Catppuccin attribution and describe the project as an independent adaptation.

1. Change `palettes/mapping.json` or the generator. Keep flavor-specific adjustments explicit if visual review shows they are needed.
2. Run the development commands in the README and commit generated themes and color guides alongside their sources. The guide generator checks that every color assignment has a descriptive label.
3. Install the affected theme, restart Xcode, and review `examples/ThemePreview.swift` in the intended appearance.
4. Check selections, cursor, comments, search results, console output, diff additions/deletions, warnings/errors, project settings, and inactive windows.
5. Include the Xcode/macOS version and real screenshots in the pull request. Remove private project names, paths, and source before sharing screenshots.

Automated checks establish file and palette correctness; only label a flavor visually verified after reviewing it in Xcode. Keep the verification record current. Avoid changing fonts or other global Xcode preferences as part of installation.

For bug reports, include flavor, Xcode version, macOS version, chosen light/dark appearance, and the affected UI element.

Before changing a shared syntax assignment, run the official-reference tests and update [the coverage manifest](palettes/upstream-coverage.json) with an explicit rationale for any intentional deviation. Keep fixture hashes and provenance pinned; do not silently replace the reference files. See [upstream compatibility](docs/UPSTREAM-COMPATIBILITY.md) for measured behavior and the proposed contribution scope.
