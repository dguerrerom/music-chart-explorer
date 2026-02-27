import os
from datetime import datetime
from pathlib import Path

import time_engine
import data_handler
import chart_discovery


def run_anniversary_search(data_dir: str, input_date: str, rank: int = 1) -> list[dict]:
    """
    Main anniversary search routine.

    1. Determines the Sunday–Saturday week containing input_date.
    2. Discovers all chart folders from *-metadata.json files.
    3. Finds every JSON file whose name ends with one of the week’s -MM-DD patterns.
    4. Extracts the song at the requested rank from each matching file.
    5. Returns a list of results sorted by date (oldest first).
    """
    patterns, start_date, end_date = time_engine.get_week_patterns(input_date)

    results = []

    print(
        f"--- Searching anniversaries for week: "
        f"{start_date.strftime('%b %d')} to {end_date.strftime('%b %d, %Y')} ---"
    )

    chart_infos = chart_discovery.discover_chart_folders(data_dir)
    if not chart_infos:
        print("No chart folders discovered from metadata files.")
        return results

    for chart_info in chart_infos:
        chart_data_p = Path(chart_info["data_dir"])
        if not chart_data_p.exists():
            print(f"Warning: Chart folder not found -> {chart_info['source']} / "
                  f"{chart_info['chart_name']} ({chart_data_p})")
            continue

        for json_file in chart_data_p.glob("*.json"):
            name_no_ext = json_file.stem
            if any(name_no_ext.endswith(p) for p in patterns):
                hit_info = data_handler.extract_hit(str(json_file), rank)
                if hit_info:
                    results.append({
                        "full_date": name_no_ext,
                        "source": chart_info["source"],
                        "chart": chart_info["chart_name"],
                        "details": hit_info,
                    })

    # Oldest anniversary first (ascending chronological order)
    return sorted(results, key=lambda x: x["full_date"], reverse=False)


if __name__ == "__main__":
    SCRIPT_DIR = Path(__file__).parent
    DATA_DIR = str(SCRIPT_DIR.parent / "data")

    SEARCH_DATE = datetime.now().strftime("%Y-%m-%d")
    TARGET_POSITION = 1

    anniversary_list = run_anniversary_search(DATA_DIR, SEARCH_DATE, TARGET_POSITION)

    if not anniversary_list:
        print("No historical records found for this week.")
    else:
        print(f"\nFound {len(anniversary_list)} historical hit(s) at position #{TARGET_POSITION}:\n")
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