# KPI Guide

## Prinsip utama

KPI mengikuti grain satu record penjualan produk teragregasi. Nama kolom `order_id` dipertahankan untuk traceability, tetapi tidak cukup membuktikan customer order.

| KPI | Formula | Kegunaan | Batasan |
|---|---|---|---|
| Recorded Revenue | `SUM(price × quantity)` | Mengukur nilai penjualan yang tercatat | Currency, discount, tax, cost, dan profit tidak diketahui |
| Sales Records | `COUNT(DISTINCT record_id)` | Mengukur jumlah record analitik | Bukan jumlah customer orders |
| Recorded Quantity | `SUM(quantity)` | Menunjukkan volume yang dicatat | Unit quantity tidak diketahui dan nilainya pecahan |
| Weighted Selling Price | `Recorded Revenue / Recorded Quantity` | Memisahkan price component dari volume | Bukan AOV |
| Active Sales Days | `COUNT(DISTINCT date)` | Menunjukkan coverage hari dalam extract | Hari tanpa record tidak dapat dibedakan dari hari tutup |
| Average Active-Day Revenue | `Recorded Revenue / Active Sales Days` | Membandingkan skala per hari yang terwakili | Tidak memakai seluruh calendar days |
| Median Active-Day Revenue | median dari daily revenue | Mengurangi pengaruh hari ekstrem | Tetap hanya mencakup active days |

## KPI yang sengaja tidak dihitung

- Total Orders
- Average Order Value
- Average Items per Order
- Profit dan Margin
- Customer Retention dan Lifetime Value

KPI tersebut baru dapat ditambahkan setelah sumber memverifikasi order header/line-item grain, customer identity, atau cost data yang relevan.
