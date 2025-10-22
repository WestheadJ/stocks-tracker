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
    conn.execute("INSERT INTO report")
