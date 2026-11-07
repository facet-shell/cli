<p align="center">
  <a href="https://github.com/facet-shell"><img src="https://raw.githubusercontent.com/facet-shell/.github/main/brand/mark.svg" alt="facet" width="64"></a>
</p>

<h3 align="center">cli</h3>

<p align="center">The facet command: install, update, switch styles and themes.</p>

<p align="center"><sub><a href="https://github.com/facet-shell">facet</a> · <a href="https://github.com/facet-shell/core">core</a> · <b>cli</b> &nbsp;|&nbsp; <a href="https://github.com/facet-shell/style-tui">tui</a> · <a href="https://github.com/facet-shell/style-bloom">bloom</a> &nbsp;|&nbsp; <a href="https://github.com/facet-shell/terminal">terminal</a> · <a href="https://github.com/facet-shell/spotify">spotify</a> · <a href="https://github.com/facet-shell/discord">discord</a> · <a href="https://github.com/facet-shell/steam">steam</a> · <a href="https://github.com/facet-shell/zed">zed</a> · <a href="https://github.com/facet-shell/zen">zen</a> · <a href="https://github.com/facet-shell/dolphin">dolphin</a> · <a href="https://github.com/facet-shell/keyboard">keyboard</a> &nbsp;|&nbsp; <a href="https://facet-shell.github.io">website</a> · <a href="https://github.com/orgs/facet-shell/projects/1">board</a></sub></p>

The `facet` command. It installs facet module by module, keeps it updated and switches
themes. The themes themselves live here too (`themes/*.json`).

```bash
curl -fsSL https://facet-shell.github.io/install.sh | bash
```

That puts the CLI in `~/.local/share/facet/cli` and starts the setup. Only the modules you
pick are downloaded, to `~/.local/share/facet/modules`.

```
facet                      a menu of the everyday commands
facet add steam            get a module and link it (no name: pick from a list)
facet update               pull everything and re-link
facet theme set            pick a theme with the arrow keys
facet status               what is installed, what is missing
facet help                 everything else
```

Ideas and bugs: [the board](https://github.com/orgs/facet-shell/projects/1).

## Wallpapers

`facet install quickshell hypr wallpaper` installs Glint and enables it for the
native wallpaper views and Hyprland autostart. It reuses a compatible Glint binary
in `~/.local/bin`, or builds one from source. This path no longer installs
linux-wallpaperengine or mpvpaper. Existing Glint state is preserved.

The Quickshell launcher and Super+W control wallpapers directly. For terminal use,
`facet wallpaper` opens Glint's TUI and `facet wallpaper <command>` forwards to
its CLI. Workshop downloads in that interface require SteamCMD separately.

## Directory migration

User data now lives in `~/.local/share/facet`, state in `~/.local/state/facet`,
configuration in `~/.config/facet` and cache in `~/.cache/facet`. Helpers use the
`facet-` prefix and Hyprland modules live in `hypr/facet`.

The CLI migrates old directories automatically without replacing existing data.
Temporary links preserve access for running clients and old launch commands.
A collision between an old and new directory stops migration for manual inspection.
Preview the path migration with `python3 tools/migrate-layout.py --dry-run`; test it
with `python3 tests/test-migrate-layout.py`. System-wide login and boot files need
their normal privileged install commands again to adopt the new names; existing
installed copies remain functional until then.
