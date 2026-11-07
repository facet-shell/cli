#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import tempfile

spec = importlib.util.spec_from_file_location("migration", Path(__file__).resolve().parents[1] / "tools/migrate-layout.py")
migration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migration)
with tempfile.TemporaryDirectory() as temp:
    home = Path(temp)
    data, state, config, cache = [home / p for p in ("data", "state", "config", "cache")]
    for base in (data, state, config, cache):
        (base / "frameshell").mkdir(parents=True)
        (base / "frameshell/keep").write_text("preserved")
    helper = data / "frameshell/modules/core/wallpaper/.local/bin/facet-glint-start"
    helper.parent.mkdir(parents=True)
    helper.write_text("start")
    bin_dir = home / ".local/bin"
    bin_dir.mkdir(parents=True)
    (bin_dir / "frame-glint-start").symlink_to(str(helper).replace("/facet-", "/frame-"))
    plugin = data / "millennium/plugins/frameshell"
    plugin.mkdir(parents=True)
    (plugin / "plugin.json").write_text("{}")
    (config / "hypr/frame").mkdir(parents=True)
    (config / "hypr/hyprland.lua").write_text('require("frame/shell")\n')
    extensions = config / "spicetify/Extensions"
    extensions.mkdir(parents=True)
    (extensions / "frameshell-token.js").write_text('window.FRAMESHELL_TOKEN = "test-value";\n')
    fish = config / "fish/conf.d"
    fish.mkdir(parents=True)
    (fish / "frameshell.fish").write_text("# config\n")
    (config / "facet").mkdir()
    before = list(home.rglob("*"))
    migration.migrate(home, data, state, config, cache, dry_run=True)
    assert list(home.rglob("*")) == before
    migration.migrate(home, data, state, config, cache)
    for base in (data, state, config, cache):
        assert (base / "facet/keep").read_text() == "preserved"
        assert (base / "frameshell").is_symlink()
    assert (data / "millennium/plugins/facet/plugin.json").is_file()
    assert not (data / "millennium/plugins/frameshell").exists()
    assert (bin_dir / "facet-glint-start").read_text() == "start"
    assert (bin_dir / "frame-glint-start").read_text() == "start"
    assert 'require("facet/shell")' in (config / "hypr/hyprland.lua").read_text()
    assert 'window.FACET_TOKEN = "test-value";' in (extensions / "facet-token.js").read_text()
    assert (fish / "facet.fish").is_file() and not (fish / "frameshell.fish").exists()
    assert migration.migrate(home, data, state, config, cache) == []
    legacy_plugin = data / "millennium/plugins/frameshell"
    legacy_plugin.symlink_to("facet")
    assert migration.migrate(home, data, state, config, cache, dry_run=True)
    assert legacy_plugin.is_symlink()
    assert migration.migrate(home, data, state, config, cache)
    assert not legacy_plugin.is_symlink()
    assert (data / "millennium/plugins/facet/plugin.json").is_file()
    assert migration.migrate(home, data, state, config, cache) == []
with tempfile.TemporaryDirectory() as temp:
    home = Path(temp)
    for name in ("frameshell", "facet"):
        (home / name).mkdir()
        (home / name / "keep").write_text(name)
    try:
        migration.migrate(home, home, home / "state", home / "config", home / "cache")
    except RuntimeError:
        pass
    else:
        raise AssertionError("conflicting directories were replaced")
    assert (home / "frameshell/keep").read_text() == "frameshell"
    assert (home / "facet/keep").read_text() == "facet"
print("Facet migration preserves data and links, supports dry-run and repeat runs, and rejects collisions")
