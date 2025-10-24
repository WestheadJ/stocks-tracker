def add_till(conn, till_name):
    conn.execute(
        """INSERT INTO tills (till_name)
            SELECT ? WHERE NOT EXISTS(
            SELECT 1 FROM tills WHERE till_name=?);""",
        [till_name, till_name],
    )
    return conn.execute(
        "SELECT till_id FROM tills WHERE till_name = ?;", [till_name]
    ).fetchone()[0]


def add_report(conn, month, year, start_date, end_date, till_id, filename):
    conn.execute(
        """INSERT INTO reports(month,year,start_date,end_date,till_id,filename)
        SELECT ?,?,?,?,?,? WHERE  NOT EXISTS
        (SELECT 1 FROM reports WHERE month=? AND year=?);""",
        [
            month,
            year,
            start_date,
            end_date,
            till_id,
            filename,
            month,
            year,
        ],
    )
    return conn.execute(
        "SELECT report_id FROM reports WHERE month = ? AND year=?;", [month, year]
    ).fetchone()[0]


def add_products(conn, df):
    # TODO: Needs to add the products via the df
    print("TODO")
