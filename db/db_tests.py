import duckdb
import argparse

DB_PATH = "sales_tracker.duckdb"


def list_products(con):
    rows = con.execute("SELECT * FROM products ORDER BY product_id").fetchall()
    print(f"\n[Products] Total: {len(rows)}")
    for r in rows:
        print(r)


def list_reports(con):
    rows = con.execute("SELECT * FROM reports ORDER BY report_id").fetchall()
    print(f"\n[Reports] Total: {len(rows)}")
    for r in rows:
        print(r)


def list_sales(con):
    rows = con.execute("SELECT * FROM sales ORDER BY sale_id").fetchall()
    print(f"\n[Sales] Total: {len(rows)}")
    for r in rows:
        print(r)


def main():
    parser = argparse.ArgumentParser(description="Test contents of DuckDB database")
    parser.add_argument("-sp", action="store_true", help="Show all products")
    parser.add_argument("-sr", action="store_true", help="Show all reports")
    parser.add_argument("-ss", action="store_true", help="Show all sales")
    args = parser.parse_args()

    con = duckdb.connect(DB_PATH)

    if args.sp:
        list_products(con)
    if args.sr:
        list_reports(con)
    if args.ss:
        list_sales(con)

    if not (args.sp or args.sr or args.ss):
        print("No argument passed. Use -sp (products), -sr (reports), -ss (sales).")

    con.close()


if __name__ == "__main__":
    main()
