import argparse
import os


from scripts.lib import read_json, write_json


def main():
    parser = argparse.ArgumentParser(description="Remove leaderboard entries.")
    parser.add_argument("ids", nargs="+", type=str, help="Leaderboard entry IDs")
    parser.add_argument(
        "--save-removed",
        action="store_true",
        help="Save the removed leaderboard data to a file",
    )
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
    removed_leaderboard_data: list[str] = []
    for old_entry in old_entries:
        if old_entry["id"] not in args.ids:
            new_entries.append(old_entry)
            removed_ids.append(old_entry["id"])
        else:
            removed_leaderboard_data.append(old_entry)
    if removed_ids:
        write_json(new_entries, file_path)
    if args.save_removed:
        os.makedirs(".temp", exist_ok=True)
        removed_leaderboard_data_file_path = os.path.join(
            ".temp", "removed_leaderboard_data.json"
        )
        write_json(removed_leaderboard_data, removed_leaderboard_data_file_path)


if __name__ == "__main__":
    main()
