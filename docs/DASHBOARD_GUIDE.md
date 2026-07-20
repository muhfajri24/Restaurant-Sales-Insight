# Dashboard Guide

Jalankan aplikasi dengan:

```bash
streamlit run app.py
```

## Lima tab

### Executive Overview

Menampilkan recorded revenue, quantity, sales records, weighted price, active-day trend, dan executive summary. Total Orders dan AOV ditampilkan `N/A` karena grain tidak mendukungnya.

### Revenue Drivers

Menjelaskan hubungan identitas `Recorded Revenue = Recorded Quantity × Weighted Selling Price`. Pengguna dapat membandingkan weekday/weekend, city, payment, purchase type, dan category.

### Menu Intelligence

Menyediakan product/category ranking, sorting berdasarkan revenue/quantity/contribution, Pareto, portfolio matrix, dan concentration context.

### Business Explorer

Filter tersedia untuk city, manager, payment, purchase type, category, dan date. Scope terpilih menampilkan recorded revenue, quantity, contribution, product mix, dan detail record.

### Opportunity Matrix

Setiap kandidat menampilkan observation, evidence, business hypothesis, next validation, limitation, priority score, dan evidence strength. Kandidat bukan guaranteed recommendation.

## Sumber dashboard

Dashboard membaca file CSV tervalidasi di `output/`. Jalankan pipeline sebelum dashboard jika raw data atau logic berubah.
