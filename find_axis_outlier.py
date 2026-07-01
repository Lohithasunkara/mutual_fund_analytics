import pandas as pd

nav5 = pd.read_csv('data/processed/five_schemes_nav_clean.csv')
nav5['date'] = pd.to_datetime(nav5['date'])

mask = (nav5['scheme_code'] == 119092) & (nav5['date'] >= '2015-08-30')
nav5.loc[mask, 'nav'] = nav5.loc[mask, 'nav'] / 100

nav5.to_csv('data/processed/five_schemes_nav_clean.csv', index=False)

axis_check = nav5[nav5['scheme_code']==119092].sort_values('date')
print(axis_check.iloc[::200][['date','nav']].to_string())