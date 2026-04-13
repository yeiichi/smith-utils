def parse_numeric_value(val: str | float | None, sep: str = ",", decimal: str = ".", relaxed: bool = False) -> float | str:
    if val is None:
        return 0.0

    s = str(val).strip()
    is_negative = False

    if s.startswith("-"):
        is_negative = True
        s = s[1:].strip()
    elif s.startswith("(") and s.endswith(")"):
        is_negative = True
        s = s[1:-1].strip()

    # Split by decimal to validate groups
    parts = s.split(decimal)
    if len(parts) > 2:
        if relaxed:
            return val
        raise ValueError(f"Invalid numeric value: '{val}'")

    # Validate integer part groups if 'sep' is used
    int_part = parts[0]
    if sep in int_part:
        groups = int_part.split(sep)
        # All groups except the first must be exactly 3 digits
        # This is a common rule for thousand separators
        if any(len(g) != 3 for g in groups[1:]):
            if relaxed:
                return val
            raise ValueError(f"Invalid numeric value: '{val}'")

    s_cleaned = s.replace(sep, "")
    if decimal != ".":
        s_cleaned = s_cleaned.replace(decimal, ".")

    try:
        # Check if separator appears after decimal
        if sep in s and decimal in s and s.rfind(sep) > s.find(decimal):
            raise ValueError

        num = float(s_cleaned)
        # Check if it was purely digits + decimal
        if not s_cleaned.replace(".", "", 1).isdigit():
            raise ValueError

        return -num if is_negative else num
    except ValueError:
        if relaxed:
            return val
        raise ValueError(f"Invalid numeric value: '{val}'")


def parse_currency_value(val: str | float | None, sep: str = ",", decimal: str = ".", relaxed: bool = False) -> float | str:
    return parse_numeric_value(val, sep=sep, decimal=decimal, relaxed=relaxed)