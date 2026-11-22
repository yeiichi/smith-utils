import hashlib
import string

from src.smith_utils.cli import main


def test_random_string_command_prints_requested_length(capsys):
    assert main(["random-string", "12"]) == 0

    output = capsys.readouterr().out.strip()
    assert len(output) == 12
    assert set(output) <= set(string.ascii_letters + string.digits)


def test_random_string_command_accepts_category(capsys):
    assert main(["random-string", "4", "--category", "kanji"]) == 0

    assert len(capsys.readouterr().out.strip()) == 4


def test_digest_command_hashes_text(capsys):
    assert main(["digest", "--text", "smith-utils"]) == 0

    assert capsys.readouterr().out.strip() == hashlib.sha256(b"smith-utils").hexdigest()


def test_digest_command_hashes_file(tmp_path, capsys):
    sample_file = tmp_path / "sample.txt"
    sample_file.write_bytes(b"file content")

    assert main(["digest", str(sample_file)]) == 0

    assert capsys.readouterr().out.strip() == hashlib.sha256(b"file content").hexdigest()


def test_normalize_text_command_normalizes_argument(capsys):
    assert main(["normalize-text", "  Ｓｍｉｔｈ  Ｕｔｉｌｓ  "]) == 0

    assert capsys.readouterr().out.strip() == "smith utils"


def test_normalize_text_command_can_read_stdin(monkeypatch, capsys):
    class FakeStdin:
        def read(self):
            return "  Hello   World  "

    monkeypatch.setattr("src.smith_utils.cli.sys.stdin", FakeStdin())

    assert main(["normalize-text"]) == 0

    assert capsys.readouterr().out.strip() == "hello world"


def test_normalize_text_command_can_keep_case(capsys):
    assert main(["normalize-text", "--keep-case", "  Hello   World  "]) == 0

    assert capsys.readouterr().out.strip() == "Hello World"


def test_com_name_cleaner_command_prints_parts(capsys):
    assert main(["com-name-cleaner", "--parts", "例示用商事（株）"]) == 0

    assert capsys.readouterr().out.strip() == '[null, "例示用商事", "株式会社"]'


def test_unicode_names_command_prints_tab_separated_records(capsys):
    assert main(["unicode-names", "Aあ"]) == 0

    assert capsys.readouterr().out.splitlines() == [
        "0\tU+0041\tA\tLATIN CAPITAL LETTER A",
        "1\tU+3042\tあ\tHIRAGANA LETTER A",
    ]


def test_classify_file_command_prints_key_value_fields(tmp_path, capsys):
    sample_file = tmp_path / "sample.pdf"
    sample_file.write_bytes(b"%PDF-1.7\nsmith-utils\n")

    assert main(["classify-file", str(sample_file)]) == 0

    output = capsys.readouterr().out.splitlines()
    assert f"path={sample_file}" in output
    assert "extension=.pdf" in output
    assert "file_class=document" in output
    assert "magic_type=PDF document" in output


def test_positive_gaussian_samples_command_prints_one_sample_per_line(monkeypatch, capsys):
    monkeypatch.setattr(
        "src.smith_utils.cli.sample_positive_gaussian",
        lambda mean, approx_upper_bound, trial_number: [1.25, 2.5],
    )

    assert main(["positive-gaussian-samples", "2", "--mean", "1", "--approx-upper-bound", "3"]) == 0

    assert capsys.readouterr().out.splitlines() == ["1.25", "2.5"]
