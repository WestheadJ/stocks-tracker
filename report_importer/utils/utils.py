""" """

import readchar
import duckdb
from console_manager import log

import pandas as pd


def check_for_existing_report(conn, period, year):

    exists = conn.execute(
        "SELECT EXISTS(SELECT 1 FROM reports WHERE year = ? AND month =?) AS exists_flag;",
        [year, period],
    )
    if exists:
        return True
    else:
        return False


def check_for_till(conn, till):
    exists = conn.execute("INSERT")
