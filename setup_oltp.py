import sqlite3
from datetime import date, timedelta
from pathlib import Path

DB = Path("retail_oltp.db")
if DB.exists():
    raise SystemExit("STOP: retail_oltp.db already exists. Preserve it and inspect before proceeding.")

conn = sqlite3.connect(DB)
conn.execute("PRAGMA foreign_keys = ON")

conn.executescript("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    city TEXT NOT NULL
) STRICT;

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL CHECK(price > 0),
    stock INTEGER NOT NULL CHECK(stock >= 0)
) STRICT;

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date TEXT NOT NULL,
    status TEXT NOT NULL
) STRICT;

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_price REAL NOT NULL CHECK(unit_price > 0)
) STRICT;

CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_order_items_order ON order_items(order_id);
""")

cities = ["Pune", "Mumbai", "Delhi", "Bengaluru", "Chennai"]
conn.executemany(
    "INSERT INTO customers VALUES (?, ?, ?)",
    [(i, f"Customer {i}", cities[(i - 1) % len(cities)])
     for i in range(1, 201)]
)

categories = ["Apparel", "Electronics", "Grocery", "Home"]
products = []
for i in range(1, 51):
    category = categories[(i - 1) % 4]
    price = round(100 + i * 37.5, 2)
    stock = 342 if i == 7 else 100 + i * 5
    products.append((i, f"Product {i}", category, price, stock))

conn.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?)", products)

start = date(2026, 1, 1)
orders = []
for i in range(1, 5001):
    if i == 42:
        order_date = "2026-03-11"
        status = "COMPLETED"
        customer_id = 86
    else:
        order_date = (start + timedelta(days=(i * 17) % 182)).isoformat()
        status = "COMPLETED" if i % 10 else "CANCELLED"
        customer_id = (i * 37) % 200 + 1
    orders.append((i, customer_id, order_date, status))

conn.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", orders)

items = []
item_id = 1
for order_id in range(1, 5001):
    count = 3 if order_id <= 61 else 2
    for j in range(count):
        product_id = ((order_id * 13 + j * 7 - 1) % 50) + 1
        quantity = (order_id + j) % 4 + 1
        price = products[product_id - 1][3]
        items.append((item_id, order_id, product_id, quantity, price))
        item_id += 1

conn.executemany(
    "INSERT INTO order_items VALUES (?, ?, ?, ?, ?)", items
)
conn.commit()

print("OLTP database created")
for table in ("customers", "products", "orders", "order_items"):
    count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table}: {count}")

print("Product 7 stock:", conn.execute(
    "SELECT stock FROM products WHERE product_id=7"
).fetchone()[0])
conn.close()
