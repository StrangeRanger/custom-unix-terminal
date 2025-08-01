# Custom Unix Terminal

[![Project Tracker](https://img.shields.io/badge/repo%20status-Project%20Tracker-lightgrey)](https://hthompson.dev/project-tracker#project-146955022)

[![Static Badge](https://img.shields.io/badge/Click%20to%20access%20Custom%20Unix%20Terminal-blue?style=for-the-badge)](https://cut.hthompson.dev)

No one asked for it, but I made it anyways because I am passionate about sharing knowledge however I can. This repository contains information regarding my terminal setup, including the tools I use, the configurations of those tools, my terminal profiles, and more. Included are instructions on how to set up and use my configurations, or at least how to get started with them.

I've attempted to make this repository as automated as possible so it always stays current. To do this, I created workflows that automate updating the files in the `includes` directory when updating my [dotfiles repository](https://github.com/StrangeRanger/dotfiles), which contains my shell and terminal configurations.

<details>
<summary><strong>Table of Contents</strong></summary>

- [Custom Unix Terminal](#custom-unix-terminal)
  - [Requirements](#requirements)
  - [Quick Start](#quick-start)
  - [Build \& Development](#build--development)
    - [Automation Scripts](#automation-scripts)
      - [`update_repo.py`](#update_repopy)
      - [`update-changelog.bash`](#update-changelogbash)
  - [License](#license)

</details>

## Requirements

These tools are necessary **only** if you wish to build or preview the documentation locally.

- Python 3.10 or higher ([Download Python](https://www.python.org/downloads/))
- [uv](https://github.com/astral-sh/uv#installation) (a fast Python package manager and resolver)

## Quick Start

To preview the Bash Style Guide locally:

1. Ensure you have Python 3.10+ installed.
2. Install [uv](https://github.com/astral-sh/uv#installation).
3. Install dependencies:
   ```bash
   uv sync
   ```
4. Start the development server:
   ```bash
   uv run mkdocs serve
   ```
5. Open [http://localhost:8000](http://localhost:8000) in your browser.

Or, visit the hosted version at [cut.hthompson.dev](https://cut.hthompson.dev).

## Build & Development

- **Install dependencies:**
  ```bash
  uv sync
  ```
- **Serve locally for live preview:**
  ```bash
  uv run mkdocs serve
  ```
- **Build the static site for deployment:**
  ```bash
  uv run mkdocs build
  ```
- **Deploy to GitHub Pages (if configured):**
  ```bash
  uv run mkdocs gh-deploy
  ```

### Automation Scripts

These scripts are integrated with the CI/CD workflow, but can also be run manually.

> [!NOTE]
> The automation scripts do not require the dependencies installed via `uv`. Those dependencies are only needed for MkDocs site development and deployment.

#### `update_repo.py`

Updates the configuration files in `includes/` from the dotfiles submodule.

Manual usage:

1. Ensure the `submodules/dotfiles` submodule is initialized and up to date:
    ```bash
    git submodule update --init --remote submodules/dotfiles
    ```
2. Run the script:
    ```bash
    python3 update_repo.py
    ```

#### `update-changelog.bash`

Updates `CHANGELOG.md` with recent changes from the dotfiles submodule.

Manual usage:

1. Ensure the `submodules/dotfiles` submodule is initialized and up to date:
    ```bash
    git submodule update --init --remote submodules/dotfiles
    ```
2. Run the script:
    ```bash
    bash update-changelog.bash
    ```

## License

This project is licensed under the [MIT License](LICENSE).
