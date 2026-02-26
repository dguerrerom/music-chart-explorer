import json
from pathlib import Path


def adjorno_to_mhollingshead_chart_format(input_folder: str, output_folder: str) -> None:
    """
    Converts chart JSON files from the adjorno structure to the mhollingshead
    structure (date + data list with this_week, last_week, peak_position, weeks_on_chart).
    """
    input_p = Path(input_folder)
    output_p = Path(output_folder)

    if not output_p.exists():
        output_p.mkdir(parents=True, exist_ok=True)
        print(f"Created destination directory: {output_p}")

    for json_file in input_p.glob("*.json"):
        try:
            with json_file.open("r", encoding="utf-8") as f:
                source_data = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {json_file.name}. Skipping.")
            continue

        standardized = {
            "date": source_data.get("chart_date", ""),
            "data": []
        }

        for track in source_data.get("tracks", []):
            pos = track.get("position", {})

            last_week_val = pos.get("Last Week")
            if isinstance(last_week_val, str) and last_week_val.strip() in {"-", ""}:
                last_week_val = None
            else:
                try:
                    last_week_val = int(last_week_val)
                except (TypeError, ValueError):
                    last_week_val = None

            new_entry = {
                "song": track.get("title"),
                "artist": track.get("artist"),
                "this_week": track.get("rank"),
                "last_week": last_week_val,
            }

            if "Peak Position" in pos:
                new_entry["peak_position"] = pos["Peak Position"]
            if "Wks on Chart" in pos:
                new_entry["weeks_on_chart"] = pos["Wks on Chart"]

            standardized["data"].append(new_entry)

        output_path = output_p / json_file.name
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(standardized, f, indent=4, ensure_ascii=False)

        print(f"Successfully standardized: {json_file.name}")


if __name__ == "__main__":
    # Update these paths for your environment
    INPUT_DIR = "../data/billboard/billboard-latin-songs"
    OUTPUT_DIR = "../data/billboard/billboard-latin"

    print("Starting conversion process...")
    adjorno_to_mhollingshead_chart_format(INPUT_DIR, OUTPUT_DIR)
    print("Process completed.")