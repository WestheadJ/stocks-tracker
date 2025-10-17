import pandas as pd
from datetime import date
from .utils import clean_file
import console_manager


class ImportFile:
    def __init__(self, path):
        console_manager.log(path)
        file = self.read_file(path)
        self.path = path
        self.till = file["till"]
        self.start_date = file["start_date"]
        self.end_date = file["end_date"]
        self.period = file["period"]
        self.df = file["df"]

    def read_file(self, path):
        df = pd.read_excel(path)
        start_date = (
            df.iloc[3, 0][16:].split("-")[0].strip(" ").replace("/", "-").split("-")
        )
        start_date = f"{start_date[2]}-{start_date[1]}-{start_date[0]}"
        print(start_date)
        end_date = (
            df.iloc[3, 0][16:].split("-")[1].strip(" ").replace("/", "-").split("-")
        )
        end_date = f"{end_date[2]}-{end_date[1]}-{end_date[0]}"

        print(end_date)
        period = date.fromisoformat(start_date).strftime("%b").upper()
        till = df.iloc[5, 0].split(":")[1].strip(" ")
        df = clean_file(path)
        return {
            "till": till,
            "start_date": start_date,
            "end_date": end_date,
            "period": period,
            "df": df,
        }

    def close(self):
        if hasattr(self, "df"):
            del self.df
        self.path = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
