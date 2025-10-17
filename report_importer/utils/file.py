import pandas as pd
from console_manager import console


def read_report(path):
    """
    Reads the report with pandas

        Parameters:
            - path (string): Path name of file to be read

        Returns:
            - df (dataframe): The dataframe of the file just read
    """
    df = pd.read_excel(path)
    return df


def strip_data(df):
    """
    Strips essential header data from the reports

        Parameters:
            - df (dataframe): The dataframe you're wanting to strip

        Returns:
            - till (string): The till the report comes from
            - start_date (string): this is the start date of the report
            - end_date (string): this is the end date of the report
            - period (string): the month of the report
    """
    start_date = (
        df.iloc[3, 0][16:].split("-")[0].strip(" ").replace("/", "-").split("-")
    )
    start_date = f"{start_date[2]}-{start_date[1]}-{start_date[0]}"

    end_date = df.iloc[3, 0][16:].split("-")[1].strip(" ").replace("/", "-").split("-")
    end_date = f"{end_date[2]}-{end_date[1]}-{end_date[0]}"
    period = date.fromisoformat(start_date).strftime("%b").upper()
    till = df.iloc[5, 0].split(":")[1].strip(" ")
    return till, start_date, end_date, period


def clean_frame(df):
    df.truncate(before=8)

    print("In progress")
