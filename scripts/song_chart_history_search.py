from pathlib import Path

import chart_discovery
import data_handler


def get_song_chart_history(data_dir: str, artist: str, song: str) -> list[dict]:
    """
    Returns chart history for a specific song across all discovered charts.
    Each result includes the full history, peak position, and total weeks.
    """
    results = []
    chart_infos = chart_discovery.discover_chart_folders(data_dir)

    for chart_info in chart_infos:
        chart_p = Path(chart_info["data_dir"])
        if not chart_p.exists():
            continue

        history = []
        json_files = sorted(chart_p.glob("*.json"), key=lambda p: p.stem)

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
    SCRIPT_DIR = Path(__file__).parent
    DATA_DIR = str(SCRIPT_DIR.parent / "data")

    artist = "Olivia Newton-John"
    song = "Physical"

    if not artist or not song:
        print("Error: Both artist and song title are required.")
    else:
        print(f'\nSearching for: "{song}" by {artist} ...\n')

        history_results = get_song_chart_history(DATA_DIR, artist, song)

        if not history_results:
            print("The song was not found in any available charts.")
        else:
            for res in history_results:
                print(f"=== {res['source']} / {res['chart']} ===")
                print("Chart History")
                print(f"{'Date':<12} {'Position':>8}")
                for h in res["history"]:
                    print(f"{h['date']:<12} {h['position']:>8}")

                print(f"\nPeak position: #{res['peak']}")
                print(f"Number of weeks on chart: {res['total_weeks']}")
                print("-" * 60)