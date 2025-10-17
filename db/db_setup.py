import duckdb
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from console_manager import log
from db.utils.sequences import drop_all_sequences, create_sequences
from db.utils.tables.tables import (
    drop_all_tables,
    create_products_table,
    create_reports_table,
    create_tills_table,
    create_sales_table,
)

console = Console()
DB_NAME = "sales_tracker.duckdb"


def setup_db(reset: bool = False):
    """Setup or reset the DuckDB database with progress display."""
    conn = duckdb.connect(DB_NAME)

    if reset:
        # Drops tables and sequences
        console.print("[red]Resetting Database...[/red]")
        drop_all_sequences(conn)
        drop_all_tables(conn)
        console.print("[chartreuse1]Tables deleted successfully![/chartreuse1]")
    # Create a spinner
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        transient=True,
        console=console,
    ) as progress:

        progress.add_task("Creating sequences...", total=None)
        create_sequences(conn)

        progress.add_task("Creating products table...", total=None)
        create_products_table(conn)

        progress.add_task("Creating sales table...", total=None)
        create_sales_table(conn)

        progress.add_task("Creating reports table...", total=None)
        create_reports_table(conn)

        progress.add_task("Creating tills table...", total=None)
        create_tills_table(conn)

    log("[green]Database setup complete![/green]")
    conn.close()
