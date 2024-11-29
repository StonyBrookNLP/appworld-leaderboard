import argparse
import os
import subprocess

from rich import print as rprint
from rich.rule import Rule


def print_rule(title: str = "") -> None:
    rprint(Rule(title=title))


def run_command(command: str) -> None:
    print()
    print_rule()
    print(command)
    print_rule()
    subprocess.run(command, check=True, shell=True)


def validate_diff(experiment_prefixes: list[str]) -> None:
    output = subprocess.run(["git", "diff", "origin/main", "--diff-filter=A", "--name-only"], capture_output=True, text=True)
    added_file_paths = output.stdout.strip().splitlines()
    output = subprocess.run(["git", "diff", "origin/main", "--diff-filter=MD", "--name-only"], capture_output=True, text=True)
    changed_or_removed_file_paths = output.stdout.strip().splitlines()
    if changed_or_removed_file_paths:
        raise Exception("The PR does not allow changes or removal to existing files.")
    expected_added_file_paths = [
        os.path.join("experiments", "outputs", f"{prefix}_{set_name}", "leaderboard.json")
        for prefix in experiment_prefixes for set_name in ["test_normal", "test_challenge"]
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
        "--validate-diff",
        action="store_true",
        help="validate the diff to ensure only expected new files are added.",
    )
    parser.add_argument(
        "--unpack-first",
        action="store_true",
        help="unpack experiment bundles before evaluation.",
    )
    parser.add_argument("--pr-branch", type=str)
    parser.add_argument(
        "--use-uv", action="store_true", help="prefix the python commands with uv run."
    )
    args = parser.parse_args()
    uv_prefix = "uv run " if args.use_uv else ""

    validate_diff(args.experiment_prefixes)

    for experiment_prefix in args.experiment_prefixes:
        print_rule(f"\nWorking on experiment prefix: {experiment_prefix}")
        experiment_names = [experiment_prefix + "_test_normal", experiment_prefix + "_test_challenge"]
        for experiment_name in experiment_names:
            # maybe download leaderboard bundle
            if args.pr_branch:
                remote_file_path = f"experiments/outputs/{experiment_name}/leaderboard.bundle"
                local_file_path = os.sep.join(remote_file_path.split("/"))
                command = f"curl -L -o {local_file_path} https://github.com/stonybrooknlp/appworld-leaderboard/raw/{args.pr_branch}/{remote_file_path}"
                run_command(command)
            # test_normal:
            run_command(
                f"{uv_prefix}appworld unpack {experiment_name}_test_normal",
                check=True,
                shell=True,
            )
            run_command(
                f"{uv_prefix}appworld evaluate {experiment_name}_test_normal test_normal",
                check=True,
                shell=True,
            )
            # test_challenge:
            run_command(
                f"{uv_prefix}appworld unpack {experiment_name}_test_challenge",
                check=True,
                shell=True,
            )
            run_command(
                f"{uv_prefix}appworld evaluate {experiment_name}_test_challenge test_challenge",
                check=True,
                shell=True,
            )
            run_command(
                f"{uv_prefix}appworld make {experiment_name}_test_normal {experiment_name}_challenge --save",
                check=True,
                shell=True,
            )


if __name__ == "__main__":
    main()
