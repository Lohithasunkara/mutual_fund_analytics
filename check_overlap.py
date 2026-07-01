import pandas as pd

nav = pd.read_csv('data/processed/nav_history_clean.csv')
perf = pd.read_csv('data/processed/scheme_performance_clean.csv')

print('Performance amfi_codes:', perf['amfi_code'].tolist())
print()
overlap = perf['amfi_code'].isin(nav['amfi_code']).sum()
print(f'Of {len(perf)} performance funds, {overlap} have matching NAV history')
print()
print('scheme_performance_clean full preview:')
print(perf.to_string())
