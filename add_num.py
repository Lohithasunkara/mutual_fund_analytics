import pandas as pd

scorecard = pd.read_csv('reports/fund_scorecard_real.csv')
aum = pd.read_csv('data/aum_data.csv')

house_map = {
    118632: 'Nippon',
    119092: 'Axis',
    119551: 'SBI',
    120503: 'ICICI',
    120841: 'Kotak'
}
scorecard['fund_house'] = scorecard['scheme_code'].map(house_map)

latest_year = aum['Year'].max()
aum_latest = aum[aum['Year'] == latest_year][['Fund_House', 'AUM_Cr']]

scorecard = scorecard.merge(aum_latest, left_on='fund_house', right_on='Fund_House', how='left')
scorecard = scorecard.drop(columns=['Fund_House'])
scorecard.to_csv('reports/fund_scorecard_powerbi.csv', index=False)
print(scorecard.to_string())