import pandas as pd

hdfc = pd.read_csv("data/raw/hdfc_top100_nav.csv")
print(f"HDFC shape before: {hdfc.shape}")
hdfc['date'] = pd.to_datetime(hdfc['date'], dayfirst=True, errors='coerce')
hdfc = hdfc.dropna(subset=['date'])
hdfc = hdfc[hdfc['nav'] > 0]
hdfc = hdfc.drop_duplicates()
hdfc = hdfc.sort_values(['scheme_code', 'date'])
hdfc.to_csv("data/processed/hdfc_top100_nav_clean.csv", index=False)
print(f"HDFC shape after:  {hdfc.shape}")
print("✅ Saved hdfc_top100_nav_clean.csv")

# Clean Five Schemes NAV 
five = pd.read_csv("data/raw/five_schemes_nav.csv")
print(f"\nFive schemes shape before: {five.shape}")
five['date'] = pd.to_datetime(five['date'], dayfirst=True, errors='coerce')
five = five.dropna(subset=['date'])
five = five[five['nav'] > 0]
five = five.drop_duplicates()
five = five.sort_values(['scheme_code', 'date'])
five.to_csv("data/processed/five_schemes_nav_clean.csv", index=False)
print(f"Five schemes shape after:  {five.shape}")
print(" Saved five_schemes_nav_clean.csv")

print("\n All live NAV data cleaned!")