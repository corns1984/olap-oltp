# Session History: Database Architecture & Data Engineering

## 1. Environment Navigation & Discovery

```bash
student@SplunkServer:~/ltiws\$ ls
pyproject.toml  src

student@SplunkServer:~/ltiws\$ cd src

student@SplunkServer:~/ltiws/src\$ ls
UNKNOWN.egg-info  build_olap.py  compare_workloads.py  retail_oltp.db  setup_oltp.py  vehicle_app.egg-info
```

## 2. OLTP Database Setup

```bash
student@SplunkServer:~/ltiws/src\$ python3 setup_oltp.py
OLTP database created
customers: 200
products: 50
orders: 5000
order_items: 10061
Product 7 stock: 342

student@SplunkServer:~/ltiws/src\$ python3 setup_oltp.py
STOP: retail_oltp.db already exists. Preserve it and inspect before proceeding.
```

## 3. OLAP Database Initialization & Schema Building (with Errors & Resolution)

```bash
student@SplunkServer:~/ltiws/src\$ python3 build_olap.py
ERROR: retail_olap.db does not exist

student@SplunkServer:~/ltiws/src\$ python3 build_olap.py
Traceback (most recent call last):
  File "/home/student/ltiws/src/build_olap.py", line 12, in <module>
    t: dst.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
sqlite3.OperationalError: no such table: dim_product

student@SplunkServer:~/ltiws/src\$ python3 setup_olap.py
SUCCESS: retail_olap.db created with clean star schema tables.

student@SplunkServer:~/ltiws/src\$ python3 build_olap.py
Traceback (most recent call last):
  File "/home/student/ltiws/src/build_olap.py", line 55, in <module>
    dst.executemany("INSERT INTO fact_sales VALUES (?, ?, ?, ?, ?, ?, ?)", rows)
sqlite3.IntegrityError: FOREIGN KEY constraint failed

student@SplunkServer:~/ltiws/src\$ python3 build_olap.py
  File "/home/student/ltiws/src/build_olap.py", line 46
    rows = src.execute("""
IndentationError: unexpected indent

student@SplunkServer:~/ltiws/src\$ python3 build_olap.py
dim_product: 50
dim_customer: 200
dim_date: 181
fact_sales: 10007
Star schema created
```

## 4. Querying and Database Inspection

```bash
student@SplunkServer:~/ltiws/src\$ python3 sql.py
Usage: python3 sql.py DATABASE "SQL QUERY"

student@SplunkServer:~/ltiws/src\$ python3 sql.py company.db "SELECT id, name, role FROM employees WHERE department = 'IT'"
SQL ERROR: no such table: employees

student@SplunkServer:~/ltiws/src\$ python3 sql.py company.db "SELECT * FROM customers"
SQL ERROR: no such table: customers

student@SplunkServer:~/ltiws/src\$ python3 sql.py retail_oltp.db "SELECT * FROM customers;"
customer_id | customer_name | city
1 | Customer 1 | Pune
...
200 | Customer 200 | Chennai

student@SplunkServer:~/ltiws/src\$ sudo apt install sqlite3
[Installs sqlite3 utility package]

student@SplunkServer:~/ltiws/src\$ sqlite3 retail_olap.db "SELECT COUNT(*) FROM fact_sales;"
0
```

## 5. Workload Performance Comparison & Diagnostics

```bash
student@SplunkServer:~/ltiws/src\$ python3 compare_workloads.py
sqlite3.OperationalError: no such column: f.revenue

student@SplunkServer:~/ltiws/src\$ python3 compare_workloads.py
sqlite3.OperationalError: no such column: f.unit_price

student@SplunkServer:~/ltiws/src\$ python3 compare_workloads.py
OLTP joins: 2 | OLAP joins: 1
OLTP time: 4.29 ms | OLAP time: 0.25 ms

--- OLTP Results ---
Apparel: 1,400,775.00
...
RESULT CHECK: MISMATCH - the models return different results
OLTP raw data: [...]
OLAP raw data: []

student@SplunkServer:~/ltiws/src\$ python3 compare_workloads.py
OLTP joins: 2 | OLAP joins: 1
OLTP time: 2.67 ms | OLAP time: 0.16 ms

--- OLTP Results (Completed Orders) ---
Apparel: 1,301,400.00
...
RESULT CHECK: MISMATCH - the models return different results
OLTP raw data: [...]
OLAP raw data: []
```

## 6. Data Structure & Format Parsing

```bash
student@SplunkServer:~/ltiws/src\$ python3 make_sample_files.py
Created data/store_sales.csv
Created data/clickstream.json
Created data/customer_reviews.txt

student@SplunkServer:~/ltiws/src\$ cat data/clickstream.json
[{"event": "page_view", ...}, ...]

student@SplunkServer:~/ltiws/src\$ python3 classify_data.py
store_sales.csv -> STRUCTURED | 3 rows, fixed columns
clickstream.json -> SEMI-STRUCTURED | 3 records, nested fields
customer_reviews.txt -> UNSTRUCTURED | 3 lines of free text

student@SplunkServer:~/ltiws/src\$ python3 query_json.py
event | user_id | device | loyalty_tier
page_view | U9 | mobile | None
add_to_cart | U9 | mobile | None
search | U4 | web | gold
```

---

## Conceptual Explanation: What We Did

During this session, you walked through two fundamental database architecture and data engineering concepts: **Data Warehousing (OLTP vs. OLAP)** and **Data Variety Classification**.

### Concept A: Moving from OLTP to OLAP (ETL Pipeline)

* **Database Generation:** You started by initializing an OLTP (Online Transaction Processing) database (`retail_oltp.db`). OLTP systems are optimized for fast row-level transactions (like inserting a single customer order).
* **Schema Architecture:** You then created a clean Star Schema inside an OLAP (Online Analytical Processing) target database (`retail_olap.db`). OLAP systems decouple transactional noise into organized `dim_` (dimension tables like customers, dates, and products) and `fact_` (quantifiable sales data metrics) structures.
* **Debugging the ETL (Extract, Transform, Load):** You debugged multiple common script errors during compilation (`build_olap.py`):
    * *Missing Target:* DB errors occur if the schema isn't created first (`setup_olap.py`).
    * *Integrity Constraints:* A `FOREIGN KEY constraint failed` error appeared because a fact row tried referencing a dimension ID that didn't yet exist in a dimension table.
    * *Syntax Check:* Fixed standard formatting issues like Python `IndentationError`.
* **Performance Verification:** You compared processing queries against the transactional structure versus the analytical star schema. The results showed that OLAP reduces table joins and massively improves query execution speeds (e.g., from 2.67 ms down to 0.16 ms), though you encountered a data mismatch bug where your analytical `fact_sales` table was returning empty array outputs (`[]`) despite having structural definitions.

### Concept B: Handling Diverse Data Varieties

You utilized utility tools (`classify_data.py`) to systematically dissect the three main categories of data engineering files:

* **Structured Data (`.csv`):** Rigid tabular formats with fixed columns and rows (`store_sales`).
* **Semi-Structured Data (`.json`):** Data containing flexible, complex key-value configurations with nesting (`clickstream`). You cleanly queried this via a parsing helper script.
* **Unstructured Data (`.txt`):** Loose-form plain sentences (like free-text consumer reviews) containing no predefined programmatic fields.
