####[ Oh-My-Zsh Configurations ]############################################################


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

# Disable auto updates for ohmyzsh. This is taken care of by chezmoi.
DISABLE_AUTO_UPDATE="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
HIST_STAMPS="yyyy-mm-dd"

# Which plugins would you like to load?
# Standard plugins can be found in ~/.oh-my-zsh/plugins/*
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(colored-man-pages copybuffer copypath copyfile bgnotify)


####[ Pre `compinit` ]######################################################################
#### These are configurations that have to be set before the `compinit` function is called,
#### which is done when sourcing the 'oh-my-zsh.sh' file.


## Zsh plugin for completions.
## This plugin is installed via chezmoi, specified in the '.chezmoiexternal.toml' file.
zsh_completion="${ZSH_CUSTOM:-${ZSH:-~/.oh-my-zsh}/custom}/plugins/zsh-completions/src"
[[ -d $zsh_completion ]] && fpath+=${zsh_completion}

# Rustup completions.
# $ rustup completions zsh > ~/.zfunc/_rustup
[[ -f ~/.zfunc/_rustup ]] && fpath+=~/.zfunc


####[ Resource File - Functions ]###########################################################


####
# Helper to run a brew subcommand with a nice, consistent, colored log line.
#
# NOTE: This function is written in zsh, rather than bash. I'm not as familiar with zsh
#   compared to bash, so this function was written with the help of ChatGPT.
_brew_exec() {
    local subcmd=$1; shift
    # Header
    print -P -- "%F{blue}%B[INFO]%b%f %F{8}Executing:%f %F{8}$%f %B%F{white}brew%f%b %F{cyan}${subcmd}%f${*:+ ${*}}"
    # Run and report
    if brew "$subcmd" "$@"; then
        print -P -- "%F{green}[OK]%f"
    else
        local ec=$?
        print -P -- "%F{red}[ERROR]%f exit %B${ec}%b"
        return $ec
    fi
}

####
# Perform the update, upgrade, and cleanup operations for Homebrew.
homebrew_update_and_cleanup() {
    _brew_exec update
    _brew_exec upgrade
    _brew_exec autoremove
    _brew_exec cleanup
    _brew_exec doctor
}


####[ Source Oh-My-Zsh ]####################################################################
#### It is in this file that the `compinit` function is called, which initializes the
#### completion system.


source "$ZSH/oh-my-zsh.sh"


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


####[ Environmental Variables ]#############################################################


# 1Password auth socket.
export SSH_AUTH_SOCK="$HOME/Library/Group Containers/2BUA8C4S2C.com.1password/t/agent.sock"

hb_prefix="$(brew --prefix 2>/dev/null || echo "/opt/homebrew")"
# Path purpose:
#   - $hb_prefix/opt/trash-cli/bin: Homebrew installed trash-cli binary.
#   - $HOME/.local/bin: User installed binaries.
#   - $HOME/.cargo/bin: Rust installed binaries.
export PATH="$hb_prefix/opt/trash-cli/bin:$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
unset hb_prefix

# Modifies the colors of files and directories when using `ls`.
export LSCOLORS="exgxfxDxcxegDaabagacaD"
## Version of LSCOLORS compatible with zsh and GNU based commands.
## You can find more information about LS_COLORS and why it's needed in addition to
## LSCOLORS, here: https://github.com/ohmyzsh/ohmyzsh/issues/6060#issuecomment-327934559
export LS_COLORS="di=34:ln=36:so=35:pi=1;33:ex=32:bd=34;46:cd=1;33;40:su=30;41:sg=30;46:tw=30;42:ow=30;1;43"

## Set default editor.
if hash nvim 2>/dev/null; then
    export EDITOR=nvim
    export VISUAL=$EDITOR
fi


####[ Sourced Files ]#######################################################################


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
[[ -f $fzf_tab ]] \
    && hash fzf 2>/dev/null \
    && source "$fzf_tab"

## Source the plugins.sh file for the `op` command.
[[ -f $HOME/.config/op/plugins.sh ]] && source "$HOME/.config/op/plugins.sh"

## Homebrew Command Not Found Handler
HB_CNF_HANDLER="$(brew --repository)/Library/Taps/homebrew/homebrew-command-not-found/handler.sh"
[[ -f $HB_CNF_HANDLER ]] && source "$HB_CNF_HANDLER"


####[ Zsh Style Configurations ]############################################################


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


####[ End of File Configurations ]##########################################################
#### These are configurations that are specified to be placed at the end of the file, by the
#### developer/documentation.


# Initialize Starship prompt, if it is installed and $ZSH_THEME is not set.
hash starship 2>/dev/null \
    && [[ -z $ZSH_THEME ]] \
    && eval "$(starship init zsh)"


####[ Chezmoi Unmodified ]##################################################################
#### This section is left untouched by chezmoi when executing 'chezmoi update' or 'chezmoi
#### apply'.
#### DO NOT MODIFY THE COMMENT BELOW! It acts as the delimiter for chezmoi to know where to
#### stop modifying the file. If it's removed, chezmoi will remove everything below it.
#### chezmoi:unmodified
