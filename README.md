# Restaurant Performance Intelligence

> Diagnosing the drivers of recorded restaurant revenue across menu, location, channel, and time.

## Business Question

**What drives restaurant revenue?**

Proyek ini memeriksa bagaimana recorded quantity, weighted selling price, menu mix, location, purchase type, payment method, dan time period muncul bersama recorded revenue. Analisis menggunakan bahasa deskriptif dan memisahkan observation dari business hypothesis.

## Dataset

Dataset bersumber dari Kaggle `rohitgrewal/restaurant-sales-data` dan mencakup **254 record** pada **7 November–29 Desember 2022**.

Grain paling aman adalah **satu record penjualan produk teragregasi dengan source `order_id` unik**. Fractional quantity yang besar tidak mendukung interpretasi bahwa satu baris merupakan satu customer order atau line item satuan.

Keterbatasan sumber utama:

- currency dan unit quantity tidak dijelaskan;
- customer identifier, discount, tax, cost, dan margin tidak tersedia;
- kedua bulan merupakan partial periods;
- data historis 2022 tidak menggambarkan operasi saat ini.

## Data Quality

Pipeline menormalisasi nama kolom, membersihkan whitespace sebelum string conversion, melakukan explicit date/numeric parsing, memisahkan repaired/removed/flagged records, dan hanya menghapus exact duplicate yang terverifikasi. Raw input tidak ditimpa dan setiap output record memiliki stable `record_id`.

Validasi fase 2 menjalankan **19 consistency checks** atas cleaned data, KPI, metadata, fact table, dimension outputs, SQL, insights, dashboard sources, dan figures. Hasil terbaru tersedia di `reports/validation/project_validation.md`.

## KPI Framework

KPI tervalidasi untuk extract ini:

| KPI | Nilai | Mengapa penting |
|---|---:|---|
| Recorded Revenue | 769.515,89 | Skala nilai penjualan yang tercatat |
| Sales Records | 254 | Coverage record analitik, bukan customer orders |
| Recorded Quantity | 116.995,31 | Observable volume component |
| Weighted Selling Price | 6,58 | Price component setelah weighting quantity |
| Active Sales Days | 53 | Coverage hari dalam extract |
| Average Active-Day Revenue | 14.519,17 | Membandingkan skala per hari yang terwakili |
| Median Active-Day Revenue | 14.200,04 | Typical active-day result yang lebih robust |

Total Orders, AOV, dan Average Items per Order tidak dihitung karena grain belum mendukungnya.

## Revenue Drivers

Analisis memakai identitas yang didukung data:

```text
Recorded Revenue = Recorded Quantity × Weighted Selling Price
```

Perbandingan tersedia menurut weekday/weekend, city, purchase type, payment method, product, dan category. Perbedaan revenue tidak dianggap disebabkan suatu kelompok; pipeline menunjukkan apakah pola diamati bersama volume, weighted price, atau keduanya.

## Menu Intelligence

Burgers memiliki recorded revenue terbesar dengan share **49,0%**. Tiga produk mencapai setidaknya **80%** cumulative revenue, dengan product HHI **0,311**. Product portfolio matrix memisahkan high/low revenue dan high/low recorded volume menggunakan median data, bukan klaim profitability.

## Location & Channel

Lisbon memiliki observed city revenue share terbesar (**31,4%**), sedangkan London memiliki recorded quantity relatif tinggi dan weighted selling price di bawah baseline keseluruhan. Online adalah purchase type terbesar (**39,7%**) dan Credit Card adalah payment method terbesar (**47,0%**).

Angka tersebut adalah observed shares, bukan bukti customer preference. Manager analysis juga bersifat deskriptif karena assignment, traffic, menu mix, staffing, dan capacity tidak tersedia.

## Opportunity Matrix

Opportunity candidates dibuat secara deterministic dari volume, weighted price, concentration, dan dimension medians. Setiap kandidat menyertakan:

- observation;
- metric evidence;
- business hypothesis;
- recommended validation action;
- limitation;
- priority score dan evidence strength.

Opportunity adalah **hipotesis untuk divalidasi**, bukan rekomendasi terjamin atau estimasi uplift.

## Dashboard

