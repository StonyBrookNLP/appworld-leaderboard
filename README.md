# AppWorld Leaderboard

This is the leaderboard repository of the benchmark proposed in [AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents](https://appworld.dev/) (ACL 2024).

The project's main repository is [here](https://github.com/stonybrooknlp/appworld), and leaderboard UI is [here](https://appworld.dev/leaderboard). This repository stores bundled (encrypted) experiment outputs from participanting models (including our baselines) and the raw [leaderboard data JSON](/experiments/outputs/_leaderboard.json) which is dynamically rendered in the UI. You can use this repository to:

1. Download and locally view experiment outputs from other participanting methods.
2. Submit your own agent's experiment outputs to be included on the leaderboard via a PR.

For both cases, you first need to

1. Install `appworld`: `pip install appworld && appworld install`.
2. Install [Git LFS](https://git-lfs.com/) and clone the `appworld-leaderboard` repository.

## Submit Your Agent's Outputs

**First**, pack your agent's `test_normal` and `test_challenge` experiment outputs:

<details>
<summary>::Click:: Experiment outputs refresher</summary>

---

Your experiment outputs are located in `./experiments/outputs/{experiment_name}` relative to the `APPWORLD_ROOT`, which as we discussed earlier, defaults to `.`, but can be configured by passing `APPWORLD_ROOT` environment variable or `--root` in CLI.

---

</details>

For the leaderboard, experiment names must be alphanumeric with optional hyphens and underscores, and they must end with the dataset name, i.e., `_test_normal` or `_test_challenge`, e.g., `react_gpt4o_test_normal`. You should have two experiment outputs, one for each dataset. The prefix portion of their names must be the same, e.g., `react_gpt4o_test_normal` and `react_gpt4o_test_challenge`. Rename the directory accordingly if necessary.

Now, `pack` the two experiments, individually, with the following commands, and same metadata.

```bash
appworld pack {test_normal_experiment_name|test_challenge_experiment_name} \
    # The method name used in the experiment:
    --method_name METHOD_NAME \
    # A brief additional note about the method:
    --method_tooltip METHOD_TOOLTIP \
    # The LLM name used in the experiment:
    --llm_name LLM_NAME \
    # A brief additional note about the LLM
    --llm_tooltip \
    # URL to find more information about this submission
    -url URL
# Example:
# appworld pack react_gpt4o_test_normal \
#   --method_name react
#   --method_tooltip 'Reason + Act'
#   --llm_name 'GPT4-o'
#   --url 'https://appworld.dev/'
```

The pack command compresses and encrypts the experiment outputs in `leaderboard.bundle` files within your experiment output directories. E.g., `./experiments/outputs/react_gpt4o_test_normal/leaderboard.bundle`.

> [!Caution]
> Do NOT put your experiment outptus in an unencrypted format publicly accessible on the internet.

**Next**, Copy the two bundle files at the following locations relative to `appworld-leaderboard` repo's root directory.

```bash
./experiments/outputs/{test_normal_experiment_name}/leaderboard.bundle
./experiments/outputs/{test_challenge_experiment_name}/leaderboard.bundle
```

Then create a PR with these two files and post a comment as follows. Here, `EXPERIMENT_NAME_PREFIX` refers to the experiment name without the suffix of `_test_normal` and `_test_challenge` for the two splits.

```bash
# Change python and appworld version as desired. NOTE: Make sure there is not white space in the comment before the command starts.
/add-to-leaderboard --python {PYTHON_VERSION} --appworld {APPWORLD_VERSION} {EXPERIMENT_NAME_PREFIX}
```

This will start an automatic GitHub workflow which you can follow along in the GitHb Actions tab. If it's successful, it'll post a comment with your leaderboard entry in the PR, and update the leaderboard file, which you will be able to see in the PR diff as well. Verify the details in the comment. If you want to update the submission, just push updated bundle files and post the command comment again. Once you're happy with the result, assign the PR to me ([Harsh](https://github.com/harshTrivedi/)). I will take a look ASAP to ensure that no new changes are made after the last evaluation, and merge it.

Note that you can also submit multiple agents submissions in the same PR. In this case add more bundle files to the PR and add more space-delimited experiment name prefixes to the PR command comment.

> [!IMPORTANT]
> **Reminder:** We track experiment outputs in encrypted `.bundle` files to reduce the risk of it becoming part of the training corpora of LLMs. So please do NOT post it here (or anywhere else publicly on the interent) in unencrypted or uncompressed format. See [license](https://github.com/stonybrooknlp/appworld/tree/main?tab=readme-ov-file#lock_with_ink_pen-license).


## View Existing Experiment Outputs

`CD` into the root of this repository. The experiment outputs are available in this format:

```bash
experiments/outputs/{experiment_name}/leaderboard.bundle
```

To unpack the bundle, run the following based on the experiment name you want to open.

```bash
appworld unpack {experiment_name}
```

The bundle will be unpacked in the directory:

```bash
experiments/outputs/{experiment_name}/
```
