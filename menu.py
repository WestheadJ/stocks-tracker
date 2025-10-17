import readchar, os, platform
from rich.console import Console
from rich.panel import Panel
from console_manager import console, render_console


def clear_terminal():
    """Cross-platform terminal clear."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear && printf '\033[3J'")


class Menu:
    def __init__(self, title, options):
        """
        Interactive Menu.
        :param title: Title of the menu panel
        :param options: List of (description, callback) tuples
        """
        self.title = title
        self.options = options
        self.current_index = 0
        self.running = True

    def display(self):
        """Render the menu with the current selection highlighted."""
        clear_terminal()

        menu_text = ""
        for i, (desc, _) in enumerate(self.options):
            if i == self.current_index:
                menu_text += f"[reverse] {desc} [/reverse]\n"
            else:
                menu_text += f"  {desc}\n"

        panel = Panel(
            menu_text,
            title=self.title,
            border_style="blue",
            expand=True,
        )

        console.print(panel)
        render_console()  # ✅ show global console at the bottom

    def run(self):
        """Main loop to handle key input and execute options."""
        while self.running:
            self.display()
            key = readchar.readkey()

            if key == readchar.key.UP:
                self.current_index = (self.current_index - 1) % len(self.options)
            elif key == readchar.key.DOWN:
                self.current_index = (self.current_index + 1) % len(self.options)
            elif key == readchar.key.ENTER:
                _, callback = self.options[self.current_index]
                callback()
                self.display()
            elif key.lower() == "q":
                self.running = False
                break
