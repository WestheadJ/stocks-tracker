# reports_display/window.py
import readchar
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from console_manager import log, render_console
from .utils import get_report_data
from menu import clear_terminal

console = Console()


def open_report(year: int, month: str, report_type: str):
    """
    Opens the report display window.
    - year, month: selected report period
    - report_type: Total, Bar, App, or Till X
    """
    # Fetch report data
    data = get_report_data(year, month, report_type)

    focus = 1  # 0=controls, 1=table
    row_offset = 0
    col_offset = 0
    visible_rows = 5
    visible_cols = 7

    while True:
        clear_terminal()

        # --- Render control panel ---
        controls_text = Text.from_markup(
            "[bold]T[/bold] Top-N  [bold]F[/bold] Filter  [bold]S[/bold] Sort  [bold]E[/bold] Export  "
            "[bold]Tab[/bold] Toggle Focus  [bold]Esc[/bold] Back"
        )
        controls_panel = Panel(controls_text, title="Controls", border_style="yellow")
        console.print(controls_panel)

        # --- Render main table viewport ---
        if not data.empty:
            # Limit columns and rows to viewport
            columns_to_show = data.columns[col_offset : col_offset + visible_cols]
            table = Table(expand=True)
            for col in columns_to_show:
                table.add_column(col)
            for row in data.iloc[row_offset : row_offset + visible_rows].itertuples(
                index=False
            ):
                table.add_row(*[str(getattr(row, col)) for col in columns_to_show])
            console.print(table)
        else:
            console.print(Panel("[red]No data for this selection[/red]"))

        # --- Render global console log ---
        console.print(render_console())

        # --- Handle keys ---
        key = readchar.readkey()

        if key.lower() == "q":
            del data
            clear_terminal()
            return

        # Top-N functionality with safe column check
        elif key.lower() == "t":
            if "Sub Category" in data.columns and "Quantity Sold" in data.columns:
                log("[INFO] Top-N activated")
                n = 5  # can later prompt user
                top_data = (
                    data.groupby("Sub Category")["Quantity Sold"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(n)
                )
                table_top = Table(title=f"Top {n} Sub-Categories")
                table_top.add_column("Sub Category")
                table_top.add_column("Quantity Sold")
                for sub_cat, qty in top_data.items():
                    table_top.add_row(sub_cat, str(qty))
                console.clear()
                console.print(table_top)
                console.print(render_console())
            else:
                log(
                    f"[WARN] Columns 'Sub Category' or 'Quantity Sold' not found. Available: {list(data.columns)}"
                )

        elif key.lower() == "f":
            log("[INFO] Filter activated (to implement)")
        elif key.lower() == "s":
            log("[INFO] Sort activated (to implement)")
        elif key.lower() == "e":
            log("[INFO] Export activated (to implement)")

        elif key == readchar.key.TAB:
            focus = 1 - focus  # toggle focus
        elif key == readchar.key.ESC or key == "\x1b\x1b":
            # Cleanup and return to main menu
            del data
            clear_terminal()
            return

        # Scroll table viewport
        elif focus == 1:
            if key == readchar.key.UP:
                row_offset = max(row_offset - 1, 0)
            elif key == readchar.key.DOWN:
                row_offset = min(row_offset + 1, max(0, len(data) - visible_rows))
            elif key == readchar.key.RIGHT:
                col_offset = min(
                    col_offset + 1, max(0, len(data.columns) - visible_cols)
                )
            elif key == readchar.key.LEFT:
                col_offset = max(col_offset - 1, 0)
