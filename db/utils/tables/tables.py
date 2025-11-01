from console_manager import console


def drop_all_tables(conn):
    console.print("[red]Deleting tables...[/red]")
    conn.execute("DROP TABLE IF EXISTS products")
    conn.execute("DROP TABLE IF EXISTS sales")
    conn.execute("DROP TABLE IF EXISTS reports")
    conn.execute("DROP TABLE IF EXISTS. tills")
    console.print("[chartreuse1]Tables deleted successfully![/chartreuse1]")


def create_products_table(conn):
    conn.execute(
        """ CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY DEFAULT nextval('seq_products'),
        product_division TEXT NOT NULL,
        category TEXT NOT NULL,
        sub_category TEXT NOT NULL,
        product_name TEXT NOT NULL,
        portion TEXT NOT NULL)"""
    )


def create_sales_table(conn):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY DEFAULT nextval('seq_sales'),
        product_id INTEGER REFERENCES products(product_id),
        sale_start_date DATE NOT NULL,
        sale_end_date DATE NOT NULL,
        quantity_sold INTEGER NOT NULL,
        report_id INTEGER REFERENCES reports(report_id),
        till_id TEXT NOT NULL)"""
    )


def create_tills_table(conn):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS tills(
                till_id INTEGER PRIMARY KEY DEFAULT nextval('seq_tills'),
                till_name TEXT NOT NULL)"""
    )


def create_reports_table(conn):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS reports (
                report_id INTEGER PRIMARY KEY DEFAULT nextval('seq_reports'),
                month TEXT NOT NULL,
                year INTEGER NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                till_id INTEGER REFERENCES tills(till_id),
                filename TEXT NOT NULL)"""
    )
