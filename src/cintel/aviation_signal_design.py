"""
aviation_signal_design.py - Enhanced aviation signal analysis.

Author: Denise Case, Kevin Hennelly
Date: 2026-03

Aviation On-Time Data

- Data is taken from airline on-time performance records.
- The data is structured and static for this example.
- Each row represents one flight observation.
- The CSV file includes columns like OP_UNIQUE_CARRIER, FL_DATE, DEP_DELAY, CANCELLED.

Purpose

- Read aviation data from a CSV file.
- Design useful signals from the raw measurements.
- Save the resulting signals as a new CSV artifact.
- Log the pipeline process to assist with debugging and transparency.

Questions to Consider

- What should we measure to understand airline performance?
- Which signals are more informative than the raw input values?
- How can derived signals help us detect operational issues?

Paths (relative to repo root)

    INPUT FILE: data/airline_ontime_data_jan_2025.csv
    OUTPUT FILE: artifacts/aviation_signals_jan_2025.csv

Terminal command to run this file from the root project folder

    uv run python -m cintel.aviation_signal_design

OBS:
  This merges the aviation analysis with the structured pipeline from signal design.
  Use as much of this code as you can when creating your own pipeline script,
  and change the logic to create signals that make sense for your project.
"""

# === DECLARE IMPORTS (packages we will use in this project) ===

# First from the Python standard library (no installation needed)
import logging
from pathlib import Path
from typing import Final

import polars as pl
from datafun_toolkit.logger import get_logger, log_header, log_path

# === CONFIGURE LOGGER ONCE PER MODULE (FILE) ===

LOG: logging.Logger = get_logger("P3", level="DEBUG")

# === DECLARE GLOBAL CONSTANTS FOR FOLDER PATHS (directories) ===

ROOT_DIR: Final[Path] = Path.cwd()
DATA_DIR: Final[Path] = ROOT_DIR / "data"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"

# === DECLARE GLOBAL CONSTANTS FOR FILE PATHS ===

DATA_FILE: Final[Path] = DATA_DIR / "airline_ontime_data_jan_2025.csv"
OUTPUT_FILE: Final[Path] = ARTIFACTS_DIR / "aviation_signals_jan_2025.csv"


# === DEFINE THE MAIN FUNCTION ===


