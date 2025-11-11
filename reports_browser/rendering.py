from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def render_panel(
    console, entries, selection, offset=0, max_visible=7, title="Reports Browser"
):
    """Render left navigation panel."""
    tbl = Table.grid(expand=True)

    start = offset
    end = min(offset + max_visible, len(entries))

    for i in range(start, end):
        entry = entries[i]
        prefix = "➤ " if i == selection else "   "
        style = "bold cyan" if i == selection else ""
        tbl.add_row(Text(f"{prefix} {entry}", style=style))
    total = len(entries)
    subtitle = f"entries {start+1}-{end} of {total} • Pos {selection+1}/{total}"
    console.print(Panel(tbl, title=title, subtitle=subtitle, border_style="cyan"))


def render_info(entry):
    """Display info about the selected node."""
    if "report_id" in entry:
        text = f"[bold]Report:[/bold] {entry['filename']} | [bold]Till:[/bold] {entry['till']} | [bold]Start:[/bold] {entry['start_date']} | [bold]End:[/bold] {entry['end_date']}"
    else:
        text = f"[bold]{entry['name']}[/bold]"
    return Panel(Text.from_markup(text), title="Info", border_style="green")


def render_controls():
    """Controls panel."""
    controls = Text.from_markup(
        "[bold]↑/↓[/bold] Navigate  [bold]Enter[/bold] Expand/Select  [bold]Esc[/bold] Back  [bold]q[/bold] Quit  [bold]Tab[/bold] Toggle Console"
    )
    return Panel(controls, title="Controls", border_style="yellow")
