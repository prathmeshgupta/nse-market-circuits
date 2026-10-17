import io
import requests
import pandas as pd
from typing import Optional

NSE_PRICE_BANDS_URL = "https://archives.nseindia.com/content/equities/sec_list.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

class MarketCircuitsFetcher:
    """Fetches daily exchange price bands (upper/lower circuit limits) for all listed NSE securities."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def fetch_price_bands(self) -> pd.DataFrame:
        resp = self.session.get(NSE_PRICE_BANDS_URL, timeout=15)
        resp.raise_for_status()
        df = pd.read_csv(io.StringIO(resp.text))
        df.columns = [c.strip().replace(" ", "_").upper() for c in df.columns]

        rename_map = {
            "SYMBOL": "symbol",
            "SERIES": "series",
            "SECURITY_NAME": "security_name",
            "BAND": "band_pct",
            "BAND_PERCENT": "band_pct",
            "REMARKS": "remarks"
        }
        df = df.rename(columns=rename_map)
        df["band_pct"] = df["band_pct"].astype(str)
        df["source"] = "NSE_SEC_LIST"
        cols = ["symbol", "series", "security_name", "band_pct", "remarks", "source"]
        for c in cols:
            if c not in df.columns:
                df[c] = ""
        return df[cols]
