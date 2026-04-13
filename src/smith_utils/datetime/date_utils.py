# src/calendar_smith/utils.py
import datetime
import re

DATE_FORMAT_BASIC = "%Y%m%d"
DATE_FORMAT_EXTENDED = "%Y-%m-%d"


def format_ordinal(n: int) -> str:
    """
    Converts an integer to its ordinal representation as a string.

    The function takes an integer input and returns the ordinal form of the 
    number as a string with its appropriate suffix. For example, 1 becomes 
    "1st", 2 becomes "2nd", and so on. The suffix rules account for the 
    exceptional cases such as numbers ending in 11, 12, or 13.

    Args:
        n (int): The integer to be converted to its ordinal equivalent.

    Returns:
        str: The ordinal representation of the input number.
    """
    if 11 <= (abs(n) % 100) <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(abs(n) % 10, 'th')
    return f"{n}{suffix}"


def parse_strict_date(date_str: str) -> datetime.date:
    """
    Parses a given date string into a `datetime.date` object.

    This function attempts to parse the input date string in various formats
    while adhering to strict expectations for valid date representations. It 
    supports both basic (YYYYMMDD) and extended (YYYY-MM-DD) formats and rejects 
    ambiguous or malformed inputs. The function raises an error if the provided 
    string does not conform to the acceptable formats.

    Note:
        The returned `datetime.date` object is naive and does not retain any time zone 
        information. If the input string contains a time component or time zone 
        identifier (e.g., after a 'T' or space), it is simply discarded without any 
        time zone conversion. This means a UTC timestamp might represent a different 
        calendar date in a local time zone.

    Parameters:
        date_str (str): The date string to be parsed. It is expected to be in either
            basic (YYYYMMDD) or extended (YYYY-MM-DD) format.

    Returns:
        datetime.date: A `date` object representing the parsed date.

    Raises:
        ValueError: If the input string contains an ambiguous or invalid date.
    """
    date_part = date_str.split('T')[0].split(' ')[0]
    digits_only = re.sub(r'[^0-9]', '', date_part)

    if len(digits_only) == 8 and date_part.isdigit():
        return datetime.datetime.strptime(digits_only, DATE_FORMAT_BASIC).date()

    if '-' in date_part:
        try:
            return datetime.datetime.strptime(date_part, DATE_FORMAT_EXTENDED).date()
        except ValueError:
            pass

    if len(digits_only) in (6, 7) or (re.match(r'^\d{1,2}-\d{1,2}$', date_part)):
        raise ValueError(
            f"Ambiguous date '{date_str}' rejected. "
            "Please use 8-digit YYYYMMDD or delimiters (YYYY-MM-DD)."
        )
    raise ValueError(f"Could not parse '{date_str}'. Expected YYYY-MM-DD or YYYYMMDD.")


def ensure_date(date_input: str | datetime.date | None) -> datetime.date:
    """
    Converts various date input formats into a `datetime.date` object.

    This function accepts a string, a `datetime.date` object, or a `None` 
    value to produce a `datetime.date` object. If the input is `None`, the 
    current date is returned. String inputs are first stripped of leading 
    and trailing whitespace, and the function attempts to parse the string 
    as an ISO 8601 formatted date. If the ISO 8601 parsing fails, the input 
    is passed to a fallback parsing function for stricter date parsing.

    Raises:
        ValueError: If the input string cannot be parsed into a valid date 
        via both ISO 8601 and the fallback parsing mechanism.

    Parameters:
        date_input (str | datetime.date | None): The input to be converted 
        to a `datetime.date` object. This can be a string representing a 
        date, a `datetime.date` object itself, or `None`.

    Returns:
        datetime.date: A valid `datetime.date` object corresponding to the 
        provided input, or the current date if the input is `None`.
    """
    if not date_input:
        return datetime.date.today()
    if isinstance(date_input, datetime.date):
        return date_input

    clean_input = str(date_input).strip()
    try:
        return datetime.date.fromisoformat(clean_input)
    except ValueError:
        return parse_strict_date(clean_input)