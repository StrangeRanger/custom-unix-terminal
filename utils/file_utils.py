"""File I/O utilities for the repository update automation system.

This module provides simple, consistent wrappers around pathlib operations for
reading and writing text files. These utilities are used throughout the project
to handle configuration file processing with proper encoding support.

All functions accept both string paths and pathlib.Path objects for flexibility.
"""

from pathlib import Path
from typing import List


def read_file(file_path: str | Path, encoding: str = "utf-8") -> str:
    """Return the full text contents of ``file_path``.

    Args:
        file_path: Filesystem path or path-like string.
        encoding: Text encoding used to decode the file (default UTF-8).

    Returns:
        The decoded file contents as a single string.
    """
    return Path(file_path).read_text(encoding=encoding)


def read_lines(file_path: str | Path, encoding: str = "utf-8") -> List[str]:
    """Return file contents as a list of lines, preserving newline characters.

    Args:
        file_path: Filesystem path or path-like string.
        encoding: Text encoding used to decode the file (default UTF-8).

    Returns:
        List of lines including their terminating newlines where present.
    """
    text = Path(file_path).read_text(encoding=encoding)
    return text.splitlines(keepends=True)


def write_file(file_path: str | Path, data: str, encoding: str = "utf-8") -> None:
    """Write text to ``file_path``, creating the file if it doesn't exist.

    Args:
        file_path: Destination path; parent directories must already exist.
        data: Text to write.
        encoding: Text encoding used to encode the file (default UTF-8).
    """
    Path(file_path).write_text(data, encoding=encoding)
