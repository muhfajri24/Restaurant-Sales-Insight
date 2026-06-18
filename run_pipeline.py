from src.restaurant_sales_pipeline import run_pipeline


if __name__ == "__main__":
    result = run_pipeline()
    print("Restaurant Sales Insight pipeline completed.")
    print(f"Rows: {result['rows']}")
    print(f"Total orders: {result['total_orders']}")
    print(f"Total revenue: {result['total_revenue']}")
    print(f"Cleaned data: {result['cleaned_path']}")
    print(f"KPI summary: {result['kpi_path']}")
    print(f"Figures: {result['figures_dir']}")
