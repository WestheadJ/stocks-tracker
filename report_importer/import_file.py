import pandas as pd
import duckdb
from .utils.file import read_report, strip_data, clean_frame
import console_manager
from .utils.utils import check_for_existing_report
from db.db_setup import DB_NAME
from db.utils.tables.insert import add_till


def start_import(file):
    # get a file
    df = read_report(file)
    till, start_date, end_date, period = strip_data(df)
    df = clean_frame(df)
    # check for report
    year = start_date.split("-")[0]

    with duckdb.connect as conn:

        if check_for_existing_report(conn, period, year):
            console_manager.log("Exists")
        else:
            console_manager.log("Doesn't exist preparing to import")

        try:
            add_till(conn, till)
        except:
            conn.execute("ROLLBACK")
            conn.close()
            return

        # Create report

        # Make sure all products exist, if not add them

        # Create sales records
        conn.execute("COMMIT")
        conn.close()
