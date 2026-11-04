#!/usr/bin/env bash
# facet installer: gets the facet command and starts its setup, which asks what you
# want and fetches only those modules.
#
#   curl -fsSL https://facet-shell.github.io/install.sh | bash
#
# Running it again updates the facet command and starts the setup again.
set -euo pipefail

CLI_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/frameshell/cli"
CLI_URL="${FACET_CLI_URL:-https://github.com/facet-shell/cli}"

[[ -r /etc/arch-release ]] || { echo "facet is made for Arch and CachyOS (pacman)" >&2; exit 1; }
command -v git >/dev/null || sudo pacman -S --needed --noconfirm git

if [[ -d $CLI_DIR/.git ]]; then
  git -C "$CLI_DIR" pull --ff-only --quiet
else
  mkdir -p "$(dirname "$CLI_DIR")"
  git clone --depth 1 --quiet "$CLI_URL" "$CLI_DIR"
fi

# Piped from curl, stdin is this script; the setup's questions need the terminal
if [[ -t 0 ]]; then
  exec "$CLI_DIR/facet" install "$@"
else
  exec "$CLI_DIR/facet" install "$@" </dev/tty
fi
