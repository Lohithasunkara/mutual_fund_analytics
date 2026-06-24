import pandas as pd

df = pd.read_csv("data/raw/nav_history.csv")
print("Shape before cleaning:", df.shape)
print(df.head())

# 1. Parse dates
df["date"] = pd.to_datetime(df["date"], format="%d-%b-%Y", errors="coerce")
df = df.dropna(subset=["date"])

# 2. Sort
df = df.sort_values(["amfi_code", "date"]).reset_index(drop=True)

# 3. Forward-fill weekends/holidays
filled_parts = []
for code, group in df.groupby("amfi_code"):
    group = group.set_index("date")
    full_range = pd.date_range(start=group.index.min(), end=group.index.max(), freq="D")
    group = group.reindex(full_range)
    group["amfi_code"] = code
    group["nav"] = group["nav"].ffill()
    group.index.name = "date"
    filled_parts.append(group.reset_index())

df = pd.concat(filled_parts, ignore_index=True)

# 4. Remove duplicates
df = df.drop_duplicates(subset=["amfi_code", "date"])

# 5. Validate NAV > 0
invalid = df[df["nav"] <= 0]
if not invalid.empty:
    print(f"⚠️ {len(invalid)} invalid rows dropped")
df = df[df["nav"] > 0]

# 6. Save
df = df.sort_values(["amfi_code", "date"]).reset_index(drop=True)
df.to_csv("data/processed/nav_history_clean.csv", index=False)
print("Shape after cleaning:", df.shape)
print("✅ Saved to data/processed/nav_history_clean.csv")
