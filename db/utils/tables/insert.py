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
    df.rename(
        columns={
            "Product Division": "product_division",
            "Category": "category",
            "Sub Category": "sub_category",
            "Product Name": "product_name",
            "Portion": "portion",
        },
        inplace=True,
    )
    conn.register("new_products", df)
    conn.execute(
        """
        INSERT INTO products (product_division, category, sub_category, product_name, portion)
        SELECT np.product_division, np.category, np.sub_category, np.product_name, np.portion
        FROM new_products np
        LEFT JOIN products p
        ON  np.product_division = p.product_division
        AND np.category = p.category
        AND np.sub_category = p.sub_category
        AND np.product_name = p.product_name
        AND np.portion = p.portion
        WHERE p.product_id IS NULL;  -- only insert new rows
    """
    )

    # Unregister after use (optional cleanup)
    conn.unregister("new_products")


def add_sales(conn, df, till_id, report_id, start_date, end_date):
    # TODO: Add the sales getting the till_id, report_id
    df = df.rename(
        columns={
            "Product Name": "product_name",
            "Portion": "portion",
            "Quantity Sold": "quantity_sold",
        }
    )

    # 2️⃣ Register the DataFrame
    conn.register("new_sales", df)

    # 3️⃣ Insert matching product IDs
    conn.execute(
        """
        INSERT INTO sales (
            product_id, sale_start_date, sale_end_date,
            quantity_sold, report_id, till_id
        )
        SELECT 
            p.product_id,
            ? AS sale_start_date,
            ? AS sale_end_date,
            ns.quantity_sold,
            ? AS report_id,
            ? AS till_id
        FROM new_sales ns
        JOIN products p
          ON  p.product_name = ns.product_name
          AND p.portion = ns.portion;
    """,
        [start_date, end_date, report_id, till_id],
    )

    # 4️⃣ Unregister the DataFrame
    conn.unregister("new_sales")
