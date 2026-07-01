import pandas as pd

alpha_beta = pd.read_csv('reports/alpha_beta.csv')
print('alpha_beta columns:', list(alpha_beta.columns))
print(alpha_beta.head(3))
print()

cagr = pd.read_csv('reports/cagr_table.csv')
print('cagr_table columns:', list(cagr.columns))
print(cagr.head(3))
print()

perf = pd.read_csv('data/processed/scheme_performance_clean.csv')
print('scheme_performance_clean columns:', list(perf.columns))
print(perf.head(3))
