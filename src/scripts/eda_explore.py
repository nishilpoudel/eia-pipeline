#!/usr/bin/env python3
"""
One-time EDA on ercot_demand.csv.
Prints summary stats to terminal, saves plots to ~/eia-pipeline/eda_output/.
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # headless — no display server needed
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / "data/raw/ercot_demand.csv"
OUTPUT_DIR = BASE_DIR / "eda_output"


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(DATA_PATH, parse_dates=["period"])

    # ── 1. Basic stats ──────────────────────────────────────
    print("=" * 60)
    print("ERCOT DEMAND — EDA SUMMARY")
    print("=" * 60)
    print(f"\nRows:           {len(df):,}")
    print(f"Date range:     {df['period'].min()} → {df['period'].max()}")
    print(f"Null periods:   {df['period'].isna().sum()}")
    print(f"Null values:    {df['value'].isna().sum()}")
    print(f"Duplicate ts:   {df['period'].duplicated().sum()}")

    print(f"\nDemand (MW):")
    print(f"  Min:    {df['value'].min():>10,.0f}")
    print(f"  Max:    {df['value'].max():>10,.0f}")
    print(f"  Mean:   {df['value'].mean():>10,.0f}")
    print(f"  Median: {df['value'].median():>10,.0f}")
    print(f"  Std:    {df['value'].std():>10,.0f}")

    # ── 2. Gap detection ────────────────────────────────────
    df = df.sort_values("period").reset_index(drop=True)
    diffs = df["period"].diff()
    gaps = df[diffs > timedelta(hours=1)]
    print(f"\nTimestamp gaps (> 1 hour): {len(gaps)}")
    if len(gaps) > 0:
        print("  First 10:")
        for _, row in gaps.head(10).iterrows():
            prev = df.loc[row.name - 1, "period"]
            gap_h = (row["period"] - prev).total_seconds() / 3600
            print(f"    {prev} → {row['period']}  ({gap_h:.0f}h)")

    # ── 3. Outlier scan ─────────────────────────────────────
    low = df[df["value"] < 20_000]
    high = df[df["value"] > 85_000]
    print(f"\nPotential outliers:")
    print(f"  Below 20,000 MW: {len(low)}")
    print(f"  Above 85,000 MW: {len(high)}")
    if len(low) > 0:
        print(f"  Lowest 5 values:")
        for _, r in low.nsmallest(5, "value").iterrows():
            print(f"    {r['period']}  {r['value']:,.0f} MW")

    # ── time features for plots ─────────────────────────────
    df["hour"] = df["period"].dt.hour
    df["dow"] = df["period"].dt.dayofweek      # 0 = Monday
    df["month"] = df["period"].dt.month
    df["year"] = df["period"].dt.year

    # ── Plot 1: Full time series ────────────────────────────
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(df["period"], df["value"], linewidth=0.3, alpha=0.7)
    ax.set_title("ERCOT Demand Over Time")
    ax.set_ylabel("Demand (MW)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "1_timeseries.png", dpi=150)
    plt.close(fig)
    print("\nSaved → 1_timeseries.png")

    # ── Plot 2: Hour-of-day pattern ─────────────────────────
    fig, ax = plt.subplots(figsize=(12, 5))
    df.boxplot(column="value", by="hour", ax=ax, showfliers=False)
    ax.set_title("Demand by Hour of Day (UTC)")
    ax.set_xlabel("Hour (UTC)")
    ax.set_ylabel("Demand (MW)")
    fig.suptitle("")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "2_hourly_pattern.png", dpi=150)
    plt.close(fig)
    print("Saved → 2_hourly_pattern.png")

    # ── Plot 3: Day-of-week pattern ─────────────────────────
    dow_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    fig, ax = plt.subplots(figsize=(10, 5))
    df.boxplot(column="value", by="dow", ax=ax, showfliers=False)
    ax.set_xticklabels(dow_labels)
    ax.set_title("Demand by Day of Week")
    ax.set_ylabel("Demand (MW)")
    fig.suptitle("")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "3_daily_pattern.png", dpi=150)
    plt.close(fig)
    print("Saved → 3_daily_pattern.png")

    # ── Plot 4: Monthly pattern ─────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 5))
    df.boxplot(column="value", by="month", ax=ax, showfliers=False)
    ax.set_title("Demand by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Demand (MW)")
    fig.suptitle("")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "4_monthly_pattern.png", dpi=150)
    plt.close(fig)
    print("Saved → 4_monthly_pattern.png")

    # ── Plot 5: Value distribution ──────────────────────────
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df["value"], bins=100, edgecolor="black", linewidth=0.3)
    ax.set_title("Demand Distribution")
    ax.set_xlabel("Demand (MW)")
    ax.set_ylabel("Frequency")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "5_distribution.png", dpi=150)
    plt.close(fig)
    print("Saved → 5_distribution.png")

    # ── Plot 6: Year-over-year monthly averages ─────────────
    monthly = df.groupby(["year", "month"])["value"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(12, 5))
    for yr in sorted(monthly["year"].unique()):
        yd = monthly[monthly["year"] == yr]
        ax.plot(yd["month"], yd["value"], marker="o", label=str(yr))
    ax.set_title("Average Monthly Demand by Year")
    ax.set_xlabel("Month")
    ax.set_ylabel("Mean Demand (MW)")
    ax.set_xticks(range(1, 13))
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "6_yearly_comparison.png", dpi=150)
    plt.close(fig)
    print("Saved → 6_yearly_comparison.png")

    print(f"\nAll plots saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
