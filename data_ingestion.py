import pandas as pd
import os

files = {
    "nav_history":            "data/raw/nav_history.csv",
    "investor_transactions":  "data/raw/investor_transactions.csv",
    "scheme_performance":     "data/raw/scheme_performance.csv",
    "hdfc_top100_nav":        "data/raw/hdfc_top100_nav.csv",
    "five_schemes_nav":       "data/raw/five_schemes_nav.csv",
}

print("=" * 60)
print("DATA INGESTION REPORT")
print("=" * 60)

anomalies = []

for name, path in files.items():
    if not os.path.exists(path):
        print(f"\n  MISSING: {path}")
        continue

    df = pd.read_csv(path)

    print(f"\n {name}")
    print(f"   Shape     : {df.shape}")
    print(f"   Columns   : {list(df.columns)}")
    print(f"   Dtypes    :\n{df.dtypes.to_string()}")
    print(f"   Head      :\n{df.head(3).to_string()}")

    # Check anomalies
    nulls = df.isnull().sum()
    null_cols = nulls[nulls > 0]
    if not null_cols.empty:
        anomalies.append(f"{name} → nulls in: {dict(null_cols)}")

    dups = df.duplicated().sum()
    if dups > 0:
        anomalies.append(f"{name} → {dups} duplicate rows")

print("\n" + "=" * 60)
print("ANOMALY SUMMARY")
print("=" * 60)
if anomalies:
    for a in anomalies:
        print(f"  {a}")
else:
    print(" No anomalies found!")

print("\n Data ingestion report complete!")