# 📘 Data Dictionary — Mutual Fund Analytics Project

> **Project:** Mutual Fund Analytics Pipeline  
> **Author:** Lohitha Sunkara  
> **Created:** June 2026  
> **Database:** `mutual_funds.db` (SQLite)  
> **Source:** AMFI India (https://www.amfiindia.com)

---

## 📑 Table of Contents

1. [dim_fund](#1-dim_fund)
2. [dim_date](#2-dim_date)
3. [fact_nav](#3-fact_nav)
4. [fact_transactions](#4-fact_transactions)
5. [fact_performance](#5-fact_performance)
6. [fact_aum](#6-fact_aum)
7. [Staging Tables](#7-staging-tables)
8. [Source Files](#8-source-files)

---

## 1. dim_fund

**Description:** Master dimension table storing details of all mutual fund schemes.  
**Source:** `nav_history_clean.csv`, `scheme_performance_clean.csv`  
**Grain:** One row per unique mutual fund scheme.

| Column | Data Type | Nullable | Business Definition | Example |
|--------|-----------|----------|---------------------|---------|
| `fund_id` | INTEGER | No | Auto-incremented surrogate primary key | `1` |
| `amfi_code` | INTEGER | No | Unique scheme code assigned by AMFI (Association of Mutual Funds in India) | `119551` |
| `scheme_name` | TEXT | No | Full official name of the mutual fund scheme | `SBI Bluechip Fund` |
| `category` | TEXT | Yes | SEBI-defined fund category | `Large Cap`, `Mid Cap`, `Index` |
| `expense_ratio` | REAL | Yes | Annual fee charged by the fund as % of AUM. Valid range: 0.1% – 2.5% | `1.20` |
| `kyc_required` | TEXT | Yes | Whether KYC is mandatory for investing. Default: YES | `YES` |

**Constraints:**
- `fund_id` → PRIMARY KEY
- `amfi_code` → UNIQUE

---

## 2. dim_date

**Description:** Calendar dimension table used to support time-based analysis across all fact tables.  
**Source:** Generated programmatically from NAV date range.  
**Grain:** One row per calendar date.

| Column | Data Type | Nullable | Business Definition | Example |
|--------|-----------|----------|---------------------|---------|
| `date_id` | INTEGER | No | Auto-incremented surrogate primary key | `1` |
| `full_date` | TEXT | No | Full calendar date in YYYY-MM-DD format | `2026-06-23` |
| `day` | INTEGER | Yes | Day of the month (1–31) | `23` |
| `month` | INTEGER | Yes | Month of the year (1–12) | `6` |
| `year` | INTEGER | Yes | Four-digit calendar year | `2026` |
| `quarter` | INTEGER | Yes | Quarter of the year (1–4) | `2` |
| `is_weekend` | INTEGER | Yes | 1 if Saturday or Sunday, 0 otherwise | `0` |
| `is_holiday` | INTEGER | Yes | 1 if a market holiday, 0 otherwise | `0` |

**Constraints:**
- `date_id` → PRIMARY KEY
- `full_date` → UNIQUE

---

## 3. fact_nav

**Description:** Fact table storing daily Net Asset Value (NAV) for each mutual fund scheme.  
**Source:** `nav_history_clean.csv` → downloaded from AMFI NAVAll.txt  
**Grain:** One row per fund per date.

| Column | Data Type | Nullable | Business Definition | Example |
|--------|-----------|----------|---------------------|---------|
| `nav_id` | INTEGER | No | Auto-incremented surrogate primary key | `1` |
| `fund_id` | INTEGER | No | Foreign key referencing `dim_fund.fund_id` | `3` |
| `date_id` | INTEGER | No | Foreign key referencing `dim_date.date_id` | `15` |
| `nav` | REAL | No | Net Asset Value per unit of the fund on that date. Must be > 0. Weekends/holidays forward-filled from last trading day | `106.04` |

**Constraints:**
- `nav_id` → PRIMARY KEY
- `fund_id` → FOREIGN KEY → `dim_fund(fund_id)`
- `date_id` → FOREIGN KEY → `dim_date(date_id)`
- `nav` → CHECK `nav > 0`
- `(fund_id, date_id)` → UNIQUE

**Cleaning Applied:**
- Non-positive NAV values dropped (243 rows removed)
- Missing dates (weekends/holidays) forward-filled using last known NAV
- Duplicates removed on `(amfi_code, date)`

---

## 4. fact_transactions

**Description:** Fact table recording all investor-level mutual fund transactions.  
**Source:** `investor_transactions_clean.csv`  
**Grain:** One row per transaction.

| Column | Data Type | Nullable | Business Definition | Example |
|--------|-----------|----------|---------------------|---------|
| `transaction_id` | INTEGER | No | Auto-incremented surrogate primary key | `1` |
| `fund_id` | INTEGER | No | Foreign key referencing `dim_fund.fund_id` | `2` |
| `date_id` | INTEGER | No | Foreign key referencing `dim_date.date_id` | `10` |
| `investor_id` | TEXT | No | Unique identifier for the investor | `INV001` |
| `transaction_type` | TEXT | No | Type of transaction. Standardised values only | `SIP`, `Lumpsum`, `Redemption` |
| `amount` | REAL | No | Transaction amount in Indian Rupees (₹). Must be > 0 | `5000.00` |
| `kyc_status` | TEXT | No | KYC verification status of the investor at time of transaction | `VERIFIED`, `PENDING`, `REJECTED` |

**Constraints:**
- `transaction_id` → PRIMARY KEY
- `fund_id` → FOREIGN KEY → `dim_fund(fund_id)`
- `date_id` → FOREIGN KEY → `dim_date(date_id)`
- `transaction_type` → CHECK IN `('SIP', 'Lumpsum', 'Redemption')`
- `amount` → CHECK `amount > 0`
- `kyc_status` → CHECK IN `('VERIFIED', 'PENDING', 'REJECTED')`

**Cleaning Applied:**
- `transaction_type` standardised: `sip/Sip` → `SIP`, `lumpsum/LUMPSUM/Lump Sum` → `Lumpsum`, `redemption/Redeem` → `Redemption`
- 4 rows dropped: `amount <= 0` (-500, 0, -100, 0)
- 2 rows dropped: unparseable date formats
- 2 rows dropped: invalid KYC values (`UNKNOWN`, `INVALID_STATUS`)

---

## 5. fact_performance

**Description:** Fact table storing return metrics and expense ratios for each fund scheme.  
**Source:** `scheme_performance_clean.csv`  
**Grain:** One row per fund per reporting period.

| Column | Data Type | Nullable | Business Definition | Example |
|--------|-----------|----------|---------------------|---------|
| `performance_id` | INTEGER | No | Auto-incremented surrogate primary key | `1` |
| `fund_id` | INTEGER | No | Foreign key referencing `dim_fund.fund_id` | `1` |
| `date_id` | INTEGER | No | Foreign key referencing `dim_date.date_id` | `5` |
| `return_1yr` | REAL | Yes | Annualised return over 1 year as percentage. NULL if unavailable or anomalous | `14.3` |
| `return_3yr` | REAL | Yes | Annualised return over 3 years as percentage. NULL if unavailable or anomalous | `9.8` |
| `return_5yr` | REAL | Yes | Annualised return over 5 years as percentage. NULL if unavailable or anomalous | `10.5` |
| `expense_ratio` | REAL | Yes | Annual fund management fee as % of AUM. Valid range: 0.1% – 2.5% | `1.20` |
| `return_1yr_anomaly` | INTEGER | Yes | 1 if return_1yr is outside -50% to 100% range, 0 otherwise | `0` |
| `return_3yr_anomaly` | INTEGER | Yes | 1 if return_3yr is outside -50% to 100% range, 0 otherwise | `0` |
| `return_5yr_anomaly` | INTEGER | Yes | 1 if return_5yr is outside -50% to 100% range, 0 otherwise | `0` |
| `expense_ratio_flag` | INTEGER | Yes | 1 if expense_ratio is outside 0.1%–2.5% range, 0 otherwise | `1` |

**Constraints:**
- `performance_id` → PRIMARY KEY
- `fund_id` → FOREIGN KEY → `dim_fund(fund_id)`
- `date_id` → FOREIGN KEY → `dim_date(date_id)`
- `expense_ratio` → CHECK `BETWEEN 0.1 AND 2.5`

**Cleaning Applied:**
- Non-numeric return values (`N/A`, `null`, `na`) → converted to NULL
- Anomaly `999.0` in `return_1yr` (Axis Midcap) → set to NULL, flagged
- 3 expense_ratio values flagged: `0.05` (too low), `3.50`, `2.80` (too high)

---

## 6. fact_aum

**Description:** Fact table storing Assets Under Management (AUM) for each fund per period.  
**Source:** To be populated from AMFI AUM reports.  
**Grain:** One row per fund per date.

| Column | Data Type | Nullable | Business Definition | Example |
|--------|-----------|----------|---------------------|---------|
| `aum_id` | INTEGER | No | Auto-incremented surrogate primary key | `1` |
| `fund_id` | INTEGER | No | Foreign key referencing `dim_fund.fund_id` | `4` |
| `date_id` | INTEGER | No | Foreign key referencing `dim_date.date_id` | `20` |
| `aum_crores` | REAL | No | Total assets under management in Indian Rupees Crores (₹ Cr). Must be > 0 | `12500.75` |
| `unit_holders` | INTEGER | Yes | Total number of active unit holders in the fund on that date | `85000` |

**Constraints:**
- `aum_id` → PRIMARY KEY
- `fund_id` → FOREIGN KEY → `dim_fund(fund_id)`
- `date_id` → FOREIGN KEY → `dim_date(date_id)`
- `aum_crores` → CHECK `aum_crores > 0`
- `(fund_id, date_id)` → UNIQUE

---

## 7. Staging Tables

Staging tables hold raw cleaned CSV data before transformation into the star schema.

| Staging Table | Maps To | Rows Loaded |
|---------------|---------|-------------|
| `fact_nav_staging` | `fact_nav` | 13,981 |
| `fact_transactions_staging` | `fact_transactions` | 12 |
| `fact_performance_staging` | `fact_performance` | 10 |

> **Note:** Staging tables do not enforce foreign keys. They are intermediate tables used for loading and validation before inserting into the final star schema tables.

---

## 8. Source Files

| File | Location | Rows | Description |
|------|----------|------|-------------|
| `nav_history.csv` | `data/raw/` | 14,224 | Raw NAV data downloaded from AMFI |
| `investor_transactions.csv` | `data/raw/` | 20 | Raw investor transaction records (sample) |
| `scheme_performance.csv` | `data/raw/` | 10 | Raw scheme performance data (sample) |
| `nav_history_clean.csv` | `data/processed/` | 13,981 | Cleaned NAV data after removing invalid rows |
| `investor_transactions_clean.csv` | `data/processed/` | 12 | Cleaned transactions after standardisation |
| `scheme_performance_clean.csv` | `data/processed/` | 10 | Cleaned performance data with anomaly flags |

---

## 🔗 Star Schema Relationships

```
dim_date ──────────────────────────────────────────┐
    │                                               │
    ├──► fact_nav          (fund_id, date_id)       │
    ├──► fact_transactions (fund_id, date_id)       │
    ├──► fact_performance  (fund_id, date_id)       │
    └──► fact_aum          (fund_id, date_id)       │
                                                    │
dim_fund ◄──────────────────────────────────────────┘
```

---

## 📌 Business Rules

| Rule | Description |
|------|-------------|
| NAV > 0 | A fund's NAV can never be zero or negative |
| Weekend NAV | Weekends and holidays carry forward the last trading day's NAV |
| Valid transaction types | Only `SIP`, `Lumpsum`, `Redemption` are accepted |
| Valid KYC status | Only `VERIFIED`, `PENDING`, `REJECTED` are accepted |
| Expense ratio range | Valid range is 0.1% to 2.5% per SEBI regulations |
| Return anomaly range | Returns outside -50% to 100% are flagged as anomalous |
| Amount > 0 | All transaction amounts must be positive |

---

*Last updated: June 2026*
