import sqlite3
conn = sqlite3.connect('data/mutual_funds.db')
cur = conn.cursor()
tables = ['dim_fund', 'dim_date', 'fact_nav', 'fact_aum', 'fact_performance', 'fact_transactions', 'fact_nav_staging', 'fact_transactions_staging', 'fact_performance_staging']
for t in tables:
    cur.execute(f"SELECT COUNT(*) FROM {t}")
    print(t, '->', cur.fetchone()[0])
conn.close()
