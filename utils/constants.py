"""Configuration constants for update_repo.py.

This module defines all the constants used by the update_repo.py script for processing
configuration files from the dotfiles submodule. It includes:

- File path mappings for Neovim and zsh configuration variants
- Section markers for extracting specific content from configuration files
- Template delimiters for identifying chezmoi template blocks
- MkDocs content markers for generated documentation snippets

The constants are organized by their functional purpose and are designed to be easily
modified when upstream dotfile structures change.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Final, Tuple


@dataclass
class ConfigPath:
    src: Path
    dest: Path


@dataclass
class SectionMarker:
    start_marker: str
    end_marker: str
    hard_coded_inclusion: Tuple[str, ...] | None = None
    is_within_section: bool = False


# Maps Neovim config variants to their source and destination paths.
NEOVIM_CONFIG_PATHS: Final[dict[str, ConfigPath]] = {
    "init_lua": ConfigPath(
        src=Path("submodules/dotfiles/private_dot_config/nvim/second_init.lua"),
        dest=Path("includes/neovim-init-files/neovim-init-lua.lua"),
    ),
    "init_vim_plug": ConfigPath(
        src=Path("submodules/dotfiles/private_dot_config/nvim/init.vim"),
        dest=Path("includes/neovim-init-files/neovim-init-vim-plug.vim"),
    ),
    "init_vim_no_plug": ConfigPath(
        src=Path("submodules/dotfiles/private_dot_config/nvim/init.vim"),
        dest=Path("includes/neovim-init-files/neovim-init-non-vim-plug.vim"),
    ),
}

# Maps zsh config variants to their source and destination paths.
ZSH_CONFIG_PATHS: Final[dict[str, ConfigPath]] = {
    "zshrc_linux": ConfigPath(
        src=Path("submodules/dotfiles/.chezmoitemplates/zshrc_linux.tmpl"),
        dest=Path("includes/zshrc-files/zshrc-linux.zsh"),
    ),
    "zshrc_linux_snippet": ConfigPath(
        src=Path("submodules/dotfiles/.chezmoitemplates/zshrc_linux.tmpl"),
        dest=Path("includes/zshrc-files/zshrc-linux-snippet.zsh"),
    ),
    "zshrc_macos": ConfigPath(
        src=Path("submodules/dotfiles/.chezmoitemplates/zshrc_darwin.tmpl"),
        dest=Path("includes/zshrc-files/zshrc-macos.zsh"),
    ),
    "zshrc_macos_snippet": ConfigPath(
        src=Path("submodules/dotfiles/.chezmoitemplates/zshrc_darwin.tmpl"),
        dest=Path("includes/zshrc-files/zshrc-macos-snippet.zsh"),
    ),
}

# Section markers for the general configuration section in ``init.vim`` for snippet
# extraction.
NEOVIM_MARKERS: Final[SectionMarker] = SectionMarker(
    start_marker='""""[ General Configurations ]',
    end_marker='""""[ vim-plug Plugin Configurations ]',
)

# Section markers for the aliases portion of ``.zshrc`` for snippet extraction.
ZSH_ALIAS_MARKERS: Final[SectionMarker] = SectionMarker(
    start_marker="####[ Aliases ]",
    end_marker="####[ Environmental Variables ]",
)

# Section markers for extracting/injecting the LS_COLORS related lines.
ZSH_LS_COLORS_MARKERS: Final[SectionMarker] = SectionMarker(
    start_marker="# Modifies the colors",
    end_marker="## Set default",
    hard_coded_inclusion=(
        "# Set list-colors to enable filename colorizing.\n",
        "zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}\n",
    ),
)

# Section markers used in generated MkDocs content for the user configuration snippet.
MKDOCS_USER_CONFIG_MARKERS: Final[SectionMarker] = SectionMarker(
    start_marker="# --8<-- [start:user_config]\n",
    end_marker="# --8<-- [end:user_config]\n",
)

# Section markers used in generated MkDocs content for the LS_COLORS snippet.
MKDOCS_LS_COLORS_MARKERS: Final[SectionMarker] = SectionMarker(
    start_marker="# --8<-- [start:ls_colors]\n",
    end_marker="# --8<-- [end:ls_colors]\n",
)
