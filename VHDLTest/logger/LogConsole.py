from typing import Any
import colorama
from .LogWriter import LogWriter
from .LogItem import LogItem


class LogConsole(LogWriter):

    def __init__(self) -> None:
        colorama.init()

    def close(self) -> None:
        pass

    def write(self, *items: Any) -> None:
        for item in items:
            if type(item) is LogItem:
                if item == LogItem.END:
                    print(colorama.Style.RESET_ALL, end='')
                elif item == LogItem.SUCCESS:
                    print(colorama.Style.BRIGHT + colorama.Fore.GREEN, end='')
                elif item == LogItem.WARNING:
                    print(colorama.Style.BRIGHT + colorama.Fore.YELLOW, end='')
                elif item == LogItem.ERROR:
                    print(colorama.Style.BRIGHT + colorama.Fore.RED, end='')
                else:
                    raise RuntimeError(f'Unknown item {item}')
            else:
                print(item, end='')
