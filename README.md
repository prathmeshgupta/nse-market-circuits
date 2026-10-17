# NSE Market Circuits & Execution Feasibility

Daily exchange **dynamic price bands** (2%, 5%, 10%, 20% upper and lower circuit limits) for 3,500+ listed securities on the National Stock Exchange of India (NSE), with an automated trade execution feasibility analyzer.

Companion repository to [`prathmeshgupta/nifty-pit-universe`](https://github.com/prathmeshgupta/nifty-pit-universe).

---

## 📊 Summary of Datasets

All processed datasets are saved in [`output/`](output/):

| Dataset | Observations | Circuit Bands Tracked | Formats |
| :--- | :---: | :--- | :--- |
| **Security Circuits** | **3,586** | 2%, 5%, 10%, 20%, No Band (F&O) | [`security_circuits.parquet`](output/security_circuits.parquet), [`security_circuits.csv`](output/security_circuits.csv) |

---

## 💡 Why This Exists: The Fictional Fill Trap

Backtesting engines routinely make the fatal assumption that a strategy can execute a trade at the closing price of day $T$ whenever an entry or exit signal triggers.

In Indian equity markets, this assumption fails catastrophically:
1. **Upper Circuit Lockouts**: When a momentum breakout occurs, mid- and small-caps frequently gap up and lock at the **Upper Circuit (UC)**. Buying is mathematically impossible because there are only buyers and zero willing sellers.
2. **Lower Circuit Traps**: When a stock breaks down, it can lock at the **Lower Circuit (LC)** for consecutive sessions. Stop-loss market orders cannot fill, turning an assumed $-5\%$ stop-loss into an unhedged $-25\%$ slide.
3. **Derivative vs. Non-Derivative Regimes**: F&O (Futures & Options) constituent stocks do not have fixed price bands ("No Band"), whereas cash-only stocks operate with rigid daily limits.

This dataset and evaluator tag price bands to every ticker session, identifying unexecutable days to prevent paper-trading alpha that cannot exist in production.

---

## 🧱 Data Schema

### `security_circuits`
| Column | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `symbol` | String | Exchange ticker | `TATAMOTORS` |
| `trade_date` | Date | Session trading date | `2026-10-17` |
| `band_pct` | String | Daily percentage band (`2`, `5`, `10`, `20`, `No Band`) | `20` |
| `lower_circuit` | Float | Lower price floor for session | `812.50` |
| `upper_circuit` | Float | Upper price cap for session | `1218.75` |
| `is_upper_circuit_hit` | Integer | `1` if locked at UC, else `0` | `0` |
| `is_lower_circuit_hit` | Integer | `1` if locked at LC, else `0` | `0` |
| `is_trade_executable` | Integer | `1` if orders can fill, `0` if locked | `1` |

---

## 🔍 How to Query

### 1. Using Python & Pandas
```python
import pandas as pd

df = pd.read_parquet("output/security_circuits.parquet")

# Filter cash stocks with restrictive 5% circuit bands
tight_bands = df[df["band_pct"] == "5"]
print(f"Securities with 5% circuit limit: {len(tight_bands)}")
print(tight_bands[["symbol", "lower_circuit", "upper_circuit"]].head())
```

### 2. Using the CLI Helper
```bash
python runner.py --symbol TATAMOTORS
```

---

## 🧪 Quality Audit
```bash
python evaluate_quality.py
```
* **Band Completeness**: 3,580+ active securities mapped ([PASS]).
* **Identifier Verification**: 0 null symbols ([PASS]).

---

## 📄 License
MIT License. Copyright (c) 2026 Prathmesh Gupta.
