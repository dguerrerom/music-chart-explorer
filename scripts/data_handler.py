import json
from pathlib import Path
from typing import Dict, Optional, Any, List


def extract_hit(file_path: str, target_rank: int) -> Optional[Dict[str, Any]]:
    """
    Reads a chart JSON file (mhollingshead format) and returns the song at the
    requested rank.

    The returned dict always contains 'title' and 'artist'.
    The key 'weeks' is included (with its exact JSON value) ONLY if
    'weeks_on_chart' exists as a key in the chart entry.

    Returns None if the file cannot be read or the rank is missing.
    """
    file_p = Path(file_path)
    if not file_p.exists():
        return None

    try:
        with file_p.open("r", encoding="utf-8") as f:
            content = json.load(f)
            chart_data = content.get("data", [])

            for entry in chart_data:
                if entry.get("this_week") == target_rank:
                    hit = {
                        "title": entry.get("song"),
                        "artist": entry.get("artist"),
                    }
                    if "weeks_on_chart" in entry:
                        hit["weeks"] = entry["weeks_on_chart"]
                    return hit
    except (json.JSONDecodeError, IOError, OSError):
        pass  # Silently skip corrupted files

    return None


def normalize_text(text: str) -> str:
    """Normalizes text for case-insensitive comparison."""
    return text.strip().lower() if isinstance(text, str) else ""


def search_song_in_file(
    file_path: str, target_artist: str, target_song: str
) -> Optional[Dict[str, Any]]:
    """
    Returns the full chart entry if artist + song match (case-insensitive).
    """
    file_p = Path(file_path)
    if not file_p.exists():
        return None

    try:
        with file_p.open("r", encoding="utf-8") as f:
            content = json.load(f)
            chart_data = content.get("data", [])

            target_a = normalize_text(target_artist)
            target_s = normalize_text(target_song)

            for entry in chart_data:
                if (normalize_text(entry.get("artist")) == target_a and
                        normalize_text(entry.get("song")) == target_s):
                    return entry
    except (json.JSONDecodeError, IOError, OSError):
        pass

    return None


def load_chart_entries(file_path: str) -> List[Dict[str, Any]]:
    """Loads the full 'data' list from a chart JSON file."""
    file_p = Path(file_path)
    if not file_p.exists():
        return []

    try:
        with file_p.open("r", encoding="utf-8") as f:
            content = json.load(f)
            return content.get("data", [])
    except (json.JSONDecodeError, IOError, OSError):
        return []