import pandas as pd
from datetime import datetime

def extract_customers():
    return pd.DataFrame([
        {'id': 1, 'name': 'Alice', 'country': 'USA'},
        {'id': 2, 'name': 'Bob', 'country': 'UK'},
    ])

def extract_products():
    return pd.DataFrame([
        {'id': 10, 'name': 'Headphones', 'category': 'Electronics'},
        {'id': 20, 'name': 'T-Shirt', 'category': 'Clothing'},
    ])

def extract_orders():
    return pd.DataFrame([
        {'id': 100, 'customer_id': 1, 'order_date': '2024-03-01 10:00:00', 'status': 'completed'},
        {'id': 101, 'customer_id': 2, 'order_date': '2024-03-01 15:00:00', 'status': 'completed'},
    ])

def extract_order_items():
    return pd.DataFrame([
        {'id': 1000, 'order_id': 100, 'product_id': 10, 'quantity': 2, 'unit_price': 50, 'currency': 'USD'},
        {'id': 1001, 'order_id': 101, 'product_id': 20, 'quantity': 1, 'unit_price': 20, 'currency': 'USD'},
    ])

def fetch_conversion_rate(date, currency_from, currency_to):
    # always 1.0 for USD
    return 1.0

# Transformation and Load

def build_dim_product(products):
    return products.rename(columns={'id': 'product_id'})[['product_id', 'name', 'category']]

def build_dim_customer(customers):
    return customers.rename(columns={'id': 'customer_id'})[['customer_id', 'name', 'country']]

def build_dim_time(orders):
    times = pd.to_datetime(orders['order_date'])
    return pd.DataFrame({
        'time_id': range(1, len(times)+1),
        'order_datetime': times,
        'order_date': times.dt.date,
        'order_hour': times.dt.hour,
        'order_weekday': times.dt.weekday
    })

def build_fact_sales(order_items, orders, products, customers, dim_time):
    merged = order_items.merge(orders, left_on='order_id', right_on='id', suffixes=('_item', '_order'))
    merged = merged.merge(products, left_on='product_id', right_on='id')
    merged = merged.merge(customers, left_on='customer_id', right_on='id')
    merged['order_datetime'] = pd.to_datetime(merged['order_date'])
    merged = merged.merge(dim_time, on='order_datetime')
    merged['revenue_usd'] = merged['unit_price'] * merged['quantity'] * 1.0  # mock rate
    return merged[['order_id', 'product_id', 'customer_id', 'time_id', 'quantity', 'revenue_usd', 'currency', 'unit_price']]

# Main ETL
def main():
    print("--- MOCK ETL PIPELINE START ---")
    customers = extract_customers()
    products = extract_products()
    orders = extract_orders()
    order_items = extract_order_items()

    print("\n[dim_product]")
    dim_product = build_dim_product(products)
    print(dim_product)

    print("\n[dim_customer]")
    dim_customer = build_dim_customer(customers)
    print(dim_customer)

    print("\n[dim_time]")
    dim_time = build_dim_time(orders)
    print(dim_time)

    print("\n[fact_sales]")
    fact_sales = build_fact_sales(order_items, orders, products, customers, dim_time)
    print(fact_sales)
    print("--- MOCK ETL PIPELINE END ---")

if __name__ == "__main__":
    main()
