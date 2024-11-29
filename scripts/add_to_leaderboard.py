import argparse
import subprocess

from appworld.common.utils import print_rule


def run_command(command: str) -> None:
    print_rule()
    print(command)
    print_rule()
    subprocess.run(command, check=True, shell=True)


def main():
    parser = argparse.ArgumentParser(description="Add entries to the leaderboard.")
    parser.add_argument(
        "experiment-prefixes", nargs="+", type=str, help="experiment prefixes"
    )
    parser.add_argument(
        "--unpack-first",
        action="store_true",
        help="unpack experiment bundles before evaluation.",
    )
    parser.add_argument(
        "--use-uv", action="store_true", help="prefix the python commands with uv run."
    )
    args = parser.parse_args()
    uv_prefix = "uv run " if args.use_uv else ""
    for experiment_prefix in args.experiment_prefixes:
        print_rule(f"\nWorking on experiment prefix: {experiment_prefix}")
        experiment_names = [
            experiment_prefix + "_test_normal",
            experiment_prefix + "_test_challenge",
        ]
        for experiment_name in experiment_names:
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
