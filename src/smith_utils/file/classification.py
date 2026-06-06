"""Utilities for classifying file types from multiple signals."""

from __future__ import annotations

from dataclasses import dataclass
import mimetypes
from pathlib import Path
import shutil
import subprocess


_MAGIC_SIGNATURES = [
    (b"%PDF-", "PDF document", "application/pdf", {"document", "pdf"}),
    (b"\x89PNG\r\n\x1a\n", "PNG image", "image/png", {"image", "png"}),
    (b"\xff\xd8\xff", "JPEG image", "image/jpeg", {"image", "jpeg"}),
    (b"GIF87a", "GIF image", "image/gif", {"image", "gif"}),
    (b"GIF89a", "GIF image", "image/gif", {"image", "gif"}),
    (b"PK\x03\x04", "ZIP archive", "application/zip", {"archive", "zip"}),
    (b"PK\x05\x06", "ZIP archive", "application/zip", {"archive", "zip"}),
    (b"PK\x07\x08", "ZIP archive", "application/zip", {"archive", "zip"}),
    (b"\x1f\x8b", "gzip compressed data", "application/gzip", {"archive", "gzip"}),
    (b"BZh", "bzip2 compressed data", "application/x-bzip2", {"archive", "bzip2"}),
    (b"7z\xbc\xaf\x27\x1c", "7-zip archive", "application/x-7z-compressed", {"archive", "7z"}),
    (b"SQLite format 3\x00", "SQLite database", "application/vnd.sqlite3", {"database", "sqlite"}),
    (b"\x7fELF", "ELF executable", "application/x-elf", {"binary", "executable", "elf"}),
    (b"\xca\xfe\xba\xbe", "Java class or Mach-O universal binary", "application/octet-stream", {"binary"}),
    (b"\xfe\xed\xfa\xce", "Mach-O executable", "application/x-mach-binary", {"binary", "executable", "mach-o"}),
    (b"\xfe\xed\xfa\xcf", "Mach-O executable", "application/x-mach-binary", {"binary", "executable", "mach-o"}),
    (b"\xce\xfa\xed\xfe", "Mach-O executable", "application/x-mach-binary", {"binary", "executable", "mach-o"}),
    (b"\xcf\xfa\xed\xfe", "Mach-O executable", "application/x-mach-binary", {"binary", "executable", "mach-o"}),
]


_MIME_CATEGORIES = {
    "application/gzip": {"archive", "gzip"},
    "application/pdf": {"document", "pdf"},
    "application/vnd.sqlite3": {"database", "sqlite"},
    "application/x-7z-compressed": {"archive", "7z"},
    "application/x-bzip2": {"archive", "bzip2"},
    "application/x-elf": {"binary", "executable", "elf"},
    "application/x-mach-binary": {"binary", "executable", "mach-o"},
    "application/zip": {"archive", "zip"},
    "text/csv": {"text", "csv"},
}


_EXTENSION_CATEGORIES = {
    ".7z": {"archive", "7z"},
    ".bz2": {"archive", "bzip2"},
    ".csv": {"text", "csv"},
    ".db": {"database"},
    ".gif": {"image", "gif"},
    ".gz": {"archive", "gzip"},
    ".jpeg": {"image", "jpeg"},
    ".jpg": {"image", "jpeg"},
    ".json": {"text", "json"},
    ".md": {"text", "markdown"},
    ".pdf": {"document", "pdf"},
    ".png": {"image", "png"},
    ".sqlite": {"database", "sqlite"},
    ".sqlite3": {"database", "sqlite"},
    ".txt": {"text"},
    ".zip": {"archive", "zip"},
}


_CLASS_PRIORITY = (
    "document",
    "image",
    "video",
    "audio",
    "archive",
    "database",
    "text",
    "binary",
    "font",
)


@dataclass(frozen=True)
class FileClassification:
    """Classification evidence for a file path."""

    path: Path
    extension: str
    file_description: str | None
    file_mime_type: str | None
    extension_mime_type: str | None
    magic_type: str | None
    magic_mime_type: str | None
    file_class: str | None
    categories: tuple[str, ...]


def classify_file(path: str | Path, *, sample_size: int = 4096) -> FileClassification:
    """Classify a file using extension, magic bytes, MIME, and ``file(1)`` signals."""

    file_path = Path(path)
    extension = file_path.suffix.lower()
    header = _read_header(file_path, sample_size)
    magic_type, magic_mime_type, magic_categories = _classify_magic(header)
    file_description = _run_file_command(file_path, "--brief")
    file_mime_type = _run_file_command(file_path, "--brief", "--mime-type")
    extension_mime_type = mimetypes.guess_type(file_path.name)[0]

    categories = set()
    categories.update(_EXTENSION_CATEGORIES.get(extension, set()))
    categories.update(magic_categories)
    categories.update(_categories_for_mime(extension_mime_type))
    categories.update(_categories_for_mime(file_mime_type))
    categories.update(_categories_for_mime(magic_mime_type))

    sorted_categories = tuple(sorted(categories))

    return FileClassification(
        path=file_path,
        extension=extension,
        file_description=file_description,
        file_mime_type=file_mime_type,
        extension_mime_type=extension_mime_type,
        magic_type=magic_type,
        magic_mime_type=magic_mime_type,
        file_class=_select_file_class(sorted_categories),
        categories=sorted_categories,
    )


def _read_header(path: Path, sample_size: int) -> bytes:
    if sample_size < 1:
        raise ValueError("sample_size must be greater than zero")

    with path.open("rb") as file:
        return file.read(sample_size)


def _classify_magic(header: bytes) -> tuple[str | None, str | None, set[str]]:
    for signature, file_type, mime_type, categories in _MAGIC_SIGNATURES:
        if header.startswith(signature):
            return file_type, mime_type, set(categories)
    return None, None, set()


def _categories_for_mime(mime_type: str | None) -> set[str]:
    if not mime_type:
        return set()

    categories = set(_MIME_CATEGORIES.get(mime_type, set()))
    root_type = mime_type.split("/", 1)[0]
    if root_type in {"audio", "font", "image", "text", "video"}:
        categories.add(root_type)
    return categories


def _select_file_class(categories: tuple[str, ...]) -> str | None:
    category_set = set(categories)
    for file_class in _CLASS_PRIORITY:
        if file_class in category_set:
            return file_class
    return categories[0] if categories else None


def _run_file_command(path: Path, *args: str) -> str | None:
    if shutil.which("file") is None:
        return None

    try:
        result = subprocess.run(
            ["file", *args, str(path)],
            capture_output=True,
            check=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None

    output = result.stdout.strip()
    return output or None
