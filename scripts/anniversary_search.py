import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict

import time_engine
import data_handler
import chart_discovery
import chart_utils

logger = logging.getLogger(__name__)

def run_anniversary_search(data_dir: str, input_date: str, rank: int = 1) -> List[Dict]:
    """
    Main anniversary search routine. Returns sorted list of results.
    """
    try:
        patterns, start_date, end_date = time_engine.get_week_patterns(input_date)
    except ValueError as e:
        raise ValueError(f"Invalid input_date: {e}")

    results = []

    logger.info(
        f"Searching anniversaries for week: "
        f"{start_date.strftime('%b %d')} to {end_date.strftime('%b %d, %Y')}"
    )

    chart_infos = chart_discovery.discover_chart_folders(data_dir)
    if not chart_infos:
        logger.warning("No chart folders discovered from metadata files.")
        return results

    for chart_info in chart_infos:
        chart_data_p = Path(chart_info["data_dir"])
        if not chart_data_p.exists():
            logger.warning(f"Chart folder not found: {chart_info['source']} / {chart_info['chart_name']}")
            continue

        matching_files = chart_utils.get_files_for_week(chart_data_p, patterns)
        for json_file in matching_files:
            hit_info = data_handler.extract_hit(str(json_file), rank)
            if hit_info:
                results.append({
                    "full_date": json_file.stem,
                    "source": chart_info["source"],
                    "chart": chart_info["chart_name"],
                    "details": hit_info,
                })

    # Sort oldest first
    return sorted(results, key=lambda x: x["full_date"])

if __name__ == "__main__":
    import argparse
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Anniversary search script")
    parser.add_argument("--data_dir", default=str(Path(__file__).parent.parent / "data"))
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--rank", type=int, default=1)
    args = parser.parse_args()

    anniversary_list = run_anniversary_search(args.data_dir, args.date, args.rank)

    if not anniversary_list:
        print("No historical records found for this week.")
    else:
        print(f"\nFound {len(anniversary_list)} historical hit(s) at position #{args.rank}:\n")
        print("| Date | Source / Chart | Artist - Title (Weeks on Chart) |")
        print("|------|----------------|---------------------------------|")
        for item in anniversary_list:
            date_str = item["full_date"]
            song = item["details"]
            weeks_str = f" ({song['weeks']} weeks on chart)" if "weeks" in song else ""
            print(
                f"| {date_str} | {item['source']} / {item['chart']} | "
                f"{song['artist']} - {song['title']}{weeks_str} |"
            )