Aplikasi Streamlit bernama **Restaurant Performance Intelligence** memiliki lima tab:

1. Executive Overview
2. Revenue Drivers
3. Menu Intelligence
4. Business Explorer
5. Opportunity Matrix

Business Explorer menyediakan filter city, manager, payment, purchase type, category, dan date. Lihat `docs/DASHBOARD_GUIDE.md` untuk interpretasi setiap tab.

## SQL Layer

Tujuh query modular mencakup schema, data quality, executive KPI, time performance, menu/Pareto, location/channel/manager, dan opportunity candidates. SQL menggunakan MySQL 8.0-style CTE, window functions, rank, cumulative sum, conditional logic, dan safe division.

## Reproduce

Supported version: **Python 3.11 or newer**.

Quick Start untuk analisis dan dashboard:

```bash
python -m venv .venv
python -m pip install -r requirements-dev.txt
python run_pipeline.py
python -m pytest -q
python validate_project.py
streamlit run app.py
```

Pipeline menghasilkan cleaned data, audit trail, KPI, analytical outputs, BI model, insight files, reports, metadata, validation, dan figures.

Runtime-only installation menggunakan `requirements.txt`. Development, notebook, coverage, Ruff, dan pre-commit menggunakan `requirements-dev.txt`.

## Validation & Testing

```bash
python -m ruff check .
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80
python validate_project.py
```

Validation command mengembalikan non-zero exit code jika required artifact, schema, metadata, figure, SQL, documentation, README path, atau reconciliation check gagal. Test memakai synthetic fixtures dan tidak membutuhkan Kaggle, MySQL, Power BI, internet, atau credentials.

## CI

GitHub Actions menjalankan lint, pipeline generation, unit tests, coverage threshold, repository validation, dan Streamlit import pada Python 3.11. Workflow tidak memakai external credentials, MySQL server, Power BI, atau Kaggle download.

Pre-commit setup:

```bash
pre-commit install
pre-commit run --all-files
```

## Deployment

Dashboard dapat dijalankan lokal atau melalui Docker:

```bash
docker compose build
docker compose up
```

Container membaca artifact yang sudah dibuat dan tidak menjalankan pipeline saat startup. Repository hanya menyiapkan deployment assets; tidak ada klaim live deployment. Lihat `docs/DEPLOYMENT.md`.

## Repository Structure

```text
├── app.py                     # Interactive Streamlit dashboard
├── validate_project.py        # CI-friendly repository validation command
├── pyproject.toml             # Ruff, pytest, and coverage configuration
├── requirements*.txt          # Runtime and development dependencies
├── Dockerfile                 # Streamlit image from prepared artifacts
├── config/                    # Product taxonomy mapping
├── data/                      # Preserved raw dataset
├── dashboard/                 # Power BI guidance and existing preview
├── docs/                      # KPI, SQL, dashboard, BI, interpretation guides
├── notebook/                  # Reproducible companion notebook
├── output/
│   ├── analysis/              # Dimension and driver outputs
│   ├── bi/                    # Dashboard-ready fact and dimensions
│   ├── figures/               # Decision-focused visuals
│   ├── insights/              # Opportunities and deterministic insights
│   └── kpis/                  # Executive KPI output
├── reports/                   # Quality, validation, storytelling, limitations
├── sql/                       # MySQL 8.0 analytical layer
├── src/                       # Modular production pipeline and validation logic
└── tests/                     # Synthetic automated tests
```

## Limitations

- Revenue bukan profit; cost dan margin tidak tersedia.
- Customer segmentation, retention, dan repeat-customer analysis tidak didukung.
- Total Orders dan AOV tidak didukung oleh grain saat ini.
- Manager comparisons mungkin terkonfounding city assignment dan coverage.
- Transaction records tidak membuktikan causality.
- Operational action memerlukan cost, inventory, staffing, traffic, dan capacity data.

## Future Work

- Customer segmentation setelah customer identifier tersedia.
- Inventory optimization setelah stock, waste, dan stockout data tersedia.
- Promotion analysis dengan discount, exposure, dan comparison design yang valid.
- Profit analysis setelah item-level cost dan contribution margin tersedia.
- Order-level decomposition setelah POS order header dan line-item grain terverifikasi.
