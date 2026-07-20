# SQL Guide

SQL berfungsi sebagai lapisan analitik yang dapat direview terpisah dari pipeline Python. Target sintaksnya adalah **MySQL 8.0**; repository melakukan structural checks, tetapi tidak menyertakan server MySQL untuk execution test.

## Urutan file

1. `01_schema.sql` — tabel `fact_sales` dan business-rule checks.
2. `02_data_quality.sql` — uniqueness, nilai nonpositif, dan revenue reconciliation.
3. `03_executive_kpis.sql` — KPI yang didukung; Total Orders dan AOV dikembalikan sebagai `NULL`.
4. `04_time_performance.sql` — monthly trend, growth, partial-period flag, dan weekday order.
5. `05_menu_performance.sql` — product ranking, share, dan cumulative Pareto.
6. `06_location_channel_performance.sql` — city, purchase type, payment, dan manager views.
7. `07_opportunity_analysis.sql` — candidate groups untuk validasi lanjutan.

## Import

Import `output/bi/fact_sales.csv` ke tabel `fact_sales` dan petakan kolom CSV `date` ke SQL `sale_date`. Path file ditentukan pada environment pengguna; tidak ada absolute local path yang disimpan dalam repository.

## Pola analitik

Layer ini menggunakan CTE, window functions, `RANK`, cumulative sum, conditional logic, dan `NULLIF` untuk safe division. `record_id` adalah analytical primary key. Jangan menghitung customer orders dari `order_id` tanpa verifikasi sumber yang lebih kaya.
