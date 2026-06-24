import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///data/mutual_funds.db")

queries = {}

# Query 1: Top 5 funds by average NAV 
queries["Q1_top5_funds_by_avg_nav"] = """
SELECT 
    amfi_code,
    scheme_name,
    ROUND(AVG(nav), 2) AS avg_nav,
    COUNT(*)           AS trading_days
FROM fact_nav_staging
JOIN fact_performance_staging USING (amfi_code)
GROUP BY amfi_code, scheme_name
ORDER BY avg_nav DESC
LIMIT 5
"""

#  Query 2: Average NAV per month 
queries["Q2_avg_nav_per_month"] = """
SELECT
    STRFTIME('%Y-%m', date) AS month,
    amfi_code,
    ROUND(AVG(nav), 2)      AS avg_nav
FROM fact_nav_staging
GROUP BY month, amfi_code
ORDER BY month, amfi_code
"""

# Query 3: SIP transactions YoY growth 
queries["Q3_sip_yoy_growth"] = """
SELECT
    STRFTIME('%Y', date)   AS year,
    COUNT(*)               AS sip_count,
    ROUND(SUM(amount), 2)  AS total_amount
FROM fact_transactions_staging
WHERE transaction_type = 'SIP'
GROUP BY year
ORDER BY year
"""

# Query 4: Transactions by KYC status 
queries["Q4_transactions_by_kyc_status"] = """
SELECT
    kyc_status,
    COUNT(*)              AS transaction_count,
    ROUND(SUM(amount), 2) AS total_amount,
    ROUND(AVG(amount), 2) AS avg_amount
FROM fact_transactions_staging
GROUP BY kyc_status
ORDER BY transaction_count DESC
"""

#  Query 5: Funds with expense_ratio < 1% 
queries["Q5_funds_expense_ratio_below_1"] = """
SELECT
    amfi_code,
    scheme_name,
    category,
    expense_ratio
FROM fact_performance_staging
WHERE expense_ratio < 1.0
  AND expense_ratio_flag = 0
ORDER BY expense_ratio ASC
"""

# Query 6: Best performing funds by 1yr return
queries["Q6_best_1yr_return"] = """
SELECT
    amfi_code,
    scheme_name,
    category,
    ROUND(return_1yr, 2) AS return_1yr,
    ROUND(return_3yr, 2) AS return_3yr,
    ROUND(return_5yr, 2) AS return_5yr
FROM fact_performance_staging
WHERE return_1yr IS NOT NULL
  AND return_1yr_anomaly = 0
ORDER BY return_1yr DESC
LIMIT 5
"""

# Query 7: Transaction type breakdown
queries["Q7_transaction_type_breakdown"] = """
SELECT
    transaction_type,
    COUNT(*)              AS count,
    ROUND(SUM(amount), 2) AS total_amount,
    ROUND(AVG(amount), 2) AS avg_amount,
    ROUND(MIN(amount), 2) AS min_amount,
    ROUND(MAX(amount), 2) AS max_amount
FROM fact_transactions_staging
GROUP BY transaction_type
ORDER BY total_amount DESC
"""

# Query 8: NAV trend for a specific fund 
queries["Q8_nav_trend_fund_119551"] = """
SELECT
    date,
    nav,
    ROUND(nav - LAG(nav) OVER (ORDER BY date), 2) AS nav_change
FROM fact_nav_staging
WHERE amfi_code = 119551
ORDER BY date
LIMIT 30
"""

# Query 9: Funds with anomaly flags 
queries["Q9_funds_with_anomalies"] = """
SELECT
    amfi_code,
    scheme_name,
    return_1yr,
    return_1yr_anomaly,
    return_3yr_anomaly,
    return_5yr_anomaly,
    expense_ratio,
    expense_ratio_flag
FROM fact_performance_staging
WHERE return_1yr_anomaly = 1
   OR return_3yr_anomaly = 1
   OR return_5yr_anomaly = 1
   OR expense_ratio_flag = 1
"""

# Query 10: Monthly SIP vs Lumpsum vs Redemption comparison 
queries["Q10_monthly_transaction_comparison"] = """
SELECT
    STRFTIME('%Y-%m', date)                                        AS month,
    ROUND(SUM(CASE WHEN transaction_type='SIP'        THEN amount ELSE 0 END), 2) AS sip_total,
    ROUND(SUM(CASE WHEN transaction_type='Lumpsum'    THEN amount ELSE 0 END), 2) AS lumpsum_total,
    ROUND(SUM(CASE WHEN transaction_type='Redemption' THEN amount ELSE 0 END), 2) AS redemption_total
FROM fact_transactions_staging
GROUP BY month
ORDER BY month
"""

# Run all queries & display results 
with engine.connect() as conn:
    for name, sql in queries.items():
        print(f"\n{'='*60}")
        print(f" {name}")
        print('='*60)
        try:
            df = pd.read_sql(text(sql), conn)
            if df.empty:
                print(" No data returned")
            else:
                print(df.to_string(index=False))
        except Exception as e:
            print(f" Error: {e}")

print("\n All 10 queries executed!")