import io

from src.smith_utils.text.newlines import normalize_newlines_stream


def test_no_newlines():
    src = io.BytesIO(b"Hello, world!")
    dst = io.BytesIO()
    result = normalize_newlines_stream(src, dst)
    assert result == "NONE"
    assert dst.getvalue() == b"Hello, world!"


def test_lf_newlines():
    src = io.BytesIO(b"Line1\nLine2\nLine3\n")
    dst = io.BytesIO()
    result = normalize_newlines_stream(src, dst)
    assert result == "LF"
    assert dst.getvalue() == b"Line1\nLine2\nLine3\n"


def test_crlf_newlines():
    src = io.BytesIO(b"Line1\r\nLine2\r\nLine3\r\n")
    dst = io.BytesIO()
    result = normalize_newlines_stream(src, dst)
    assert result == "CRLF"
    assert dst.getvalue() == b"Line1\nLine2\nLine3\n"


def test_cr_newlines():
    src = io.BytesIO(b"Line1\rLine2\rLine3\r")
    dst = io.BytesIO()
    result = normalize_newlines_stream(src, dst)
    assert result == "CR"
    assert dst.getvalue() == b"Line1\nLine2\nLine3\n"


def test_mixed_newlines():
    src = io.BytesIO(b"Line1\nLine2\r\nLine3\r")
    dst = io.BytesIO()
    result = normalize_newlines_stream(src, dst)
    assert result == "MIXED"
    assert dst.getvalue() == b"Line1\nLine2\nLine3\n"


def test_partial_cr_followed_by_lf():
    src = io.BytesIO(b"Line1\r\nLine3")
    dst = io.BytesIO()
    result = normalize_newlines_stream(src, dst, chunk_size=6)
    assert result == "CRLF"
    assert dst.getvalue() == b"Line1\nLine3"
