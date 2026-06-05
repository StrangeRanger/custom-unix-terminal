"""Text-file helpers shared by the repository update scripts.

This module centralizes simple UTF-8 file operations used by ``update_repo.py``:
reading a whole file, reading newline-preserving lines, and writing text while
creating parent directories when needed.
"""

from pathlib import Path

PathLike = str | Path
DEFAULT_ENCODING = "utf-8"


def read_text(file_path: PathLike, encoding: str = DEFAULT_ENCODING) -> str:
    """Read a text file as a single string."""
    return Path(file_path).read_text(encoding=encoding)


def read_lines(file_path: PathLike, encoding: str = DEFAULT_ENCODING) -> list[str]:
    """Read a text file as newline-preserving lines."""
    return read_text(file_path, encoding=encoding).splitlines(keepends=True)


def write_text(
    file_path: PathLike, data: str, encoding: str = DEFAULT_ENCODING
) -> None:
    """Write text to a file, creating parent directories when needed."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding=encoding)
