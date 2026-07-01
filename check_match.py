import pandas as pd

nav = pd.read_csv('data/processed/nav_history_clean.csv')
scorecard = pd.read_csv('reports/fund_scorecard.csv')

print('Unique NAV scheme names (sample):')
print(nav['scheme_name'].unique()[:5])
print()
print('Unique scorecard scheme names (sample):')
print(scorecard['Scheme_Name'].unique()[:5])
print()
print('NAV unique scheme count:', nav['scheme_name'].nunique())
print('Scorecard unique scheme count:', scorecard['Scheme_Name'].nunique())
