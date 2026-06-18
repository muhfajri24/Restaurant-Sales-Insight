# Restaurant Sales Insight

Restaurant Sales Insight is an end-to-end Data Analyst and Data Scientist portfolio project that analyzes restaurant sales data using SQL, Python, and Power BI. The goal is to transform raw transaction data into business insight around revenue performance, top-selling menu items, category contribution, demand trends, and actionable sales strategy.

## Problem Statement

Restaurant managers need a clear way to monitor sales performance and identify where revenue is coming from. This project answers practical business questions such as:

- How much total revenue did the restaurant generate?
- Which menu items drive the most revenue?
- Which product categories perform best?
- How does revenue move by day and month?
- What actions could improve sales performance and menu strategy?

## Dataset

- Source: Kaggle dataset `rohitgrewal/restaurant-sales-data`
- Raw file: [data/restaurant_sales_raw.csv](/d:/code/project%20portfolio/Restaurant%20Sales%20Insight/data/restaurant_sales_raw.csv)
- Cleaned file for analytics and Power BI: [output/restaurant_sales_cleaned.csv](/d:/code/project%20portfolio/Restaurant%20Sales%20Insight/output/restaurant_sales_cleaned.csv)
- Rows: `254`
- Columns after cleaning: `18`
- Date range: `2022-11-07` to `2022-12-29`

## Tools

- SQL: MySQL
- Python: pandas, numpy, matplotlib, seaborn, mysql-connector-python
- BI: Power BI
- Notebook: Jupyter

## Project Structure

```text
restaurant-sales-insight/
|-- data/
|-- sql/
|-- notebook/
|-- dashboard/
|-- output/
|-- README.md
`-- requirements.txt
```

## Workflow

1. Load the restaurant sales CSV dataset.
2. Clean and standardize the raw data in Python.
3. Create an analysis-ready dataset with derived columns such as `revenue`, `month_name`, and `product_category`.
4. Build the MySQL database and table schema.
5. Run SQL queries for KPI and trend analysis.
6. Export the cleaned dataset for Power BI.
7. Build the dashboard using the Power BI guide in [dashboard/powerbi_dashboard_guide.md](/d:/code/project%20portfolio/Restaurant%20Sales%20Insight/dashboard/powerbi_dashboard_guide.md).

## Data Cleaning Highlights

- Standardized column names into snake_case
- Parsed `Date` into a proper date field
- Removed duplicate `order_id` records
- Converted numeric columns into analysis-ready types
- Derived `revenue = price * quantity`
- Added `day_name`, `month_name`, `week_num`, and `is_weekend`
- Grouped products into portfolio-friendly categories:
  - `Main Course`
  - `Sides`
  - `Beverage`

## SQL Analysis

SQL scripts are available in:

- [sql/01_create_database.sql](/d:/code/project%20portfolio/Restaurant%20Sales%20Insight/sql/01_create_database.sql)
- [sql/02_analysis_queries.sql](/d:/code/project%20portfolio/Restaurant%20Sales%20Insight/sql/02_analysis_queries.sql)
- [output/kpi_summary.csv](/d:/code/project%20portfolio/Restaurant%20Sales%20Insight/output/kpi_summary.csv)

Key analysis covered:

- Total revenue
- Total orders
- Top selling menu
- Sales by category
- Sales by day
- Sales by month
- Average order value
- Optional branch and purchase-type breakdowns

Note: the source dataset does not contain transaction timestamps, so a true `sales by hour` analysis is not available without richer POS data. A placeholder query is included in the SQL file to show how the analysis should be written once an hourly timestamp is available.

## Dashboard Preview

Dashboard design guidance is provided in [dashboard/powerbi_dashboard_guide.md](/d:/code/project%20portfolio/Restaurant%20Sales%20Insight/dashboard/powerbi_dashboard_guide.md).

![Restaurant Sales Dashboard Preview](/d:/code/project%20portfolio/Restaurant%20Sales%20Insight/dashboard/restaurant_sales_dashboard_preview.png)

Suggested visuals:

- KPI Cards: Total Revenue, Total Orders, Average Order Value
- Revenue trend line chart
- Top menu bar chart
- Category sales donut chart
- Sales by day chart
- Filters for date, category, city, and purchase type

## Key Insights

- Total revenue reached `769,515.89`.
- Total distinct orders reached `254`.
- Average order value was `3,029.59`.
- `Burgers` was the top-selling menu item by revenue with `376,999.85`.
- `Main Course` was the strongest category with `491,641.52` in revenue.
- November revenue reached `332,114.70`.
- December revenue increased to `437,401.19`.
- `Wednesday` delivered the highest weekday revenue contribution.
- `Lisbon` recorded the highest city-level revenue in this dataset.

## Business Recommendations

- Protect and expand the burger lineup because it is the main revenue engine.
- Increase beverage attachment rate through combo meals and upsell prompts at checkout.
- Prioritize campaigns in December or around year-end periods when demand is stronger.
- Use city-level performance to allocate promotions and staffing more effectively.
- Add transaction timestamp data in the POS pipeline so the business can analyze peak hours and staffing demand.

## How To Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Download the Kaggle dataset

```python
import kagglehub

path = kagglehub.dataset_download("rohitgrewal/restaurant-sales-data")
print("Path to dataset files:", path)
```

### 3. Open the notebook

Run [notebook/restaurant_sales_insight.ipynb](/d:/code/project%20portfolio/Restaurant%20Sales%20Insight/notebook/restaurant_sales_insight.ipynb) to:

- clean the raw data
- generate exploratory analysis
- export the cleaned CSV to `output/restaurant_sales_cleaned.csv`

### 4. Load data into MySQL

Run [sql/01_create_database.sql](/d:/code/project%20portfolio/Restaurant%20Sales%20Insight/sql/01_create_database.sql) and then [sql/02_analysis_queries.sql](/d:/code/project%20portfolio/Restaurant%20Sales%20Insight/sql/02_analysis_queries.sql).

### 5. Build the Power BI dashboard

Import the cleaned CSV and follow the design notes in [dashboard/powerbi_dashboard_guide.md](/d:/code/project%20portfolio/Restaurant%20Sales%20Insight/dashboard/powerbi_dashboard_guide.md).

## Portfolio Notes

- This project is intentionally structured for GitHub presentation and recruiter review.
- It demonstrates SQL analysis, Python data preparation, exploratory data analysis, and BI storytelling in one repository.
- The source data has no hourly timestamp, so hourly demand analysis should be treated as a recommended future enhancement rather than a completed finding.
