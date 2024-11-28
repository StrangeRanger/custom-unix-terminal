# Changelog

All notable changes to this project will be documented in this file.

/// admonition | Note

Entries under the **Removed** section indicate items removed from the entire README unless specified otherwise. If an item is removed from a specific section, it will be specified within parentheses next to the change.

## Unreleased

## 2024.11.28

This update includes a significant overhaul of several aspects of the project. As a result, the changes will look different from previous updates. Only the major changes are listed below, covering both the documentation and the repository as a whole.

### Added

- Added the `dotfiles` submodule for easy access to shell and terminal configurations.
- Introduced `update_repo.py` to simplify updating `neovim`, `zsh`, and other configuration files by retrieving them from the `dotfiles` submodule.
- Created `update_submodule.bash` to automate updating the `dotfiles` submodule with the latest changes from the dotfiles repository.
- Added `terminal-profile-setup.bash` to automate the setup of the terminal profile on Linux (requires Gnome).
- Implemented a workflow that automates updating the `dotfiles` submodule via Dependabot.
- Added a new section regarding syntax highlighting for `neovim`.

### Changed

- Replaced the shell theme **Powerlevel10k** with **Starship**.
- Updated all code examples to reflect the latest changes.
- Reworked the Gnome Terminal Profile so it no longer overwrites existing profiles.
- Updated the wording and information in the main document.
- Improved the context of several sections.


## 2024-04-25

### Added

- Added programs: `cheat`, `fzf-tab`, and `eza`.
- Included the `rainbow_csv` plugin (`mechatroner/rainbow_csv`) in `init.vim`.
- Updated and added new `zstyle` settings in `zshrc`; these are now located in a section called "Zsh Style Configurations".
- Added new sections in the README for future documentation.

### Changed

- Modified `zshrc` to check if `fzf` is installed before sourcing `fzf-tab`.
- Removed Azure autoload and source commands from `zshrc`.
- Added the recommended method of installing `fzf` on Linux in the README.
- Renamed several aliases and added a new alias for `eza`.

### Removed

- Eliminated `lsd`-based aliases.
- Removed the `PATH` variable from `zshrc`.

## 2024-04-22

This update is a major overhaul and rewrite of the entire repository. Due to the extensive changes, only the major updates are listed below.

### Changed

- Updated the list of programs to better reflect those consistently used.
- Switched from using Vim to Neovim; all configurations and documentation have been updated accordingly.
- Updated the main configuration file (`init.vim`) for Neovim to reflect changes in programs and plugins.
- Updated and added new aliases.
- Rewrote 90% of the documentation to improve wording, clarity, and readability; added new sections and removed outdated ones.
- Added a notice section in the README to inform users to view the document on the website for the full content.

## 2023-06-27

### Added

- Added `vim-better-whitespace` plugin (`ntpeters/vim-better-whitespace`) to `vimrc`.
- Introduced new file-specific configurations in `vimrc`.

### Changed

- Updated the URL link of the website status badge in the README.
- Simplified repository maintenance by removing redundant files and replacing them with a single file used in multiple places, leveraging new features from updated dependencies and packages.

## 2022-08-25

### Added

- Added new aliases in `zshrc`.
- Included the `git` plugin in `zshrc`.
- Added specific configurations for Markdown and text files in `vimrc`.

### Changed

- Updated existing aliases in `zshrc`.
- Modified `.zshrc` to contain only general configurations, simplifying maintenance.
- Made slight wording and formatting changes in `vimrc`.

### Removed

- Removed unnecessary code from `zshrc`.
- Eliminated programs `fd`/`fd-find` and `git-quick-stats`.

## 2022-07-17

### Added

- Added `YouCompleteMe` plugin (`valloric/youcompleteme`) to `vimrc`.
- Introduced new aliases in `zshrc`.
- Added a link to the repository of the newly added `vimrc` plugin in the README.
- Included comments on commands to download `zsh` plugins in `zshrc`.

### Changed

- Made slight formatting changes in `vimrc`.
- Modified plugins and performed general refactoring in `zshrc`.
- Implemented several small changes throughout `zshrc`.

## 2022-05-26

### Changed

- Removed code from the Linux `zshrc` files that wasn't considered general configurations.
- Added specific configurations for Markdown files in `vimrc`.
- Changed the website status badge in the README.

## 2022-05-24

### Added

- Set `LS_COLORS` in `zshrc` to match `LSCOLORS`.
- Added `set colorcolumn=89` in `vimrc`.
- Included a terminal profile for the Gnome terminal.
- Added programs: `fzf`, `zsh-completions`, and `gallery-dl`.
- Incorporated `zsh-autosuggestions` as an Oh My Zsh plugin, removing the need to source it.

### Changed

- Updated information in the **Modifying CLI Colors** section to include details about `LS_COLORS`.
- Improved wording and updated various small details throughout the document.
- Switched from Vundle to `vim-plug` for plugin management in `vimrc`; all references to Vundle have been updated.
- Adjusted `LSCOLOR` in `zshrc` from `exgxfxDxcxegDhabagacaD` to `exgxfxDxcxegDhabagacaD`.
- Created separate versions of the Linux `zshrc` file for desktop and server.
- Updated alias information in `aliases`.

### Removed

- Eliminated unneeded aliases and alias content.
- Removed programs: `bottom` and `hstr`.

## 2022-03-01

### Added

- Added comments to `mkdocs.yml`.

### Changed

- Updated plugins, features, and extensions in `mkdocs.yml`.
- Bumped version numbers of all packages in `mkdocs-requirements.txt`.
- Updated deprecated `zsh` plugin `copydir` to `copypath` in `zshrc`.
- Adjusted the **My .zshrc** and **My .vimrc** sections in the README to display code from files in the `insides` folder.

## 2021-12-21

### Added

- Added programs: `git-quick-stats`, `pyenv`, `ffmpeg`, `asciinema`, `m-cli`, `.tmux`, `tmux`, and `imagemagick`.
- Included several other additions that enhance functionality.

### Changed

- Updated the **Custom Aliases** and **My .zshrc** sections.
- Modified the terminal profile.

### Removed

- Removed programs: `duti`, `jq`, `Homebrew Command Not Found`, `symboliclinker`, `gistome`, `git-extras`, `pdfgrep`, `hub`, and `cloc`.
- Eliminated `tmux`, `wget`, and `tree`, as they are usually installed by default.
- Removed `jedi-vim` (`davidhalter/jedi-vim`) and `vim-fugitive` (`tpope/vim-fugitive`) from `vimrc`.
- Deleted `edkolev/tmuxline.vim` from the list of programs.

### Fixed

- Improved wording and grammar throughout the `README.md`.

## 2021-06-05

This is the first release where all configurations and related content have been fully added.
