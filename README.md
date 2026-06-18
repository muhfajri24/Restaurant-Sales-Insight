# Restaurant Sales Insight

This project turns raw restaurant sales data into KPI summaries, trend analysis, and dashboard-ready outputs using Python and SQL.

## What This Project Does

- Cleans and standardizes the raw restaurant sales dataset
- Creates analysis-ready fields such as revenue, calendar features, and product categories
- Exports cleaned data, KPI summaries, and reusable analysis figures
- Supports SQL analysis and Power BI dashboard storytelling

## Why It Matters

This project demonstrates the analytical foundation that supports data science work: cleaning transactional data, engineering reporting fields, measuring performance, and producing structured outputs for analysis and decision making.

## Data Science Focus

- Data cleaning and transformation for structured sales data
- Exploratory analysis and KPI generation
- SQL-based business analysis
- Reporting-ready datasets for downstream modeling or BI

## Primary Workflow

Python is the main way to run this project.

```bash
pip install -r requirements.txt
python run_pipeline.py
```

Main entrypoints:

- `run_pipeline.py` for the end-to-end export flow
- `src/restaurant_sales_pipeline.py` for reusable cleaning and reporting logic
- `sql/` for supporting KPI queries

## Optional Notebook

The notebook is included only as a secondary option for walkthroughs, recruiter demos, or quick testing.

- `notebook/restaurant_sales_insight.ipynb`

## Dataset

Source dataset: Kaggle `rohitgrewal/restaurant-sales-data`

Primary local raw file: `data/restaurant_sales_raw.csv`

## Tools

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- MySQL
- Power BI

## Project Structure

```text
Restaurant Sales Insight/
|-- dashboard/
|-- data/
|-- notebook/
|-- output/
|-- sql/
|-- src/
|   `-- restaurant_sales_pipeline.py
|-- run_pipeline.py
|-- requirements.txt
`-- README.md
```
