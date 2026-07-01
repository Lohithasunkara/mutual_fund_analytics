import pandas as pd
import numpy as np

nav = pd.read_csv('data/processed/nav_history_clean.csv')
perf = pd.read_csv('data/processed/scheme_performance_clean.csv')
aum = pd.read_csv('data/aum_data.csv')

target_codes = [119551, 119552, 119553, 108272, 110282]
nav_filtered = nav[nav['amfi_code'].isin(target_codes)].copy()
nav_filtered['date'] = pd.to_datetime(nav_filtered['date'])
nav_filtered = nav_filtered.sort_values(['amfi_code', 'date'])

# Daily returns and annualized StdDev per fund
nav_filtered['daily_return'] = nav_filtered.groupby('amfi_code')['nav'].pct_change()
risk = nav_filtered.groupby('amfi_code')['daily_return'].std().reset_index()
risk['risk_stddev_annualized'] = risk['daily_return'] * np.sqrt(252) * 100
risk = risk[['amfi_code', 'risk_stddev_annualized']]

# Deduplicate performance: average the two snapshots per fund
perf_dedup = perf.groupby(['amfi_code', 'scheme_name', 'category'], as_index=False).agg({
    'return_1yr': 'mean',
    'return_3yr': 'mean',
    'return_5yr': 'mean',
    'expense_ratio': 'mean'
})

# Merge performance + risk
result = perf_dedup.merge(risk, on='amfi_code', how='left')

print(result.to_string())
print()
print('AUM data columns:', list(aum.columns))
print(aum.head())

result.to_csv('reports/fund_scorecard_final.csv', index=False)
print()
print('Saved to reports/fund_scorecard_final.csv')
