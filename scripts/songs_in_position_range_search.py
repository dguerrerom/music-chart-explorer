from pathlib import Path

import chart_discovery
import data_handler
import time_engine


def get_songs_in_position_range(
    data_dir: str,
    chart_info: dict,
    start_date: str,
    end_date: str,
    min_pos: int = 1,
    max_pos: int = 10,
) -> list[dict]:
    """
    Returns unique songs that appeared between min_pos and max_pos in the
    given chart and date range. Tracks best peak and weeks spent at that peak.
    """
    results: dict[tuple[str, str], dict] = {}
    chart_p = Path(chart_info["data_dir"])
    if not chart_p.exists():
        return []

    date_files = [
        f.name
        for f in chart_p.glob("*.json")
        if time_engine.is_date_in_range(f.name, start_date, end_date)
    ]
    date_files.sort()

    for filename in date_files:
        file_path = str(chart_p / filename)
        entries = data_handler.load_chart_entries(file_path)

        for entry in entries:
            pos = entry.get("this_week")
            if pos is None or not (min_pos <= pos <= max_pos):
                continue

            artist = entry.get("artist", "").strip()
            song = entry.get("song", "").strip()
            if not artist or not song:
                continue

            key = (
                data_handler.normalize_text(artist),
                data_handler.normalize_text(song),
            )

            if key not in results:
                results[key] = {
                    "artist": artist,
                    "song": song,
                    "peak": pos,
                    "weeks_at_peak": 1,
                }
            else:
                current = results[key]
                if pos < current["peak"]:
                    current["peak"] = pos
                    current["weeks_at_peak"] = 1
                elif pos == current["peak"]:
                    current["weeks_at_peak"] += 1

    result_list = list(results.values())
    result_list.sort(key=lambda x: (x["peak"], -x["weeks_at_peak"], x["artist"]))
    return result_list


if __name__ == "__main__":
    SCRIPT_DIR = Path(__file__).parent
    DATA_DIR = str(SCRIPT_DIR.parent / "data")

    print("\n" + "=" * 80)
    print("  Searching Songs in Position Range")
    print("=" * 80 + "\n")

    chart_infos = chart_discovery.discover_chart_folders(DATA_DIR)
    if not chart_infos:
        print("No charts found in data folder.")
        exit()

    print("Available charts:")
    for i, c in enumerate(chart_infos, 1):
        print(f"{i:2d}. {c['source']} / {c['chart_name']}")

    try:
        choice = int(input("\nSelect chart number: ")) - 1
        selected_chart = chart_infos[choice]
    except (ValueError, IndexError):
        print("Invalid selection.")
        exit()

    start_date = input("Start date (YYYY-MM-DD): ").strip()
    end_date = input("End date   (YYYY-MM-DD): ").strip()

    try:
        min_pos = int(input("Minimum position (default 1): ") or 1)
        max_pos = int(input("Maximum position (default 10): ") or 10)
    except ValueError:
        print("Invalid position values.")
        exit()

    print(f"\nSearching {selected_chart['source']} / {selected_chart['chart_name']} "
          f"({min_pos}-{max_pos}) from {start_date} to {end_date}...\n")

    songs = get_songs_in_position_range(
        DATA_DIR, selected_chart, start_date, end_date, min_pos, max_pos
    )

    if not songs:
        print("No songs found with the specified criteria.")
    else:
        print(f"Found {len(songs)} unique song(s)\n")
        print(f"{'Artist':<35} | {'Song':<45} | {'Peak':>6} | {'Weeks at Peak':>14}")
        print("-" * 115)
        for s in songs:
            print(
                f"{s['artist']:<35} | {s['song']:<45} | "
                f"#{s['peak']:<4} | {s['weeks_at_peak']:>14} weeks"
            )