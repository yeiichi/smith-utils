"""Command line interface for smith-utils."""

from __future__ import annotations

import argparse
import sys

from . import (
    classify_file,
    get_file_digest,
    get_text_digest,
    make_unicode_char_name_records,
    normalize_kanji_variants,
    normalize_text,
    random_string,
    sample_positive_gaussian,
)
from .com_name_cleaner.cli import configure_parser as configure_com_name_cleaner_parser


def main(argv: list[str] | None = None) -> int:
    parser = _make_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


def _make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="smith")
    subparsers = parser.add_subparsers(dest="command", required=True)

    random_parser = subparsers.add_parser("random-string", help="generate a random string")
    random_parser.add_argument("length", type=int)
    random_parser.add_argument(
        "--category",
        choices=("ascii", "kanji", "mix"),
        default="ascii",
        help="character category to use",
    )
    random_parser.add_argument(
        "--ascii-ratio",
        type=float,
        default=0.5,
        help="ASCII probability for --category mix",
    )
    random_parser.set_defaults(func=_random_string_command)

    digest_parser = subparsers.add_parser("digest", help="calculate a SHA-256 digest")
    digest_input = digest_parser.add_mutually_exclusive_group(required=True)
    digest_input.add_argument("--text", help="text to digest")
    digest_input.add_argument("path", nargs="?", help="file path to digest")
    digest_parser.set_defaults(func=_digest_command)

    normalize_parser = subparsers.add_parser("normalize-text", help="normalize text")
    normalize_parser.add_argument("text", nargs="?", help="text to normalize; reads stdin when omitted")
    normalize_parser.add_argument("--keep-case", action="store_true", help="preserve text case")
    normalize_parser.add_argument(
        "--remove-all-whitespace",
        action="store_true",
        help="remove all whitespace instead of collapsing it",
    )
    normalize_parser.add_argument("--no-nfkc", action="store_true", help="skip NFKC normalization")
    normalize_parser.set_defaults(func=_normalize_text_command)

    kanji_parser = subparsers.add_parser(
        "normalize-kanji-variants",
        help="normalize Japanese kanji variants using MJSU 1.2.0",
    )
    kanji_parser.add_argument("text", nargs="?", help="text to normalize; reads stdin when omitted")
    kanji_parser.set_defaults(func=_normalize_kanji_variants_command)

    com_name_parser = subparsers.add_parser(
        "com-name-cleaner",
        help="normalize Japanese organization names",
    )
    configure_com_name_cleaner_parser(com_name_parser)

    unicode_parser = subparsers.add_parser("unicode-names", help="show Unicode character names")
    unicode_parser.add_argument("text", help="text to inspect")
    unicode_parser.set_defaults(func=_unicode_names_command)

    classify_parser = subparsers.add_parser("classify-file", help="classify a file")
    classify_parser.add_argument("path", help="file path to classify")
    classify_parser.set_defaults(func=_classify_file_command)

    gaussian_parser = subparsers.add_parser(
        "positive-gaussian-samples",
        help="sample positive Gaussian values",
    )
    gaussian_parser.add_argument("trial_number", type=int, help="number of samples to generate")
    gaussian_parser.add_argument("--mean", type=float, required=True, help="Gaussian mean")
    gaussian_parser.add_argument(
        "--approx-upper-bound",
        type=float,
        required=True,
        help="approximate upper bound used as mean + 3 sigma and as a truncation bound",
    )
    gaussian_parser.set_defaults(func=_positive_gaussian_samples_command)

    return parser


def _random_string_command(args: argparse.Namespace) -> None:
    print(
        random_string(
            args.length,
            char_category=args.category,
            ascii_ratio=args.ascii_ratio,
        )
    )


def _digest_command(args: argparse.Namespace) -> None:
    if args.text is not None:
        print(get_text_digest(args.text))
        return

    print(get_file_digest(args.path))


def _normalize_text_command(args: argparse.Namespace) -> None:
    text = sys.stdin.read() if args.text is None else args.text
    print(
        normalize_text(
            text,
            ignore_case=not args.keep_case,
            remove_all_whitespace=args.remove_all_whitespace,
            nfkc=not args.no_nfkc,
        )
    )


def _normalize_kanji_variants_command(args: argparse.Namespace) -> None:
    if args.text is None:
        sys.stdout.write(normalize_kanji_variants(sys.stdin.read()))
    else:
        print(normalize_kanji_variants(args.text))


def _unicode_names_command(args: argparse.Namespace) -> None:
    for record in make_unicode_char_name_records(args.text):
        print(f"{record.index}\t{record.codepoint}\t{record.char}\t{record.name}")


def _classify_file_command(args: argparse.Namespace) -> None:
    result = classify_file(args.path)
    fields = (
        ("path", str(result.path)),
        ("extension", result.extension),
        ("file_class", result.file_class),
        ("categories", ",".join(result.categories)),
        ("extension_mime_type", result.extension_mime_type),
        ("magic_type", result.magic_type),
        ("magic_mime_type", result.magic_mime_type),
        ("file_description", result.file_description),
        ("file_mime_type", result.file_mime_type),
    )
    for key, value in fields:
        print(f"{key}={'' if value is None else value}")


def _positive_gaussian_samples_command(args: argparse.Namespace) -> None:
    for sample in sample_positive_gaussian(
        mean=args.mean,
        approx_upper_bound=args.approx_upper_bound,
        trial_number=args.trial_number,
    ):
        print(sample)


if __name__ == "__main__":
    raise SystemExit(main())
