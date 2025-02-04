####[ Oh-My-Zsh Configurations ]########################################################


# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
#ZSH_THEME=""

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS=true

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Disable audo updates for ohmyzsh. This is taken care of by chezmoi.
DISABLE_AUTO_UPDATE="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
HIST_STAMPS="yyyy-mm-dd"

# Which plugins would you like to load?
# Standard plugins can be found in $ZSH/plugins/
# Custom plugins may be added to $ZSH_CUSTOM/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
#plugins=(colored-man-pages copybuffer copypath copyfile bgnotify command-not-found)  # Desktop
plugins=(colored-man-pages command-not-found)  # Server


####[ Pre `compinit` ]##################################################################
#### These are configurations that have to be set before the `compinit` function is
#### called, which is done when sourcing the 'oh-my-zsh.sh' file.


## Zsh plugin for completions.
## This plugin is installed via chezmoi, specified in the '.chezmoiexternal.toml' file.
zsh_completion="${ZSH_CUSTOM:-${ZSH:-~/.oh-my-zsh}/custom}/plugins/zsh-completions/src"
[[ -d $zsh_completion ]] && fpath+=${zsh_completion}

# Rustup completions.
# $ rustup completions zsh > ~/.zfunc/_rustup
[[ -f ~/.zfunc/_rustup ]] && fpath+=~/.zfunc


####[ Source Oh-My-Zsh ]################################################################


source "$ZSH/oh-my-zsh.sh"


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


####[ Environmental Variables ]#########################################################


## Path purpose:
##   $HOME/.local/bin:      User installed binaries.
##   $HOME/.dotnet/tools:   .NET Core tools.
##   /opt/nvim/bin: Neovim binary.
export PATH="$HOME/.local/bin:$PATH:$HOME/.dotnet/tools"
[[ -d /opt/nvim/bin ]] && export PATH="/opt/nvim/bin:$PATH"

# Modifies the colors of files and directories in the terminal.
export LS_COLORS="di=34:ln=36:so=35:pi=1;33:ex=32:bd=34;46:cd=1;33;40:su=30;41:sg=30;46:tw=30;42:ow=30;1;43"

## Set default editor.
if hash nvim 2>/dev/null; then
    export EDITOR=nvim
    export VISUAL=$EDITOR
fi

# Node Version Manager (NVM) configurations.
export NVM_DIR="$HOME/.nvm"


####[ Sourced Files ]###################################################################


## Load NVM.
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

## Zsh plugin for syntax highlighting.
## This plugin is installed via chezmoi, specified in the '.chezmoiexternal.toml' file.
zsh_syntax_highlighting="${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
[[ -f $zsh_syntax_highlighting ]] && source "$zsh_syntax_highlighting"

## Zsh plugin for autosuggestions.
## This plugin is installed via chezmoi, specified in the '.chezmoiexternal.toml' file.
zsh_autosuggestions="${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh"
[[ -f $zsh_autosuggestions ]] && source "$zsh_autosuggestions"

## Zsh plugin for fzf-tab.
## This plugin is installed via chezmoi, specified in the '.chezmoiexternal.toml' file.
fzf_tab="${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/fzf-tab/fzf-tab.plugin.zsh"
[[ -f $fzf_tab ]] && hash fzf 2>/dev/null && source "$fzf_tab"

## Source the plugins.sh file for the `op` command.
[[ -f $HOME/.config/op/plugins.sh ]] \
    && source "$HOME/.config/op/plugins.sh"


####[ Zsh Style Configurations ]########################################################


# Disable sort when completing `git checkout`.
zstyle ':completion:*:git-checkout:*' sort false
# Set descriptions format to enable group support.
# NOTE: Don't use escape sequences here, fzf-tab will ignore them.
zstyle ':completion:*:descriptions' format '[%d]'
# Set list-colors to enable filename colorizing.
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
## Preview directory's content with `eza` when completing `cd`.
hash eza 2>/dev/null \
    && zstyle ':fzf-tab:complete:cd:*' fzf-preview 'eza -1 --color=always $realpath'
# Switch group using `<` and `>`.
zstyle ':fzf-tab:*' switch-group '<' '>'


####[ End of File Configurations ]######################################################
#### These are configurations that are specified to be placed at the end of the file, by
#### the developer/documentation.


# Initialize Starship prompt, if it is installed and $ZSH_THEME is not set.
hash starship 2>/dev/null \
    && [[ -z $ZSH_THEME ]] \
    && eval "$(starship init zsh)"


####[ Others ]##########################################################################
#### These are generally configurations set up by setup scripts or other programs.

