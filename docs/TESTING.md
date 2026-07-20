# Testing Guide

## Test layers

- Unit tests memakai synthetic data dan tidak memerlukan network atau service eksternal.
- Pipeline tests memeriksa generated schemas dan portable metadata.
- Streamlit AppTest merender lima tab tanpa menjalankan browser/server eksternal.
- Repository validation merekonsiliasi KPI, dimensions, SQL, figures, README, docs, dan paths.

## Commands

```bash
python -m pytest -q
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80
python -m ruff check .
python validate_project.py
```

Windows PowerShell memakai perintah yang sama. Alternatif GNU Make: `make test`, `make coverage`, `make lint`, dan `make validate`.

## Deterministic fixtures

Fixtures harus mendefinisikan date, product, price, quantity, purchase type, payment, manager, dan city secara eksplisit. Jangan mengambil fixture dari Kaggle atau output production secara remote.

## Adding tests

Setiap perubahan formula atau schema harus menguji normal path, invalid input, boundary condition, dan reconciliation total. Order-level KPI harus tetap unsupported sampai fixture dan source contract membuktikan customer-order grain.
