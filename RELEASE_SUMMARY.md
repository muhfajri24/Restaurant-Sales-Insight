# Release Summary

## Title

Restaurant Sales Insight: portfolio-ready analytics project setup

## Summary

This update packages the `Restaurant Sales Insight` repository into a cleaner, recruiter-friendly analytics portfolio project. It includes the complete project structure, cleaned dataset output, SQL scripts, Python notebook, Power BI guidance, and improved documentation for GitHub presentation.

## What Changed

- Added a professional `.gitignore` for Python, Jupyter, and local development files
- Improved `README.md` with stronger project framing for recruiters
- Highlighted project scope, deliverables, and recruiter takeaways
- Updated run instructions to prefer `python -m pip install -r requirements.txt`
- Preserved links to dataset, notebook, SQL scripts, and dashboard assets

## Included Artifacts

- Raw dataset in `data/restaurant_sales_raw.csv`
- Cleaned reporting dataset in `output/restaurant_sales_cleaned.csv`
- KPI export in `output/kpi_summary.csv`
- SQL schema and analysis queries in `sql/`
- Analysis notebook in `notebook/restaurant_sales_insight.ipynb`
- Power BI dashboard guide and dashboard preview image in `dashboard/`

## Key Business Findings

- Total revenue: `769,515.89`
- Total sales records: `254`
- Total orders and average order value: not supported by the verified aggregated product-record grain
- Top product by revenue: `Burgers`
- Top category by revenue: `Main Course`
- City with the highest recorded revenue: `Lisbon`
- November and December are both partial periods, so direct full-month growth is not claimed

## Notes

- The source dataset does not include an hourly timestamp, so `sales by hour` is documented as a future enhancement rather than a completed analysis.
- This repository is intended for portfolio presentation and interview discussion.

## Suggested PR Description

### What changed

This PR adds portfolio polish to the `Restaurant Sales Insight` repository by introducing a `.gitignore`, improving the README for recruiter-facing presentation, and adding a reusable release summary.

### Why it changed

The project already contained the core analysis assets, but the repository needed stronger GitHub presentation, cleaner development defaults, and a ready-made summary for publishing and sharing.

### Impact

- Easier for recruiters and reviewers to understand the project quickly
- Better repository hygiene for future local work
- Ready-to-use summary text for PRs, releases, or LinkedIn/GitHub sharing
