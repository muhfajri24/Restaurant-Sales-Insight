# Contributing

## Development setup

Python 3.11 atau lebih baru diperlukan.

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements-dev.txt
pre-commit install
```

Gunakan `source .venv/bin/activate` pada Linux atau macOS.

## Change workflow

1. Pertahankan raw input dan verified grain.
2. Tambahkan synthetic test untuk perubahan cleaning, KPI, analysis, insight, atau schema.
3. Jalankan pipeline, lint, coverage, dan validation.
4. Jangan memperkenalkan customer-order KPI, profit, atau causal claim tanpa field dan desain yang mendukung.
5. Jangan menyimpan credential, absolute local path, atau generated secret.

## Required checks

```bash
python run_pipeline.py
python -m ruff check .
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80
python validate_project.py
```

Pull request sebaiknya menjelaskan perubahan kontrak data, output yang terpengaruh, test baru, dan remaining limitations.
