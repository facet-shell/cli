#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import tempfile

spec = importlib.util.spec_from_file_location("migration", Path(__file__).resolve().parents[1] / "tools/migrate-system-layout.py")
migration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migration)
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    files = {
        "usr/share/frameshell/greeter/frame-greeter-session": '#!/bin/sh\nexec qs -p /usr/share/frameshell/greeter/shell.qml\n',
        "usr/share/plymouth/themes/frameshell/frameshell.plymouth": 'ScriptFile=/usr/share/plymouth/themes/frameshell/frameshell.script\n',
        "usr/share/plymouth/themes/frameshell/frameshell.script": 'Image("frame-logo.png");\n',
        "boot/grub/themes/frameshell/theme.txt": 'desktop-image: "frame-bg.png"\n',
        "etc/default/grub": 'GRUB_THEME="/boot/grub/themes/frameshell/theme.txt"\n',
        "etc/greetd/config.toml": 'command = "/usr/share/frameshell/greeter/frame-greeter-session"\n',
        "etc/plymouth/plymouthd.conf": 'Theme=frameshell\n',
    }
    for name, text in files.items():
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    helper = root / "usr/share/frameshell/greeter/frame-greeter-session"
    helper.chmod(0o755)
    assert migration.migrate(root)
    assert helper.is_file() and not (root / "usr/share/facet").exists()
    migration.migrate(root, apply=True)
    assert (root / "usr/share/facet/greeter/facet-greeter-session").stat().st_mode & 0o111
    assert 'themes/facet/facet.script' in (root / "usr/share/plymouth/themes/facet/facet.plymouth").read_text()
    assert 'themes/facet/theme.txt' in (root / "etc/default/grub").read_text()
    assert list((root / "var/lib/facet").glob("layout-before-*/etc/default/grub"))
    assert not migration.migrate(root, apply=True)
print("System migration previews, preserves helpers and backups, and remains repeatable")
