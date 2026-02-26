import re
from datetime import datetime, timedelta, date
from typing import Tuple, List, Optional


def get_week_patterns(reference_date_str: str) -> Tuple[List[str], date, date]:
    """
    Calculates the '-MM-DD' suffixes for the Sunday–Saturday week that contains
    the provided reference date.

    Returns:
        patterns: list of '-MM-DD' strings (7 entries)
        sunday_start: date object of the Sunday that starts the week
        saturday_end: date object of the Saturday that ends the week
    """
    try:
        date_obj = datetime.strptime(reference_date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Date format must be YYYY-MM-DD")

    # Week starts on Sunday
    offset = (date_obj.weekday() + 1) % 7
    sunday_start = date_obj - timedelta(days=offset)
    saturday_end = sunday_start + timedelta(days=6)

    patterns = [
        (sunday_start + timedelta(days=i)).strftime("-%m-%d")
        for i in range(7)
    ]
    return patterns, sunday_start, saturday_end


def extract_date_from_filename(filename: str) -> Optional[str]:
    """
    Extracts the first YYYY-MM-DD date found in the filename string.
    Works with or without prefixes (e.g. 'billboard-hot-100-2025-01-04.json').
    """
    match = re.search(r"(\d{4}-\d{2}-\d{2})", filename)
    return match.group(1) if match else None


def is_date_in_range(filename: str, start_date_str: str, end_date_str: str) -> bool:
    """
    Checks if the date extracted from the filename falls within the given range (inclusive).
    """
    date_str = extract_date_from_filename(filename)
    if not date_str:
        return False

    try:
        file_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        start = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        return start <= file_date <= end
    except ValueError:
        return False