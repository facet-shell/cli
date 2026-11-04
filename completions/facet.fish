# Tab completion for facet in fish. Linked to ~/.config/fish/completions
# by `facet install` and `facet update`; the lists come from `facet __complete`.

function __facet_list
    facet __complete $argv 2>/dev/null
end

set -l commands install add update remove backup restore theme style grub boot goxlr audio keyboard kb login wallpaper spotify layout status clean help

complete -c facet -f
complete -c facet -s n -l dry-run -d "print what would happen, change nothing"
complete -c facet -s y -l yes -d "do not ask, take the defaults"
complete -c facet -s v -l verbose -d "full output of long commands instead of a spinner"

complete -c facet -n "not __fish_seen_subcommand_from $commands" -a install -d "the setup, or just some modules"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a add -d "fetch and set up a module (no name: pick)"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a update -d "pull, back up, relink, re-apply themes"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a remove -d "unlink and delete a module (no name: pick)"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a backup -d "snapshot configs and app settings"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a restore -d "list backups or put one back"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a theme -d "list, set or check the theme"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a grub -d "theme the GRUB boot menu"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a boot -d "boot splash and console colors"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a goxlr -d "GoXLR lights in the theme's colors"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a audio -d "virtual sound channels without a GoXLR"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a keyboard -d "supported keyboards, pick yours"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a login -d "the lockscreen look as the login screen"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a wallpaper -d "wallpaper backends"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a spotify -d "Spotify Web API for the launcher"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a layout -d "tiling or the infinite canvas"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a style -d "the look of the desktop"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a status -d "what is linked and what is missing"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a clean -d "free disk space"
complete -c facet -n "not __fish_seen_subcommand_from $commands" -a help -d "all commands"

complete -c facet -n "__fish_seen_subcommand_from install add update backup" -a "(__facet_list modules)" -d module
complete -c facet -n "__fish_seen_subcommand_from install update backup" -a "(__facet_list packages)" -d package
complete -c facet -n "__fish_seen_subcommand_from remove" -a "(__facet_list modules) (__facet_list installed)"
complete -c facet -n "__fish_seen_subcommand_from restore" -a "latest (__facet_list backups)"

# theme: the actions, and the names (facet theme sakura works too); after set only names
complete -c facet -n "__fish_seen_subcommand_from theme; and not __fish_seen_subcommand_from list ls set use pick check" -a "list set check" -d action
complete -c facet -n "__fish_seen_subcommand_from theme; and not __fish_seen_subcommand_from list ls check" -a "(__facet_list themes)" -d theme

complete -c facet -n "__fish_seen_subcommand_from grub login" -a "install remove"
complete -c facet -n "__fish_seen_subcommand_from boot" -a "install check remove"
complete -c facet -n "__fish_seen_subcommand_from layout" -a "tiling canvas"
complete -c facet -n "__fish_seen_subcommand_from style" -a "list (__facet_list styles)" -d style
complete -c facet -n "__fish_seen_subcommand_from spotify" -a "login logout status"
complete -c facet -n "__fish_seen_subcommand_from wallpaper; and not __fish_seen_subcommand_from list set option backend apply pause resume stop" -a "list set option backend apply pause resume stop"
complete -c facet -n "__fish_seen_subcommand_from wallpaper; and __fish_seen_subcommand_from backend" -a "both mpv image"
complete -c facet -n "__fish_seen_subcommand_from wallpaper; and __fish_seen_subcommand_from set" -F

# keyboard list|search <text>|set [board]|request
complete -c facet -n "__fish_seen_subcommand_from keyboard kb; and not __fish_seen_subcommand_from list ls search find set use pick request" -a "list search set request" -d action
complete -c facet -n "__fish_seen_subcommand_from keyboard kb; and __fish_seen_subcommand_from set use pick" -a "(__facet_list keyboards)" -d keyboard
# audio channels on|off|output <sink>|status
complete -c facet -n "__fish_seen_subcommand_from audio; and not __fish_seen_subcommand_from channels status" -a "channels status"
complete -c facet -n "__fish_seen_subcommand_from audio; and __fish_seen_subcommand_from channels; and not __fish_seen_subcommand_from on off output status" -a "on off output status"
complete -c facet -n "__fish_seen_subcommand_from audio; and __fish_seen_subcommand_from on; and not __fish_seen_subcommand_from --output" -a "system game chat music --output" -d channel
complete -c facet -n "__fish_seen_subcommand_from audio; and __fish_seen_subcommand_from output --output" -a "(__facet_list sinks)" -d output
