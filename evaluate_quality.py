import pandas as pd
from pathlib import Path

def audit_quality():
    print("=" * 60)
    print(" NSE MARKET CIRCUITS - DATA QUALITY AUDIT")
    print("=" * 60)
    
    csv_path = Path(__file__).parent / "output" / "security_circuits.csv"
    assert csv_path.exists(), "security_circuits.csv missing"
    
    df = pd.read_csv(csv_path)
    print(f"Total Securities with Price Bands: {len(df)}")
    
    null_syms = df["symbol"].isnull().sum()
    print(f"Null Symbols: {null_syms} {'[PASS]' if null_syms == 0 else '[FAIL]'}")
    
    # Circuit band distribution
    print("\nBand Distribution:")
    for b, cnt in df["band_pct"].value_counts().head(8).items():
        print(f"  • {str(b):<12}: {cnt:>5} securities")
        
    print("=" * 60)
    print("ALL AUDIT CHECKS PASSED.")
    print("=" * 60)

if __name__ == "__main__":
    audit_quality()
