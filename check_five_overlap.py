import pandas as pd

nav5 = pd.read_csv('data/processed/five_schemes_nav_clean.csv')
perf = pd.read_csv('data/processed/scheme_performance_clean.csv')

print('five_schemes_nav_clean scheme codes:', sorted(nav5['scheme_code'].unique()))
print('scheme_performance_clean amfi_codes:', sorted(perf['amfi_code'].unique()))
print()
overlap = set(nav5['scheme_code'].unique()) & set(perf['amfi_code'].unique())
print('Overlap:', overlap)
print()
print('Rows per scheme in five_schemes_nav_clean:')
print(nav5.groupby(['scheme_code','scheme_name']).size())
