#!/usr/bin/env python3
"""Generate documentation includes from the dotfiles submodule.

The update flow is intentionally split into small steps:

1. Read a configured source file.
2. Render repository-specific chezmoi template choices when needed.
3. Extract configured sections when needed.
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


@dataclass(frozen=True)
class GeneratedFile:
    """A generated file that can be written or checked."""

    name: str
    source: Path
    destination: Path
    content: str


@dataclass(frozen=True)
class ChezmoiIfBlock:
    """A simple chezmoi if/else/end block extracted from a zsh template."""

    then_lines: list[str]
    else_lines: list[str] | None
    end_index: int


def count_lines(text: str) -> int:
    """Return a human-friendly line count for logging."""
    return len(text.splitlines())


def configure_logging(debug: bool) -> None:
    """Configure console logging for the update run."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format="[%(levelname)s] %(message)s")


def is_template_directive(line: str) -> bool:
    """Return whether a line starts with a chezmoi template action."""
    return line.lstrip().startswith(TEMPLATE_PREFIX)


def is_gui_if_directive(line: str) -> bool:
    """Return whether a template directive opens the supported GUI condition."""
    return (
        is_template_directive(line)
        and line.lstrip().startswith("{{ if")
        and GUI_CONDITION in line
    )


def is_if_directive(line: str) -> bool:
    """Return whether a template directive opens any chezmoi if block."""
    return is_template_directive(line) and line.lstrip().startswith("{{ if")


def extract_section(
    lines: list[str],
    markers: SectionMarker,
    *,
    include_start: bool = True,
    include_end: bool = False,
    required: bool = True,
    source_label: str = "input",
) -> list[str]:
    """Extract lines inside a marker-delimited section.

    Args:
        lines: Source contents split into newline-preserving lines.
        markers: Marker pair that identifies the section to extract.
        include_start: Include the line containing ``markers.start_marker``.
        include_end: Include the line containing ``markers.end_marker``.
        required: Raise ``ValueError`` when markers are missing. If ``False``,
            return an empty list instead.
        source_label: Human-readable source name for logs and errors.

    Returns:
        Extracted lines in their original order.

    Raises:
        ValueError: A required start or end marker was not found.
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


def find_marker(lines: list[str], marker: str, *, start_at: int = 0) -> int | None:
    """Return the first index containing ``marker`` at or after ``start_at``."""
    for index in range(start_at, len(lines)):
        if marker in lines[index]:
            return index
    return None


def parse_chezmoi_if_block(
    lines: list[str],
    start_index: int,
    *,
    source_label: str,
) -> ChezmoiIfBlock:
    """Parse the simple chezmoi if blocks used by the zsh templates.

    The current templates only need one level of ``if`` with an optional ``else``.
    Raising on nested or unclosed blocks makes upstream template changes obvious.
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
    """Render the small chezmoi subset used by zsh templates for docs output.

    The docs output intentionally keeps the non-GUI branch when a GUI condition
    has an ``else`` block. If the GUI condition has no ``else`` block, the body is
    kept to preserve the historical generated output.
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


def build_zsh_snippet(rendered_lines: list[str], *, source_label: str) -> str:
    """Build a Zensical zsh snippet from rendered zsh lines."""
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
    """Render one Neovim output job."""
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
    """Render one zsh output job."""
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
    """Generate all configured Neovim outputs in memory."""
    return [render_neovim_job(job) for job in NEOVIM_JOBS]


def generate_zsh_outputs() -> list[GeneratedFile]:
    """Generate all configured zsh outputs in memory."""
    return [render_zsh_job(job) for job in ZSH_JOBS]


def generate_outputs() -> list[GeneratedFile]:
    """Generate every configured output in memory."""
    return [*generate_neovim_outputs(), *generate_zsh_outputs()]


def write_outputs(generated_files: Sequence[GeneratedFile]) -> None:
    """Write generated files to disk."""
    for generated_file in generated_files:
        write_text(generated_file.destination, generated_file.content)
        LOGGER.info("Wrote %s", generated_file.destination)


def check_outputs(generated_files: Sequence[GeneratedFile]) -> bool:
    """Return whether generated content matches files already on disk."""
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


def neovim_config() -> None:
    """Compatibility wrapper that writes only Neovim outputs."""
    write_outputs(generate_neovim_outputs())


def zsh_config() -> None:
    """Compatibility wrapper that writes only zsh outputs."""
    write_outputs(generate_zsh_outputs())


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
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
    """Generate or check repository include files."""
    args = parse_args(argv)
    configure_logging(debug=args.debug)

    LOGGER.info("Generating repository include files")
    generated_files = generate_outputs()

    if args.check:
        return 0 if check_outputs(generated_files) else 1

    write_outputs(generated_files)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
