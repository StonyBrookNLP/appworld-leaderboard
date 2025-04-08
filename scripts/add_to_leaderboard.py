import argparse
import os
import subprocess

from scripts.lib import read_json, write_json


MAIN_REPO_REMOTE = "https://github.com/stonybrooknlp/appworld-leaderboard.git"


def print_rule(title: str = "") -> None:
    line = "-" * 40
    if title:
        title_line = f" {title} "
        center_position = (len(line) - len(title_line)) // 2
        line = (
            line[:center_position]
            + title_line
            + line[center_position + len(title_line) :]
        )
    print(line)


def run_command(command: str) -> None:
    print()
    print_rule()
    print(command)
    print_rule()
    subprocess.run(command, check=True, shell=True)


def validate_diff(experiment_prefixes: list[str]) -> None:
    temporary_remote = "temp-remote"
    subprocess.run(
        ["git", "remote", "add", temporary_remote, MAIN_REPO_REMOTE],
        check=True,
        text=True,
    )
    subprocess.run(["git", "fetch", temporary_remote], check=True, text=True)
    output = subprocess.run(
        ["git", "diff", f"{temporary_remote}/main", "--diff-filter=A", "--name-only"],
        capture_output=True,
        text=True,
    )
    added_file_paths = output.stdout.strip().splitlines()
    added_file_paths = [
        file_path
        for file_path in added_file_paths
        if file_path != os.path.join("experiments", "outputs", "_leaderboard.json")
    ]
    output = subprocess.run(
        ["git", "diff", f"{temporary_remote}/main", "--diff-filter=MD", "--name-only"],
        capture_output=True,
        text=True,
    )
    subprocess.run(["git", "remote", "remove", temporary_remote], check=True, text=True)
    changed_or_removed_file_paths = output.stdout.strip().splitlines()
    if changed_or_removed_file_paths:
        raise Exception(
            "The PR does not allow changes or removal to existing files."
            f"\nChanged/removed files: {changed_or_removed_file_paths}"
        )
    expected_added_file_paths = [
        os.path.join(
            "experiments", "outputs", f"{prefix}_{set_name}", "leaderboard.bundle"
        )
        for prefix in experiment_prefixes
        for set_name in ["test_normal", "test_challenge"]
    ]
    added_file_paths = sorted(added_file_paths)
    expected_added_file_paths = sorted(expected_added_file_paths)
    if added_file_paths != expected_added_file_paths:
        raise Exception(
            "The added PR files do not match the expected ones."
            f"\nExpected: {expected_added_file_paths}"
            f"\nActual: {added_file_paths}"
        )


def main():
    parser = argparse.ArgumentParser(description="Add entries to the leaderboard.")
    parser.add_argument(
        "experiment-prefixes", nargs="+", type=str, help="experiment prefixes"
    )
    parser.add_argument(
        "--pr-repo",
        type=str,
        default="",
        help="If this is run from a github action PR workflow, pass this. Otherwise, leave it empty.",
    )
    parser.add_argument(
        "--pr-branch",
        type=str,
        default="",
        help="If this is run from a github action PR workflow, pass this. Otherwise, leave it empty.",
    )
    args = parser.parse_args()
    if bool(args.pr_repo) != bool(args.pr_branch):
        raise Exception(
            "Either both --pr-repo and --pr-branch should be provided, or neither."
        )
    uv_prefix = "uv run " if args.pr_branch else ""
    experiment_prefixes = getattr(args, "experiment-prefixes")
    if args.pr_branch:
        validate_diff(experiment_prefixes)
    leaderboard_file_path = os.path.join("experiments", "outputs", "_leaderboard.json")
    original_leaderboard_data = read_json(leaderboard_file_path)
    pr_repo = args.pr_repo or "stonybrooknlp/appworld-leaderboard"
    for experiment_prefix in experiment_prefixes:
        print_rule(f"\nWorking on experiment prefix: {experiment_prefix}")
        experiment_names = [
            experiment_prefix + "_test_normal",
            experiment_prefix + "_test_challenge",
        ]
        dataset_names = ["test_normal", "test_challenge"]
        if args.pr_branch:
            for experiment_name, dataset_name in zip(experiment_names, dataset_names):
                remote_file_path = (
                    f"experiments/outputs/{experiment_name}/leaderboard.bundle"
                )
                local_file_path = os.sep.join(remote_file_path.split("/"))
                command = f"curl -L -o {local_file_path} https://github.com/{pr_repo}/raw/{args.pr_branch}/{remote_file_path}"
                run_command(command)
                run_command(f"{uv_prefix}appworld unpack {experiment_name}")
                run_command(
                    f"{uv_prefix}appworld evaluate {experiment_name} {dataset_name}"
                )
        run_command(f"{uv_prefix}appworld make {' '.join(experiment_names)} --save")
    added_leaderboard_data = read_json(leaderboard_file_path)[
        len(original_leaderboard_data) :
    ]
    if args.pr_branch:
        os.makedirs(".temp", exist_ok=True)
        added_leaderboard_data_file_path = os.path.join(
            ".temp", "added_leaderboard_data.json"
        )
        write_json(added_leaderboard_data, added_leaderboard_data_file_path)


if __name__ == "__main__":
    main()
