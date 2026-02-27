import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any, List

logger = logging.getLogger(__name__)

def normalize_text(text: str) -> str:
    """Normalizes text for case-insensitive comparison."""
    return text.strip().lower() if isinstance(text, str) else ""

def extract_hit(file_path: str, target_rank: int, normalize: bool = False) -> Optional[Dict[str, Any]]:
    """
    Reads a chart JSON file and returns the song at the requested rank.
    Optionally normalizes artist/title.
    """
    file_p = Path(file_path)
    if not file_p.exists():
        logger.warning(f"File not found: {file_path}")
        return None

    try:
        with file_p.open("r", encoding="utf-8") as f:
            content = json.load(f)
            chart_data = content.get("data", [])

            for entry in chart_data:
                if entry.get("this_week") == target_rank:
                    hit = {
                        "title": normalize_text(entry.get("song")) if normalize else entry.get("song"),
                        "artist": normalize_text(entry.get("artist")) if normalize else entry.get("artist"),
                    }
                    if "weeks_on_chart" in entry:
                        hit["weeks"] = entry["weeks_on_chart"]
                    return hit
    except (json.JSONDecodeError, IOError, OSError) as e:
        logger.error(f"Error loading {file_path}: {e}")
    return None

def search_song_in_file(
    file_path: str, target_artist: str, target_song: str
) -> Optional[Dict[str, Any]]:
    # Existing, with logging
    file_p = Path(file_path)
    if not file_p.exists():
        logger.warning(f"File not found: {file_path}")
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
    except (json.JSONDecodeError, IOError, OSError) as e:
        logger.error(f"Error loading {file_path}: {e}")
    return None

def load_chart_entries(file_path: str) -> List[Dict[str, Any]]:
    # Existing, with logging
    file_p = Path(file_path)
    if not file_p.exists():
        logger.warning(f"File not found: {file_path}")
        return []

    try:
        with file_p.open("r", encoding="utf-8") as f:
            content = json.load(f)
            return content.get("data", [])
    except (json.JSONDecodeError, IOError, OSError) as e:
        logger.error(f"Error loading {file_path}: {e}")
        return []