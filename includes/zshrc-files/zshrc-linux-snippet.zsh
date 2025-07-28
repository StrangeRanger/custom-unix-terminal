# --8<-- [start:user_config]
####[ Aliases ]#############################################################################


###
### [ Group 1 ]
###

## General aliases.
alias python="python3"
hash xdg-open 2>/dev/null && alias open="xdg-open"

## Configuration related aliases.
alias update_grub_config="sudo grub-mkconfig -o /boot/grub/grub.cfg"

## File action related aliases.
alias format_csharp_code="find . -name '*.cs' -type f -exec clang-format --style='file:$HOME/Programs/Mine/Formatter Configs/CSharp_clang-format/_clang-format' -i {} +"
alias delete_local_git_branches="git branch | grep -v 'main' | xargs git branch -D"

## Update based aliases.
alias update_apt="apt_update_and_cleanup"
alias update_pacman="pacman_update_and_cleanup"

## Systemd aliases.
alias start_bluetooth="sudo systemctl start bluetooth.service"
alias stop_bluetooth="sudo systemctl stop bluetooth.service"
alias start_firewalld="sudo systemctl start firewalld.service"
alias stop_firewalld="sudo systemctl stop firewalld.service"
alias start_docker="sudo systemctl start docker.service containerd.service"
alias stop_docker="sudo systemctl stop docker.socket docker.service containerd.service"

###
### [ Group 2 ]
###
### Due to the number of commands that I find to be useful, I've created aliases containing
### some of these commands. They are specifically commands that I don't often use, but are
### useful to have on hand. Having these aliases allows me to see a list of these commands,
### without having to commit them to memory.
###

alias lt="alias_lt"
alias lt_conversion="alias_lt_conversion"
alias lt_git="alias_lt_git"


# --8<-- [end:user_config]
# --8<-- [start:ls_colors]
# Modifies the colors of files and directories in the terminal.
export LS_COLORS="di=34:ln=36:so=35:pi=1;33:ex=32:bd=34;46:cd=1;33;40:su=30;41:sg=30;46:tw=30;42:ow=30;1;43"

# Set list-colors to enable filename colorizing.
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
# --8<-- [end:ls_colors]
