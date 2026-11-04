# Tab completion for facet in bash. Linked to
# ~/.local/share/bash-completion/completions/facet by `facet install` and `facet update`
# (needs the bash-completion package); the lists come from `facet __complete`.

_facet() {
    local cur=${COMP_WORDS[COMP_CWORD]} prev=${COMP_WORDS[COMP_CWORD - 1]} cmd=${COMP_WORDS[1]:-} words=""

    if [[ $cur == -* ]]; then
        words="-n --dry-run -y --yes -v --verbose"
    elif ((COMP_CWORD == 1)); then
        words=$(facet __complete commands 2>/dev/null)
    else
        case $cmd in
            install | update | backup) words="$(facet __complete modules 2>/dev/null) $(facet __complete packages 2>/dev/null)" ;;
            add) words=$(facet __complete modules 2>/dev/null) ;;
            remove) words="$(facet __complete modules 2>/dev/null) $(facet __complete installed 2>/dev/null)" ;;
            restore) words="latest $(facet __complete backups 2>/dev/null)" ;;
            theme)
                if ((COMP_CWORD == 2)); then
                    words="list set check $(facet __complete themes 2>/dev/null)"
                elif [[ $prev == set || $prev == use || $prev == pick ]]; then
                    words=$(facet __complete themes 2>/dev/null)
                fi
                ;;
            grub | login) words="install remove" ;;
            boot) words="install check remove" ;;
            layout) words="tiling canvas" ;;
            style) words="list $(facet __complete styles 2>/dev/null)" ;;
            audio)
                if ((COMP_CWORD == 2)); then
                    words="channels status"
                elif ((COMP_CWORD == 3)) && [[ $prev == channels ]]; then
                    words="on off output status"
                elif [[ $prev == output || $prev == --output ]]; then
                    words=$(facet __complete sinks 2>/dev/null)
                elif [[ ${COMP_WORDS[3]:-} == on ]]; then
                    words="system game chat music --output"
                fi
                ;;
            spotify) words="login logout status" ;;
            wallpaper)
                if ((COMP_CWORD == 2)); then
                    words="list set option backend apply pause resume stop"
                elif [[ $prev == backend ]]; then
                    words="both mpv image"
                elif [[ $prev == set ]]; then
                    mapfile -t COMPREPLY < <(compgen -f -- "$cur")
                    return
                fi
                ;;
        esac
    fi
    mapfile -t COMPREPLY < <(compgen -W "$words" -- "$cur")
}
complete -F _facet facet
