# Dashboard/Report Outline

##1. Top Products by Sales Volume
-  Metric : Total quantity sold per product
-  Query : 
  ```sql
  SELECT p.name, SUM(f.quantity) AS total_sold
  FROM fact_sales f
  JOIN dim_product p ON f.product_id = p.product_id
  GROUP BY p.name
  ORDER BY total_sold DESC
  LIMIT 10;
  ```
-  Visualization : Bar chart (Product vs. Quantity Sold)

## 2. Top Products by Revenue
-  Metric : Total revenue (USD) per product
-  Query :
  ```sql
  SELECT p.name, SUM(f.revenue_usd) AS total_revenue
  FROM fact_sales f
  JOIN dim_product p ON f.product_id = p.product_id
  GROUP BY p.name
  ORDER BY total_revenue DESC
  LIMIT 10;
  ```
-  Visualization : Bar chart (Product vs. Revenue)

## 3. Optimal Time for Promotions
-  Metric : Sales volume by hour of day
-  Query :
  ```sql
  SELECT t.order_hour, SUM(f.quantity) AS total_sold
  FROM fact_sales f
  JOIN dim_time t ON f.time_id = t.time_id
  GROUP BY t.order_hour
  ORDER BY t.order_hour;
  ```
-  Visualization : Line or bar chart (Hour vs. Quantity Sold)

## Notes
- All revenue is normalized to USD.
- Only completed orders are included.
- Further breakdowns (by country, category) can be added as needed.
