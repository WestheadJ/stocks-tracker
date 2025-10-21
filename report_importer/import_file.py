import pandas as pd
from datetime import date
from .utils.file import read_report, strip_data, clean_frame
import console_manager


def start_import(file):
    df = read_report(file)
    till, start_date, end_date, period = strip_data()
    df = clean_frame(df)
