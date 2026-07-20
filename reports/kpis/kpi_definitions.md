# KPI Definitions

| KPI | Formula | Grain | Limitation |
|---|---|---|---|
| Total revenue | sum(price × quantity) | sales record | Currency, discount, tax, cost, and profit unknown |
| Total sales records | count distinct record_id | sales record | Not customer orders |
| Total quantity sold | sum(quantity) | sales record | Quantity unit undocumented |
| Average selling price | total revenue / total quantity | dataset | Not AOV |
| Active sales days | count distinct date | day | Unobserved calendar days excluded |
| Average/median daily revenue | aggregate active-day revenue | active day | Active days only |
| Total orders / AOV / items per order | not calculated | order | Unsupported grain |
