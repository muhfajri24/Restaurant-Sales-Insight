# Pipeline Engineering Guide

## Module ownership

- `config.py`: paths, columns, grain, KPI definitions, dan stable settings.
- `exceptions.py`: project-specific failure types.
- `validation.py`: schema, text, domain, dan duplicate checks.
- `cleaning.py`: repairs, exact-duplicate removal, flags, mapping, stable record key.
- `kpis.py`: grain-safe KPI formulas.
- `analysis.py`: time, menu, dimension, Pareto, dan concentration outputs.
- `insights.py`: deterministic opportunity and insight rules.
- `visualization.py`: static decision-focused figures.
- `reporting.py`: Markdown/data-quality reports.
- `metadata.py`: portable project metadata.
- `sql_exports.py`: SQL structure and schema-reference checks.
- `pipeline.py`: orchestration and exports.
- `restaurant_sales_pipeline.py`: backward-compatible import façade.

## Failure behavior

Pipeline memakai exceptions spesifik untuk missing raw file, invalid schema, malformed mapping, dan missing/broken SQL artifacts. Invalid data records diekspor untuk audit; record tidak dibuang diam-diam.

## Output contract

Output utama mencakup cleaned data, audit/removal/flag files, KPI, analytical CSV, BI fact/dimensions, insights, reports, figures, validation report, dan metadata. `python validate_project.py` memeriksa kontrak tersebut.
