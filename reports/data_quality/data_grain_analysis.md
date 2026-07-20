# Data Grain Analysis

## Verified conclusion

The safest supported grain is **one aggregated product sales record with a unique source order_id**. `order_id` is unique, but one product per row and fractional quantities from 200.40 to 754.43 do not establish customer-order grain.

- Raw rows: 254
- Unique source order IDs: 254
- Exact duplicate extra copies: 0
- Generated analytical primary key: `record_id`

Order count, AOV, and average items per order remain unsupported.
