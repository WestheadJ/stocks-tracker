from console_manager import console


def drop_all_sequences(conn):
    console.print("[red]Resetting database...[/red]")
    conn.execute("DROP SEQUENCE IF EXISTS seq_products")
    conn.execute("DROP SEQUENCE IF EXISTS seq_sales")
    conn.execute("DROP SEQUENCE IF EXISTS seq_reports")
    conn.execute("DROP SEQUENCE IF EXISTS seq_tills")

    console.print("[chartreuse1]Database Reset![/chartreuse1]")


def create_sequences(conn):
    console.print("[lightsalmon1]Creating sequences...[/lightsalmon1]")
    conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_products START 1")
    conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_sales START 1")
    conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_reports START 1")
    conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_tills START 1")
    console.print("[chartreuse1]Created Sequences![/chartreuse1]")
