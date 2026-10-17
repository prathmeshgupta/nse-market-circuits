"""
Automated Weekly Dataset Updater for nse-market-circuits
Can be executed locally or via GitHub Actions.
Zero credentials required.
"""

import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
from nse_market_circuits.fetcher import MarketCircuitsFetcher

OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILE = OUTPUT_DIR / "security_circuits.csv"
PARQUET_FILE = OUTPUT_DIR / "security_circuits.parquet"


def update():
    print("[1/3] Fetching latest daily dynamic price bands from official NSE archives...")
    fetcher = MarketCircuitsFetcher()
    
    bands_df = fetcher.fetch_price_bands()
    bands_df["trade_date"] = date.today().isoformat()
    bands_df["band_pct"] = bands_df["band_pct"].astype(str)
    print(f"      Retrieved price bands for {len(bands_df)} securities as of {date.today().isoformat()}.")

    print("[2/3] Merging and saving updated price bands...")
    if CSV_FILE.exists():
        existing_df = pd.read_csv(CSV_FILE)
        existing_df["band_pct"] = existing_df["band_pct"].astype(str)
        combined = pd.concat([existing_df, bands_df], ignore_index=True)
    else:
        combined = bands_df.copy()

    combined = combined.drop_duplicates(subset=["symbol", "trade_date"], keep="last")
    combined = combined.sort_values(by=["trade_date", "symbol"], ascending=[False, True])

    combined.to_csv(CSV_FILE, index=False)
    combined.to_parquet(PARQUET_FILE, index=False)
    print(f"      Saved {len(combined)} records to {CSV_FILE.name} and {PARQUET_FILE.name}.")

    print("[3/3] Running automated quality audit...")
    from evaluate_quality import audit_quality
    audit_quality()
    print("Update complete successfully.")


if __name__ == "__main__":
    update()
