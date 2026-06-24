import pandas as pd
from sqlalchemy import create_engine, text

# Connect to SQLite 
engine = create_engine("sqlite:///data/mutual_funds.db")
print(" Connected to data/mutual_funds.db")

# Load cleaned CSVs 
nav         = pd.read_csv("data/processed/nav_history_clean.csv")
transactions = pd.read_csv("data/processed/investor_transactions_clean.csv")
performance  = pd.read_csv("data/processed/scheme_performance_clean.csv")

print(f"\n CSV row counts:")
print(f"   nav_history_clean        → {len(nav)} rows")
print(f"   investor_transactions    → {len(transactions)} rows")
print(f"   scheme_performance_clean → {len(performance)} rows")

# Load into SQLite tables 
nav.to_sql("fact_nav_staging",          con=engine, if_exists="replace", index=False)
transactions.to_sql("fact_transactions_staging", con=engine, if_exists="replace", index=False)
performance.to_sql("fact_performance_staging",  con=engine, if_exists="replace", index=False)

print(f"\n Data loaded into staging tables")

# Verify row counts match 
print(f"\n Verifying row counts in SQLite:")

with engine.connect() as conn:
    for table, source_df in [
        ("fact_nav_staging",           nav),
        ("fact_transactions_staging",  transactions),
        ("fact_performance_staging",   performance)
    ]:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
        db_count = result.fetchone()[0]
        csv_count = len(source_df)
        status = " MATCH" if db_count == csv_count else "❌ MISMATCH"
        print(f"   {table:<35} CSV: {csv_count:<6} DB: {db_count:<6} {status}")

# Show all tables in DB 
print(f"\n All tables in mutual_funds.db:")
with engine.connect() as conn:
    result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
    for row in result:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {row[0]}")).fetchone()[0]
        print(f"   → {row[0]:<40} {count} rows")

print("\n All done!")