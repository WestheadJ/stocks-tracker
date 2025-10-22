def add_till(conn, till):
    conn.execute(
        """INSERT INTO tills (till_name)
            SELECT ? WHERE NOT EXISTS(
            SELECT 1 FROM tills WHERE till_name=?);""",
        [till, till],
    )


def add_report(conn, month, year, start_date, end_date, till_id, filename):
    conn.execute("INSERT INTO report")
