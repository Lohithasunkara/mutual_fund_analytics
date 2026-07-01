import pandas as pd

nav = pd.read_csv('data/processed/nav_history_clean.csv')
target_codes = [119551, 119552, 119553, 108272, 110282]
nav_filtered = nav[nav['amfi_code'].isin(target_codes)]

print('Row count per amfi_code:')
print(nav_filtered.groupby('amfi_code').size())
print()
print('Unique dates per amfi_code:')
print(nav_filtered.groupby('amfi_code')['date'].nunique())
print()
print('Date range overall:', nav['date'].min(), 'to', nav['date'].max())
print('Total unique dates in file:', nav['date'].nunique())
