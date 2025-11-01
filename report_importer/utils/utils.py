""" """

import readchar
import duckdb
from console_manager import log

import pandas as pd


def check_for_existing_report(conn, period, year):

    result = conn.execute(
        "SELECT EXISTS(SELECT 1 FROM reports WHERE year = ? AND month = ?) AS exists_flag;",
        [year, period],
    ).fetchone()[
        0
    ]  # get the actual boolean (0 or 1)

    return bool(result)


def check_for_till(conn, till):
    exists = conn.execute("INSERT")
