# Custom Unix Terminal

[![Project Tracker](https://img.shields.io/badge/repo%20status-Project%20Tracker-lightgrey)](https://hthompson.dev/project-tracker#project-146955022)

[![Static Badge](https://img.shields.io/badge/Click%20to%20access%20Custom%20Unix%20Terminal-blue?style=for-the-badge)](https://cut.hthompson.dev)

No one asked for it, but I made it anyways because I am passionate about sharing knowledge however I can. This repository contains information regarding my terminal setup, including the tools I use, the configurations of those tools, my terminal profiles, and more. Included are instructions on how to set up and use my configurations, or at least how to get started with them.

I've attempted to make this repository as automated as possible so it always stays current. To do this, I created workflows that automate updating the files in the `includes` directory when updating my [dotfiles repository](https://github.com/StrangeRanger/dotfiles), which contains my shell and terminal configurations.

<details>
<summary><strong>Table of Contents</strong></summary>

- [Custom Unix Terminal](#custom-unix-terminal)
  - [What's Included](#whats-included)
  - [Local Development](#local-development)
    - [Prerequisites](#prerequisites)
    - [Download and Setup](#download-and-setup)
  - [Automation Scripts](#automation-scripts)
    - [`update_repo.py`](#update_repopy)
    - [`update-changelog.bash`](#update-changelogbash)
  - [License](#license)

</details>

## What's Included

The documentation includes:
- **Package recommendations** for native package managers and other tools
- **Zsh configurations** with aliases, functions, and environment setup
- **Color schemes and themes** for enhanced terminal experience
- **Neovim configurations** for various use cases
- **Terminal profiles** for macOS and GNOME Terminal

## Local Development

> [!NOTE]
> The documentation is hosted online at [cut.hthompson.dev](https://cut.hthompson.dev). You only need to set up a local environment if you want to preview changes or contribute to the documentation.

### Prerequisites

To build and preview the documentation locally, you'll need:

- **Python** 3.9 or higher
- **[uv](https://github.com/astral-sh/uv#installation)** (a fast Python package manager and resolver)

### Download and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/StrangeRanger/custom-unix-terminal
   cd custom-unix-terminal
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Start the development server:**
   ```bash
   uv run mkdocs serve
   ```

4. **Open your browser:**
   Visit [http://localhost:8000](http://localhost:8000) to view the documentation with live reload.

## Automation Scripts

These scripts are integrated with the CI/CD workflow, but can also be run manually. Both scripts require the dotfiles submodule to be initialized and up to date:

```bash
git submodule update --init --remote submodules/dotfiles
```

> [!NOTE]
> The automation scripts do not require the dependencies installed via `uv`. Those dependencies are only needed for MkDocs site development and deployment.

### `update_repo.py`

Updates the configuration files in `includes/` from the dotfiles submodule.

**Manual usage:**
```bash
python3 update_repo.py
```

### `update-changelog.bash`

Updates `CHANGELOG.md` with recent changes from the dotfiles submodule.

**Manual usage:**
```bash
bash update-changelog.bash
```

## License

This project is licensed under the [MIT License](LICENSE).
