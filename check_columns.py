import sqlite3
conn = sqlite3.connect('data/mutual_funds.db')
cur = conn.cursor()
for t in ['dim_fund', 'fact_performance', 'fact_transactions', 'fact_aum', 'fact_nav', 'dim_date']:
    cur.execute(f"PRAGMA table_info({t})")
    cols = [row[1] for row in cur.fetchall()]
    print(t, '->', cols)
conn.close()
