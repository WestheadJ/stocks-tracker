from rich.console import Console
from rich.panel import Panel

console = Console()
log_history = []  # full log
max_display = 7  # how many lines visible
scroll_index = 0  # scroll offset
focus_console = False  # whether console is focused


def log(message: str):
    """Append message to the log."""
    global log_history, scroll_index
    log_history.append(message)

    # Auto-stick to bottom unless user is scrolling
    if not focus_console:
        scroll_index = 0


def render_console():
    """Render the console log panel."""
    global log_history, scroll_index
    if not log_history:
        text = "[dim]No logs yet...[/dim]"
    else:
        if scroll_index == 0:
            lines = log_history[-max_display:]
        else:
            start = max(0, len(log_history) - max_display - scroll_index)
            end = start + max_display
            lines = log_history[start:end]
        text = "\n".join(lines)

    return Panel(text, title="Console Log", border_style="green", expand=True)


def scroll_up():
    """Scroll console up."""
    global scroll_index
    if len(log_history) > max_display and scroll_index < len(log_history) - max_display:
        scroll_index += 1


def scroll_down():
    """Scroll console down."""
    global scroll_index
    if scroll_index > 0:
        scroll_index -= 1


def toggle_focus():
    """Toggle focus between UI and console."""
    global focus_console
    focus_console = not focus_console
    return focus_console
