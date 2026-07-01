import pandas as pd
import numpy as np

nav5 = pd.read_csv('data/processed/five_schemes_nav_clean.csv')
print('Columns:', list(nav5.columns))
print(nav5.head(5))
print()
print('Row count per scheme identifier:')
id_col = [c for c in nav5.columns if 'code' in c.lower() or 'scheme' in c.lower() or 'fund' in c.lower()]
print('Likely ID columns:', id_col)
print(nav5.shape)
