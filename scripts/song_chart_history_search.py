import logging
from pathlib import Path
from typing import List, Dict

import chart_discovery
import data_handler
import chart_utils

logger = logging.getLogger(__name__)

def get_song_chart_history(data_dir: str, artist: str, song: str) -> List[Dict]:
    """
    Returns chart history for a specific song across all discovered charts.
    """
    if not artist.strip() or not song.strip():
        raise ValueError("Both artist and song title are required.")

    results = []
    chart_infos = chart_discovery.discover_chart_folders(data_dir)

    for chart_info in chart_infos:
        chart_p = Path(chart_info["data_dir"])
        if not chart_p.exists():
            logger.warning(f"Chart folder not found: {chart_info['source']} / {chart_info['chart_name']}")
            continue

        history = []
        json_files = chart_utils.get_all_files(chart_p)

        for json_file in json_files:
            entry = data_handler.search_song_in_file(str(json_file), artist, song)
            if entry:
                history.append({
                    "date": json_file.stem,
                    "position": entry.get("this_week"),
                    "weeks_on_chart": entry.get("weeks_on_chart", 0),
                })

        if history:
            peak = min(h["position"] for h in history)
            total_weeks = max(h["weeks_on_chart"] for h in history)

            results.append({
                "source": chart_info["source"],
                "chart": chart_info["chart_name"],
                "history": history,
                "peak": peak,
                "total_weeks": total_weeks,
            })

    return results

if __name__ == "__main__":
    import argparse
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Song chart history search")
    parser.add_argument("--data_dir", default=str(Path(__file__).parent.parent / "data"))
    parser.add_argument("--artist", default="Olivia Newton-John")
    parser.add_argument("--song", default="Physical")
    args = parser.parse_args()

    history_results = get_song_chart_history(args.data_dir, args.artist, args.song)

    if not history_results:
        print("The song was not found in any available charts.")
    else:
        for res in history_results:
            print(f"## {res['source']} / {res['chart']}\n")
            print("### Chart History\n")
            print("| Date | Position |")
            print("|------|----------|")
            for h in res["history"]:
                print(f"| {h['date']} | {h['position']} |")

            print(f"\nPeak position: #{res['peak']}")
            print(f"Number of weeks on chart: {res['total_weeks']}")
            print("\n---\n")