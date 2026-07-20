# Reproducibility

## Supported environment

- Python 3.11+
- Windows, Linux, atau macOS
- Tidak memerlukan internet setelah dependencies terpasang dan raw CSV tersedia
- Tests tidak memerlukan Kaggle, MySQL, Power BI, atau external credentials

## Clean setup

```bash
python -m venv .venv
python -m pip install -r requirements-dev.txt
python run_pipeline.py
python -m pytest -q
python validate_project.py
```

Aktivasi Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Aktivasi Linux/macOS:

```bash
source .venv/bin/activate
```

## Determinism

- Raw file tidak dimodifikasi.
- Stable `record_id` berasal dari source row dan record content.
- Cleaning, mapping, KPI, aggregation, concentration, dan opportunity rules bersifat deterministic.
- Tidak ada network call atau random sampling dalam pipeline.
- Metadata tidak menyimpan absolute local path.

## Rebuild sequence

1. Pastikan `data/restaurant_sales_raw.csv` dan `config/product_category_mapping.csv` tersedia.
2. Jalankan `python run_pipeline.py`.
3. Jalankan `python validate_project.py`.
4. Jalankan test dan lint sebelum membagikan output.

Notebook bukan sumber logic; notebook memanggil production API dan membaca output.
