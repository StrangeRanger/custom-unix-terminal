#!/usr/bin/env python3
"""Generate documentation includes from the dotfiles submodule.

The update flow is intentionally split into small steps:

1. Read a configured source file.
2. Resolve repository-specific chezmoi template choices when needed.
3. Copy configured sections when needed.
4. Write or check the generated include files.

Most brittleness is isolated in ``utils.constants`` so upstream dotfile layout
changes fail with targeted errors instead of silently generating partial files.

NOTE: This script was rewritten with Codex.
"""

from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from utils.constants import (
    NEOVIM_JOBS,
    ZSH_JOBS,
    ZSH_SNIPPET_SECTIONS,
    RenderJob,
    RenderKind,
    SectionMarker,
)
from utils.file_utils import read_lines, read_text, write_text

LOGGER = logging.getLogger(__name__)
GUI_CONDITION = "data.isGUIEnvironment"
TEMPLATE_PREFIX = "{{"
TEMPLATE_ELSE = "{{- else -}}"
TEMPLATE_END = "{{- end }}"


# [ Data containers ] ##########################################################


@dataclass(frozen=True)
class GeneratedFile:
    """Details for one file this script creates or compares."""

    name: str
    source: Path
    destination: Path
    content: str


@dataclass(frozen=True)
class ChezmoiIfBlock:
    """The parts of one small chezmoi if/else/end section in a zsh file."""

    then_lines: list[str]
    else_lines: list[str] | None
    end_index: int


# [ General helpers ] ##########################################################


def count_lines(text: str) -> int:
    """Count text lines in the same way people usually count file lines."""
    return len(text.splitlines())


