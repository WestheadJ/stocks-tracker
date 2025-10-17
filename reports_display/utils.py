# reports_display/utils.py
import duckdb
import pandas as pd

DB_PATH = "sales_tracker.duckdb"


def get_report_data(year: int, month: str, report_type: str) -> pd.DataFrame:
    """
    Return a DataFrame with the report data for the given year/month/report_type.
    Handles:
        - Total: sum of all tills for the month
        - Bar: sum of tills 1-4
        - App: MOA / App tills
        - Individual Till
    """
    con = duckdb.connect(DB_PATH)

    if report_type == "Total":
        query = """
            SELECT s.*, r.till, r.start_date, r.end_date
            FROM sales s
            JOIN reports r ON s.report_id = r.report_id
            WHERE r.year = ? AND upper(strftime(r.start_date, '%b')) = ?
        """
        df = con.execute(query, (year, month.upper())).fetchdf()

    elif report_type == "Bar":
        query = """
            SELECT s.*, r.till, r.start_date, r.end_date
            FROM sales s
            JOIN reports r ON s.report_id = r.report_id
            WHERE r.year = ? AND upper(strftime(r.start_date, '%b')) = ?
              AND s.till IN ('Till 1','Till 2','Till 3','Till 4')
        """
        df = con.execute(query, (year, month.upper())).fetchdf()

    elif report_type.upper().startswith("APP"):
        query = """
            SELECT s.*, r.till, r.start_date, r.end_date
            FROM sales s
            JOIN reports r ON s.report_id = r.report_id
            WHERE r.year = ? AND upper(strftime(r.start_date, '%b')) = ?
              AND (upper(s.till) LIKE '%MOA%' OR upper(s.till) LIKE '%APP%')
        """
        df = con.execute(query, (year, month.upper())).fetchdf()

    else:  # individual till
        query = """
            SELECT s.*, r.till, r.start_date, r.end_date
            FROM sales s
            JOIN reports r ON s.report_id = r.report_id
            WHERE r.year = ? AND upper(strftime(r.start_date, '%b')) = ?
              AND s.till = ?
        """
        df = con.execute(query, (year, month.upper(), report_type)).fetchdf()

    con.close()
    return df
