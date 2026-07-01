import pandas as pd

# Load NAV history and inspect columns first
nav = pd.read_csv('data/processed/nav_history_clean.csv')
print('NAV columns:', list(nav.columns))
print(nav.head(3))

scorecard = pd.read_csv('reports/fund_scorecard.csv')
print('Scorecard columns:', list(scorecard.columns))
