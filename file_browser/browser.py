import os
import readchar
from rich.console import Console
from .utils import list_entries
from .preview import SelectionMeta
from .rendering import render_left, render_info, render_controls
import console_manager
from menu import clear_terminal

console = console_manager.console


def file_browser(start_dir=None):
    cwd = os.path.abspath(start_dir or os.getcwd())
    entries = list_entries(cwd)
    sel = 0
    offset = 0
    max_visible = 7

    while True:
        clear_terminal()
        entries = list_entries(cwd)
        sel = max(0, min(sel, len(entries) - 1))
        if sel < offset:
            offset = sel
        elif sel >= offset + max_visible:
            offset = sel - max_visible + 1

        left_panel = render_left(entries, sel, offset, max_visible)
        meta = SelectionMeta(entries[sel][1] if entries else cwd)
        info_panel = render_info(meta)
        controls_panel = render_controls()

        console.print(left_panel)
        console.print(info_panel)
        console.print(controls_panel)
        console.print(console_manager.render_console())

        key = readchar.readkey()
        console_manager.log(repr(key))
        if key == readchar.key.UP:
            sel = (sel - 1) % len(entries) if entries else 0
        elif key == readchar.key.DOWN:
            sel = (sel + 1) % len(entries) if entries else 0
        elif key in (readchar.key.ENTER, readchar.key.CR):
            if not entries:
                continue
            name, full, is_dir = entries[sel]
            if is_dir:
                cwd = full
                sel, offset = 0, 0
            else:
                console_manager.log(f"[INFO] File selected: {full}")
                return full
        elif key == readchar.key.ESC or key == "\x1b\x1b":
            return "ESC"
        elif key.lower() == "q":
            exit(0)
        elif key == readchar.key.TAB or key == "\t":
            console_manager.toggle_focus()
