from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
from helpers import (
    get_pg_engine, fetch_conversion_rate,
    extract_orders, extract_order_items, extract_customers, extract_products,
    load_dim_product, load_dim_customer, load_dim_time, load_fact_sales
)

def etl_main():
    db1 = get_pg_engine('postgres_db1', 5432, 'ecommerce_orders', 'postgres', 'postgres')
    db2 = get_pg_engine('postgres_db2', 5432, 'ecommerce_products', 'postgres', 'postgres')
    # Warehouse
    wh = get_pg_engine('postgres_warehouse', 5432, 'data_warehouse', 'postgres', 'postgres')
    # Extract
    orders = extract_orders(db1)
    order_items = extract_order_items(db1)
    customers = extract_customers(db1)
    products = extract_products(db2)
    # Load dimensions
    load_dim_product(products, wh)
    load_dim_customer(customers, wh)
    # Time dim
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    load_dim_time(orders[['order_date']], wh)
    # Prepare fact_sales
    merged = order_items.merge(orders, left_on='order_id', right_on='id', suffixes=('_item', '_order'))
    merged = merged.merge(products, left_on='product_id', right_on='id', suffixes=('', '_prod'))
    merged = merged.merge(customers, left_on='customer_id', right_on='id', suffixes=('', '_cust'))
    # Currency normalization
    fact_rows = []
    for _, row in merged.iterrows():
        rate = 1.0
        if row['currency_item'] != 'USD':
            rate = fetch_conversion_rate(row['order_date'].strftime('%Y-%m-%d'), row['currency_item'], 'USD')
        revenue_usd = float(row['unit_price']) * row['quantity'] * rate
        fact_rows.append({
            'order_id': row['order_id'],
            'product_id': row['product_id'],
            'customer_id': row['customer_id'],
            'time_id': None,  # To be updated after dim_time load
            'quantity': row['quantity'],
            'revenue_usd': revenue_usd,
            'currency': row['currency_item'],
            'original_amount': float(row['unit_price']) * row['quantity']
        })
    fact_df = pd.DataFrame(fact_rows)
    # Map time_id
    time_dim = pd.read_sql('SELECT * FROM dim_time', wh)
    fact_df = fact_df.merge(
        time_dim,
        left_on=fact_df['order_id'].map(lambda oid: orders.loc[orders['id'] == oid, 'order_date'].values[0]),
        right_on='order_datetime',
        how='left'
    )
    fact_df['time_id'] = fact_df['time_id']
    fact_df = fact_df.drop(columns=['order_datetime', 'order_date', 'order_hour', 'order_weekday', 'key_0'])
    load_fact_sales(fact_df, wh)

default_args = {
    'owner': 'data_engineer_candidate',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_sales_pipeline',
    default_args=default_args,
    description='ETL pipeline for eCommerce analytics',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['etl', 'challenge'],
)

etl_task = PythonOperator(
    task_id='run_etl',
    python_callable=etl_main,
    dag=dag,
)
