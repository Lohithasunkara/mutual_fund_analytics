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
# Explore fund master
print("\n" + "="*60)
print("STEP 6 — FUND MASTER EXPLORATION")
print("="*60)

nav = pd.read_csv("data/raw/nav_history.csv")

print(f"\nTotal schemes in nav_history: {nav['amfi_code'].nunique()}")
print(f"\nSample scheme names:")
print(nav['scheme_name'].unique()[:10])

# Extract fund house from scheme name 
print(f"\nSample AMFI codes:")
print(nav['amfi_code'].unique()[:15])

print(f"\nDate range:")
print(f"  Earliest: {nav['date'].min()}")
print(f"  Latest:   {nav['date'].max()}")

# Validate AMFI codes 
print("\n" + "="*60)
print("STEP 7 — AMFI CODE VALIDATION")
print("="*60)

five = pd.read_csv("data/raw/five_schemes_nav.csv")
hdfc = pd.read_csv("data/raw/hdfc_top100_nav.csv")

nav_codes    = set(nav['amfi_code'].astype(str))
five_codes   = set(five['scheme_code'].astype(str))
hdfc_codes   = set(hdfc['scheme_code'].astype(str))

all_fetched  = five_codes | hdfc_codes
missing      = all_fetched - nav_codes
matched      = all_fetched & nav_codes

print(f"\nCodes in nav_history          : {len(nav_codes)}")
print(f"Codes fetched (5+HDFC schemes): {len(all_fetched)}")
print(f"Matched codes                 : {len(matched)}")
print(f"Missing from nav_history      : {len(missing)}")

if missing:
    print(f"  Missing codes: {missing}")
else:
    print(" All fetched codes exist in nav_history")

print("\n── DATA QUALITY SUMMARY ──")
print(f"  nav_history   → {nav.shape[0]} rows, {nav['amfi_code'].nunique()} unique schemes")
print(f"  Null values   → {nav.isnull().sum().sum()}")
print(f"  Duplicate rows→ {nav.duplicated().sum()}")
print("\n Step 6 & 7 complete!")