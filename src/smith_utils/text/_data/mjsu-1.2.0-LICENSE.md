# MJSU 1.2.0 replacement data

`mjsu-1.2.0.tsv` is adapted from two works by the Information-technology
Promotion Agency, Japan (IPA, 独立行政法人情報処理推進機構), published by the
Character Information Technology Promotion Council (文字情報技術促進協議会).
The derived table is distributed under the
[Creative Commons Attribution-ShareAlike 2.1 Japan license](https://creativecommons.org/licenses/by-sa/2.1/jp/).
The Python code is distributed under the repository's MIT license.

| Upstream work | Release | SHA-256 |
| --- | --- | --- |
| [MJ Single-Choice Reduction Table (MJ縮退マップ 一意な変換表)](https://moji.or.jp/wp-content/mojikiban/lab/xb657/MJSU.1.2.0.json) | 1.2.0, 2018-01-26 | `beff70c8d07cd5701af5a64c88acc862982ba4521c6384e8a1694326704022c7` |
| [MJ Character Information List (MJ文字情報一覧表)](https://moji.or.jp/wp-content/uploads/2024/01/mji.00602.xlsx) | 006.02, January 2024 | `f79075bf006b66c5e57a6df60503c5a01679cabbcea2f124eb3758593cf6fd3f` |

The generator joins the two works by MJ glyph ID. It takes the implemented
UCS, Moji_Joho IVS, and standardized variation sequences as inputs and the
MJSU UCS value as the output. It excludes JIS X 0213 `1-01-18` (no target),
omits identities, and emits 21,623 rows sorted by input code points. Each
row contains one or two space-separated hexadecimal input code points,
a tab, and one hexadecimal output code point.

From a repository checkout, regenerate the table with the pinned downloads.

```sh
python tools/generate_kanji_variants.py MJSU.1.2.0.json mji.00602.xlsx
```

[Reduction table release and licensing](https://moji.or.jp/mojikiban/map/) ·
[Character list release and licensing](https://moji.or.jp/mojikiban/mjlist/)
