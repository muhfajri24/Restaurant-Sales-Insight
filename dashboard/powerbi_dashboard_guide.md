# Power BI Dashboard Guide

## 1. Recommended Pages

### Executive Overview
- KPI Card: `Total Revenue`
- KPI Card: `Total Orders`
- KPI Card: `Average Order Value`
- Line chart: `Revenue Trend by Date`
- Bar chart: `Top Selling Menu by Revenue`
- Donut chart: `Sales by Category`

### Sales Pattern
- Column chart: `Sales by Day Name`
- Column chart: `Sales by Month`
- Slicer: `Date`
- Slicer: `Product Category`
- Slicer: `City`

## 2. Data Source

Import [restaurant_sales_cleaned.csv](/d:/code/project%20portfolio/Restaurant%20Sales%20Insight/output/restaurant_sales_cleaned.csv) into Power BI.

## 3. Recommended Measures

```DAX
Total Revenue = SUM(restaurant_sales_cleaned[revenue])

Total Orders = DISTINCTCOUNT(restaurant_sales_cleaned[order_id])

Average Order Value = DIVIDE([Total Revenue], [Total Orders])

Total Quantity = SUM(restaurant_sales_cleaned[quantity])
```

## 4. Suggested Visual Mapping

- KPI Cards:
  - `Total Revenue`
  - `Total Orders`
  - `Average Order Value`
- Revenue trend chart:
  - Axis: `date`
  - Values: `Total Revenue`
- Top menu bar chart:
  - Axis: `product`
  - Values: `Total Revenue`
  - Sort descending by `Total Revenue`
- Category sales pie/donut chart:
  - Legend: `product_category`
  - Values: `Total Revenue`
- Sales by hour chart:
  - Not available in the source dataset because no transaction timestamp exists
  - If a future POS dataset contains `order_timestamp`, use `HOUR(order_timestamp)` as the axis
- Filters:
  - `date`
  - `product_category`
  - `city`
  - `purchase_type`
  - `payment_method`

## 5. Styling Tips

- Use a light background with 1 accent color for revenue visuals and 1 accent color for category visuals.
- Format `Total Revenue` as currency.
- Add dynamic titles such as `Revenue Trend by Selected Period`.
- Keep the overview page focused on 5-6 visuals maximum.

## 6. Suggested Dashboard Narrative

- Revenue is concentrated in `Main Course`, especially `Burgers`.
- December outperformed November, indicating stronger year-end demand.
- Midweek days contributed the highest revenue, especially Wednesday.
- City-level analysis highlights which branch or market should receive stronger promotional focus.
