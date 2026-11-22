import csv
import subprocess
import sys

import pytest

from smith_utils.com_name_cleaner.csv_io import clean_csv


@pytest.mark.parametrize("entry_point", [
    ["-m", "smith_utils.com_name_cleaner"],
    ["-m", "smith_utils.cli", "com-name-cleaner"],
])
def test_csv_cli(tmp_path, entry_point):
    source = tmp_path / "list.csv"
    source.write_bytes('ID,会社名,備考\r\n001,川崎車両　(株),"引用,あり\n続き"\r\n002,㈱青空,\r\n003,,空欄\r\n'.encode("cp932"))
    subprocess.run([sys.executable, *entry_point, "--csv", str(source),
                    "--column", "会社名", "--encoding", "cp932"], check=True)
    with (tmp_path / "list_cleaned.csv").open(encoding="utf-8-sig", newline="") as f:
        assert list(csv.reader(f)) == [
            ["ID", "会社名", "備考", "normalized_name", "prefix", "stem", "suffix", "parse_status"],
            ["001", "川崎車両　(株)", "引用,あり\n続き", "川崎車両株式会社", "", "川崎車両", "株式会社", "parsed"],
            ["002", "㈱青空", "", "株式会社青空", "株式会社", "青空", "", "parsed"],
            ["003", "", "空欄", "", "", "", "", "empty"],
        ]


@pytest.mark.parametrize("data", ["ID\n1\n", "会社名,stem\na,b\n", "会社名\na\nb,c\n"])
def test_invalid_csv_preserves_destination(tmp_path, data):
    source, destination = tmp_path / "in.csv", tmp_path / "out.csv"
    source.write_text(data, encoding="utf-8")
    destination.write_bytes(b"previous")
    with pytest.raises(ValueError):
        clean_csv(source, "会社名", destination)
    assert destination.read_bytes() == b"previous"
