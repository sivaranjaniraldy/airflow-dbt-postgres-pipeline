import pandas as pd
from sqlalchemy import create_engine, inspect
import os

# Connection to the warehouse Postgres
DB_USER = "warehouse"
DB_PASSWORD = "warehouse"
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5433")
DB_NAME = "olist"

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

# Map of CSV filename -> target table name in the 'raw' schema
files_to_load = {
    "olist_orders_dataset.csv": "orders",
    "olist_customers_dataset.csv": "customers",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "olist_geolocation_dataset.csv": "geolocation",
    "product_category_name_translation.csv": "product_category_translation",
}

with engine.begin() as conn:
    conn.exec_driver_sql("CREATE SCHEMA IF NOT EXISTS raw;")

inspector = inspect(engine)

for filename, table_name in files_to_load.items():
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"⚠️  Skipping {filename} — not found in {DATA_DIR}")
        continue
    df = pd.read_csv(filepath)

    table_exists = inspector.has_table(table_name, schema="raw")

    if table_exists:
        with engine.begin() as conn:
            conn.exec_driver_sql(f"TRUNCATE TABLE raw.{table_name};")
        df.to_sql(table_name, engine, schema="raw", if_exists="append", index=False)
    else:
        df.to_sql(table_name, engine, schema="raw", if_exists="replace", index=False)

    print(f"✅ Loaded {len(df)} rows into raw.{table_name}")

print("Done.")