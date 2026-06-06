import pytest

from src.smith_utils import FileClassification, classify_file
from src.smith_utils.file import classification


def test_classify_file_combines_extension_magic_and_mime(tmp_path):
    sample_file = tmp_path / "sample.pdf"
    sample_file.write_bytes(b"%PDF-1.7\nsmith-utils\n")

    result = classify_file(sample_file)

    assert isinstance(result, FileClassification)
    assert result.path == sample_file
    assert result.extension == ".pdf"
    assert result.extension_mime_type == "application/pdf"
    assert result.magic_type == "PDF document"
    assert result.magic_mime_type == "application/pdf"
    assert result.file_class == "document"
    assert "document" in result.categories
    assert "pdf" in result.categories


def test_classify_file_detects_magic_even_when_extension_disagrees(tmp_path):
    sample_file = tmp_path / "wrong.txt"
    sample_file.write_bytes(b"\x89PNG\r\n\x1a\nimage bytes")

    result = classify_file(sample_file)

    assert result.extension == ".txt"
    assert result.extension_mime_type == "text/plain"
    assert result.magic_type == "PNG image"
    assert result.magic_mime_type == "image/png"
    assert result.file_class == "image"
    assert "text" in result.categories
    assert "image" in result.categories
    assert "png" in result.categories


def test_classify_file_returns_file_command_output_when_available(tmp_path, monkeypatch):
    sample_file = tmp_path / "sample.bin"
    sample_file.write_bytes(b"data")

    monkeypatch.setattr(classification.shutil, "which", lambda command: "/usr/bin/file")

    def fake_run(command, capture_output, check, text):
        assert command[-1] == str(sample_file)

        class Result:
            stdout = "ASCII text\n" if "--mime-type" not in command else "text/plain\n"

        return Result()

    monkeypatch.setattr(classification.subprocess, "run", fake_run)

    result = classify_file(sample_file)

    assert result.file_description == "ASCII text"
    assert result.file_mime_type == "text/plain"
    assert "text" in result.categories


def test_classify_file_tolerates_missing_file_command(tmp_path, monkeypatch):
    sample_file = tmp_path / "sample.unknown"
    sample_file.write_bytes(b"data")
    monkeypatch.setattr(classification.shutil, "which", lambda command: None)

    result = classify_file(sample_file)

    assert result.file_description is None
    assert result.file_mime_type is None


def test_classify_file_rejects_invalid_sample_size(tmp_path):
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("text")

    with pytest.raises(ValueError, match="sample_size"):
        classify_file(sample_file, sample_size=0)
