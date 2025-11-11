import duckdb
from datetime import datetime

DB_PATH = "sales_tracker.duckdb"


def get_years():
    con = duckdb.connect(DB_PATH)
    rows = con.execute(
        "SELECT DISTINCT year FROM reports ORDER BY year DESC"
    ).fetchall()
    con.close()
    return [int(r[0]) for r in rows]


def get_months(year):
    conn = duckdb.connect("sales_tracker.duckdb")
    query = """
    SELECT
    DISTINCT strftime('%m', r.start_date) AS month_num,
    CASE
        WHEN LOWER(t.till_name) IN ('till_1', 'till_2', 'till_3', 'till_4') THEN 'bar'
        WHEN LOWER(t.till_name) = 'moa 14905' THEN 'app'
        ELSE 'other'
    END AS till_type
FROM reports r
JOIN tills t ON r.till_id = t.till_id
WHERE strftime('%Y', r.start_date) = ?
ORDER BY month_num;
    """

    rows = conn.execute(query, [str(year)]).fetchall()

    if not rows:
        return []
    # Determine which till types exist in the year
    till_types = {row[1] for row in rows}
    months = sorted({f"{int(row[0]):02d}" for row in rows})
    # Convert month numbers to names
    month_names = [
        datetime.strptime(m.zfill(2), "%m").strftime("%b").upper() for m in months
    ]
    # Build list for display
    display_list = []
    if "bar" in till_types and "app" in till_types:
        display_list.append("TOTAL")
        display_list.append("BAR")
        display_list.append("APP")
    elif "bar" in till_types:
        display_list.append("BAR")
    elif "app" in till_types:
        display_list.append("APP")

    display_list.extend(month_names)
    return display_list


def get_tills(year: int, month: str):
    conn = duckdb.connect("sales_tracker.duckdb")
    month_num = datetime.strptime(month, "%b").month  # short month (Jan, Feb, Mar...)
    start_date = f"{year}-{month_num:02d}-01"

    # run parameterized query
    query = """
    SELECT DISTINCT t.till_name
    FROM reports r
    JOIN tills t ON r.till_id = t.till_id
    WHERE r.start_date >= ?
    """

    # execute with parameters
    results = conn.execute(query, [start_date]).fetchall()
    till_names = [row[0] for row in results]

    # print results
    return till_names


def get_month_breakdown(year: int, month: str):
    """Return a list of items for the month: Total, Bar, App, then individual tills."""
    tills = get_tills(year, month)
    breakdown = []
    if len(tills) == 1:
        if tills[0] == "MOA 14905":
            breakdown.append("App")
    else:
        breakdown.append("Total")
        for item in tills:
            if item == "MOA 14905":
                breakdown[0].append("Bar")
                breakdown.append("App")
            breakdown.append(item)

    return breakdown
