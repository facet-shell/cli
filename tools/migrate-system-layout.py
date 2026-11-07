#!/usr/bin/env python3
"""Rename installed Facet login and boot files; preview unless --apply is passed."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import time


def renamed(text):
    return text.replace("frameshell", "facet").replace("Frameshell", "Facet").replace("frame-", "facet-").replace("frame/", "facet/")


def migrate(root, apply=False):
    pairs = [("usr/share/frameshell", "usr/share/facet"),
             ("usr/share/plymouth/themes/frameshell", "usr/share/plymouth/themes/facet"),
             ("boot/grub/themes/frameshell", "boot/grub/themes/facet")]
    moves = [(root / a, root / b) for a, b in pairs if (root / a).is_dir() and not (root / a).is_symlink()]
    for old, new in moves:
        if os.path.lexists(new):
            raise RuntimeError(f"Both {old} and {new} exist; refusing to replace either")
    configs = [root / p for p in ("etc/greetd/config.toml", "etc/default/grub", "etc/plymouth/plymouthd.conf", "etc/udev/rules.d/70-facet-keyboards.rules")]
    changes = [f"{a} -> {b}" for a, b in moves]
    edits = []
    for config in configs:
        if not config.is_file():
            continue
        original = config.read_text()
        updated = renamed(original)
        if updated != original:
            edits.append((config, updated))
            changes.append(f"update {config}")
    if not apply:
        return changes
    if edits:
        backup = root / "var/lib/facet" / ("layout-before-" + str(time.time_ns()))
        backup.mkdir(parents=True, mode=0o700)
        for config, _ in edits:
            target = backup / config.relative_to(root)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(config, target)
    for old, new in moves:
        old.rename(new)
        old.symlink_to(new.name)
        for directory, dirs, files in os.walk(new, topdown=False):
            for entry in files:
                path = Path(directory) / entry
                if not path.is_symlink():
                    try:
                        original = path.read_text()
                    except UnicodeError:
                        original = None
                    if original is not None and renamed(original) != original:
                        path.write_text(renamed(original))
            for entry in files + dirs:
                path = Path(directory) / entry
                target = path.with_name(renamed(entry))
                if target != path:
                    if os.path.lexists(target):
                        raise RuntimeError(f"Rename collision: {target}")
                    path.rename(target)
    for config, updated in edits:
        config.write_text(updated)
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--rebuild", action="store_true", help="regenerate GRUB and initramfs after applying changes")
    args = parser.parse_args()
    if args.rebuild and not args.apply:
        parser.error("--rebuild requires --apply")
    if args.apply and os.geteuid() != 0:
        parser.error("system files require root; run this command with sudo")
    try:
        changes = migrate(Path("/"), args.apply)
        for change in changes:
            print(change)
        print(f"Facet system migration: {len(changes)} changes" + ("" if args.apply else " (dry run)"))
        if changes and args.rebuild:
            if Path("/boot/grub/grub.cfg").is_file():
                subprocess.run(["grub-mkconfig", "-o", "/boot/grub/grub.cfg"], check=True)
            if Path("/etc/mkinitcpio.conf").is_file():
                subprocess.run(["mkinitcpio", "-P"], check=True)
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"facet system migration: {error}\n")


if __name__ == "__main__":
    main()
