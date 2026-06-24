import pandas as pd
import numpy as np

data = {
    "amfi_code": [119551, 119552, 119553, 108272, 110282,
                  119551, 119552, 119553, 108272, 110282],
    "scheme_name": [
        "SBI Bluechip Fund", "HDFC Top 100", "ICICI Pru Nifty",
        "Axis Midcap", "Mirae Asset Largecap",
        "SBI Bluechip Fund", "HDFC Top 100", "ICICI Pru Nifty",
        "Axis Midcap", "Mirae Asset Largecap"
    ],
    "return_1yr": [12.5, "N/A", 9.8, 999, -5.2,
                   14.3, 11.2, "null", 18.7, 7.6],
    "return_3yr": [10.2, 13.5, 8.9, 22.1, 11.4,
                   9.8, "N/A", 10.5, 25.3, 10.1],
    "return_5yr": [11.8, 12.9, 9.1, 19.8, 12.3,
                   10.5, 13.1, "na", 21.4, 11.9],
    "expense_ratio": [1.2, 0.05, 1.8, 3.5, 1.05,
                      0.9, 2.1, 1.45, 2.8, 1.75],
    "category": ["Large Cap", "Large Cap", "Index", "Mid Cap", "Large Cap",
                 "Large Cap", "Large Cap", "Index", "Mid Cap", "Large Cap"]
}

df = pd.DataFrame(data)
df.to_csv("data/raw/scheme_performance.csv", index=False)
print(f"✅ Created {len(df)} records")
print(df)