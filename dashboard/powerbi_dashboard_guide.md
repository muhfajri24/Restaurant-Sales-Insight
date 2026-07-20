# Power BI Dashboard Guide

## 1. Recommended Pages

### Executive Overview
- KPI Card: `Total Revenue`
- KPI Card: `Total Sales Records`
- KPI Card: `Weighted Selling Price`
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

Import `output/restaurant_sales_cleaned.csv` into Power BI.

## 3. Recommended Measures

```DAX
Total Revenue = SUM(restaurant_sales_cleaned[revenue])

Total Sales Records = DISTINCTCOUNT(restaurant_sales_cleaned[record_id])

Weighted Selling Price = DIVIDE([Total Revenue], SUM(restaurant_sales_cleaned[quantity]))

Total Quantity = SUM(restaurant_sales_cleaned[quantity])
```

## 4. Suggested Visual Mapping

- KPI Cards:
  - `Total Revenue`
  - `Total Sales Records`
  - `Weighted Selling Price`
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
- Format monetary values as generic decimal measures unless the source currency is verified.
- Add dynamic titles such as `Revenue Trend by Selected Period`.
- Keep the overview page focused on 5-6 visuals maximum.

## 6. Suggested Dashboard Narrative

- Report the observed revenue share for `Main Course` and `Burgers` without implying profitability.
- Label both November and December as partial periods before showing them together.
- Describe weekday results as recorded patterns, not evidence of causal demand drivers.
- Use city views to separate recorded quantity from weighted selling price and frame follow-up hypotheses.