def configure_logging(debug: bool) -> None:
    """Set how much progress information the script prints."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format="[%(levelname)s] %(message)s")


# [ Section extraction helpers ] ###############################################


def find_marker(lines: list[str], marker: str, *, start_at: int = 0) -> int | None:
    """Find the first line number that contains ``marker``.

    The returned number starts at 0 because Python lists start counting at 0.
    Returns ``None`` when the marker is not found.

    Args:
        lines: Lines to search through.
        marker: Text to look for inside each line.
        start_at: Line number to start searching from. This also starts at 0.
    """
    for index in range(start_at, len(lines)):
        if marker in lines[index]:
            return index
    return None


def extract_section(
    lines: list[str],
    markers: SectionMarker,
    *,
    include_start: bool = True,
    include_end: bool = False,
    required: bool = True,
    source_label: str = "input",
) -> list[str]:
    """Copy a block of lines between two known marker strings.

    Args:
        lines: File contents as a list of lines. Each line still includes its
            ending newline character, if it had one.
        markers: The start and end text that identify the block to copy.
        include_start: Include the line that contains the start marker.
        include_end: Include the line that contains the end marker.
        required: If ``True``, stop with an error when a marker is missing. If
            ``False``, return an empty list when a marker is missing.
        source_label: Name to show in log messages and errors.

    Returns:
        The copied lines, in the same order they appeared in the source file.

    Raises:
        ValueError: A required start or end marker could not be found.
    """
    start_index = find_marker(lines, markers.start_marker)
    if start_index is None:
        if required:
            raise ValueError(
                f"{source_label}: start marker not found: {markers.start_marker!r}"
            )
        LOGGER.debug(
            "%s: optional start marker not found: %r",
            source_label,
            markers.start_marker,
        )
        return []

    end_index = find_marker(lines, markers.end_marker, start_at=start_index)
    if end_index is None:
        if required:
            raise ValueError(
                f"{source_label}: end marker not found: {markers.end_marker!r}"
            )
        LOGGER.debug(
            "%s: optional end marker not found: %r", source_label, markers.end_marker
        )
        return []

    if start_index == end_index:
        section = [lines[start_index]] if include_start or include_end else []
    else:
        first_index = start_index if include_start else start_index + 1
        last_index = end_index + 1 if include_end else end_index
        section = lines[first_index:last_index]

    LOGGER.debug(
        "%s: extracted lines %d-%d using %r -> %r (%d line(s))",
        source_label,
        start_index + 1,
        end_index + 1,
        markers.start_marker,
        markers.end_marker,
        len(section),
    )
    return section


# [ Chezmoi template helpers] ##################################################


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
            block = parse_chezmoi_if_block(lines, index, source_label=source_label)
            selected_lines = (
                block.else_lines if block.else_lines is not None else block.then_lines
            )
            selected_branch = (
                "else/non-GUI" if block.else_lines is not None else "then/no-else"
            )

            LOGGER.debug(
                "%s:%d: selected %s branch from GUI block (%d line(s))",
                source_label,
                index + 1,
                selected_branch,
                len(selected_lines),
            )
            output_lines.extend(selected_lines)
            dropped_directives += 3 if block.else_lines is not None else 2
            resolved_blocks += 1
            index = block.end_index + 1
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


# [ Documentation content builders ] ###########################################


def build_zsh_snippet(rendered_lines: list[str], *, source_label: str) -> str:
    """Create the smaller zsh snippet used by the Zensical documentation."""
    output_lines: list[str] = []

    for section in ZSH_SNIPPET_SECTIONS:
        section_lines = extract_section(
            rendered_lines,
            section.source,
            include_start=True,
            include_end=False,
            source_label=source_label,
        )

        if section.source.hard_coded_inclusion:
            LOGGER.debug(
                "%s: appended %d hard-coded line(s) after %r section",
                source_label,
                len(section.source.hard_coded_inclusion),
                section.source.start_marker,
            )
            section_lines = [*section_lines, *section.source.hard_coded_inclusion]

        output_lines.extend(
            [
                section.wrapper.start_marker,
                *section_lines,
                section.wrapper.end_marker,
            ]
        )
        LOGGER.info(
            "Built snippet section %r from %s (%d line(s))",
            section.wrapper.start_marker.strip(),
            source_label,
            len(section_lines),
        )

    return "".join(output_lines)


def render_neovim_job(job: RenderJob) -> GeneratedFile:
    """Create the content for one generated Neovim documentation file."""
    if job.kind == RenderKind.COPY:
        content = read_text(job.paths.src)
    elif job.kind == RenderKind.EXTRACT_SECTION:
        if job.section is None:
            raise ValueError(f"{job.name}: extract job is missing section markers")
        content = "".join(
            extract_section(
                read_lines(job.paths.src),
                job.section,
                include_start=True,
                include_end=False,
                source_label=str(job.paths.src),
            )
        )
    else:
        raise ValueError(f"{job.name}: unsupported Neovim render kind: {job.kind}")

    LOGGER.info(
        "Prepared %s: %s -> %s (%d line(s))",
        job.name,
        job.paths.src,
        job.paths.dest,
        count_lines(content),
    )
    return GeneratedFile(job.name, job.paths.src, job.paths.dest, content)


def render_zsh_job(job: RenderJob) -> GeneratedFile:
    """Create the content for one generated zsh documentation file."""
    rendered_lines = render_zsh_template_for_docs(
        read_lines(job.paths.src),
        source_label=str(job.paths.src),
    )

    if job.kind == RenderKind.ZSH_FULL:
        content = "".join(rendered_lines)
    elif job.kind == RenderKind.ZSH_SNIPPET:
        content = build_zsh_snippet(rendered_lines, source_label=str(job.paths.src))
    else:
        raise ValueError(f"{job.name}: unsupported zsh render kind: {job.kind}")

    LOGGER.info(
        "Prepared %s: %s -> %s (%d line(s))",
        job.name,
        job.paths.src,
        job.paths.dest,
        count_lines(content),
    )
    return GeneratedFile(job.name, job.paths.src, job.paths.dest, content)


def generate_neovim_outputs() -> list[GeneratedFile]:
    """Create all Neovim documentation files without writing them yet."""
    return [render_neovim_job(job) for job in NEOVIM_JOBS]


def generate_zsh_outputs() -> list[GeneratedFile]:
    """Create all zsh documentation files without writing them yet."""
    return [render_zsh_job(job) for job in ZSH_JOBS]


def generate_outputs() -> list[GeneratedFile]:
    """Create every documentation file without writing anything yet."""
    return [*generate_neovim_outputs(), *generate_zsh_outputs()]


# [ Generated file operations ] ################################################


def write_outputs(generated_files: Sequence[GeneratedFile]) -> None:
    """Save generated files to their destination paths."""
    for generated_file in generated_files:
        write_text(generated_file.destination, generated_file.content)
        LOGGER.info("Wrote %s", generated_file.destination)


def check_outputs(generated_files: Sequence[GeneratedFile]) -> bool:
    """Check whether the saved files already match the generated content."""
    is_current = True

    for generated_file in generated_files:
        if not generated_file.destination.exists():
            LOGGER.error("Missing generated file: %s", generated_file.destination)
            is_current = False
            continue

        current_content = read_text(generated_file.destination)
        if current_content != generated_file.content:
            LOGGER.error("Out of date: %s", generated_file.destination)
            is_current = False
        else:
            LOGGER.info("Up to date: %s", generated_file.destination)

    return is_current


# [ Old function names kept for compatibility ] ################################


def neovim_config() -> None:
    """Keep the old Neovim-only update function available."""
    write_outputs(generate_neovim_outputs())


def zsh_config() -> None:
    """Keep the old zsh-only update function available."""
    write_outputs(generate_zsh_outputs())


# [ Command-line interface ] ###################################################


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Read the command-line options passed to this script."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify generated files are current without writing them",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="show detailed rendering decisions",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the script: either update generated files or check if they are current."""
    args = parse_args(argv)
    configure_logging(debug=args.debug)

    LOGGER.info("Generating repository include files")
    generated_files = generate_outputs()

    if args.check:
        return 0 if check_outputs(generated_files) else 1

    write_outputs(generated_files)
    return 0


# [ Dunder Main ] ##############################################################

if __name__ == "__main__":
    raise SystemExit(main())
