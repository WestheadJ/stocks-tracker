import duckdb

DB_PATH = "sales_tracker.duckdb"


def get_years():
    con = duckdb.connect(DB_PATH)
    rows = con.execute(
        "SELECT DISTINCT year FROM reports ORDER BY year DESC"
    ).fetchall()
    con.close()
    return [int(r[0]) for r in rows]


def get_months(year: int):
    con = duckdb.connect(DB_PATH)
    rows = con.execute(
        """
        SELECT upper(strftime(start_date, '%b')) AS month,
               MIN(start_date) AS first_day
        FROM reports
        WHERE EXTRACT(YEAR FROM start_date) = ?
        GROUP BY upper(strftime(start_date, '%b'))
        ORDER BY first_day
        """,
        (year,),
    ).fetchall()
    con.close()
    return rows


def get_tills(year: int, month: str):
    con = duckdb.connect(DB_PATH)
    rows = con.execute(
        """
        SELECT DISTINCT till
        FROM reports
        WHERE EXTRACT(YEAR FROM start_date) = ?
          AND upper(strftime(start_date, '%b')) = upper(?)
        ORDER BY till
        """,
        (year, month),
    ).fetchall()
    con.close()
    return [r[0] for r in rows]


def get_month_breakdown(year: int, month: str):
    """Return a list of items for the month: Total, Bar, App, then individual tills."""
    tills = get_tills(year, month)

    breakdown = ["Total", "Bar"]

    # App tills (MOA or App in name)
    app_tills = [t for t in tills if "MOA" in t.upper() or "APP" in t.upper()]
    if app_tills:
        breakdown.append(f"App ({', '.join(app_tills)})")

    # Add remaining individual tills
    breakdown.extend([t for t in tills if t not in app_tills])
    return breakdown
