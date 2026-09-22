#!/bin/sh
# Install a selected flavor without changing Xcode preferences or restarting it.
set -eu
THEME_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
THEME_DEST=${XCODE_THEME_DIR:-"$HOME/Library/Developer/Xcode/UserData/FontAndColorThemes"}

case "${1:-mocha}" in
  latte) THEME_NAMES='Latte' ;;
  frappe) THEME_NAMES='Frappé' ;;
  macchiato) THEME_NAMES='Macchiato' ;;
  mocha) THEME_NAMES='Mocha' ;;
  --all) THEME_NAMES='Latte
Frappé
Macchiato
Mocha' ;;
  -h|--help)
    printf '%s\n' 'Usage: sh install.sh [mocha|latte|frappe|macchiato|--all]'
    exit 0 ;;
  *) printf '%s\n' 'Unknown flavor. Use mocha, latte, frappe, macchiato, or --all.' >&2; exit 1 ;;
esac
if [ "$#" -gt 1 ]; then
  printf '%s\n' 'Expected at most one flavor argument.' >&2
  exit 1
fi

# Verify the complete selection before copying anything.
printf '%s\n' "$THEME_NAMES" | while IFS= read -r THEME_NAME; do
  test -f "$THEME_ROOT/themes/Catppuccin $THEME_NAME.xcworkspacecolortheme"
done
mkdir -p "$THEME_DEST"
printf '%s\n' "$THEME_NAMES" | while IFS= read -r THEME_NAME; do
  THEME_FILE="Catppuccin $THEME_NAME.xcworkspacecolortheme"
  THEME_SOURCE="$THEME_ROOT/themes/$THEME_FILE"
  THEME_TARGET="$THEME_DEST/$THEME_FILE"
  if [ -f "$THEME_TARGET" ] && ! cmp -s "$THEME_SOURCE" "$THEME_TARGET"; then
    mkdir -p "$THEME_DEST/Backups"
    THEME_BACKUP=$(mktemp -d "$THEME_DEST/Backups/catppuccin.XXXXXX")
    cp -p "$THEME_TARGET" "$THEME_BACKUP/$THEME_FILE"
    printf 'Backed up existing theme: %s\n' "$THEME_BACKUP/$THEME_FILE"
  fi
  cp "$THEME_SOURCE" "$THEME_TARGET"
  printf 'Installed Catppuccin %s\n' "$THEME_NAME"
done
printf '%s\n' 'Restart Xcode when convenient, then choose your theme in Settings > Appearance.'
printf '%s\n' 'Latte is a light theme; Frappé, Macchiato, and Mocha are dark themes.'
