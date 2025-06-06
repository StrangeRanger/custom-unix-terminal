#!/usr/bin/env python3
#
# Automates the process of updating zsh and neovim configuration files in the 'includes'
# directory. This is done by reading my 'dotfiles' in the 'submodules/dotfiles'
# submodule and applying the necessary changes to the 'includes' directory.
#
# NOTE:
#   - This script does not require the initialization of a virtual environment. The
#     Pipfiles are only required when deploying the MkDocs site.
#   - This script has some hard-coded values that may make it fragile in some cases.
#     I've attempted to do my best an indicate where these values are, but it's always a
#     good idea to keep an eye on this script when making changes to the configuration.
#
########################################################################################
# [ Imports ]###########################################################################


from utils.file_utils import read_file, write_file
from utils.constants import (
    CHEZMOI_STATEMENTS,
    NEOVIM_CONFIG_PATHS,
    ZSH_CONFIG_PATHS,
    NEOVIM_MARKERS,
    ZSH_ALIAS_MARKERS,
    ZSH_LS_COLORS_MARKERS,
    MKDOCS_USER_CONFIG_MARKERS,
    MKDOCS_LS_COLORS_MARKERS,
)


# [ Functions ]#########################################################################


def neovim_config():
    """Updates the neovim configuration files."""
    for operation, paths in NEOVIM_CONFIG_PATHS.items():
        data: list[str] | str = read_file(
            paths["from"], read_lines=(operation == "init_vim_no_plug")
        )

        if operation == "init_vim_no_plug":
            filtered_data: list[str] = []
            for line in data:
                if NEOVIM_MARKERS.start_marker in line:
                    NEOVIM_MARKERS.is_within_section = True
                if (
                    NEOVIM_MARKERS.end_marker in line
                    and NEOVIM_MARKERS.is_within_section
                ):
                    NEOVIM_MARKERS.is_within_section = False
                    break
                if NEOVIM_MARKERS.is_within_section:
                    filtered_data.append(line)
            write_file(paths["to"], "".join(filtered_data))
        else:
            write_file(paths["to"], data)


def zsh_config():
    """Updates the zsh configuration files."""
    for file_operation, file_paths in ZSH_CONFIG_PATHS.items():
        data: list[str] = read_file(file_paths["from"], read_lines=True)
        output_data: list[str] = []
        line_number = 0

        while line_number < len(data):
            line = data[line_number]

            ## DEBUG: The below lines help with debugging, especially when running in a
            ##  CI/CD environment.
            print(f"Processing line {line_number + 1} of {file_paths['from']}")
            print(f"Line: {line}")

            if any(marker in line for marker in CHEZMOI_STATEMENTS):
                line_number += 1
                continue

            if not file_operation.endswith("snippet"):
                output_data.append(line)
                line_number += 1
                continue

            if ZSH_ALIAS_MARKERS.start_marker in line:
                ZSH_ALIAS_MARKERS.is_within_section = True
                output_data.append(MKDOCS_USER_CONFIG_MARKERS.start_marker)
            elif ZSH_LS_COLORS_MARKERS.start_marker in line:
                ZSH_LS_COLORS_MARKERS.is_within_section = True
                output_data.append(MKDOCS_LS_COLORS_MARKERS.start_marker)

            if (
                ZSH_ALIAS_MARKERS.end_marker in line
                and ZSH_ALIAS_MARKERS.is_within_section
            ):
                ZSH_ALIAS_MARKERS.is_within_section = False
                output_data.append(MKDOCS_USER_CONFIG_MARKERS.end_marker)
            elif (
                ZSH_LS_COLORS_MARKERS.end_marker in line
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
                output_data.append(line)

            line_number += 1

        write_file(file_paths["to"], "".join(output_data))


def main():
    """Main function."""
    neovim_config()
    zsh_config()


# [ Dunder Main ]#######################################################################

if __name__ == "__main__":
    main()
