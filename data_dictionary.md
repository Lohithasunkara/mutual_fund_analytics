# 📘 Data Dictionary — Mutual Fund Analytics Project

> \*\*Project:\*\* Mutual Fund Analytics Pipeline  
> \*\*Author:\*\* Lohitha Sunkara  
> \*\*Created:\*\* June 2026  
> \*\*Database:\*\* `mutual\_funds.db` (SQLite)  
> \*\*Source:\*\* AMFI India (https://www.amfiindia.com)

\---

## 📑 Table of Contents

1. [dim\_fund](#1-dim_fund)
2. [dim\_date](#2-dim_date)
3. [fact\_nav](#3-fact_nav)
4. [fact\_transactions](#4-fact_transactions)
5. [fact\_performance](#5-fact_performance)
6. [fact\_aum](#6-fact_aum)
7. [Staging Tables](#7-staging-tables)
8. [Source Files](#8-source-files)

\---

## 1\. dim\_fund

**Description:** Master dimension table storing details of all mutual fund schemes.  
**Source:** `nav\_history\_clean.csv`, `scheme\_performance\_clean.csv`  
**Grain:** One row per unique mutual fund scheme.

|Column|Data Type|Nullable|Business Definition|Example|
|-|-|-|-|-|
|`fund\_id`|INTEGER|No|Auto-incremented surrogate primary key|`1`|
|`amfi\_code`|INTEGER|No|Unique scheme code assigned by AMFI (Association of Mutual Funds in India)|`119551`|
|`scheme\_name`|TEXT|No|Full official name of the mutual fund scheme|`SBI Bluechip Fund`|
|`category`|TEXT|Yes|SEBI-defined fund category|`Large Cap`, `Mid Cap`, `Index`|
|`expense\_ratio`|REAL|Yes|Annual fee charged by the fund as % of AUM. Valid range: 0.1% – 2.5%|`1.20`|
|`kyc\_required`|TEXT|Yes|Whether KYC is mandatory for investing. Default: YES|`YES`|

**Constraints:**

* `fund\_id` → PRIMARY KEY
* `amfi\_code` → UNIQUE

\---

## 2\. dim\_date

**Description:** Calendar dimension table used to support time-based analysis across all fact tables.  
**Source:** Generated programmatically from NAV date range.  
**Grain:** One row per calendar date.

|Column|Data Type|Nullable|Business Definition|Example|
|-|-|-|-|-|
|`date\_id`|INTEGER|No|Auto-incremented surrogate primary key|`1`|
|`full\_date`|TEXT|No|Full calendar date in YYYY-MM-DD format|`2026-06-23`|
|`day`|INTEGER|Yes|Day of the month (1–31)|`23`|
|`month`|INTEGER|Yes|Month of the year (1–12)|`6`|
|`year`|INTEGER|Yes|Four-digit calendar year|`2026`|
|`quarter`|INTEGER|Yes|Quarter of the year (1–4)|`2`|
|`is\_weekend`|INTEGER|Yes|1 if Saturday or Sunday, 0 otherwise|`0`|
|`is\_holiday`|INTEGER|Yes|1 if a market holiday, 0 otherwise|`0`|

**Constraints:**

* `date\_id` → PRIMARY KEY
* `full\_date` → UNIQUE

\---

## 3\. fact\_nav

**Description:** Fact table storing daily Net Asset Value (NAV) for each mutual fund scheme.  
**Source:** `nav\_history\_clean.csv` → downloaded from AMFI NAVAll.txt  
**Grain:** One row per fund per date.

|Column|Data Type|Nullable|Business Definition|Example|
|-|-|-|-|-|
|`nav\_id`|INTEGER|No|Auto-incremented surrogate primary key|`1`|
|`fund\_id`|INTEGER|No|Foreign key referencing `dim\_fund.fund\_id`|`3`|
|`date\_id`|INTEGER|No|Foreign key referencing `dim\_date.date\_id`|`15`|
|`nav`|REAL|No|Net Asset Value per unit of the fund on that date. Must be > 0. Weekends/holidays forward-filled from last trading day|`106.04`|

**Constraints:**

* `nav\_id` → PRIMARY KEY
* `fund\_id` → FOREIGN KEY → `dim\_fund(fund\_id)`
* `date\_id` → FOREIGN KEY → `dim\_date(date\_id)`
* `nav` → CHECK `nav > 0`
* `(fund\_id, date\_id)` → UNIQUE

**Cleaning Applied:**

* Non-positive NAV values dropped (243 rows removed)
* Missing dates (weekends/holidays) forward-filled using last known NAV
* Duplicates removed on `(amfi\_code, date)`

\---

## 4\. fact\_transactions

**Description:** Fact table recording all investor-level mutual fund transactions.  
**Source:** `investor\_transactions\_clean.csv`  
**Grain:** One row per transaction.

|Column|Data Type|Nullable|Business Definition|Example|
|-|-|-|-|-|
|`transaction\_id`|INTEGER|No|Auto-incremented surrogate primary key|`1`|
|`fund\_id`|INTEGER|No|Foreign key referencing `dim\_fund.fund\_id`|`2`|
|`date\_id`|INTEGER|No|Foreign key referencing `dim\_date.date\_id`|`10`|
|`investor\_id`|TEXT|No|Unique identifier for the investor|`INV001`|
|`transaction\_type`|TEXT|No|Type of transaction. Standardised values only|`SIP`, `Lumpsum`, `Redemption`|
|`amount`|REAL|No|Transaction amount in Indian Rupees (₹). Must be > 0|`5000.00`|
|`kyc\_status`|TEXT|No|KYC verification status of the investor at time of transaction|`VERIFIED`, `PENDING`, `REJECTED`|

**Constraints:**

* `transaction\_id` → PRIMARY KEY
* `fund\_id` → FOREIGN KEY → `dim\_fund(fund\_id)`
* `date\_id` → FOREIGN KEY → `dim\_date(date\_id)`
* `transaction\_type` → CHECK IN `('SIP', 'Lumpsum', 'Redemption')`
* `amount` → CHECK `amount > 0`
* `kyc\_status` → CHECK IN `('VERIFIED', 'PENDING', 'REJECTED')`

**Cleaning Applied:**

* `transaction\_type` standardised: `sip/Sip` → `SIP`, `lumpsum/LUMPSUM/Lump Sum` → `Lumpsum`, `redemption/Redeem` → `Redemption`
* 4 rows dropped: `amount <= 0` (-500, 0, -100, 0)
* 2 rows dropped: unparseable date formats
* 2 rows dropped: invalid KYC values (`UNKNOWN`, `INVALID\_STATUS`)

\---

## 5\. fact\_performance

**Description:** Fact table storing return metrics and expense ratios for each fund scheme.  
**Source:** `scheme\_performance\_clean.csv`  
**Grain:** One row per fund per reporting period.

|Column|Data Type|Nullable|Business Definition|Example|
|-|-|-|-|-|
|`performance\_id`|INTEGER|No|Auto-incremented surrogate primary key|`1`|
|`fund\_id`|INTEGER|No|Foreign key referencing `dim\_fund.fund\_id`|`1`|
|`date\_id`|INTEGER|No|Foreign key referencing `dim\_date.date\_id`|`5`|
|`return\_1yr`|REAL|Yes|Annualised return over 1 year as percentage. NULL if unavailable or anomalous|`14.3`|
|`return\_3yr`|REAL|Yes|Annualised return over 3 years as percentage. NULL if unavailable or anomalous|`9.8`|
|`return\_5yr`|REAL|Yes|Annualised return over 5 years as percentage. NULL if unavailable or anomalous|`10.5`|
|`expense\_ratio`|REAL|Yes|Annual fund management fee as % of AUM. Valid range: 0.1% – 2.5%|`1.20`|
|`return\_1yr\_anomaly`|INTEGER|Yes|1 if return\_1yr is outside -50% to 100% range, 0 otherwise|`0`|
|`return\_3yr\_anomaly`|INTEGER|Yes|1 if return\_3yr is outside -50% to 100% range, 0 otherwise|`0`|
|`return\_5yr\_anomaly`|INTEGER|Yes|1 if return\_5yr is outside -50% to 100% range, 0 otherwise|`0`|
|`expense\_ratio\_flag`|INTEGER|Yes|1 if expense\_ratio is outside 0.1%–2.5% range, 0 otherwise|`1`|

**Constraints:**

* `performance\_id` → PRIMARY KEY
* `fund\_id` → FOREIGN KEY → `dim\_fund(fund\_id)`
* `date\_id` → FOREIGN KEY → `dim\_date(date\_id)`
* `expense\_ratio` → CHECK `BETWEEN 0.1 AND 2.5`

**Cleaning Applied:**

* Non-numeric return values (`N/A`, `null`, `na`) → converted to NULL
* Anomaly `999.0` in `return\_1yr` (Axis Midcap) → set to NULL, flagged
* 3 expense\_ratio values flagged: `0.05` (too low), `3.50`, `2.80` (too high)

\---

## 6\. fact\_aum

**Description:** Fact table storing Assets Under Management (AUM) for each fund per period.  
**Source:** To be populated from AMFI AUM reports.  
**Grain:** One row per fund per date.

|Column|Data Type|Nullable|Business Definition|Example|
|-|-|-|-|-|
|`aum\_id`|INTEGER|No|Auto-incremented surrogate primary key|`1`|
|`fund\_id`|INTEGER|No|Foreign key referencing `dim\_fund.fund\_id`|`4`|
|`date\_id`|INTEGER|No|Foreign key referencing `dim\_date.date\_id`|`20`|
|`aum\_crores`|REAL|No|Total assets under management in Indian Rupees Crores (₹ Cr). Must be > 0|`12500.75`|
|`unit\_holders`|INTEGER|Yes|Total number of active unit holders in the fund on that date|`85000`|

**Constraints:**

* `aum\_id` → PRIMARY KEY
* `fund\_id` → FOREIGN KEY → `dim\_fund(fund\_id)`
* `date\_id` → FOREIGN KEY → `dim\_date(date\_id)`
* `aum\_crores` → CHECK `aum\_crores > 0`
* `(fund\_id, date\_id)` → UNIQUE

\---

## 7\. Staging Tables

Staging tables hold raw cleaned CSV data before transformation into the star schema.

|Staging Table|Maps To|Rows Loaded|
|-|-|-|
|`fact\_nav\_staging`|`fact\_nav`|13,981|
|`fact\_transactions\_staging`|`fact\_transactions`|12|
|`fact\_performance\_staging`|`fact\_performance`|10|

> \*\*Note:\*\* Staging tables do not enforce foreign keys. They are intermediate tables used for loading and validation before inserting into the final star schema tables.

\---

## 8\. Source Files

|File|Location|Rows|Description|
|-|-|-|-|
|`nav\_history.csv`|`data/raw/`|14,224|Raw NAV data downloaded from AMFI|
|`investor\_transactions.csv`|`data/raw/`|20|Raw investor transaction records (sample)|
|`scheme\_performance.csv`|`data/raw/`|10|Raw scheme performance data (sample)|
|`nav\_history\_clean.csv`|`data/processed/`|13,981|Cleaned NAV data after removing invalid rows|
|`investor\_transactions\_clean.csv`|`data/processed/`|12|Cleaned transactions after standardisation|
|`scheme\_performance\_clean.csv`|`data/processed/`|10|Cleaned performance data with anomaly flags|

\---

## 🔗 Star Schema Relationships

```
dim\_date ──────────────────────────────────────────┐
    │                                               │
    ├──► fact\_nav          (fund\_id, date\_id)       │
    ├──► fact\_transactions (fund\_id, date\_id)       │
    ├──► fact\_performance  (fund\_id, date\_id)       │
    └──► fact\_aum          (fund\_id, date\_id)       │
                                                    │
dim\_fund ◄──────────────────────────────────────────┘
```

\---

## 📌 Business Rules

|Rule|Description|
|-|-|
|NAV > 0|A fund's NAV can never be zero or negative|
|Weekend NAV|Weekends and holidays carry forward the last trading day's NAV|
|Valid transaction types|Only `SIP`, `Lumpsum`, `Redemption` are accepted|
|Valid KYC status|Only `VERIFIED`, `PENDING`, `REJECTED` are accepted|
|Expense ratio range|Valid range is 0.1% to 2.5% per SEBI regulations|
|Return anomaly range|Returns outside -50% to 100% are flagged as anomalous|
|Amount > 0|All transaction amounts must be positive|

\---

*Last updated: June 2026*

