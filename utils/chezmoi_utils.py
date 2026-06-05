"""Helpers for rendering supported chezmoi zsh templates for documentation.

This module handles only the small subset of chezmoi template syntax used by the
zsh source files. Unsupported or more complex template blocks raise errors so
source template changes do not silently produce misleading documentation.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

LOGGER = logging.getLogger(__name__)
GUI_CONDITION = "data.isGUIEnvironment"
TEMPLATE_PREFIX = "{{"
TEMPLATE_ELSE = "{{- else -}}"
TEMPLATE_END = "{{- end }}"


@dataclass(frozen=True)
class ChezmoiIfBlock:
    """The parts of one small chezmoi if/else/end section in a zsh file."""

    then_lines: list[str]
    else_lines: list[str] | None
    end_index: int


def is_template_directive(line: str) -> bool:
    """Check whether a line starts with a chezmoi template command."""
    return line.lstrip().startswith(TEMPLATE_PREFIX)


def is_gui_if_directive(line: str) -> bool:
    """Check whether a line starts the GUI-only chezmoi condition we support."""
    return (
        is_template_directive(line)
        and line.lstrip().startswith("{{ if")
        and GUI_CONDITION in line
    )


def is_if_directive(line: str) -> bool:
    """Check whether a line starts any chezmoi if statement."""
    return is_template_directive(line) and line.lstrip().startswith("{{ if")


def parse_chezmoi_if_block(
    lines: list[str],
    start_index: int,
    *,
    source_label: str,
) -> ChezmoiIfBlock:
    """Read one simple chezmoi if block from a zsh template.

    This script only understands one ``if`` with an optional ``else``. It raises
    an error for more complicated blocks so template changes do not get handled
    incorrectly without anyone noticing.

    Args:
        lines: Template file contents as a list of lines.
        start_index: Line number where the opening chezmoi ``if`` starts. This
            starts at 0 because Python lists start counting at 0.
        source_label: Name to show in error messages.

    Raises:
        ValueError: The block has duplicate ``else`` lines, contains another
            ``if`` block, or does not have a closing ``end`` line.
    """
    then_lines: list[str] = []
    else_lines: list[str] | None = None
    # active_lines points at the list that should receive body lines as we scan.
    # It starts with the "if" body and switches to the "else" body if one exists.
    active_lines = then_lines

    for index in range(start_index + 1, len(lines)):
        current_line = lines[index]
        stripped_line = current_line.strip()

        if stripped_line == TEMPLATE_ELSE:
            if else_lines is not None:
                raise ValueError(f"{source_label}:{index + 1}: duplicate chezmoi else")
            else_lines = []
            active_lines = else_lines
            continue

        if stripped_line == TEMPLATE_END:
            return ChezmoiIfBlock(
                then_lines=then_lines,
                else_lines=else_lines,
                end_index=index,
            )

        if is_if_directive(current_line):
            raise ValueError(
                f"{source_label}:{index + 1}: nested chezmoi if blocks are not supported"
            )

        active_lines.append(current_line)

    raise ValueError(f"{source_label}:{start_index + 1}: unclosed chezmoi if block")


def resolve_gui_if_block(
    lines: list[str],
    start_index: int,
    *,
    source_label: str,
) -> tuple[list[str], int, int]:
    """Choose the zsh lines to keep from one supported GUI template block."""
    block = parse_chezmoi_if_block(lines, start_index, source_label=source_label)
    # Docs should show the non-GUI setup when the template offers one.
    # If no "else" exists, keep the GUI body to preserve older output.
    selected_lines = (
        block.else_lines if block.else_lines is not None else block.then_lines
    )
    selected_branch = "else/non-GUI" if block.else_lines is not None else "then/no-else"

    LOGGER.debug(
        "%s:%d: selected %s branch from GUI block (%d line(s))",
        source_label,
        start_index + 1,
        selected_branch,
        len(selected_lines),
    )

    # Count the template-only lines removed from the final zsh output.
    dropped_directives = 3 if block.else_lines is not None else 2
    return selected_lines, block.end_index + 1, dropped_directives


def render_zsh_template_for_docs(lines: list[str], *, source_label: str) -> list[str]:
    """Turn zsh template lines into plain zsh lines for documentation.

    When the template has separate GUI and non-GUI versions, the documentation
    uses the non-GUI version. If there is no non-GUI version, the GUI-only lines
    are kept so the generated documentation stays the same as before.
    """
    output_lines: list[str] = []
    dropped_directives = 0
    resolved_blocks = 0
    index = 0

    while index < len(lines):
        current_line = lines[index]

        if not is_template_directive(current_line):
            output_lines.append(current_line)
            index += 1
            continue

        if is_gui_if_directive(current_line):
            selected_lines, next_index, dropped_count = resolve_gui_if_block(
                lines,
                index,
                source_label=source_label,
            )
            output_lines.extend(selected_lines)
            dropped_directives += dropped_count
            resolved_blocks += 1
            index = next_index
            continue

        if is_if_directive(current_line):
            raise ValueError(
                f"{source_label}:{index + 1}: unsupported chezmoi if directive"
            )

        LOGGER.debug(
            "%s:%d: dropped template directive: %s",
            source_label,
            index + 1,
            current_line.strip(),
        )
        dropped_directives += 1
        index += 1

    LOGGER.info(
        "Rendered %s: %d source line(s) -> %d output line(s), "
        "dropped %d directive(s), resolved %d block(s)",
        source_label,
        len(lines),
        len(output_lines),
        dropped_directives,
        resolved_blocks,
    )
    return output_lines
