"""Helpers for copying marker-bounded sections from text files.

This module contains the reusable line-search and section-copying logic used by
``update_repo.py``. It works with already-read line lists so callers can decide
where the text comes from and what to do with the copied section.
"""

from __future__ import annotations

import logging

from utils.constants import SectionMarker

LOGGER = logging.getLogger(__name__)


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


def handle_missing_marker(
    marker_kind: str,
    marker: str,
    *,
    required: bool,
    source_label: str,
) -> None:
    """Log optional missing markers or raise for required ones."""
    if required:
        raise ValueError(f"{source_label}: {marker_kind} marker not found: {marker!r}")

    LOGGER.debug(
        "%s: optional %s marker not found: %r",
        source_label,
        marker_kind,
        marker,
    )


def find_section_bounds(
    lines: list[str],
    markers: SectionMarker,
    *,
    required: bool,
    source_label: str,
) -> tuple[int, int] | None:
    """Find the start and end line numbers for a configured section."""
    start_index = find_marker(lines, markers.start_marker)
    if start_index is None:
        handle_missing_marker(
            "start",
            markers.start_marker,
            required=required,
            source_label=source_label,
        )
        return None

    end_index = find_marker(lines, markers.end_marker, start_at=start_index)
    if end_index is None:
        handle_missing_marker(
            "end",
            markers.end_marker,
            required=required,
            source_label=source_label,
        )
        return None

    return start_index, end_index


def copy_section_lines(
    lines: list[str],
    start_index: int,
    end_index: int,
    *,
    include_start: bool,
    include_end: bool,
) -> list[str]:
    """Copy selected lines using already-found section bounds."""
    if start_index == end_index:
        return [lines[start_index]] if include_start or include_end else []

    first_index = start_index if include_start else start_index + 1
    last_index = end_index + 1 if include_end else end_index
    return lines[first_index:last_index]


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
    bounds = find_section_bounds(
        lines,
        markers,
        required=required,
        source_label=source_label,
    )
    if bounds is None:
        return []

    start_index, end_index = bounds
    section = copy_section_lines(
        lines,
        start_index,
        end_index,
        include_start=include_start,
        include_end=include_end,
    )

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
