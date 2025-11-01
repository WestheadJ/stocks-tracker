import readchar
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from console_manager import log, render_console
from .utils import get_years, get_months, get_month_breakdown
from menu import clear_terminal
from .rendering import render_left

console = Console()


def render_controls():
    controls = Text.from_markup(
        "[bold]↑/↓[/bold] Navigate  [bold]Enter[/bold] Expand/Select  [bold]Esc[/bold] Back  [bold]q[/bold] Quit "
    )
    return Panel(controls, title="Controls", border_style="yellow")


def reports_browser():
    level = 0  # 0=Years, 1=Months, 2=Breakdown
    current_year = None
    current_month = None
    index = 0

    year_index = 0  # track current year selection for going back to all years

    while True:
        clear_terminal()

        # --- Determine current items and title ---
        if level == 0:
            items = get_years()
            title = "Reports Browser - Years"
        elif level == 1:
            items = [m[0] for m in get_months(current_year)]
            title = f"Reports Browser - {current_year}"
        elif level == 2:
            items = get_month_breakdown(current_year, current_month)
            title = f"Reports Browser - {current_year} {current_month}"
        entries = [".."]
        for each in items:
            entries.append(each)
        # --- Render controls and console ---
        left_panel = render_left(entries, index, 0, 7)
        console.print(left_panel)
        controls_panel = render_controls()
        console.print(controls_panel)
        console.print(render_console())

        # --- Handle keys ---
        key = readchar.readkey()
        if key == readchar.key.UP:
            index = (index - 1) % len(entries)
        elif key == readchar.key.DOWN:
            index = (index + 1) % len(entries)
        elif key == readchar.key.ENTER:
            if index == 0:
                index = 0
                if level != 0:
                    level -= 1
                else:
                    level = 0
            else:
                if level == 0:
                    current_year = entries[index]
                    level = 1
                    index = 0
                elif level == 1:
                    current_month = entries[index]
                    level = 2
                    index = 0
                elif level == 2:
                    return {
                        "current_year": current_year,
                        "current_month": current_month,
                        "breakdown": entries[index],
                    }
        elif key == readchar.key.ESC or key == "\x1b\x1b":
            return "ESC"
        elif key.lower() == "q":
            return None
