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

from pathlib import Path

from utils.file_utils import read_file, read_lines, write_file
from utils.constants import (
    NEOVIM_CONFIG_PATHS,
    ZSH_CONFIG_PATHS,
    NEOVIM_MARKERS,
    SectionMarker,
    ZSH_ALIAS_MARKERS,
    ZSH_LS_COLORS_MARKERS,
    ZENSICAL_USER_CONFIG_MARKERS,
    ZENSICAL_LS_COLORS_MARKERS,
)


# [ Functions ]#########################################################################


def extract_between(
    lines: list[str],
    markers: SectionMarker,
    *,
    include_start: bool = True,
    include_end: bool = False,
    required: bool = True,
) -> list[str]:
    """Return lines inside a marker-delimited section.

    Args:
        lines: Source file contents split into newline-preserving lines.
        markers: Marker pair that identifies the section to extract.
        include_start: Include the line containing ``markers.start_marker``.
        include_end: Include the line containing ``markers.end_marker``.
        required: Raise ``ValueError`` when markers are missing. If ``False``,
            return an empty list instead.

    Returns:
        Extracted lines in their original order.

    Raises:
        ValueError: The start or end marker was not found and ``required`` is
            ``True``.
    """
    extracted_lines: list[str] = []
    is_within_section = False
    found_start_marker = False

    for current_line in lines:
        if not is_within_section:
            if markers.start_marker in current_line:
                found_start_marker = True
                is_within_section = True
                if include_start:
                    extracted_lines.append(current_line)

                # Keep the helper safe for single-line sections, even though the
                # current config markers are expected to be on separate lines.
                if markers.end_marker in current_line:
                    if include_end and not include_start:
                        extracted_lines.append(current_line)
                    return extracted_lines

            continue

        if markers.end_marker in current_line:
            if include_end:
                extracted_lines.append(current_line)
            return extracted_lines

        extracted_lines.append(current_line)

    if not required:
        return []

    # Marker drift should stop generation instead of silently writing partial files.
    if not found_start_marker:
        raise ValueError(f"Start marker not found: {markers.start_marker!r}")

    raise ValueError(f"End marker not found: {markers.end_marker!r}")


def neovim_config() -> None:
    """Process and write Neovim config file variants to the `includes` directory.

    The `init_vim_no_plug` variant extracts from the general configuration
    marker through, but not including, the vim-plug marker. Other variants copy
    the source file unchanged.

    Raises:
        ValueError: The Neovim section markers are missing or reordered.
    """
    for operation, paths in NEOVIM_CONFIG_PATHS.items():
        if operation == "init_vim_no_plug":
            data: list[str] = read_lines(paths.src)
            filtered_data = extract_between(data, NEOVIM_MARKERS)
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


def filter_chezmoi_template_actions(data: list[str], file_path: Path) -> list[str]:
    """Remove chezmoi template action lines before writing shell snippets.

    Args:
        data: Source zsh template contents split into newline-preserving lines.
        file_path: Source path used only for debug output.

    Returns:
        Lines with chezmoi action delimiters removed. Some known branch content is
        skipped by `chezmoi_edge_case()` to preserve the intended generated zsh
        output.
    """
    output_data: list[str] = []
    line_number = 0

    while line_number < len(data):
        current_line = data[line_number]

        ## DEBUG: The below lines help with debugging...
        print(f"Processing line {line_number + 1} of {file_path}")
        print(f"Line: {current_line}")

        if current_line.lstrip().startswith("{{"):
            # Chezmoi directives are not valid shell output; skip the directive and
            # any branch content that this repository intentionally omits.
            skip_line_count = chezmoi_edge_case(current_line, data, line_number)
            line_number += skip_line_count
            continue

        output_data.append(current_line)
        line_number += 1

    return output_data


def zsh_config() -> None:
    """Process and write zsh config file variants and snippets to the `includes`
    directory.

    Full zsh outputs are the source templates with chezmoi actions filtered out.
    Snippet outputs extract the aliases and `LS_COLORS` sections, then wrap them
    with Zensical include markers.

    Raises:
        ValueError: A required zsh snippet section marker is missing or reordered.
    """
    for file_operation, file_paths in ZSH_CONFIG_PATHS.items():
        data: list[str] = read_lines(file_paths.src)
        output_data = filter_chezmoi_template_actions(data, file_paths.src)

        if file_operation.endswith("snippet"):
            alias_lines = extract_between(output_data, ZSH_ALIAS_MARKERS)
            ls_colors_lines = extract_between(output_data, ZSH_LS_COLORS_MARKERS)
            if ZSH_LS_COLORS_MARKERS.hard_coded_inclusion:
                ls_colors_lines.extend(ZSH_LS_COLORS_MARKERS.hard_coded_inclusion)

            output_data = [
                ZENSICAL_USER_CONFIG_MARKERS.start_marker,
                # Expand the extracted lines into the output list; join() expects
                # a flat list of strings, not nested lists.
                *alias_lines,
                ZENSICAL_USER_CONFIG_MARKERS.end_marker,
                ZENSICAL_LS_COLORS_MARKERS.start_marker,
                *ls_colors_lines,
                ZENSICAL_LS_COLORS_MARKERS.end_marker,
            ]

        write_file(file_paths.dest, "".join(output_data))


def main() -> None:
    """Execute all configuration file update routines."""
    neovim_config()
    zsh_config()


# [ Dunder Main ]#######################################################################

if __name__ == "__main__":
    main()
