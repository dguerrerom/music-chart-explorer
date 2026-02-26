import json
from pathlib import Path
from typing import List, Dict


def discover_chart_folders(data_dir: str) -> List[Dict[str, str]]:
    """
    Scans the data directory for all *-metadata.json and *-manifest.json files
    and returns information about every chart defined inside them.
    """
    chart_infos: List[Dict[str, str]] = []
    data_path = Path(data_dir)

    if not data_path.exists():
        print(f"Warning: Data directory '{data_dir}' does not exist.")
        return chart_infos

    for meta_file in data_path.iterdir():
        if not meta_file.is_file():
            continue
        if not meta_file.name.endswith(("-metadata.json", "-manifest.json")):
            continue

        try:
            with meta_file.open("r", encoding="utf-8") as f:
                metadata = json.load(f)

            source_name = metadata.get("name", "Unknown Source")
            source_folder = metadata.get("folder", "")

            if not source_folder:
                name = meta_file.name
                for suffix in ["-metadata.json", "-manifest.json"]:
                    if name.endswith(suffix):
                        source_folder = name[:-len(suffix)]
                        break
                else:
                    source_folder = meta_file.stem

            for chart in metadata.get("charts", []):
                if isinstance(chart, dict) and "folder" in chart:
                    chart_folder = chart["folder"]
                    chart_data_path = str(data_path / source_folder / chart_folder)

                    chart_infos.append({
                        "source": source_name,
                        "chart_name": chart.get("name", chart_folder),
                        "data_dir": chart_data_path,
                    })

        except (json.JSONDecodeError, IOError, KeyError, OSError) as e:
            print(f"Warning: Could not parse metadata file '{meta_file.name}': {e}")
            continue

    return chart_infos