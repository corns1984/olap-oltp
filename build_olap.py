import sqlite3
from pathlib import Path

if not Path("retail_olap.db").exists():
    raise SystemExit("ERROR: retail_olap.db does not exist")

src = sqlite3.connect("retail_oltp.db")
dst = sqlite3.connect("retail_olap.db")

try:
    counts = {
        t: dst.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        for t in ("dim_product", "dim_customer", "dim_date", "fact_sales")
    }
    if any(counts.values()):
        raise SystemExit(f"STOP: OLAP tables are not empty: {counts}")

    dst.execute("PRAGMA foreign_keys = ON")

    dst.executemany(
        "INSERT INTO dim_product VALUES (?, ?, ?, ?)",
        src.execute(
            "SELECT product_id, product_name, category, price FROM products"
        ).fetchall()
    )

    dst.executemany(
        "INSERT INTO dim_customer VALUES (?, ?, ?)",
        src.execute(
            "SELECT customer_id, customer_name, city FROM customers"
        ).fetchall()
    )

    dates = src.execute("""
        SELECT DISTINCT order_date FROM orders
        WHERE order_date BETWEEN '2026-01-01' AND '2026-06-30'
        ORDER BY order_date
    """).fetchall()

    dst.executemany(
        "INSERT INTO dim_date VALUES (?, ?, ?, ?)",
        [(d[0], int(d[0][:4]), int(d[0][5:7]), int(d[0][8:10]))
         for d in dates]
    )

    rows = src.execute("""
        SELECT oi.order_item_id, oi.order_id, oi.product_id,
               o.customer_id, o.order_date, oi.quantity,
               ROUND(oi.quantity * oi.unit_price, 2)
        FROM order_items oi
        JOIN orders o ON o.order_id = oi.order_id
        WHERE o.order_date BETWEEN '2026-01-01' AND '2026-06-30'
        ORDER BY oi.order_item_id
    """).fetchall()

    dst.executemany(
        "INSERT INTO fact_sales VALUES (?, ?, ?, ?, ?, ?, ?)",
        rows
    )

    dst.commit()

    for table in ("dim_product", "dim_customer", "dim_date", "fact_sales"):
        count = dst.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table}: {count}")

    print("Star schema created")

except Exception:
    dst.rollback()
    raise
finally:
    src.close()
    dst.close()
