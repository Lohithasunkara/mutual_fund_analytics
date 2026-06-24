import sqlite3

conn = sqlite3.connect("data/mutual_funds.db")
cursor = conn.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = ON")

# ── 1. dim_fund ───────────────────────────────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_fund (
    fund_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code     INTEGER NOT NULL UNIQUE,
    scheme_name   TEXT    NOT NULL,
    category      TEXT,
    expense_ratio REAL,
    kyc_required  TEXT    DEFAULT 'YES'
)
""")

# ── 2. dim_date ───────────────────────────────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_date (
    date_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    full_date  TEXT    NOT NULL UNIQUE,
    day        INTEGER,
    month      INTEGER,
    year       INTEGER,
    quarter    INTEGER,
    is_weekend INTEGER DEFAULT 0,
    is_holiday INTEGER DEFAULT 0
)
""")

# ── 3. fact_nav ───────────────────────────────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_nav (
    nav_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id   INTEGER NOT NULL,
    date_id   INTEGER NOT NULL,
    nav       REAL    NOT NULL CHECK (nav > 0),
    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    UNIQUE (fund_id, date_id)
)
""")

# ── 4. fact_transactions ──────────────────────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id          INTEGER NOT NULL,
    date_id          INTEGER NOT NULL,
    investor_id      TEXT    NOT NULL,
    transaction_type TEXT    NOT NULL CHECK (transaction_type IN ('SIP','Lumpsum','Redemption')),
    amount           REAL    NOT NULL CHECK (amount > 0),
    kyc_status       TEXT    NOT NULL CHECK (kyc_status IN ('VERIFIED','PENDING','REJECTED')),
    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
)
""")

# ── 5. fact_performance ───────────────────────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_performance (
    performance_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id              INTEGER NOT NULL,
    date_id              INTEGER NOT NULL,
    return_1yr           REAL,
    return_3yr           REAL,
    return_5yr           REAL,
    expense_ratio        REAL    CHECK (expense_ratio BETWEEN 0.1 AND 2.5),
    return_1yr_anomaly   INTEGER DEFAULT 0,
    return_3yr_anomaly   INTEGER DEFAULT 0,
    return_5yr_anomaly   INTEGER DEFAULT 0,
    expense_ratio_flag   INTEGER DEFAULT 0,
    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
)
""")

# ── 6. fact_aum ───────────────────────────────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_aum (
    aum_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id      INTEGER NOT NULL,
    date_id      INTEGER NOT NULL,
    aum_crores   REAL    NOT NULL CHECK (aum_crores > 0),
    unit_holders INTEGER,
    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    UNIQUE (fund_id, date_id)
)
""")

conn.commit()

# ── Verify all tables created ─────────────────────────────────────────────────
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("✅ Tables created:")
for t in tables:
    print(f"   → {t[0]}")

conn.close()
print("\n✅ Schema saved to data/mutual_funds.db")