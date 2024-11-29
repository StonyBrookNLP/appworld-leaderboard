import argparse
import json
import os


def read_json(file_path: str) -> list[dict] | dict:
    with open(file_path) as file:
        content = file.read()
    data = json.loads(content)
    return data


def write_json(data: list[dict] | dict, file_path: str) -> None:
    with open(file_path, "w") as file:
        with open(file_path, "w") as file:
            file.write(json.dumps(data, indent=4))


def main():
    parser = argparse.ArgumentParser(description="Remove leaderboard entries.")
    parser.add_argument("ids", nargs="+", type=str, help="Leaderboard entry IDs")
    args = parser.parse_args()

    file_path = os.path.join("experiments", "outputs", "_leaderboard.json")
    old_entries = read_json(file_path)
    new_entries: list[str] = []
    removed_ids: list[str] = []
    existing_ids = {entry["id"] for entry in old_entries}
    for to_remove_id in args.ids:
        if to_remove_id not in existing_ids:
            raise Exception(
                f"The leaderboard entry ID {to_remove_id} is not present in the leaderboard, so cannot remove it."
            )
    for old_entry in old_entries:
        if old_entry["id"] not in args.ids:
            new_entries.append(old_entry)
            removed_ids.append(old_entry["id"])
    if removed_ids:
        write_json(new_entries, file_path)


if __name__ == "__main__":
    main()
