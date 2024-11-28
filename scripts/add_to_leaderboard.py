import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser(description="Add entries to the leaderboard.")
    parser.add_argument("experiment_prefixes", nargs="+", type=str, help="experiment prefixes")
    args = parser.parse_args()
    for experiment_prefix in args.experiment_prefixes:
        print(f"\nWorking on experiment prefix: {experiment_prefix}")
        experiment_names = [experiment_prefix + "_test_normal", experiment_prefix + "_test_challenge"]
        for experiment_name in experiment_names:
            subprocess.run(f"appworld evaluate {experiment_name}_test_normal test_normal", check=True, shell=True)
            subprocess.run(f"appworld evaluate {experiment_name}_test_challenge test_challenge", check=True, shell=True)
            subprocess.run(f"appworld make {experiment_name}_test_normal {experiment_name}_challenge --save", check=True, shell=True)

if __name__ == "__main__":
    main()
