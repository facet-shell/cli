# frameshell · cli

The `frame` command. It installs frameshell module by module, keeps it updated and switches
themes. The themes themselves live here too (`themes/*.json`).

```bash
curl -fsSL https://frame-shell.github.io/install.sh | bash
```

That puts the CLI in `~/.local/share/frameshell/cli` and starts the setup. Only the modules you
pick are downloaded, to `~/.local/share/frameshell/modules`.

```
frame                      a menu of the everyday commands
frame add steam            get a module and link it (no name: pick from a list)
frame update               pull everything and re-link
frame theme set            pick a theme with the arrow keys
frame status               what is installed, what is missing
frame help                 everything else
```

Ideas and bugs: [the board](https://github.com/orgs/frame-shell/projects/1).
