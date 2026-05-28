from pathlib import Path
import tempfile
from typing import BinaryIO, Literal

NewlineType = Literal["LF", "CRLF", "CR", "MIXED", "NONE"]


def normalize_newlines_stream(
        src: BinaryIO,
        dst: BinaryIO,
        chunk_size: int = 1024 * 1024,
) -> NewlineType:
    """
    Normalize newlines in a stream, replacing CR and CRLF with LF, and writing the
    result to the destination stream.

    This function processes a binary stream to unify newline characters into a
    single format (LF). It reads the source stream in chunks, processes each chunk
    to replace CR and CRLF with LF, and writes the normalized output to the
    destination stream. Additionally, it returns the newline type present in the
    original data: "LF", "CRLF", "CR", or "MIXED". If no newlines are present, it
    returns "NONE".

    Parameters:
        src (BinaryIO): The source stream to read binary data from.
        dst (BinaryIO): The destination stream to write the normalized binary data to.
        chunk_size (int): The size of chunks to read from the source stream. The default
                          is 1024 * 1024 bytes (1 MB).

    Returns:
        NewlineType: A string representing the type of newline characters found in
                     the source stream, which can be "LF", "CRLF", "CR", "MIXED",
                     or "NONE".
    """
    pending_cr = False

    lf_count = 0
    crlf_count = 0
    cr_count = 0

    while True:
        chunk = src.read(chunk_size)
        if not chunk:
            break

        out = bytearray()
        i = 0

        if pending_cr:
            if chunk.startswith(b"\n"):
                out.append(0x0A)
                crlf_count += 1
                i = 1
            else:
                out.append(0x0A)
                cr_count += 1
            pending_cr = False

        while i < len(chunk):
            b = chunk[i]

            if b == 0x0D:  # CR
                if i + 1 < len(chunk):
                    if chunk[i + 1] == 0x0A:  # CRLF
                        out.append(0x0A)
                        crlf_count += 1
                        i += 2
                    else:
                        out.append(0x0A)
                        cr_count += 1
                        i += 1
                else:
                    pending_cr = True
                    i += 1

            elif b == 0x0A:  # LF
                out.append(0x0A)
                lf_count += 1
                i += 1

            else:
                out.append(b)
                i += 1

        dst.write(out)

    if pending_cr:
        dst.write(b"\n")
        cr_count += 1

    kinds = sum(bool(x) for x in (lf_count, crlf_count, cr_count))

    if kinds == 0:
        return "NONE"
    if kinds > 1:
        return "MIXED"
    if crlf_count:
        return "CRLF"
    if lf_count:
        return "LF"
    return "CR"


def normalize_file_to_lf(
        input_path: Path,
        output_path: Path,
        *,
        chunk_size: int = 1024 * 1024,
) -> dict:
    """
    Normalize line endings to LF in a streaming fashion.

    Returns:
        dict with:
            - newline_type: str  (LF, CRLF, CR, MIXED, NONE)
            - bytes_in: int
            - bytes_out: int
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    bytes_in = input_path.stat().st_size

    # Ensure output directory exists when writing to a different location.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    same_file = False
    try:
        same_file = input_path.resolve() == output_path.resolve()
    except FileNotFoundError:
        # If either path can't be resolved (e.g., output doesn't exist yet), treat as different.
        same_file = False

    if same_file:
        # Avoid clobbering the source while reading. Write to a temp file in the same
        # directory and atomically replace the original.
        with tempfile.NamedTemporaryFile(
                mode="wb",
                dir=str(output_path.parent),
                prefix=f".{output_path.name}.",
                suffix=".tmp",
                delete=False,
        ) as tmp:
            tmp_path = Path(tmp.name)
            with input_path.open("rb") as src:
                newline_type = normalize_newlines_stream(src, tmp, chunk_size=chunk_size)
                bytes_out = tmp.tell()
        tmp_path.replace(output_path)
    else:
        with input_path.open("rb") as src, output_path.open("wb") as dst:
            newline_type = normalize_newlines_stream(src, dst, chunk_size=chunk_size)
            bytes_out = dst.tell()

    return {"newline_type": newline_type, "bytes_in": bytes_in, "bytes_out": bytes_out}
