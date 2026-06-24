import requests
import pandas as pd

# Fetch HDFC Top 100 Direct
print("Fetching HDFC Top 100 Direct (125497)...")
url = "https://api.mfapi.in/mf/125497"
response = requests.get(url)
data = response.json()

scheme_name = data["meta"]["scheme_name"]
nav_records = data["data"]

df_hdfc = pd.DataFrame(nav_records)
df_hdfc["scheme_code"] = 125497
df_hdfc["scheme_name"] = scheme_name
df_hdfc.to_csv("data/raw/hdfc_top100_nav.csv", index=False)
print(f" {scheme_name}")
print(f"   Records: {len(df_hdfc)}")
print(df_hdfc.head(3))

# Fetch NAV for 5 key schemes
schemes = {
    119551: "SBI Bluechip",
    120503: "ICICI Bluechip",
    118632: "Nippon Large Cap",
    119092: "Axis Bluechip",
    120841: "Kotak Bluechip"
}

all_nav = []

print("\nFetching 5 key schemes...")
for code, name in schemes.items():
    try:
        res = requests.get(f"https://api.mfapi.in/mf/{code}")
        d = res.json()
        records = d["data"]
        for r in records:
            r["scheme_code"] = code
            r["scheme_name"] = name
        all_nav.extend(records)
        print(f" {name} ({code}) → {len(records)} records")
    except Exception as e:
        print(f" {name} ({code}) → Error: {e}")

df_all = pd.DataFrame(all_nav)
df_all.to_csv("data/raw/five_schemes_nav.csv", index=False)
print(f"\n Saved {len(df_all)} total records to data/raw/five_schemes_nav.csv")
print(df_all.head())