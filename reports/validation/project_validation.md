# Project Validation

## Overall assessment

**PASSED — 32/32 checks passed.** Phase-1 outputs reconcile at the verified aggregated product-record grain. Total Orders and AOV remain intentionally unavailable because the source does not prove customer-order grain.

## Validated totals

- Recorded revenue: 769,515.89 (currency unspecified)
- Recorded quantity: 116,995.31 (unit unspecified)
- Sales records: 254
- Data through: 2022-12-29

## Checks

| Result | Check | Evidence |
|---|---|---|
| PASS | cleaned_revenue_vs_kpi | cleaned=769515.89; kpi=769515.89 |
| PASS | cleaned_quantity_vs_kpi | cleaned=116995.31; kpi=116995.31 |
| PASS | cleaned_revenue_vs_metadata | cleaned=769515.89; metadata=769515.89 |
| PASS | cleaned_vs_fact_rows | cleaned=254; fact=254 |
| PASS | cleaned_vs_fact_revenue | cleaned=769515.89; fact=769515.89 |
| PASS | product_dimension_reconciles | product_sum=769515.89 |
| PASS | city_dimension_reconciles | city_sum=769515.89 |
| PASS | payment_dimension_reconciles | payment_sum=769515.89 |
| PASS | manager_dimension_reconciles | manager_sum=769515.89 |
| PASS | purchase_type_dimension_reconciles | purchase_type_sum=769515.89 |
| PASS | unsupported_fields_absent | unsupported_found=[] |
| PASS | order_kpis_explicitly_unsupported | total_orders and average_order_value are null with unsupported_grain status |
| PASS | opportunity_insights_unique | duplicate_rows=0 |
| PASS | business_insights_unique | duplicate_rows=0 |
| PASS | sql_layer_present | sql_files=7 |
| PASS | sql_uses_clean_schema | SQL references fact_sales and record_id |
| PASS | dashboard_sources_present | sources_present=6/6 |
| PASS | figures_nonempty | nonempty_figures=17/17 |
| PASS | metadata_has_no_absolute_paths | metadata contains portable relative/source labels |
| PASS | readme_case_study_structure | sections_present=14/14 |
| PASS | readme_kpis_reconcile | README headline values match validated outputs |
| PASS | streamlit_five_tabs_declared | tabs_declared=5/5 |
| PASS | phase_two_figures_valid | valid_figures=8/8 |
| PASS | phase_two_documentation_present | four focused guides present |
| PASS | opportunity_schema_complete | all opportunity cards have observation, evidence, hypothesis, validation, limitation, and score |
| PASS | opportunity_claims_supported | no guaranteed/causal/uplift wording; priority scores within 0-100 |
| PASS | portable_presentation_paths | absolute_path_hits=[] |
| PASS | required_engineering_artifacts | missing_artifacts=[] |
| PASS | csv_schema_contracts | schema_failures=[] |
| PASS | readme_links_resolve | broken_links=[] |
| PASS | sql_files_independently_valid | 7 ordered SQL files passed static validation |
| PASS | engineering_automation_present | quality, CI, and container configuration present |

## Decision gate

Presentation work may proceed because all critical checks passed. Customer-order KPIs, profit, margin, retention, and causal claims remain outside the supported evidence.
