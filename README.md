# IBM HR Attrition Dataset Analysis

![Python](https://img.shields.io/badge/Python-3.12-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-database-336791)
![Power BI](https://img.shields.io/badge/Power%20BI-dashboard-F2C811)
![License](https://img.shields.io/badge/license-MIT-green)

A full data pipeline built around the [IBM HR Analytics Employee Attrition Dataset](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset): raw data ingested and cleaned in PostgreSQL, audited in Excel, visualized in Power BI, and cross-validated with a set of matching Python visualizations.

**Blog writeup:** [IBM HR Attrition: The Long Way Around](https://medium.com/@vanshkhetarpal/ibm-employees-attrition-relationship-8da664de8ae6)

## Overview

This project explores employee attrition (voluntary departures without replacement) using IBM's well-known HR analytics sample dataset. The pipeline moves through four stages:

1. **Ingestion & Cleaning (PostgreSQL)** - raw CSV loaded into a staging table, cleaned into a production table via SQL
2. **Reconciliation (Excel)** - XLOOKUP-based audit comparing raw vs. cleaned data to confirm zero data loss
3. **Dashboard (Power BI)** - a one-page executive dashboard covering attrition by department, overtime, tenure, gender, and job role
4. **Cross-validation (Python)** - the same core visuals rebuilt independently in pandas/matplotlib/seaborn/squarify, to confirm the dashboard's numbers hold up outside of Power BI

## Key Finding

Employees who work overtime leave at roughly **3x the rate** of those who don't (30.5% vs. 10.4%), the strongest single driver of attrition in this dataset. This result was confirmed independently in both Power BI and Python.

## Repo Structure

```
.
├── data/                       # Raw and cleaned CSV files
├── excel/                      # Excel reconciliation workbook (XLOOKUP audit)
├── images/                     # Exported Python chart images
├── powerbi/                    # Power BI dashboard (.pbix)
├── hr-attrition-analytics.ipynb  # Python EDA / cross-validation notebook
├── main.py                     # SQL ingestion + cleaning script
├── docker-compose.yaml         # Postgres service for local development
├── pyproject.toml              # Project dependencies (uv)
└── uv.lock                     # Locked dependency versions
```

## Pipeline Details

### 1. Ingestion & Cleaning (`main.py`)

- Raw CSV loaded into Postgres as an immutable `hr_raw` staging table
- Column names normalized to lowercase in Python to avoid Postgres identifier case-sensitivity issues
- Cleaned into a `hr_clean` production table via `CREATE TABLE ... AS SELECT`:
  - Filtered rows with a null `employeenumber`
  - Dropped zero-variance columns (`employeecount`, `over18`, `standardhours`)
  - Deduplicated on `employeenumber`
  - Added a primary key constraint on `employeenumber`
- Exported the cleaned table back to CSV for the Excel audit

### 2. Reconciliation (`excel/`)

Three-sheet workbook (`Raw_CSV`, `SQL_Clean`, `Audit_Reconciliation`) using `XLOOKUP` on `employeenumber` to confirm no data loss or corruption between the raw CSV and the cleaned SQL output.

### 3. Dashboard (`powerbi/`)

A single-page dashboard with:
- KPI cards: total headcount, average tenure, attrition count, attrition rate
- Attrition by gender, department, overtime, tenure, and job role
- Interactive slicers for age group, education, and marital status
- DAX measures isolated in a dedicated `Measure Table` table

### 4. Cross-validation (`hr-attrition-analytics.ipynb`)

Rebuilds the five core Power BI visuals in Python:
- Attrition by gender (pie chart)
- Attrition by department (bar chart)
- Attrition by overtime (bar chart)
- Attrition by tenure (line chart)
- Attrition by job role (treemap, via `squarify`)

All numbers matched the Power BI dashboard exactly.

## Setup

```bash
# clone the repo
git clone https://github.com/Varsedile/ibm-attrition-dataset-analysis.git
cd ibm-attrition-dataset-analysis

# start Postgres
docker compose up -d

# install dependencies (uv)
uv sync

# run the cleaning pipeline
uv run main.py
```

Then open `hr-attrition-analytics.ipynb` in Jupyter to run the Python visualizations, or open the `.pbix` file in `powerbi/` with Power BI Desktop.

## Dataset

[IBM HR Analytics Employee Attrition Dataset](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset), originally distributed as a fictional sample dataset created by IBM data scientists.

## Tools Used

PostgreSQL, SQLAlchemy, Pandas, Excel, Power BI (DAX), Python (matplotlib, seaborn, squarify)
