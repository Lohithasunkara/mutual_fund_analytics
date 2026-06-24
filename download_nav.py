import requests
import pandas as pd
from io import StringIO

url = "https://www.amfiindia.com/spages/NAVAll.txt"
response = requests.get(url)

lines = response.text.strip().split("\n")

records = []
for line in lines:
    parts = line.strip().split(";")
    if len(parts) >= 5:
        try:
            records.append({
                "amfi_code": parts[0].strip(),
                "scheme_name": parts[3].strip(),
                "nav": float(parts[4].strip()),
                "date": parts[5].strip()
            })
        except:
            continue

df = pd.DataFrame(records)
df.to_csv("data/raw/nav_history.csv", index=False)
print(f"✅ Saved {len(df)} records to data/raw/nav_history.csv")
print(df.head())