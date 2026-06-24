import pandas as pd
import numpy as np

df = pd.read_csv("data/raw/scheme_performance.csv")
print("Shape before cleaning:", df.shape)
print(df)

# ── 1. Validate return columns are numeric ────────────────────────────────────
return_cols = ["return_1yr", "return_3yr", "return_5yr"]

for col in return_cols:
    # Replace non-numeric strings with NaN
    df[col] = pd.to_numeric(df[col], errors="coerce")
    non_numeric = df[col].isna().sum()
    if non_numeric > 0:
        print(f"⚠️  {non_numeric} non-numeric values found in {col} → set to NaN")

print("✅ Return columns converted to numeric")

# ── 2. Flag anomalies in return values ───────────────────────────────────────
# Returns outside -50% to 100% are suspicious for mutual funds
for col in return_cols:
    anomalies = df[(df[col] < -50) | (df[col] > 100)]
    if not anomalies.empty:
        print(f"⚠️  Anomalies in {col}:")
        print(anomalies[["amfi_code", "scheme_name", col]])
        # Flag them
        df[f"{col}_anomaly"] = ((df[col] < -50) | (df[col] > 100))
    else:
        df[f"{col}_anomaly"] = False

# Set anomaly values to NaN
for col in return_cols:
    df.loc[df[f"{col}_anomaly"] == True, col] = np.nan

print("✅ Anomalies flagged and set to NaN")

# ── 3. Check expense_ratio range (0.1% to 2.5%) ──────────────────────────────
df["expense_ratio"] = pd.to_numeric(df["expense_ratio"], errors="coerce")

out_of_range = df[(df["expense_ratio"] < 0.1) | (df["expense_ratio"] > 2.5)]
if not out_of_range.empty:
    print(f"⚠️  {len(out_of_range)} rows with expense_ratio out of range (0.1–2.5):")
    print(out_of_range[["amfi_code", "scheme_name", "expense_ratio"]])
    df["expense_ratio_flag"] = (df["expense_ratio"] < 0.1) | (df["expense_ratio"] > 2.5)
else:
    df["expense_ratio_flag"] = False

print("✅ expense_ratio checked")

# ── 4. Save ───────────────────────────────────────────────────────────────────
df.to_csv("data/processed/scheme_performance_clean.csv", index=False)
print("\nShape after cleaning:", df.shape)
print(df)
print("✅ Saved to data/processed/scheme_performance_clean.csv")