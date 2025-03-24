# --8<-- [start:user_config]
####[ Aliases ]#########################################################################


###
### [ Group 1 ]
###

## General aliases.
alias zls="eza"
alias code="open -a 'Visual Studio Code.app' ."

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
# Modifies the colors of files and directories when using `ls`.
export LSCOLORS="exgxfxDxcxegDaabagacaD"
## Version of LSCOLORS compatible with zsh and GNU based commands.
## You can find more information about LS_COLORS and why it's needed in addition to
## LSCOLORS, here: https://github.com/ohmyzsh/ohmyzsh/issues/6060#issuecomment-327934559
export LS_COLORS="di=34:ln=36:so=35:pi=1;33:ex=32:bd=34;46:cd=1;33;40:su=30;41:sg=30;46:tw=30;42:ow=30;1;43"

# Set list-colors to enable filename colorizing.
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
# --8<-- [end:ls_colors]
