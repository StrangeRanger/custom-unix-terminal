from pathlib import Path
from utils.marker_config import Markers

CHEZMOI_STATEMENTS = ["{{ ", "{{- "]

NEOVIM_CONFIG_PATHS = {
    "init_lua": {
        "from": Path("submodules/dotfiles/private_dot_config/nvim/second_init.lua"),
        "to": Path("includes/neovim-init-files/neovim-init-lua.lua"),
    },
    "init_vim_plug": {
        "from": Path("submodules/dotfiles/private_dot_config/nvim/init.vim"),
        "to": Path("includes/neovim-init-files/neovim-init-vim-plug.vim"),
    },
    "init_vim_no_plug": {
        "from": Path("submodules/dotfiles/private_dot_config/nvim/init.vim"),
        "to": Path("includes/neovim-init-files/neovim-init-non-vim-plug.vim"),
    },
}

ZSH_CONFIG_PATHS = {
    "zshrc_linux": {
        "from": Path("submodules/dotfiles/.zshrc_linux.tmpl"),
        "to": Path("includes/zshrc-files/zshrc-linux.zsh"),
    },
    "zshrc_linux_snippet": {
        "from": Path("submodules/dotfiles/.zshrc_linux.tmpl"),
        "to": Path("includes/zshrc-files/zshrc-linux-snippet.zsh"),
    },
    "zshrc_macos": {
        "from": Path("submodules/dotfiles/.zshrc_darwin.tmpl"),
        "to": Path("includes/zshrc-files/zshrc-macos.zsh"),
    },
    "zshrc_macos_snippet": {
        "from": Path("submodules/dotfiles/.zshrc_darwin.tmpl"),
        "to": Path("includes/zshrc-files/zshrc-macos-snippet.zsh"),
    },
}

NEOVIM_MARKERS = Markers(
    start_marker='""""[ General Configurations ]',
    end_marker='""""[ vim-plug Plugin Configurations ]',
)

ZSH_ALIAS_MARKERS = Markers(
    start_marker="####[ Aliases ]",
    end_marker="####[ Environmental Variables ]",
)

# NOTE: This is an "estimated" value, that relies on the position of comments and other
#   commands that may not always be present. Compared to the previous markers, this one
#   is more likely to be wrong, if the `.zshrc` related files are modified.
ZSH_LS_COLORS_MARKERS = Markers(
    start_marker="# Modifies the colors",
    end_marker="## Set default",
    hard_coded_inclusion=(
        "# Set list-colors to enable filename colorizing.\n",
        "zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}\n",
    ),
)

MKDOCS_USER_CONFIG_MARKERS = Markers(
    start_marker="# --8<-- [start:user_config]\n",
    end_marker="# --8<-- [end:user_config]\n",
)

MKDOCS_LS_COLORS_MARKERS = Markers(
    start_marker="# --8<-- [start:ls_colors]\n",
    end_marker="# --8<-- [end:ls_colors]\n",
)
