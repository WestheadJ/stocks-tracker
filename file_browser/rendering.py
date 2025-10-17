from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from .utils import human_size


def render_left(entries, selection, offset=0, max_visible=7):
    t = Table.grid(expand=True)

    start = offset
    end = min(offset + max_visible, len(entries))
    for i in range(start, end):
        name, _, is_dir = entries[i]
        icon = "📁" if is_dir else "📄"
        is_sel = i == selection
        prefix = "➤ " if is_sel else "   "
        style = "bold cyan" if is_sel else ""
        t.add_row(Text(f"{prefix}{icon} {name}", style=style))

    total = len(entries)
    a = start + 1 if total else 0
    b = end
    pos = selection + 1 if total else 0
    subtitle = f"Items {a}-{b} of {total} • Pos {pos}/{total}"

    return Panel(
        t,
        title="Directories & .xlsx",
        subtitle=subtitle,
        subtitle_align="right",
        border_style="cyan",
    )


def render_info(meta):
    parts = [f"[bold]Path:[/bold] {meta.path}"]
    if meta.size is not None:
        parts.append(f"[bold]Size:[/bold] {human_size(meta.size)}")
    if meta.rows is not None and meta.cols is not None:
        parts.append(f"[bold]Shape:[/bold] {meta.rows}×{meta.cols}")

    txt = Text.from_markup(" | ".join(parts))  # <-- parse markup correctly
    return Panel(txt, title="Info", border_style="green")


def render_controls():
    txt = Text.from_markup(
        "[bold]↑/↓[/bold] Navigate | "
        "[bold]Enter[/bold] Open/Select | "
        "[bold]Esc[/bold] Back | "
        "[bold]q[/bold] Quit"
    )
    txt.justify = "center"
    return Panel(txt, title="Controls", border_style="yellow")
