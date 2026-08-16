import asyncio

from src.agent import agent
from src.utils.terminal import Terminal

terminal = Terminal()
terminal.show_banner()

asyncio.run(agent())
