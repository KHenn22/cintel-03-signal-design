# cintel-03-signal-design

[![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](#)
[![MIT](https://img.shields.io/badge/license-see%20LICENSE-yellow.svg)](./LICENSE)

> Professional Python project for continuous intelligence.

Continuous intelligence systems monitor data streams, detect change, and respond in real time.
This course builds those capabilities through working projects.

In the age of generative AI, durable skills are grounded in real work:
setting up a professional environment,
reading and running code,
understanding the logic,
and pushing work to a shared repository.
Each project follows the structure of professional Python projects.
We learn by doing.

## This Project

This project introduces **signal design**.

The goal is to copy this repository,
set up your environment,
run the example analysis,
and explore how useful signals can be derived from raw system metrics.

You will run the example pipeline, read the code,
and make small modifications to understand how
signals are created from raw measurements.

## Data

The example pipeline reads system metrics from: `data/system_metrics_case.csv`.

Each row represents a system observation with raw measurements
such as requests, errors, and total latency.
The pipeline derives signals such as **error rate** and
**average latency** from these raw values.

## Working Files

You'll work with just these areas:

- **data/** - it starts with the data
- **docs/** - tell the story
- **src/cintel/** - where the magic happens
- **pyproject.toml** - update authorship & links
- **zensical.toml** - update authorship & links

## Instructions

Follow the [step-by-step workflow guide](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/) to complete:

1. Phase 1. **Start & Run**
2. Phase 2. **Change Authorship**
3. Phase 3. **Read & Understand**
4. Phase 4. **Modify**
5. Phase 5. **Apply**

## Challenges

Challenges are expected.
Sometimes instructions may not quite match your operating system.
When issues occur, share screenshots, error messages, and details about what you tried.
Working through issues is part of implementing professional projects.

## Success

After completing Phase 1. **Start & Run**, you'll have your own GitHub project,
running on your machine, and running the example will print out:

```shell
========================
Pipeline executed successfully!
========================
```

And a new file named `project.log` will appear in the project folder.

## Command Reference

The commands below are used in the workflow guide above.
They are provided here for convenience.

Follow the guide for the **full instructions**.

<details>
<summary>Show command reference</summary>

### In a machine terminal (open in your `Repos` folder)

After you get a copy of this repo in your own GitHub account,
open a machine terminal in your `Repos` folder:

```shell
git clone https://github.com/KHenn22/cintel-03-signal-design

cd cintel-03-signal-design
code .
```

### In a VS Code terminal

```shell
uv self update
uv python pin 3.14
uv sync --extra dev --extra docs --upgrade

uvx pre-commit install
git add -A
uvx pre-commit run --all-files

uv run python -m cintel.signal_design_case

uv run ruff format .
uv run ruff check . --fix
uv run zensical build

git add -A
git commit -m "update"
git push -u origin main
```

</details>

## Notes

- Use the **UP ARROW** and **DOWN ARROW** in the terminal to scroll through past commands.
- Use `CTRL+f` to find (and replace) text within a file.

## Modifications

- Added new derived signal column `high_error_alert` to the signal design pipeline
- Uses a boolean flag (`True`) to identify any observation where the error rate (errors/requests) exceeds 5%.  Otherwise it is `False`.
- This modification makes it easier to quickly identify problematic observations by flagging those above a certain threshold (5%).

- Code to run
```
uv run python -m cintel.signal_design_hennelly
```

-artifacts/signals_hennelly.csv now includes a `high_error_alert` column

-observed that none of the present data was flagged as a `high_error_alert`.  All were false.

## Skills Applied to a New Problem

### What the Project Does

1. **Aviation Signal Analysis**: Analyzes airline on-time performance data for January 2025 to identify carriers with high delay rates (>= 15 minutes on over 20% of flights)

### How to Run It

`python src/cintel/aviation_signal_design.py`
note: `aviation_signal_analysis.py` will also execute but was the original experimentation python script for `airline_ontime_data_jan_2025.csv` and does not include the full signal design. Proper script to scale and run for analysis is `aviation_signal_design.py`

Successful runs will create artifacts in the `artifacts/` folder and log to `project.log`.

### Documentation and Notebooks

- **Documentation**: Visit the built site at `site/index.html` or build with `uv run zensical build`

- **Project Docs**: See `docs/` folder for detailed instructions, glossary, and project files.

- **Notebooks**: No Jupyter notebooks are included, but the scripts can be adapted for interactive analysis.

### Showcase

#### Key Visualization

Run the aviation analysis to see carrier performance rankings in the terminal output.

#### Results Table

Aviation Signal Analysis Results:

| Carrier        | Flights | Delayed | Delay Rate | High Delay Alert |
|----------------|---------|---------|------------|------------------|
| WN (Southwest) | 105307  | 20891   | 19.8%      | false            |
| UA (United)    | 62007   | 11299   | 18.2%      | false            |
| AS (Alaska)    | 18163   | 3236    | 17.8%      | false            |
| YX (Republic)  | 27833   | 4392    | 15.8%      | false            |
| HA (Hawaiian)  | 6690    | 874     | 13.1%      | false            |
| MQ (Envoy)     | 21890   | 4314    | 19.7%      | false            |
| F9 (Frontier)  | 15526   | 3903    | 25.1%      | true             |
| OO (SkyWest)   | 65036   | 13253   | 20.4%      | true             |
| DL (Delta)     | 76306   | 16661   | 21.8%      | true             |
| B6 (JetBlue)   | 17918   | 4264    | 23.8%      | true             |
| OH (PSA)       | 21094   | 6338    | 30.0%      | true             |
| NK (Spirit)    | 17544   | 3656    | 20.8%      | true             |
| G4 (Allegiant) | 9345    | 2294    | 24.5%      | true             |
| AA (American)  | 75088   | 16369   | 21.8%      | true             |

#### Summary of Insights

- **Aviation**: 8 out of 14 major carriers exceed the 20% delay threshold, highlighting areas for operational improvement. Southwest (WN) leads with the most flights and a manageable delay rate.

This project showcases how derived signals enable proactive monitoring and data-driven decision making.
