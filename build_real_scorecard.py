import pandas as pd
import numpy as np

nav5 = pd.read_csv('data/processed/five_schemes_nav_clean.csv')
nav5['date'] = pd.to_datetime(nav5['date'])
nav5 = nav5.sort_values(['scheme_code', 'date'])

results = []
latest_date = nav5['date'].max()

for code, grp in nav5.groupby('scheme_code'):
    grp = grp.sort_values('date')
    name = grp['scheme_name'].iloc[0]

    # Daily returns -> annualized StdDev (risk)
    daily_ret = grp['nav'].pct_change()
    risk_stddev = daily_ret.std() * np.sqrt(252) * 100

    # 1yr and 3yr return using NAV ~365/1095 days back from latest date
    def nav_on_or_before(target_date):
        sub = grp[grp['date'] <= target_date]
        return sub['nav'].iloc[-1] if len(sub) else None

    nav_latest = grp['nav'].iloc[-1]
    nav_1yr_ago = nav_on_or_before(latest_date - pd.Timedelta(days=365))
    nav_3yr_ago = nav_on_or_before(latest_date - pd.Timedelta(days=365*3))

    return_1yr = ((nav_latest / nav_1yr_ago) - 1) * 100 if nav_1yr_ago else None
    return_3yr = (((nav_latest / nav_3yr_ago) ** (1/3)) - 1) * 100 if nav_3yr_ago else None

    results.append({
        'scheme_code': code,
        'scheme_name': name,
        'nav_latest': nav_latest,
        'return_1yr': round(return_1yr, 2) if return_1yr else None,
        'return_3yr_cagr': round(return_3yr, 2) if return_3yr else None,
        'risk_stddev_annualized': round(risk_stddev, 2)
    })

result_df = pd.DataFrame(results)
print(result_df.to_string())

result_df.to_csv('reports/fund_scorecard_real.csv', index=False)
print()
print('Saved to reports/fund_scorecard_real.csv')
