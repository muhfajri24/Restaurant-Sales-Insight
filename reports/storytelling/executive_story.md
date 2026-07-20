# Executive Story — Restaurant Performance Intelligence

## Problem

Manajemen membutuhkan cara yang lebih disiplin untuk memahami **di mana recorded revenue terkonsentrasi** dan kelompok mana yang layak diperiksa lebih lanjut. Dataset tidak menyediakan customer ID, cost, discount, atau bukti bahwa setiap baris adalah satu pesanan pelanggan. Karena itu analisis difokuskan pada grain yang benar-benar dapat dibuktikan: satu record penjualan produk teragregasi.

## What happened

Pada 7 November–29 Desember 2022, data mencatat:

- recorded revenue **769.515,89**;
- recorded quantity **116.995,31**;
- **254** sales records pada **53** active sales days;
- weighted selling price **6,58**.

Burgers menyumbang **49,0%** recorded revenue. Lisbon mencatat share kota terbesar (**31,4%**), Online merupakan purchase type terbesar (**39,7%**), dan Credit Card merupakan payment method terbesar (**47,0%**).

## Why

Data hanya mendukung penjelasan deskriptif. Recorded revenue diamati bersama dua komponen yang tersedia: **recorded quantity** dan **weighted selling price**. Perbedaan antarproduk, kota, atau channel dapat berkaitan dengan salah satu atau kombinasi keduanya; data tidak membuktikan penyebabnya.

Contohnya, Online memiliki recorded quantity **48.999,16**, tetapi weighted selling price **6,23**, di bawah baseline keseluruhan **6,58**. London juga memiliki recorded quantity relatif tinggi (**33.535,34**) dan weighted selling price **6,30**. Pola tersebut konsisten dengan kemungkinan perbedaan product mix, tetapi discount dan komposisi order tidak tersedia untuk mengonfirmasinya.

## Evidence

- Tiga produk mencapai setidaknya 80% recorded revenue; product HHI **0,311**.
- Burgers menyumbang **49,0%**, Fries **16,3%**, dan Chicken Sandwiches **14,9%**.
- Lisbon mencatat **31,4%** revenue; London **27,4%**.
- Online mencatat **39,7%** revenue; In-store **37,1%**; Drive-thru **23,2%**.
- Credit Card mencatat **47,0%** revenue; Cash **31,1%**; Gift Card **21,9%**.
- November dan Desember adalah partial periods, sehingga total keduanya tidak diperlakukan sebagai perbandingan full-month.

## Business hypothesis

1. Konsentrasi Burgers mungkin memberi fokus operasional sekaligus menciptakan ketergantungan pada menu terbatas.
2. Weighted price Online dan London yang berada di bawah baseline mungkin berkaitan dengan product mix yang lebih murah.
3. Produk high-volume/low-price mungkin dapat dievaluasi untuk bundling, tetapi hanya setelah discount, cost, inventory, dan capacity tersedia.

Hipotesis tersebut bukan rekomendasi terjamin dan tidak mengandung estimasi uplift.

## Next analysis

1. Verifikasi grain melalui data POS line-item dan order header.
2. Tambahkan currency, quantity unit, discount, tax, cost, dan contribution margin.
3. Pisahkan perubahan quantity, mix, dan price realization pada periode lengkap.
4. Uji inventory availability, staffing, dan capacity sebelum keputusan operasional.
5. Tambahkan customer identifier sebelum segmentation, repeat behavior, atau retention analysis.
