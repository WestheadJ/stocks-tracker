import readchar
import duckdb
from console_manager import log, console
from db.db_setup import DB_NAME
import pandas as pd


def clean_file(path: str) -> pd.DataFrame:
    df = pd.read_excel(path, skiprows=8)  # skip header row

    # Drop rows that are subtotal/category total junk
    df = df[~df["Product Name"].str.contains("Total", na=False)]

    # Clean numeric columns
    for col in ["Quantity Sold", "Value of Sales", "Net Value of Sales"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)  # remove commas
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Keep only the useful fields
    df = df[
        [
            "Product Division",
            "Category",
            "Sub Category",
            "Product Name",
            "Portion",  # 👈 new
            "Quantity Sold",
            "Value of Sales",
            "Net Value of Sales",
        ]
    ]

    return df


def prompt_duplicate_action(duplicates):
    log(f"[yellow]Found {len(duplicates)} duplicate report(s).[/yellow]")
    print("\nDuplicate reports detected:")
    for rid, s, e in duplicates:
        print(f" - Report {rid} ({s} → {e})")

    print("\nOptions:")
    print("  [r] Replace all duplicates")
    print("  [s] Skip all duplicates")
    print("  [i] Handle individually")
    print("  [c] Cancel import")

    while True:
        key = readchar.readkey().lower()
        mapping = {
            "r": "replace_all",
            "s": "skip_all",
            "i": "individual",
            "c": "cancel",
        }
        if key in mapping:
            return mapping[key]


def save_import(importer):
    """Save cleaned ImportFile into DuckDB with duplicate handling"""
    con = duckdb.connect(DB_NAME)
    duplicates = con.execute(
        "SELECT report_id, start_date, end_date FROM reports WHERE till=? AND start_date=? AND end_date=?",
        (importer.till, importer.start_date, importer.end_date),
    ).fetchall()

    if duplicates:
        action = prompt_duplicate_action(duplicates)
        if action == "cancel":
            log("[red]Import cancelled by user.[/red]")
            con.close()
            return
        elif action == "skip_all":
            skipped = ", ".join(str(rid) for rid, _, _ in duplicates)
            log(
                f"[yellow]Skipped import. Duplicate reports untouched: {skipped}[/yellow]"
            )
            con.close()
            return
        elif action == "replace_all":
            for rid, _, _ in duplicates:
                con.execute("DELETE FROM sales WHERE report_id=?", (rid,))
                con.execute("DELETE FROM reports WHERE report_id=?", (rid,))
                log(f"[yellow]Replaced report {rid}[/yellow]")
        elif action == "individual":
            for rid, s, e in duplicates:
                print(f"\nDuplicate Report {rid} ({s} → {e})")
                print("Options: [r] Replace | [s] Skip | [c] Cancel")
                while True:
                    key = readchar.readkey().lower()
                    if key == "r":
                        con.execute("DELETE FROM sales WHERE report_id=?", (rid,))
                        con.execute("DELETE FROM reports WHERE report_id=?", (rid,))
                        log(f"[yellow]Replaced report {rid}[/yellow]")
                        break
                    elif key == "s":
                        log(f"[yellow]Skipped duplicate report {rid}[/yellow]")
                        break
                    elif key == "c":
                        log("[red]Import cancelled by user.[/red]")
                        con.close()
                        return

    # Insert report row
    report_id = con.execute(
        """
        INSERT INTO reports (month, year, start_date, end_date, till, filename)
        VALUES (?, ?, ?, ?, ?, ?) RETURNING report_id
    """,
        (
            importer.period,
            int(importer.start_date[:4]),
            importer.start_date,
            importer.end_date,
            importer.till,
            importer.path,
        ),
    ).fetchone()[0]
    log(f"[cyan]Report ID {report_id} created.[/cyan]")

    # Insert sales
    sales_rows = []
    for _, row in importer.df.iterrows():
        # Insert or fetch product
        pname = row["Product Name"]
        prod = con.execute(
            "SELECT product_id FROM products WHERE product_name=?", (pname,)
        ).fetchone()
        if prod:
            pid = prod[0]
        else:
            pid = con.execute(
                """
                INSERT INTO products (product_division, category, sub_category, product_name, portion)
                VALUES (?, ?, ?, ?, ?) RETURNING product_id
            """,
                (
                    row.get("Product Division"),
                    row.get("Category"),
                    row.get("Sub Category"),
                    pname,
                    row.get("Portion", ""),
                ),
            ).fetchone()[0]

        sales_rows.append(
            (
                pid,
                importer.start_date,
                importer.end_date,
                int(row.get("Quantity Sold", 0)),
                float(row.get("Value of Sales", 0)),
                float(row.get("Net Value of Sales", 0)),
                report_id,
                importer.till,
            )
        )

    if sales_rows:
        con.executemany(
            """
            INSERT INTO sales (product_id, sale_start_date, sale_end_date, quantity_sold, value_of_sales, net_value_of_sales, report_id, till)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            sales_rows,
        )

    for sale in sales_rows[0:10]:
        log(sale)
    con.close()
