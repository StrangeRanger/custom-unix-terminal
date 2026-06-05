#!/usr/bin/env python3
"""Generate checked-in documentation snippets from the dotfiles submodule.

This script keeps the documentation include files in sync with the source
configuration files stored under ``submodules/dotfiles``. It reads the configured
Neovim and zsh source files, prepares the documentation-friendly versions, and
either writes the generated include files or checks that the checked-in files are
already current.

The main update flow is:

1. Read a configured source file.
2. Resolve the small chezmoi template patterns used by zsh files.
3. Copy configured sections when only part of a source file belongs in docs.
4. Build ``GeneratedFile`` objects that describe the intended output files.
5. Write those files, or compare them with the files already on disk.

The exact source paths, destination paths, and section markers live in
``utils.constants``. Keeping that configuration separate makes source layout
changes fail with targeted errors instead of silently producing partial or
misleading documentation.

NOTE: Almost all the Python scripts were rewritten with Codex and modified by Hunter T.
"""

from __future__ import annotations

import argparse
import logging
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

from utils.constants import (
    NEOVIM_JOBS,
    ZSH_JOBS,
    ZSH_SNIPPET_SECTIONS,
    RenderJob,
    RenderKind,
)
from utils.chezmoi_utils import render_zsh_template_for_docs
from utils.file_utils import read_lines, read_text, write_text
from utils.section_utils import extract_section

LOGGER = logging.getLogger(__name__)


# [ Data containers ] ##########################################################


@dataclass(frozen=True)
class GeneratedFile:
    """Details for one file this script creates or compares."""

    name: str
    source: Path
    destination: Path
    content: str


# [ General helpers ] ##########################################################


def count_lines(text: str) -> int:
    """Count text lines in the same way people usually count file lines."""
    return len(text.splitlines())


def configure_logging(debug: bool) -> None:
    """Set how much progress information the script prints."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format="[%(levelname)s] %(message)s")


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
            # Some docs snippets include helper lines that are implied by the
            # source section but are not physically inside the copied range.
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


def write_outputs(generated_files: Iterable[GeneratedFile]) -> None:
    """Save generated files to their destination paths."""
    for generated_file in generated_files:
        write_text(generated_file.destination, generated_file.content)
        LOGGER.info("Wrote %s", generated_file.destination)


def check_outputs(generated_files: Iterable[GeneratedFile]) -> bool:
    """Check whether the saved files already match the generated content."""
    is_current = True

    for generated_file in generated_files:
        # Check mode reports every mismatch instead of stopping at the first one.
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


# [ Command-line interface ] ###################################################


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Read the command-line options passed to this script."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--check",
        action="store_true",
        help="verify generated files are current without writing them",
    )
    parser.add_argument(
        "-d",
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
