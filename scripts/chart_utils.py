import logging
from pathlib import Path
from typing import List

import time_engine

logger = logging.getLogger(__name__)

def get_files_for_week(chart_dir: Path, patterns: List[str]) -> List[Path]:
    """
    Returns sorted list of JSON files matching any of the -MM-DD patterns.
    """
    files = [f for f in chart_dir.glob("*.json") if any(f.stem.endswith(p) for p in patterns)]
    files.sort(key=lambda f: f.stem)
    return files

def get_files_for_date_range(chart_dir: Path, start_date: str, end_date: str) -> List[Path]:
    """
    Returns sorted list of JSON files within the date range (inclusive).
    """
    try:
        # Validate dates
        time_engine.get_week_patterns(start_date)
        time_engine.get_week_patterns(end_date)
    except ValueError as e:
        raise ValueError(f"Invalid date range: {e}")

    files = [
        f for f in chart_dir.glob("*.json")
        if time_engine.is_date_in_range(f.name, start_date, end_date)
    ]
    files.sort(key=lambda f: time_engine.extract_date_from_filename(f.name) or '0000-00-00')
    return files

def get_all_files(chart_dir: Path) -> List[Path]:
    """
    Returns all sorted JSON files in the chart directory.
    """
    files = list(chart_dir.glob("*.json"))
    files.sort(key=lambda f: f.stem)
    return files