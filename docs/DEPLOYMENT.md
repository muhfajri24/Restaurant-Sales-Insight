# Deployment Guide

Repository menyiapkan artefak deployment, tetapi **tidak mengklaim adanya deployment live**.

## Local Streamlit

```bash
python -m pip install -r requirements.txt
python run_pipeline.py
python -m streamlit run app.py
```

Buka `http://localhost:8501` setelah Streamlit memberikan alamat lokal.

## Docker

Image menjalankan dashboard dari output yang sudah dibuat; pipeline tidak dijalankan saat container startup.

```bash
docker compose build
docker compose up
```

Port host `8501` dipetakan ke container. Jalankan pipeline dan validation sebelum membangun image bila data atau logic berubah.

## Streamlit Community Cloud atau platform serupa

1. Pastikan `app.py`, runtime requirements, dan output dashboard-ready berada dalam revision yang akan dideploy.
2. Gunakan `app.py` sebagai entrypoint.
3. Pilih Python 3.11 bila platform mendukung pemilihan versi.
4. Tidak ada secret yang diperlukan untuk dataset repository saat ini.
5. Verifikasi health, lima tab, filters, dan grain caveat setelah deployment.

## Power BI

Import CSV dari `output/bi/` dan gunakan relationship di `docs/BI_DATA_MODEL.md`. Power BI tidak dijalankan oleh CI dan file preview bukan bukti live dashboard.

## Artifact preparation

```bash
python run_pipeline.py
python validate_project.py
python -m pytest --cov=src --cov-fail-under=80
python -m ruff check .
```

## Limitations

Currency, quantity unit, order grain, cost, margin, customer identity, dan causal evidence tetap tidak tersedia setelah deployment.
