# Data Warehouse & ETL Design Process

## Schema Design
- **Star schema**: Simple, supports analytics for product performance and sales timing.
- **Dimensions**: Product, Customer, Time.
- **Fact**: Sales (normalized to USD).
- **Rationale**: Enables easy queries for top products and sales by hour.

## ETL Pipeline
- **Extract**: Source DBs (orders, order_items, customers, products).
- **Transform**: Join, currency normalization (API), enrich with dimensions.
- **Load**: Insert into warehouse tables.
- **Airflow**: Orchestrates the pipeline, modular Python for clarity.

## Assumptions
- Only completed orders are loaded.
- All currencies normalized to USD for revenue.
- Time zone is UTC.
- No SCD or incremental logic (full load for challenge scope).
- API is available and reliable.

## Tradeoffs
- No SCD or advanced warehouse features for simplicity.
- No error handling for partial loads (could be added for production).
- Loads all data each run (could be optimized for incremental loads).

## Improvements (with more time)
- Add SCD for dimensions.
- Incremental ETL (change data capture).
- More robust error handling and logging.
- Automated data quality checks.
- Parameterize currency and time zone handling.
