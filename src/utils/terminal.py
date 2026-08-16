from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text


class Terminal:
    DAWNCODE_BANNER = """\
██████╗  █████╗ ██╗    ██╗███╗   ██╗ ██████╗ ██████╗ ██████╗ ███████╗
██╔══██╗██╔══██╗██║    ██║████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔════╝
██║  ██║███████║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║██║  ██║█████╗
██║  ██║██╔══██║██║███╗██║██║╚██╗██║██║     ██║   ██║██║  ██║██╔══╝
██████╔╝██║  ██║╚███╔███╔╝██║ ╚████║╚██████╗╚██████╔╝██████╔╝███████╗
╚═════╝ ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚══════╝"""

    def __init__(self):
        self.console = Console()

    def show_banner(self):
        self.console.print(self.DAWNCODE_BANNER)

    def user_input(self) -> str:
        return Prompt.ask("[bold magenta]You[/bold magenta]")

    def user(self, message: str):
        text = Text(message, style="bold magenta")
        self.console.print(text)

    def start_assistant(self):
        self.console.print("[bold blue]DawnCode[/bold blue]")

    def stream_assistant(self, content: str):
        self.console.print(
            content,
            style="blue",
            end="",
        )
    def error(self, message: str):
        self.console.print(message, style="bold red")

    def end_assistant(self):
        self.console.print()