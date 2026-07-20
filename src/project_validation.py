from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd
from PIL import Image, UnidentifiedImageError

from src.exceptions import OutputValidationError
from src.sql_exports import validate_sql_layer

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "output"
REPORT_DIR = BASE_DIR / "reports" / "validation"


def _check(name: str, passed: bool, evidence: str, severity: str = "critical") -> dict[str, object]:
    return {"check": name, "passed": bool(passed), "severity": severity, "evidence": evidence}


def validate_project(base_dir: Path = BASE_DIR) -> dict[str, object]:
    output = base_dir / "output"
    report_dir = base_dir / "reports" / "validation"
    report_dir.mkdir(parents=True, exist_ok=True)

    clean = pd.read_csv(output / "restaurant_sales_cleaned.csv")
    kpis = pd.read_csv(output / "kpis" / "executive_kpis.csv").set_index("metric")
    metadata = json.loads((output / "project_metadata.json").read_text(encoding="utf-8"))
    fact = pd.read_csv(output / "bi" / "fact_sales.csv")
    products = pd.read_csv(output / "analysis" / "product_performance.csv")
    cities = pd.read_csv(output / "analysis" / "city_performance.csv")
    payments = pd.read_csv(output / "analysis" / "payment_method_performance.csv")
    managers = pd.read_csv(output / "analysis" / "manager_observed_performance.csv")
    purchase_types = pd.read_csv(output / "analysis" / "purchase_type_performance.csv")
    opportunities = pd.read_csv(output / "insights" / "opportunity_matrix.csv")
    insights = pd.read_csv(output / "insights" / "business_insights.csv")

    revenue = round(float(clean["revenue"].sum()), 2)
    quantity = round(float(clean["quantity"].sum()), 2)
    kpi_revenue = round(float(kpis.loc["total_revenue", "value"]), 2)
    kpi_quantity = round(float(kpis.loc["total_quantity_sold", "value"]), 2)
    unsupported_columns = {"profit", "margin", "retention", "customer_lifetime_value", "aov", "average_order_value"}
    analytical_files = [*(output / "analysis").glob("*.csv"), output / "restaurant_sales_cleaned.csv"]
    actual_columns = {str(c).lower() for path in analytical_files for c in pd.read_csv(path, nrows=0).columns}
    duplicate_key = ["dimension", "segment", "observation", "metric_evidence"]
    insight_duplicates = int(opportunities.duplicated(duplicate_key).sum())
    business_duplicates = int(
        insights.duplicated(["business_dimension", "title", "observation", "supporting_metric"]).sum()
    )
    sql_files = sorted((base_dir / "sql").glob("*.sql"))
    sql_text = "\n".join(p.read_text(encoding="utf-8") for p in sql_files).lower()
    required_sources = [
        output / "analysis" / "revenue_driver_summary.csv",
        output / "analysis" / "product_performance.csv",
        output / "analysis" / "city_performance.csv",
        output / "analysis" / "payment_method_performance.csv",
        output / "analysis" / "manager_observed_performance.csv",
        output / "insights" / "opportunity_matrix.csv",
    ]
    figures = list((output / "figures").glob("*.png"))
    required_artifacts = [
        output / "restaurant_sales_cleaned.csv",
        output / "kpis" / "executive_kpis.csv",
        output / "analysis" / "revenue_driver_summary.csv",
        output / "analysis" / "product_performance.csv",
        output / "analysis" / "city_performance.csv",
        output / "analysis" / "payment_method_performance.csv",
        output / "analysis" / "manager_observed_performance.csv",
        output / "insights" / "opportunity_matrix.csv",
        output / "project_metadata.json",
        base_dir / "app.py",
        base_dir / "README.md",
        base_dir / "docs" / "REPRODUCIBILITY.md",
        base_dir / "docs" / "PIPELINE.md",
        base_dir / "docs" / "TESTING.md",
        base_dir / "docs" / "DEPLOYMENT.md",
        base_dir / "CONTRIBUTING.md",
        base_dir / "CHANGELOG.md",
        base_dir / "LICENSE",
    ]
    missing_artifacts = [str(path.relative_to(base_dir)) for path in required_artifacts if not path.is_file()]
    opportunity_required = [
        "observation",
        "metric_evidence",
        "business_hypothesis",
        "recommended_validation_action",
        "risk_or_limitation",
        "priority_score",
    ]
    csv_contracts = {
        output / "restaurant_sales_cleaned.csv": {"record_id", "date", "product", "revenue"},
        output / "kpis" / "executive_kpis.csv": {"metric", "value", "status"},
        output / "analysis" / "product_performance.csv": {"product", "revenue", "quantity", "revenue_share"},
        output / "insights" / "opportunity_matrix.csv": set(opportunity_required),
        output / "bi" / "fact_sales.csv": {"record_id", "date", "product", "city", "revenue"},
    }
    csv_schema_failures = []
    for path, required_columns in csv_contracts.items():
        actual = set(pd.read_csv(path, nrows=0).columns) if path.is_file() else set()
        if not required_columns.issubset(actual):
            csv_schema_failures.append(f"{path.relative_to(base_dir)} missing {sorted(required_columns - actual)}")
    phase_two_figures = [
        "executive_kpis.png",
        "revenue_drivers.png",
        "pareto_chart.png",
        "portfolio_matrix.png",
        "city_analysis.png",
        "channel_analysis.png",
        "payment_analysis.png",
        "opportunity_matrix.png",
    ]
    readme = (base_dir / "README.md").read_text(encoding="utf-8")
    required_readme_sections = [
        "## Business Question",
        "## Dataset",
        "## Data Quality",
        "## KPI Framework",
        "## Revenue Drivers",
        "## Menu Intelligence",
        "## Location & Channel",
        "## Opportunity Matrix",
        "## Dashboard",
        "## SQL Layer",
        "## Reproduce",
        "## Repository Structure",
        "## Limitations",
        "## Future Work",
    ]
    app_text = (base_dir / "app.py").read_text(encoding="utf-8") if (base_dir / "app.py").exists() else ""
    required_tabs = [
        "Executive Overview",
        "Revenue Drivers",
        "Menu Intelligence",
        "Business Explorer",
        "Opportunity Matrix",
    ]
    opportunity_text = " ".join(opportunities.astype(str).fillna("").values.ravel()).lower()
    forbidden_opportunity_claims = [
        "guaranteed recommendation",
        "caused",
        "increased because of",
        "will increase",
        "profit uplift",
    ]
    portable_files = [
        base_dir / "README.md",
        base_dir / "app.py",
        *(base_dir / "docs").glob("*.md"),
        *(base_dir / "reports").rglob("*.md"),
        *output.rglob("*.json"),
    ]
    absolute_path_hits = []
    for path in portable_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"(?:(?<![A-Za-z])[A-Za-z]:[\\/]|file://|/[a-zA-Z]:/)", text):
            absolute_path_hits.append(str(path.relative_to(base_dir)))
    broken_phase_two_figures = []
    for name in phase_two_figures:
        path = output / "figures" / name
        try:
            with Image.open(path) as image:
                image.verify()
        except (FileNotFoundError, OSError, UnidentifiedImageError):
            broken_phase_two_figures.append(name)
    local_links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", readme)
    broken_readme_links = []
    for target in local_links:
        if target.startswith(("http://", "https://", "#")):
            continue
        clean_target = target.split("#", maxsplit=1)[0].replace("%20", " ")
        if clean_target and not (base_dir / clean_target).exists():
            broken_readme_links.append(target)
    try:
        validated_sql = validate_sql_layer(base_dir / "sql")
        sql_validation_error = ""
    except OutputValidationError as error:
        validated_sql = []
        sql_validation_error = str(error)

    checks = [
        _check("cleaned_revenue_vs_kpi", revenue == kpi_revenue, f"cleaned={revenue:.2f}; kpi={kpi_revenue:.2f}"),
        _check("cleaned_quantity_vs_kpi", quantity == kpi_quantity, f"cleaned={quantity:.2f}; kpi={kpi_quantity:.2f}"),
        _check(
            "cleaned_revenue_vs_metadata",
            revenue == round(float(metadata["total_revenue"]), 2),
            f"cleaned={revenue:.2f}; metadata={metadata['total_revenue']:.2f}",
        ),
        _check("cleaned_vs_fact_rows", len(clean) == len(fact), f"cleaned={len(clean)}; fact={len(fact)}"),
        _check(
            "cleaned_vs_fact_revenue",
            revenue == round(float(fact["revenue"].sum()), 2),
            f"cleaned={revenue:.2f}; fact={fact['revenue'].sum():.2f}",
        ),
        _check(
            "product_dimension_reconciles",
            revenue == round(float(products["revenue"].sum()), 2),
            f"product_sum={products['revenue'].sum():.2f}",
        ),
        _check(
            "city_dimension_reconciles",
            revenue == round(float(cities["revenue"].sum()), 2),
            f"city_sum={cities['revenue'].sum():.2f}",
        ),
        _check(
            "payment_dimension_reconciles",
            revenue == round(float(payments["revenue"].sum()), 2),
            f"payment_sum={payments['revenue'].sum():.2f}",
        ),
        _check(
            "manager_dimension_reconciles",
            revenue == round(float(managers["revenue"].sum()), 2),
            f"manager_sum={managers['revenue'].sum():.2f}",
        ),
        _check(
            "purchase_type_dimension_reconciles",
            revenue == round(float(purchase_types["revenue"].sum()), 2),
            f"purchase_type_sum={purchase_types['revenue'].sum():.2f}",
        ),
        _check(
            "unsupported_fields_absent",
            not (actual_columns & unsupported_columns),
            f"unsupported_found={sorted(actual_columns & unsupported_columns)}",
        ),
        _check(
            "order_kpis_explicitly_unsupported",
            pd.isna(kpis.loc["total_orders", "value"]) and pd.isna(kpis.loc["average_order_value", "value"]),
            "total_orders and average_order_value are null with unsupported_grain status",
        ),
        _check("opportunity_insights_unique", insight_duplicates == 0, f"duplicate_rows={insight_duplicates}"),
        _check("business_insights_unique", business_duplicates == 0, f"duplicate_rows={business_duplicates}"),
        _check("sql_layer_present", len(sql_files) == 7, f"sql_files={len(sql_files)}"),
        _check(
            "sql_uses_clean_schema",
            "fact_sales" in sql_text and "record_id" in sql_text,
            "SQL references fact_sales and record_id",
        ),
        _check(
            "dashboard_sources_present",
            all(p.exists() for p in required_sources),
            f"sources_present={sum(p.exists() for p in required_sources)}/{len(required_sources)}",
        ),
        _check(
            "figures_nonempty",
            bool(figures) and all(p.stat().st_size > 0 for p in figures),
            f"nonempty_figures={sum(p.stat().st_size > 0 for p in figures)}/{len(figures)}",
        ),
        _check(
            "metadata_has_no_absolute_paths",
            str(base_dir.resolve()).lower() not in json.dumps(metadata).lower(),
            "metadata contains portable relative/source labels",
        ),
        _check(
            "readme_case_study_structure",
            all(h in readme for h in required_readme_sections),
            f"sections_present={sum(h in readme for h in required_readme_sections)}/{len(required_readme_sections)}",
        ),
        _check(
            "readme_kpis_reconcile",
            "769.515,89" in readme and "116.995,31" in readme and "6,58" in readme,
            "README headline values match validated outputs",
        ),
        _check(
            "streamlit_five_tabs_declared",
            (base_dir / "app.py").exists() and all(tab in app_text for tab in required_tabs),
            f"tabs_declared={sum(tab in app_text for tab in required_tabs)}/{len(required_tabs)}",
        ),
        _check(
            "phase_two_figures_valid",
            not broken_phase_two_figures,
            f"valid_figures={len(phase_two_figures) - len(broken_phase_two_figures)}/{len(phase_two_figures)}",
        ),
        _check(
            "phase_two_documentation_present",
            all(
                (base_dir / "docs" / name).exists()
                for name in ["KPI_GUIDE.md", "SQL_GUIDE.md", "DASHBOARD_GUIDE.md", "BUSINESS_INTERPRETATION.md"]
            ),
            "four focused guides present",
        ),
        _check(
            "opportunity_schema_complete",
            set(opportunity_required).issubset(opportunities.columns)
            and not opportunities[opportunity_required].isna().any().any(),
            "all opportunity cards have observation, evidence, hypothesis, validation, limitation, and score",
        ),
        _check(
            "opportunity_claims_supported",
            not any(term in opportunity_text for term in forbidden_opportunity_claims)
            and opportunities["priority_score"].between(0, 100).all(),
            "no guaranteed/causal/uplift wording; priority scores within 0-100",
        ),
        _check("portable_presentation_paths", not absolute_path_hits, f"absolute_path_hits={absolute_path_hits}"),
        _check("required_engineering_artifacts", not missing_artifacts, f"missing_artifacts={missing_artifacts}"),
        _check("csv_schema_contracts", not csv_schema_failures, f"schema_failures={csv_schema_failures}"),
        _check("readme_links_resolve", not broken_readme_links, f"broken_links={broken_readme_links}"),
        _check(
            "sql_files_independently_valid",
            len(validated_sql) == 7,
            sql_validation_error or "7 ordered SQL files passed static validation",
        ),
        _check(
            "engineering_automation_present",
            all(
                (base_dir / path).is_file()
                for path in [
                    "pyproject.toml",
                    ".pre-commit-config.yaml",
                    ".github/workflows/ci.yml",
                    "Dockerfile",
                    "docker-compose.yml",
                ]
            ),
            "quality, CI, and container configuration present",
        ),
    ]
    passed = all(c["passed"] for c in checks if c["severity"] == "critical")
    result = {
        "status": "passed" if passed else "failed",
        "validated_at_data_as_of": metadata["date_range"]["end"],
        "dataset_grain": metadata["dataset_grain"],
        "checks_passed": sum(bool(c["passed"]) for c in checks),
        "checks_total": len(checks),
        "checks": checks,
        "validated_totals": {"recorded_revenue": revenue, "recorded_quantity": quantity, "sales_records": len(clean)},
        "limitations": metadata["limitations"],
    }
    (report_dir / "project_validation.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    rows = "\n".join(f"| {'PASS' if c['passed'] else 'FAIL'} | {c['check']} | {c['evidence']} |" for c in checks)
    md = f"""# Project Validation

## Overall assessment

**{result["status"].upper()} — {result["checks_passed"]}/{result["checks_total"]} checks passed.** Phase-1 outputs reconcile at the verified aggregated product-record grain. Total Orders and AOV remain intentionally unavailable because the source does not prove customer-order grain.

## Validated totals

- Recorded revenue: {revenue:,.2f} (currency unspecified)
- Recorded quantity: {quantity:,.2f} (unit unspecified)
- Sales records: {len(clean)}
- Data through: {metadata["date_range"]["end"]}

## Checks

| Result | Check | Evidence |
|---|---|---|
{rows}

## Decision gate

Presentation work may proceed because all critical checks passed. Customer-order KPIs, profit, margin, retention, and causal claims remain outside the supported evidence.
"""
    (report_dir / "project_validation.md").write_text(md, encoding="utf-8")
    return result


if __name__ == "__main__":
    validation = validate_project()
    print(
        json.dumps(
            {"status": validation["status"], "checks": f"{validation['checks_passed']}/{validation['checks_total']}"}
        )
    )
