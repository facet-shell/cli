# facet · cli

The `facet` command. It installs facet module by module, keeps it updated and switches
themes. The themes themselves live here too (`themes/*.json`).

```bash
curl -fsSL https://facet-shell.github.io/install.sh | bash
```

That puts the CLI in `~/.local/share/frameshell/cli` and starts the setup. Only the modules you
pick are downloaded, to `~/.local/share/frameshell/modules`.

```
facet                      a menu of the everyday commands
facet add steam            get a module and link it (no name: pick from a list)
facet update               pull everything and re-link
facet theme set            pick a theme with the arrow keys
facet status               what is installed, what is missing
facet help                 everything else
```

Ideas and bugs: [the board](https://github.com/orgs/facet-shell/projects/1).
