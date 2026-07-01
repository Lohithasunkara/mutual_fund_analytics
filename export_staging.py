import sqlite3
import csv

conn = sqlite3.connect('data/mutual_funds.db')
tables = ['fact_nav_staging', 'fact_transactions_staging', 'fact_performance_staging']

for t in tables:
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {t}")
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    with open(f'data/{t}.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        writer.writerows(rows)
    print(t, '->', len(rows), 'rows exported')

conn.close()
