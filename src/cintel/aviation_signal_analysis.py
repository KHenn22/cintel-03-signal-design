import polars as pl

# 1. Load the data from your new location
path = r"data\airline_ontime_data_jan_2025.csv"
df_raw = pl.read_csv(path)

# 2. Group by Airline to get counts
# Any flight delayed >= 15 mins OR cancelled is 'delayed'
df = df_raw.group_by("OP_UNIQUE_CARRIER").agg(
    [
        pl.count("FL_DATE").alias("flights"),  # Total flights
        ((pl.col("DEP_DELAY") >= 15) | (pl.col("CANCELLED") == 1))
        .sum()
        .alias("delayed"),
    ]
)

# 3. Apply Signal Recipe
DELAY_THRESHOLD = 0.20  # Flag carriers with > 20% as problematic flights

high_delay_alert_recipe = (
    pl.when(pl.col("delayed") / pl.col("flights") > DELAY_THRESHOLD)
    .then(pl.lit(True))
    .otherwise(pl.lit(False))
    .alias("high_delay_alert")
)

# 4. Final DataFrame
df_with_signals = df.with_columns([high_delay_alert_recipe])

# Print All Carriers
print("\n--- Aviation Signal Analysis: All Carriers ---")
with pl.Config(tbl_rows=20):
    print(df_with_signals.sort("flights", descending=True))

# Print Problematic (Above Threshold)
print("\n--- High Risk Carriers (Exceeded 20% Threshold) ---")
print(df_with_signals.filter(pl.col("high_delay_alert")))

# Print Safe Last (At or Below Threshold)
print("\n--- Top Performing Carriers (At or Below 20% Threshold) ---")
print(df_with_signals.filter(pl.col("high_delay_alert").not_()))

# 5. Define the output path for your artifacts folder
output_path = r"artifacts/aviation_signals_jan_2025.csv"

# 6. Save the full 'All Carriers' table to CSV
df_with_signals.write_csv(output_path)

print(f"\n--- Artifact successfully created at: {output_path} ---")
