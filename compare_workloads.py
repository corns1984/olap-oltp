import sqlite3
import time

OLTP_DB = "retail_oltp.db"
OLAP_DB = "retail_olap.db"

def run_query(db_path, query):
    conn = sqlite3.connect(db_path)
    start = time.perf_counter()
    rows = conn.execute(query).fetchall()
    elapsed_ms = (time.perf_counter() - start) * 1000
    conn.close()
    return rows, elapsed_ms

# 1. Aligned OLTP Query (Added status filter to match typical OLAP behavior)
oltp_query = """
SELECT p.category, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
JOIN products p ON p.product_id = oi.product_id
WHERE o.order_date >= '2026-03-01'
  AND o.order_date < '2026-04-01'
  AND o.status = 'COMPLETED'
GROUP BY p.category
ORDER BY p.category
"""

# 2. Aligned OLAP Query 
olap_query = """
SELECT p.category, ROUND(SUM(f.total_amount), 2) AS revenue
FROM fact_sales f
JOIN dim_product p ON p.product_id = f.product_id
WHERE f.date_key >= '2026-03-01'
  AND f.date_key < '2026-04-01'
GROUP BY p.category
ORDER BY p.category
"""

try:
    oltp_rows, oltp_ms = run_query(OLTP_DB, oltp_query)
    olap_rows, olap_ms = run_query(OLAP_DB, olap_query)

    print(f"OLTP joins: 2 | OLAP joins: 1")
    print(f"OLTP time: {oltp_ms:.2f} ms | OLAP time: {olap_ms:.2f} ms")
    
    print("\n--- OLTP Results (Completed Orders) ---")
    for category, revenue in oltp_rows:
        print(f"{category}: {revenue:,.2f}")

    print("\nRESULT CHECK: " + (
        "MATCH - both models give the same answer"
        if oltp_rows == olap_rows
        else "MISMATCH - the models return different results"
    ))
    if oltp_rows != olap_rows:
        print("\nOLTP raw data:", oltp_rows)
        print("OLAP raw data:", olap_rows)
        
except sqlite3.Error as exc:
    print(f"Database query error: {exc}")
    raise
