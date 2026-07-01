import sqlite3
conn = sqlite3.connect('data/mutual_funds.db')
cur = conn.cursor()
for t in ['fact_nav_staging', 'fact_transactions_staging', 'fact_performance_staging']:
    cur.execute(f"PRAGMA table_info({t})")
    cols = [row[1] for row in cur.fetchall()]
    print(t, '->', cols)
    cur.execute(f"SELECT * FROM {t} LIMIT 2")
    for row in cur.fetchall():
        print('   sample:', row)
conn.close()
