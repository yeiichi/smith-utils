# tests/test_metrics.py

from src.smith_utils.text.metrics import StringDistance, Relation, Result


def test_equals_ignore_case():
    assert StringDistance.equals_ignore_case("Test", "test")
    assert StringDistance.equals_ignore_case("TEST", "test")
    assert not StringDistance.equals_ignore_case("Test", "Another")


def test_trim():
    assert StringDistance.trim("  hello  ") == "hello"
    assert StringDistance.trim("\t\ttest\t") == "test"
    assert StringDistance.trim("no_spaces") == "no_spaces"


def test_strip_all():
    assert StringDistance.strip_all("  he  llo  ") == "hello"
    assert StringDistance.strip_all("\t\tt e\ts\tt\t") == "test"
    assert StringDistance.strip_all("no   spaces\t") == "nospaces"


def test_classify_exact_match():
    result = StringDistance.classify("hello", "hello")
    assert result == Relation.EXACT_MATCH


def test_classify_case_insensitive_match():
    result = StringDistance.classify("HELLO", "hello")
    assert result == Relation.CASE_INSENSITIVE_MATCH


def test_classify_whitespace_trimmed_match():
    result = StringDistance.classify("  hello  ", "hello")
    assert result == Relation.WHITESPACE_TRIMMED_MATCH


def test_classify_normalized_space_match():
    result = StringDistance.classify("he llo", "hel lo")
    assert result == Relation.NORMALIZED_SPACE_MATCH


def test_classify_no_structural_match():
    result = StringDistance.classify("hello", "world")
    assert result == Relation.NO_STRUCTURAL_MATCH


def test_analyze_similarity_metrics_case_insensitive():
    result = StringDistance.analyze("HELLO", "hello", ignore_case=True)
    assert isinstance(result, Result)
    assert result.classification == Relation.CASE_INSENSITIVE_MATCH
    assert result.damerau_levenshtein_distance == 0
    assert result.jaro_winkler_score > 0.9
    assert result.similarity_percentage == 100.0


def test_calculate_damerau_levenshtein():
    distance = StringDistance.calculate_damerau_levenshtein("kitten", "sitting")
    assert distance == 3


def test_calculate_jaro_winkler():
    score = StringDistance.calculate_jaro_winkler("MARTHA", "MARHTA")
    assert score > 0.9


def test_analyze_empty_strings():
    result = StringDistance.analyze("", "", ignore_case=False)
    assert isinstance(result, Result)
    assert result.classification == Relation.EXACT_MATCH
    assert result.damerau_levenshtein_distance == 0
    assert result.jaro_winkler_score == 1.0
    assert result.similarity_percentage == 100.0
