#!/usr/bin/env python3
"""Configuration file update automation script.

This script automates the process of updating Neovim and zsh configuration files in the
`includes` directory by extracting relevant sections from dotfiles stored in the
`submodules/dotfiles` submodule.

The script handles two main types of configuration updates:
    - Neovim configuration files with selective content extraction
    - Zsh configuration files with snippet-based processing

Notes:
    - This script is, unfortunately, fragile by nature. Changes to upstream marker text
      or chezmoi template layout can silently break extractions. When this occurs,
      adjust the markers in the constants module or update the `chezmoi_edge_case`
      function as needed.
    - No external dependencies are required; a virtual environment is not necessary.

Example:
    Run the script directly to update all configuration files:

    ```bash
    $ python3 update_repo.py
    ```
"""

# [ Imports ]###########################################################################

from utils.file_utils import read_file, read_lines, write_file
from utils.constants import (
    NEOVIM_CONFIG_PATHS,
    ZSH_CONFIG_PATHS,
    NEOVIM_MARKERS,
    ZSH_ALIAS_MARKERS,
    ZSH_LS_COLORS_MARKERS,
    MKDOCS_USER_CONFIG_MARKERS,
    MKDOCS_LS_COLORS_MARKERS,
)


# [ Functions ]#########################################################################


def neovim_config() -> None:
    """Process and write Neovim config file variants to the `includes` directory.

    Handles two types of Neovim config processing:
        1. `init_vim_no_plug`: Extracts content between designated section markers,
           excluding plugin-related configurations.
        2. Other variants: Copies the entire source file without modification.

    The function iterates through all Neovim config paths defined in
    `NEOVIM_CONFIG_PATHS` and processes each according to its operation type.

    Note:
        The `init_vim_no_plug` operation relies on `NEOVIM_MARKERS` to identify
        content boundaries. The end marker line itself is excluded from output.
    """
    for operation, paths in NEOVIM_CONFIG_PATHS.items():
        if operation == "init_vim_no_plug":
            data: list[str] = read_lines(paths.src)
            filtered_data: list[str] = []

            for current_line in data:
                if NEOVIM_MARKERS.start_marker in current_line:
                    NEOVIM_MARKERS.is_within_section = True
                if (
                    NEOVIM_MARKERS.end_marker in current_line
                    and NEOVIM_MARKERS.is_within_section
                ):
                    NEOVIM_MARKERS.is_within_section = False
                    break
                if NEOVIM_MARKERS.is_within_section:
                    filtered_data.append(current_line)
            write_file(paths.dest, "".join(filtered_data))
        else:
            data: str = read_file(paths.src)
            write_file(paths.dest, data)


def chezmoi_edge_case(current_line: str, data: list[str], line_number: int) -> int:
    """Calculate the number of lines to skip for chezmoi template actions.

    Handles special cases in chezmoi template processing by analyzing the current line
    and subsequent lines to determine how many lines should be skipped during zsh
    configuration processing.

    Note:
        This function's logic is tightly coupled to the current structure of the
        dotfiles. Changes to the upstream chezmoi template layout may require updates
        to the pattern matching logic.

    Args:
        current_line: The current line being processed, which contains a chezmoi
            template delimiter.
        data: Complete list of lines from the source zsh configuration file.
        line_number: Zero-based index of the current line within the data list.

    Returns:
        Number of lines to skip (minimum 1).
    """
    if "data.isGUIEnvironment" in current_line:
        if (
            "plugins=(" in data[line_number + 1]
            and "plugins=(" in data[line_number + 2]
        ):
            return 3
        elif (
            "hash xdg-open" in data[line_number + 1]
            and "{{- end }}" in data[line_number + 2]
        ):
            return 1

    return 1


def zsh_config() -> None:
    """Process and write zsh config file variants and snippets to the `includes`
    directory.

    Handles two types of processing:
        1. Full file operations: Copies entire source file, filtering chezmoi template
           actions.
        2. Snippet operations: Extracts specific sections and wraps with MkDocs section
           markers.

    For snippet operations, extracts alias and `LS_COLORS` sections based on predefined
    markers and optionally appends hard-coded content.

    Note:
        Includes debug output for CI/CD troubleshooting.
    """
    for file_operation, file_paths in ZSH_CONFIG_PATHS.items():
        data: list[str] = read_lines(file_paths.src)
        output_data: list[str] = []
        line_number = 0

        while line_number < len(data):
            current_line = data[line_number]

            ## DEBUG: The below lines help with debugging...
            print(f"Processing line {line_number + 1} of {file_paths.src}")
            print(f"Line: {current_line}")

            if current_line.lstrip().startswith("{{"):
                skip_line_count = chezmoi_edge_case(current_line, data, line_number)
                line_number += skip_line_count
                continue

            if not file_operation.endswith("snippet"):
                output_data.append(current_line)
                line_number += 1
                continue

            if ZSH_ALIAS_MARKERS.start_marker in current_line:
                ZSH_ALIAS_MARKERS.is_within_section = True
                output_data.append(MKDOCS_USER_CONFIG_MARKERS.start_marker)
            elif ZSH_LS_COLORS_MARKERS.start_marker in current_line:
                ZSH_LS_COLORS_MARKERS.is_within_section = True
                output_data.append(MKDOCS_LS_COLORS_MARKERS.start_marker)

            if (
                ZSH_ALIAS_MARKERS.end_marker in current_line
                and ZSH_ALIAS_MARKERS.is_within_section
            ):
                ZSH_ALIAS_MARKERS.is_within_section = False
                output_data.append(MKDOCS_USER_CONFIG_MARKERS.end_marker)
            elif (
                ZSH_LS_COLORS_MARKERS.end_marker in current_line
                and ZSH_LS_COLORS_MARKERS.is_within_section
            ):
                ZSH_LS_COLORS_MARKERS.is_within_section = False
                if ZSH_LS_COLORS_MARKERS.hard_coded_inclusion:
                    output_data.extend(ZSH_LS_COLORS_MARKERS.hard_coded_inclusion)
                output_data.append(MKDOCS_LS_COLORS_MARKERS.end_marker)

            if (
                ZSH_ALIAS_MARKERS.is_within_section
                or ZSH_LS_COLORS_MARKERS.is_within_section
            ):
                output_data.append(current_line)

            line_number += 1

        write_file(file_paths.dest, "".join(output_data))


def main() -> None:
    """Execute all configuration file update routines."""
    neovim_config()
    zsh_config()


# [ Dunder Main ]#######################################################################

if __name__ == "__main__":
    main()
