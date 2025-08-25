# Changelog

All notable changes to this project will be documented in this file. This includes changes to configuration files (such as `.zshrc`, Neovim configs), terminal profiles, aliases, functions, and plugins that are shared through this documentation. Changes to automation scripts, repository maintenance, dependency updates, and other backend changes are **not** included here.

/// admonition | Note

Entries under the **Removed** section indicate items removed from the entire document unless specified otherwise. If an item is removed from a specific section, it will be specified in the entry.

///

## Unreleased

## 2025-08-25

## 2025-08-20

### Changed

- changed(zshrc): remove unused paths from $PATH

### Added

- added(PATH): add local cargo path to $PATH

## 2025-08-18

### Changed

- changed(zshrc): fix typos and comment format

### Added

- added(zshrc): add configurations for 'command-not-found' homebrew tap

## 2025-08-14

### Changed

- changed(zshrc): modify end section to be excluded from modification by 'chezmoi apply'

## 2025-08-11

### Added

- added(programs): add 'uv' and 'ruff'
- added(programs): add 'shellharden' to native package manager table
- added(programs): add 'wget' to native package manager table

### Changed

- changed(programs): modify 'git-open' to use different repo/package manager
- changed(programs): add git as an option/recommendation for 'neovim' on Linux

### Removed

- removed(programs): remove 'black', 'pipx', 'isort', and 'pyenv'
- removed(programs): remove 'pylint'

### Fixed

- fixed(programs): fix inaccurate "is a command"

## 2025-08-04

### Changed

- changed(zshrc): modify pkg update functions to use colorized output

## 2025-07-28

### Changed

- changed(alias): remove alias for 'eza'
- changed(alias): add alias python for python3

## 2025-07-21

### Changed

- changed(zshrc): remove 'tailscale' from oh-my-zsh plugins

## 2025-06-12

### Changed

- changed(terminal): update GNOME terminal profile

## 2025-06-11

### Changed

- changed(terminal): update macOS terminal profile

## 2025-06-04

### Added

- added(zshrc): add new 'tailscale' to plugins

## 2025-03-31

### Changed

- changed(neovim): remove redundant expandtab from one augroup

### Added

- added(nvim): autocmd for *.sln, *.csproj, and vim; wrap autocmd in augroup

## 2025-03-26

### Changed

- changed(neovim): modify default color column length

## 2025-03-24

### Changed

- changed(style/alias): modify format and style of comments and aliases
- changed(function): implement functions for update aliases
- changed(function): Update the description of the functions
- changed(alias): update the style and seperation of aliases

### Fixed

- fixed(white-space): remove extra blank line

### Added

- added(alias): add section for functions to improve alias functionality
- added(alias): alias restarts the Core Auido Process (can resolve audio issues)

## 2025-03-17

### Changed

- changed(nvm): Remove 'nvm' and its configurations

## 2025-03-14

### Changed

- changed(PATH): Modify existing paths for $PATH

## 2025-03-06

### Removed

- removed(aliases): Remove vmware network aliases

## 2025-02-27

### Added

- added(zshrc): add env variable for ssh auth socket

## 2025-02-24

### Changed

- changed(aliases): replace 'pacman -Fy' with 'pkgfile -u'
- changed(aliases): update 'updatepacman' to perform 'sudo pacman -Fy'
- changed(zshrc): modify source commands and add sourcing 'command-not-found.zsh'

## 2025-02-17

### Added

- added(nvim-plugin): enable mini.comment and mini.pairs
- added(nvim-plugin): enable mini.move
- added(nvim-plugin): add 'mini.nvim' plugin

## 2025-02-07

### Changed

- changed(alias): include 'docker.socket' when stopping 'docker.service'
- changed(alias): update docker alias to include 'containerd.servic'

### Added

- added(PATH): add path to ruby 3.3.0 gems

## 2025-02-04

### Changed

- changed(PATH): modify path to 'nvim' when in '/opt/'

## 2025-01-27

### Added

- added(PATH): dotnet tools directory is included at the end of $PATH

## 2025-01-23

### Added

- added(aliases): add docker start and stop aliases

## 2024-12-20

### Fixed

- fixed(.zshrc): fix spelling problems

### Added

- added(zshrc): seperate update based variables
- added(alias): add new alias `deletelocalbranches`
- added(alias): add `update-grub-config` to `updatepacman` alias

## 2024-12-02

### Added

- Several new aliases have been added to the linux `.zshrc` file:
    ```bash
    alias update-grub-config="sudo grub-mkconfig -o /boot/grub/grub.cfg"

    ## Systemd aliases.
    alias start-bluetooth="sudo systemctl start bluetooth.service"
    alias stop-bluetooth="sudo systemctl stop bluetooth.service"
    alias start-vmware-networking="sudo systemctl start vmware-networks.service"
    alias stop-vmware-networking="sudo systemctl stop vmware-networks.service"
    alias start-firewalld="sudo systemctl start firewalld.service"
    alias stop-firewalld="sudo systemctl stop firewalld.service"
    ```

### Removed

- Removed the `rrm` and `rm` aliases from the linux `.zshrc` file.

## 2024-11-28

This update includes a significant overhaul of several aspects of the project. As a result, only the major changes are listed below. The changes cover both the documentation and the repository as a whole.

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
