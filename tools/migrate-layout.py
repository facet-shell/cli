#!/usr/bin/env python3
"""Move legacy Facet user directories and links without discarding existing data."""
import argparse
import os
from pathlib import Path


def renamed(text):
    for old, new in (("frameshell", "facet"), ("frame-", "facet-"), ("frame/", "facet/")):
        text = text.replace(old, new)
    return text


def exists(path):
    return os.path.lexists(path)


def replace_link(path, target):
    temporary = path.with_name(path.name + ".facet-migration")
    if exists(temporary):
        raise RuntimeError(f"Temporary link already exists: {temporary}")
    temporary.symlink_to(target)
    os.replace(temporary, path)


def migrate(home, data, state, config, cache, dry_run=False):
    moves = [(base / "frameshell", base / "facet") for base in (data, state, config, cache)]
    moves += [(config / "hypr/frame", config / "hypr/facet"),
              (data / "millennium/plugins/frameshell", data / "millennium/plugins/facet")]
    for old, new in moves:
        if exists(old) and not old.is_symlink() and exists(new):
            if not new.is_symlink() and new.is_dir() and not any(new.iterdir()):
                continue
            raise RuntimeError(f"Both {old} and {new} exist; refusing to merge or replace data")
    changes = []
    plugin_old = data / "millennium/plugins/frameshell"
    plugin_new = data / "millennium/plugins/facet"
    for old, new in moves:
        # Millennium discovers each directory entry separately, including symlinks.
        # A legacy alias to the same plugin makes it load twice and can hang Steam.
        if old == plugin_old and old.is_symlink() and new.exists() and old.resolve() == new.resolve():
            changes.append(f"remove duplicate plugin link {old}")
            if not dry_run:
                old.unlink()
            continue
        if not exists(old) or old.is_symlink():
            continue
        changes.append(f"{old} -> {new}")
        if not dry_run:
            if new.is_dir() and not new.is_symlink():
                new.rmdir()
            old.rename(new)
            if old != plugin_old:
                old.symlink_to(new.name)

    roots = [home / ".local/bin", config, data / "applications", data / "millennium", data / "facet"]
    for root in roots:
        if not root.exists():
            continue
        for directory, dirs, files in os.walk(root, followlinks=False):
            dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "Cache", "cache", "sessionData", "vencord"}]
            for entry in files + [d for d in dirs if (Path(directory) / d).is_symlink()]:
                link = Path(directory) / entry
                if not link.is_symlink():
                    continue
                before = os.readlink(link)
                after = renamed(before)
                destination = link.parent / after
                if before != after and destination.exists():
                    changes.append(f"relink {link}")
                    if not dry_run:
                        replace_link(link, after)

    # Keep old names as links while already-running programs still use them.
    folders = [home / ".local/bin", data / "applications", config / "fish/conf.d", config / "spicetify/Extensions"]
    for folder in folders:
        if not folder.is_dir():
            continue
        for old in sorted(folder.iterdir()):
            if not (old.name.startswith("frame-") or old.name.startswith("frameshell")):
                continue
            new = old.with_name(renamed(old.name))
            if exists(new):
                if old.is_symlink() and old.resolve() == new.resolve():
                    continue
                raise RuntimeError(f"Both {old} and {new} exist; refusing to replace a file")
            changes.append(f"{old} -> {new}")
            if not dry_run:
                old.rename(new)
                if folder in (home / ".local/bin", config / "spicetify/Extensions"):
                    old.symlink_to(new.name)

    for path in (config / "hypr/hyprland.lua", config / "hypr/config/binds.lua", config / "hypr/config/autostart.lua", config / "spicetify/config-xpui.ini", config / "millennium/config.json", config / "starship.toml", config / "fastfetch/config.jsonc", config / "facet/shell.json"):
        if not path.is_file() or path.is_symlink():
            continue
        before = path.read_text()
        after = renamed(before)
        if before != after:
            changes.append(f"update {path}")
            if not dry_run:
                path.write_text(after)
    token = config / "spicetify/Extensions/facet-token.js"
    if token.is_file():
        before = token.read_text()
        after = before.replace('window.FRAMESHELL_TOKEN = "', 'window.FACET_TOKEN = "')
        if "window.FACET_TOKEN =" in after and "window.FRAMESHELL_TOKEN = window.FACET_TOKEN;" not in after:
            after += "\nwindow.FRAMESHELL_TOKEN = window.FACET_TOKEN;\n"
        if before != after:
            changes.append(f"update {token}")
            if not dry_run:
                token.write_text(after)
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    home = Path.home()
    try:
        changes = migrate(home, Path(os.environ.get("XDG_DATA_HOME") or home / ".local/share"),
                          Path(os.environ.get("XDG_STATE_HOME") or home / ".local/state"),
                          Path(os.environ.get("XDG_CONFIG_HOME") or home / ".config"),
                          Path(os.environ.get("XDG_CACHE_HOME") or home / ".cache"), args.dry_run)
    except (OSError, RuntimeError) as error:
        parser.exit(1, f"facet migration: {error}\n")
    print(f"Facet directory migration: {len(changes)} changes" + (" (dry run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
