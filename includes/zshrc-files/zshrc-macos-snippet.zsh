# --8<-- [start:user_config]
####[ Aliases ]#############################################################################


###
### [ Group 1 ]
###

## General aliases.
alias code="open -a 'Visual Studio Code.app' ."
alias python="python3"

## Directory related aliases.
alias move_to_icloud="cd ~/Library/Mobile\ Documents/com~apple~CloudDocs"
alias move_to_volumes="cd /Volumes && ll"

## File action related aliases.
alias remove_ds_store="find . -name '*.DS_Store' -type f -delete"
alias format_csharp_code="find . -name '*.cs' -type f -exec clang-format --style='file:$HOME/Programs/Mine/Formatter Configs/CSharp_clang-format/_clang-format' -i {} +"
alias delete_local_git_branches="git branch | grep -v 'main' | xargs git branch -D"

## Audio related aliases.
# Restarting the Core Audio Process can often resolve issues such as no sound, crackling
# noise, or intermittent audio problems.
alias restart_core_audio_process="sudo killall coreaudiod"

## Update based aliases.
alias update_brew="homebrew_update_and_cleanup"

###
### [ Group 2 ]
###
### Below are aliases that provide a list of commands and keyboard combinations that I often
### forget about. They act as a reference for me, so that I don't have to commit these
### commands to memory.
###

alias list_tools="echo '
####[ Installed Commands ]######################################################

bandwhich - Terminal bandwidth utilization tool.
bat       - A cat(1) clone with wings.
cheat     - Allows you to create and view interactive cheatsheets on the
            command-line.
codespell - Check code for common misspellings.
duf       - Disk Usage/Free Utility - a better 'df' alternative.
fzf       - A command-line fuzzy finder.
ncdu      - ncdu (NCurses Disk Usage) is a curses-based version of the
            well-known 'du'.
pstree    - List processes as a tree.


####[ Keyboard Combinations ]###################################################

Ctrl + O - Allows you to copy what you are currently typing, via 'Ctrl' + 'O'.'"


# --8<-- [end:user_config]
# --8<-- [start:ls_colors]
# Modifies the colors of files and directories when using `ls`.
export LSCOLORS="exgxfxDxcxegDaabagacaD"
## Version of LSCOLORS compatible with zsh and GNU based commands.
## You can find more information about LS_COLORS and why it's needed in addition to
## LSCOLORS, here: https://github.com/ohmyzsh/ohmyzsh/issues/6060#issuecomment-327934559
export LS_COLORS="di=34:ln=36:so=35:pi=1;33:ex=32:bd=34;46:cd=1;33;40:su=30;41:sg=30;46:tw=30;42:ow=30;1;43"

# Set list-colors to enable filename colorizing.
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
# --8<-- [end:ls_colors]