def main() -> None:
    """Run the pipeline.

    log_header() logs a standard run header.
    log_path() logs repo-relative paths (privacy-safe).
    """
    log_header(LOG, "CINTEL")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    # Log the constants to help with debugging and transparency.
    log_path(LOG, "ROOT_DIR", ROOT_DIR)
    log_path(LOG, "DATA_FILE", DATA_FILE)
    log_path(LOG, "OUTPUT_FILE", OUTPUT_FILE)

    # Call the mkdir() method to ensure it exists
    # The parents=True argument allows it to create any necessary parent directories.
    # The exist_ok=True argument prevents an error if the directory already exists.
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    log_path(LOG, "ARTIFACTS_DIR", ARTIFACTS_DIR)

    # ----------------------------------------------------
    # STEP 1: READ CSV DATA FILE INTO A POLARS DATAFRAME (TABLE)
    # ----------------------------------------------------
    # Polars is great for tabular data.
    # We will use the polars package to
    # read CSV (comma-separated values) files
    # into a two-dimensional table called a DataFrame.

    # Call the Polars library read_csv() method.
    # Pass in (provide) the DATA_FILE path of the CSV file.
    # Name the result "df_raw" as in the original.
    df_raw: pl.DataFrame = pl.read_csv(DATA_FILE)

    # Visually inspect the file in the data/ folder.
    # The DataFrame height attribute returns the number of rows.
    LOG.info(f"Loaded {df_raw.height} flight records")

    # ----------------------------------------------------
    # STEP 2: DESIGN SIGNALS FROM RAW METRICS
    # ----------------------------------------------------
    # Analysts often create derived values that are more useful than
    # the original raw columns alone.
    LOG.info("Designing signals from the raw metrics...")

    # ----------------------------------------------------
    # STEP 2.1: GROUP BY CARRIER AND AGGREGATE
    # ----------------------------------------------------
    # Group by airline carrier to get total flights and delayed flights.
    # A flight is considered delayed if DEP_DELAY >= 15 or CANCELLED == 1.
    df_grouped: pl.DataFrame = df_raw.group_by("OP_UNIQUE_CARRIER").agg(
        [
            pl.count("FL_DATE").alias("flights"),  # Total flights
            ((pl.col("DEP_DELAY") >= 15) | (pl.col("CANCELLED") == 1))
            .sum()
            .alias("delayed"),
        ]
    )

    LOG.info(f"Grouped into {df_grouped.height} carriers")

    # ----------------------------------------------------
    # STEP 2.2: DEFINE A CONDITION WE CAN REUSE
    # ----------------------------------------------------
    # Only calculate per-flight signals when flights > 0.
    # Use the Polars col() function to refer to a column by name.
    # This creates a boolean expression:
    # True when flights > 0, False otherwise.
    is_flights_positive: pl.Expr = pl.col("flights") > 0

    # ----------------------------------------------------
    # STEP 2.3: DEFINE THE DELAY RATE CALCULATION
    # ----------------------------------------------------
    # This creates an expression for:
    #     delayed / flights
    # It is only a calculation recipe at this point.
    calculated_delay_rate: pl.Expr = pl.col("delayed") / pl.col("flights")

    # ----------------------------------------------------
    # STEP 2.4: DEFINE THE DELAY RATE SIGNAL RECIPE
    # ----------------------------------------------------
    # A signal recipe tells Polars how to build a new column.
    # If flights > 0, use delayed / flights.
    # Otherwise, use 0.0.
    # Name the new column "delay_rate".
    delay_rate_signal_recipe: pl.Expr = (
        pl.when(is_flights_positive)
        .then(calculated_delay_rate)
        .otherwise(0.0)
        .alias("delay_rate")
    )

    # ----------------------------------------------------
    # STEP 2.5: DEFINE HIGH DELAY ALERT SIGNAL RECIPE
    # ----------------------------------------------------
    # Flag carriers where delay_rate exceeds threshold.
    # This is useful for alerting or filtering anomalies.
    # Use the calculated delay_rate for consistency.
    DELAY_THRESHOLD: Final[float] = 0.20  # 20%

    high_delay_alert_recipe: pl.Expr = (
        pl.when(is_flights_positive & (calculated_delay_rate > DELAY_THRESHOLD))
        .then(pl.lit(True))
        .otherwise(pl.lit(False))
        .alias("high_delay_alert")
    )

    # ----------------------------------------------------
    # STEP 2.5: APPLY THE SIGNAL RECIPES TO THE DATAFRAME
    # ----------------------------------------------------
    # Now we use with_columns() to apply all the recipes
    # and create a new DataFrame with the added signal columns.
    df_with_signals: pl.DataFrame = df_grouped.with_columns(
        [
            delay_rate_signal_recipe,
            high_delay_alert_recipe,
        ]
    )

    LOG.info("Created signal columns: delay_rate, high_delay_alert")

    # ----------------------------------------------------
    # STEP 3: SELECT THE COLUMNS WE WANT TO SAVE
    # ----------------------------------------------------
    # Keep the original columns and the new signal columns together.
    # And use the select() method to choose which columns
    # to include in the final output.
    signals_df = df_with_signals.select(
        [
            "OP_UNIQUE_CARRIER",
            "flights",
            "delayed",
            "delay_rate",
            "high_delay_alert",
        ]
    )

    LOG.info(f"Enhanced signals table has {signals_df.height} rows")

    # ----------------------------------------------------
    # STEP 4: PRINT RESULTS TO TERMINAL
    # ----------------------------------------------------
    # Print All Carriers
    print("\n--- Aviation Signal Analysis: All Carriers ---")
    with pl.Config(tbl_rows=20):
        print(signals_df.sort("flights", descending=True))

    # Print Problematic (Above Threshold)
    print("\n--- High Risk Carriers (Exceeded 20% Threshold) ---")
    print(signals_df.filter(pl.col("high_delay_alert")))

    # Print Safe (At or Below Threshold)
    print("\n--- Top Performing Carriers (At or Below 20% Threshold) ---")
    print(signals_df.filter(pl.col("high_delay_alert").not_()))

    # ----------------------------------------------------
    # STEP 5: SAVE THE SIGNALS TABLE AS AN ARTIFACT
    # ----------------------------------------------------
    # We call generated files artifacts.
    # Use the write_csv() method to save the signals_df DataFrame
    # as a CSV file at the OUTPUT_FILE path.
    signals_df.write_csv(OUTPUT_FILE)
    LOG.info(f"Wrote signals file: {OUTPUT_FILE}")

    print(f"\n--- Artifact successfully created at: {OUTPUT_FILE} ---")

    LOG.info("========================")
    LOG.info("Pipeline executed successfully!")
    LOG.info("========================")
    LOG.info("END main()")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
