import argparse
import pandas as pd
from pathlib import Path
from nse_market_circuits.fetcher import MarketCircuitsFetcher
from nse_market_circuits.analyzer import CircuitAnalyzer

def main():
    parser = argparse.ArgumentParser(description="NSE Market Circuits & Price Bands Agent")
    parser.add_argument("--symbol", help="Query circuit bands for symbol")
    parser.add_argument("--sync", action="store_true", help="Sync latest daily price bands from NSE")
    args = parser.parse_args()

    csv_path = Path(__file__).parent / "output" / "security_circuits.csv"
    if not csv_path.exists():
        print("Output file not found. Run sync first.")
        return

    df = pd.read_csv(csv_path)
    if args.symbol:
        sym_df = df[df["symbol"] == args.symbol.upper()]
        print(f"\n--- Price Bands for {args.symbol} ---")
        print(sym_df[["symbol", "trade_date", "band_pct", "lower_circuit", "upper_circuit"]].to_string())
    elif args.sync:
        fetcher = MarketCircuitsFetcher()
        live = fetcher.fetch_price_bands()
        print(f"Retrieved price bands for {len(live)} securities.")
    else:
        print(f"Loaded {len(df)} circuit band records. Use --symbol <TICKER> or --sync.")

if __name__ == "__main__":
    main()
