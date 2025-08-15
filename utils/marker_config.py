"""Configuration utilities for text section parsing.

This module provides the SectionMarkers class, which is used throughout the
repository update automation system to define and track delimited text sections
in configuration files. It supports the extraction of specific content blocks
from dotfiles during the automated update process.

The primary use case is in update_repo.py, where SectionMarkers instances are
used to extract snippets from Neovim and zsh configuration files for inclusion
in the project documentation.
"""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class SectionMarkers:
    """A configuration class for identifying and processing delimited text sections.

    This class provides a stateful mechanism for extracting content between the start
    and end markers in text files. The caller is responsible for managing the
    `is_within_section` state and handling any `hard_coded_inclusion` content.

    Note:
        - Matching uses plain substring comparison (no regex).
        - Instance state is mutable and not thread-safe.
        - The caller must handle the `hard_coded_inclusion` content manually.

    Attributes:
        start_marker: Substring that signals the beginning of a section.
        end_marker: Substring that signals the end of a section.
        hard_coded_inclusion: Optional literal lines (with newlines) that the caller
            should append immediately after the section closes.
        is_within_section: Mutable flag that tracks whether the parser is currently
            within a marked section. Defaults to False.

    Example:
        Basic usage for extracting content between markers:

        ```python
        collected = []
        markers = SectionMarkers(start_marker='## Start', end_marker='## End')

        for line in lines:
            if markers.start_marker in line:
                markers.is_within_section = True
            elif markers.end_marker in line and markers.is_within_section:
                markers.is_within_section = False
            elif markers.is_within_section:
                collected.append(line)
        ```
    """

    start_marker: str
    end_marker: str
    hard_coded_inclusion: Optional[Tuple[str, ...]] = None
    is_within_section: bool = False
