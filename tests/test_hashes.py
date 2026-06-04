import hashlib

from src.smith_utils import crypto
from src.smith_utils.crypto import hashes
from src.smith_utils.crypto import get_file_digest, get_text_digest


def test_get_file_digest_returns_sha256_hexdigest(tmp_path):
    sample_file = tmp_path / "sample.txt"
    content = b"smith-utils\n"
    sample_file.write_bytes(content)

    assert get_file_digest(sample_file) == hashlib.sha256(content).hexdigest()


def test_get_text_digest_returns_sha256_hexdigest():
    text = "smith-utils\n"

    assert get_text_digest(text) == hashlib.sha256(text.encode("utf-8")).hexdigest()


def test_get_text_digest_handles_unicode_text():
    text = "こんにちは smith-utils"

    assert get_text_digest(text) == hashlib.sha256(text.encode("utf-8")).hexdigest()


def test_crypto_package_exports_hash_functions():
    assert "get_file_digest" in crypto.__all__
    assert "get_text_digest" in crypto.__all__
    assert crypto.get_file_digest is get_file_digest
    assert crypto.get_text_digest is get_text_digest
    assert hashes.get_file_digest is get_file_digest
    assert hashes.get_text_digest is get_text_digest
