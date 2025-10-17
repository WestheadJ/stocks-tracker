import duckdb
from console_manager import log


def get_connection(db_path="sales_tracker.duckdb"):
    """Open a connection to DuckDB"""
    return duckdb.connect(db_path)


def create_tables(con):
    """Ensure required tables exist"""
    con.execute(
        """
    CREATE TABLE IF NOT EXISTS tills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    );
    """
    )

    con.execute(
        """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_division TEXT,
        category TEXT,
        sub_category TEXT,
        destination TEXT,
        product_name TEXT UNIQUE
    );
    """
    )

    con.execute(
        """
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        till_id INTEGER,
        start_date TEXT,
        end_date TEXT,
        period TEXT,
        UNIQUE(till_id, start_date, end_date),
        FOREIGN KEY (till_id) REFERENCES tills(id)
    );
    """
    )

    con.execute(
        """
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_id INTEGER,
        till_id INTEGER,
        product_id INTEGER,
        value NUMERIC,
        FOREIGN KEY (report_id) REFERENCES reports(id),
        FOREIGN KEY (till_id) REFERENCES tills(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    );
    """
    )

    log("[green]Database tables ensured.[/green]")


def get_or_create_till(con, name: str) -> int:
    """Fetch or insert a till, return its ID"""
    row = con.execute("SELECT id FROM tills WHERE name = ?", (name,)).fetchone()
    if row:
        return row[0]
    return con.execute(
        "INSERT INTO tills (name) VALUES (?) RETURNING id;", (name,)
    ).fetchone()[0]


def get_or_create_product(con, row) -> int:
    """Fetch or insert a product, return its ID"""
    pname = row.get("Product Name")
    if not pname:
        return None

    existing = con.execute(
        "SELECT id FROM products WHERE product_name = ?", (pname,)
    ).fetchone()
    if existing:
        return existing[0]

    return con.execute(
        """
        INSERT INTO products (product_division, category, sub_category, destination, product_name)
        VALUES (?, ?, ?, ?, ?) RETURNING id;
        """,
        (
            row.get("Product Division"),
            row.get("Category"),
            row.get("Sub Category"),
            row.get("Destination"),
            pname,
        ),
    ).fetchone()[0]


def insert_report(con, till_id, start_date, end_date, period) -> int:
    """Insert report row and return its id"""
    return con.execute(
        "INSERT INTO reports (till_id, start_date, end_date, period) VALUES (?, ?, ?, ?) RETURNING id;",
        (till_id, start_date, end_date, period),
    ).fetchone()[0]


def find_duplicates(con, till_id, start_date, end_date):
    """Return all report ids for same till and period"""
    return con.execute(
        "SELECT id, start_date, end_date FROM reports WHERE till_id = ? AND start_date = ? AND end_date = ?",
        (till_id, start_date, end_date),
    ).fetchall()


def delete_report(con, report_id):
    """Delete a report and all its sales"""
    con.execute("DELETE FROM sales WHERE report_id = ?", (report_id,))
    con.execute("DELETE FROM reports WHERE id = ?", (report_id,))
