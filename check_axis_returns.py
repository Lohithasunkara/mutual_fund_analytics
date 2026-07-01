import pandas as pd

nav5 = pd.read_csv('data/processed/five_schemes_nav_clean.csv')
nav5['date'] = pd.to_datetime(nav5['date'])

axis = nav5[nav5['scheme_code'] == 119092].sort_values('date').reset_index(drop=True)
axis['daily_return'] = axis['nav'].pct_change()

print('Daily return stats:')
print(axis['daily_return'].describe())
print()
print('Sample of consecutive daily returns:')
print(axis[['date','nav','daily_return']].iloc[100:115].to_string())
