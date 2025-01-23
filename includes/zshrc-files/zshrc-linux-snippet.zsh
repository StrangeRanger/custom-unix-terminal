# --8<-- [start:user_config]
####[ Aliases ]#########################################################################


###
### [ Group 1 ]
###

## General aliases.
alias zls="eza"
alias formatc="find . -name '*.cs' -type f -exec clang-format --style='file:$HOME/Programs/Mine/Formatter Configs/CSharp_clang-format/_clang-format' -i {} +"
alias update-grub-config="sudo grub-mkconfig -o /boot/grub/grub.cfg"
alias deletelocalbranches="git branch | grep -v 'main' | xargs git branch -D"
hash xdg-open 2>/dev/null && alias open="xdg-open"

## Update based aliases.
alias updateapt="sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y && sudo apt autoclean"
alias updatepacman="sudo pacman -Syu && yay && yay -Yc && update-grub-config"

## Systemd aliases.
alias start-bluetooth="sudo systemctl start bluetooth.service"
alias stop-bluetooth="sudo systemctl stop bluetooth.service"
alias start-vmware-networking="sudo systemctl start vmware-networks.service"
alias stop-vmware-networking="sudo systemctl stop vmware-networks.service"
alias start-firewalld="sudo systemctl start firewalld.service"
alias stop-firewalld="sudo systemctl stop firewalld.service"
alias start-docker="sudo systemctl start docker.service"
alias stop-docker="sudo systemctl stop docker.service"

###
### [ Group 2 ]
###
### Due to the number of commands that I find to be useful, I've created aliases
### containing some of these commands. They are specifically commands that I don't
### often use, but are useful to have on hand. Having these aliases allows me to see
### a list of these commands, without having to commit them to memory.
###

alias lt="echo -e \"
####[ Installed Commands ]##############################################################

bandwhich  - Terminal bandwidth utilization tool.
bat        - A cat(1) clone with wings.
cheat      - Allows you to create and view interactive cheatsheets on the command-line.
codespell  - Check code for common misspellings.
duf        - Disk Usage/Free Utility - a better 'df' alternative.
fzf        - A command-line fuzzy finder.
ncdu       - ncdu (NCurses Disk Usage) is a curses-based version of the well-known 'du'.
pstree     - List processes as a tree.
tmux       - Terminal multiplexer.

####[[ Grouped Commands ]]##############################################################

lt_conversion - List of programs used for converting the formats of videos, images, etc.
lt_git        - List of programs used for git related commands.


####[ Keyboard Combinations ]###########################################################

Ctrl + O - Allows you to copy what you are currently typing, via 'Ctrl' + 'O'.
\""
alias lt_conversion="echo -e \"
####[ Image and Video Formatters ]######################################################

ffmpeg - FFmpeg is a collection of libraries and tools to process multimedia content.
magick - Convert between image formats as well as resize an image, blur, crop,
         despeckle, dither, draw on, flip, join, re-sample, and much more.
\""
alias lt_git="echo -e \"
####[ Git Related Commands ]############################################################

lazygit  - Simple terminal UI for git commands.
git open - Opens the GitHub page for a repo/branch in your browser.
\""


# --8<-- [end:user_config]
# --8<-- [start:ls_colors]
# Modifies the colors of files and directories in the terminal.
export LS_COLORS="di=34:ln=36:so=35:pi=1;33:ex=32:bd=34;46:cd=1;33;40:su=30;41:sg=30;46:tw=30;42:ow=30;1;43"

# Set list-colors to enable filename colorizing.
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
# --8<-- [end:ls_colors]
