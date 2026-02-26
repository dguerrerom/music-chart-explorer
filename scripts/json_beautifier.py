<DOCUMENT filename="json_beautifier.py">
import json
from pathlib import Path


def beautify_json_folder(input_folder: str, output_folder: str, indent_size: int = 4) -> None:
    """
    Reads minified JSON files from input_folder and writes them with proper
    indentation to output_folder.
    """
    input_p = Path(input_folder)
    output_p = Path(output_folder)

    if not output_p.exists():
        output_p.mkdir(parents=True, exist_ok=True)
        print(f"Created destination directory: {output_p}")

    for json_file in input_p.glob("*.json"):
        try:
            with json_file.open("r", encoding="utf-8") as f:
                data = json.load(f)

            output_path = output_p / json_file.name
            with output_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=indent_size, ensure_ascii=False)

            print(f"Successfully beautified: {json_file.name}")

        except json.JSONDecodeError:
            print(f"Error: {json_file.name} is not a valid JSON file. Skipping.")
        except Exception as e:
            print(f"An unexpected error occurred with {json_file.name}: {e}")


if __name__ == "__main__":
    # Update these paths for your environment
    SOURCE_DIRECTORY = "../data/billboard/billboard-hot-100"
    DESTINATION_DIRECTORY = "../data/billboard/billboard-hot"

    print("Starting JSON beautification process...")
    beautify_json_folder(SOURCE_DIRECTORY, DESTINATION_DIRECTORY)
    print("Process finished.")