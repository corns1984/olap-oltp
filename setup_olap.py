import sqlite3
from pathlib import Path

# Define the target database file
db_path = Path("retail_olap.db")

# Optional: Remove existing database to ensure a clean start
if db_path.exists():
    db_path.unlink()

# Connect to the new OLAP database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Create Product Dimension Table
    cursor.execute("""
        CREATE TABLE dim_product (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        );
    """)

    # 2. Create Customer Dimension Table
    cursor.execute("""
        CREATE TABLE dim_customer (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            city TEXT NOT NULL
        );
    """)

    # 3. Create Date Dimension Table
    cursor.execute("""
        CREATE TABLE dim_date (
            date_key TEXT PRIMARY KEY,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            day INTEGER NOT NULL
        );
    """)

    # 4. Create Sales Fact Table
    cursor.execute("""
        CREATE TABLE fact_sales (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            date_key TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
            FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
            FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
        );
    """)

    conn.commit()
    print("SUCCESS: retail_olap.db created with clean star schema tables.")

except Exception as e:
    conn.rollback()
    print(f"ERROR: Failed to set up OLAP schema: {e}")
    raise

finally:
    conn.close()
