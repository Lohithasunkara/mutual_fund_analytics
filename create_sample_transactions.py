import pandas as pd
import numpy as np

data = {
    "transaction_id": range(1, 21),
    "amfi_code": [119551, 119552, 119553, 108272, 110282] * 4,
    "investor_id": [f"INV{str(i).zfill(3)}" for i in range(1, 21)],
    "transaction_type": [
        "SIP", "sip", "Sip", "LUMPSUM", "lumpsum",
        "Lump Sum", "REDEMPTION", "redemption", "Redeem", "SIP",
        "SIP", "Lumpsum", "REDEMPTION", "sip", "LUMPSUM",
        "redemption", "SIP", "lumpsum", "Redemption", "SIP"
    ],
    "amount": [
        5000, 10000, -500, 25000, 0,
        15000, 8000, -100, 12000, 5000,
        3000, 20000, 7000, 5000, 50000,
        9000, 4000, 0, 6000, 5000
    ],
    "date": [
        "01-01-2026", "2026/02/15", "March 3 2026", "04-04-2026", "2026-05-01",
        "06/06/2026", "07-07-2026", "2026-08-08", "09-09-2026", "10-10-2026",
        "11-11-2026", "12-12-2025", "01-06-2026", "15-02-2026", "03-03-2026",
        "04-04-2026", "05-05-2026", "06-06-2026", "07-07-2026", "08-08-2026"
    ],
    "kyc_status": [
        "VERIFIED", "verified", "Verified", "PENDING", "pending",
        "Pending", "REJECTED", "rejected", "VERIFIED", "Unknown",
        "VERIFIED", "PENDING", "verified", "REJECTED", "VERIFIED",
        "pending", "Verified", "VERIFIED", "invalid_status", "VERIFIED"
    ]
}

df = pd.DataFrame(data)
df.to_csv("data/raw/investor_transactions.csv", index=False)
print(f"✅ Created {len(df)} sample transactions")
print(df.head())