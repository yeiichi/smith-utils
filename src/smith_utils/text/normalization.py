import unicodedata


def normalize_text(text, ignore_case=True, remove_all_whitespace=False, nfkc=True):
    """
    Normalizes the input text by applying transformations such as Unicode normalization,
    case folding, and whitespace handling.

    Parameters:
        text (str or None): The input text to normalize_text. If None, an empty string is returned.
        ignore_case (bool, optional): Whether to convert the text to lowercase. Defaults to True.
        remove_all_whitespace (bool, optional): Whether to remove all internal whitespace and trim outer
            whitespace. Defaults to False.
        nfkc (bool, optional): Whether to apply Unicode normalization using NFKC form. Defaults to
            True.

    Returns:
        str: The normalized text.
    """
    if text is None:
        return ""

    # Cast to string to handle numeric cells safely
    text = str(text)

    # 1. Unicode Compatibility (Handles full-width/ligatures)
    if nfkc:
        text = unicodedata.normalize('NFKC', text)

    # 3. Whitespace handling
    # Always trim outer whitespace, and optionally remove all internal whitespace.
    text = text.strip()
    if remove_all_whitespace:
        text = "".join(text.split())
    else:
        # Note: join(split()) reduces multiple spaces to one.
        text = " ".join(text.split())

    # 2. Case Folding
    if ignore_case:
        text = text.lower()

    return text