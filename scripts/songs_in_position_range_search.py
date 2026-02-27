import logging
from pathlib import Path
from typing import List, Dict, Tuple

import chart_discovery
import data_handler
import time_engine
import chart_utils

logger = logging.getLogger(__name__)

def get_songs_in_position_range(
    data_dir: str,
    chart_info: Dict,
    start_date: str,
    end_date: str,
    min_pos: int = 1,
    max_pos: int = 10,
    include_peak_date: bool = False,
) -> List[Dict]:
    """
    Returns unique songs in position range. Optionally tracks earliest peak date.
    """
    if min_pos > max_pos or min_pos < 1:
        raise ValueError("Invalid position range.")

    results: Dict[Tuple[str, str], Dict] = {}
    chart_p = Path(chart_info["data_dir"])
    if not chart_p.exists():
        logger.warning(f"Chart folder not found: {chart_info['source']} / {chart_info['chart_name']}")
        return []

    date_files = chart_utils.get_files_for_date_range(chart_p, start_date, end_date)

    for filename in date_files:
        file_path = str(chart_p / filename)
        date_str = time_engine.extract_date_from_filename(filename.name)
        if not date_str:
            continue
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
                new_entry = {
                    "artist": artist,
                    "song": song,
                    "peak": pos,
                    "weeks_at_peak": 1,
                }
                if include_peak_date:
                    new_entry["peak_date"] = date_str
                results[key] = new_entry
            else:
                current = results[key]
                if pos < current["peak"]:
                    current["peak"] = pos
                    current["weeks_at_peak"] = 1
                    if include_peak_date:
                        current["peak_date"] = date_str
                elif pos == current["peak"]:
                    current["weeks_at_peak"] += 1

    result_list = list(results.values())
    if include_peak_date:
        result_list.sort(key=lambda x: (x["peak_date"], x["peak"], -x["weeks_at_peak"]))
    else:
        result_list.sort(key=lambda x: (x["peak"], -x["weeks_at_peak"], x["artist"]))
    return result_list

if __name__ == "__main__":
    import argparse
    import sys
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Songs in position range search")
    parser.add_argument("--data_dir", default=str(Path(__file__).parent.parent / "data"))
    parser.add_argument("--chart_num", type=int, help="Chart number from list")
    parser.add_argument("--start_date", required=True)
    parser.add_argument("--end_date", required=True)
    parser.add_argument("--min_pos", type=int, default=1)
    parser.add_argument("--max_pos", type=int, default=10)
    parser.add_argument("--include_peak_date", action="store_true")
    args = parser.parse_args()

    chart_infos = chart_discovery.discover_chart_folders(args.data_dir)
    if not chart_infos:
        print("No charts found in data folder.")
        sys.exit(1)

    print("Available charts:")
    for i, c in enumerate(chart_infos, 1):
        print(f"{i:2d}. {c['source']} / {c['chart_name']}")

    if args.chart_num is None:
        try:
            choice = int(input("\nSelect chart number: ")) - 1
        except (ValueError, EOFError):
            print("Invalid selection.")
            sys.exit(1)
    else:
        choice = args.chart_num - 1

    try:
        selected_chart = chart_infos[choice]
    except IndexError:
        print("Invalid selection.")
        sys.exit(1)

    print(f"\nSearching {selected_chart['source']} / {selected_chart['chart_name']} "
          f"({args.min_pos}-{args.max_pos}) from {args.start_date} to {args.end_date}...\n")

    songs = get_songs_in_position_range(
        args.data_dir, selected_chart, args.start_date, args.end_date,
        args.min_pos, args.max_pos, args.include_peak_date
    )

    if not songs:
        print("No songs found with the specified criteria.")
    else:
        print(f"Found {len(songs)} unique song(s)\n")
        if args.include_peak_date:
            print("| Artist | Song | Peak Date | Peak | Weeks at Peak |")
            print("|--------|------|-----------|------|---------------|")
            for s in songs:
                print(
                    f"| {s['artist']} | {s['song']} | "
                    f"{s['peak_date']} | #{s['peak']} | {s['weeks_at_peak']} weeks |"
                )
        else:
            print("| Artist | Song | Peak | Weeks at Peak |")
            print("|--------|------|------|---------------|")
            for s in songs:
                print(
                    f"| {s['artist']} | {s['song']} | "
                    f"#{s['peak']} | {s['weeks_at_peak']} weeks |"
                )