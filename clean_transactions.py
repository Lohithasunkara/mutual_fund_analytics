import pandas as pd

df = pd.read_csv("data/raw/investor_transactions.csv")
print("Shape before cleaning:", df.shape)
print(df.head())

# ── 1. Standardise transaction_type ──────────────────────────────────────────
# Map all variations to standard values
transaction_map = {
    "sip": "SIP",
    "lumpsum": "Lumpsum",
    "lump sum": "Lumpsum",
    "redemption": "Redemption",
    "redeem": "Redemption"
}

df["transaction_type"] = df["transaction_type"].str.strip().str.lower()
df["transaction_type"] = df["transaction_type"].replace(transaction_map)

# Capitalize properly for mapped values
valid_types = ["SIP", "Lumpsum", "Redemption"]
invalid_types = df[~df["transaction_type"].isin([t.lower() for t in valid_types]) & 
                   ~df["transaction_type"].isin(valid_types)]
if not invalid_types.empty:
    print(f"⚠️ {len(invalid_types)} unknown transaction_type rows dropped")
    df = df[df["transaction_type"].isin(valid_types)]

print("✅ transaction_type standardised")

# ── 2. Validate amount > 0 ────────────────────────────────────────────────────
invalid_amount = df[df["amount"] <= 0]
if not invalid_amount.empty:
    print(f"⚠️ {len(invalid_amount)} rows with amount <= 0 dropped")
    print(invalid_amount[["transaction_id", "amount"]])
df = df[df["amount"] > 0]
print("✅ amount validated")

# ── 3. Fix date formats ───────────────────────────────────────────────────────
df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
invalid_dates = df[df["date"].isna()]
if not invalid_dates.empty:
    print(f"⚠️ {len(invalid_dates)} rows with unparseable dates dropped")
df = df.dropna(subset=["date"])
print("✅ dates fixed")

# ── 4. Check KYC status enum values ──────────────────────────────────────────
valid_kyc = ["VERIFIED", "PENDING", "REJECTED"]
df["kyc_status"] = df["kyc_status"].str.strip().str.upper()

invalid_kyc = df[~df["kyc_status"].isin(valid_kyc)]
if not invalid_kyc.empty:
    print(f"⚠️ {len(invalid_kyc)} rows with invalid KYC status dropped")
    print(invalid_kyc[["transaction_id", "kyc_status"]])
df = df[df["kyc_status"].isin(valid_kyc)]
print("✅ kyc_status validated")

# ── 5. Save ───────────────────────────────────────────────────────────────────
df = df.reset_index(drop=True)
df.to_csv("data/processed/investor_transactions_clean.csv", index=False)
print("\nShape after cleaning:", df.shape)
print(df.head())
print("✅ Saved to data/processed/investor_transactions_clean.csv")