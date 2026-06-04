"""Utilities for calculating SHA-256 digests."""

import hashlib
import sys
from pathlib import Path


def get_text_digest(text, encoding="utf-8"):
    """Return the SHA-256 hexadecimal digest for ``text`` encoded as ``encoding``."""

    return hashlib.sha256(text.encode(encoding)).hexdigest()


def get_file_digest(file_path):
    """Return the SHA-256 hexadecimal digest for the file at ``file_path``."""

    file_path = Path(file_path)
    if sys.version_info >= (3, 11):
        with open(file_path, "rb") as file:
            return hashlib.file_digest(file, "sha256").hexdigest()

    hasher = hashlib.sha256()
    with open(file_path, "rb") as file:
        while chunk := file.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()
