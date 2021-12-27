import datetime as dtime
import sys
import os


__version__ = "1.0.0.0"

__all__ = (
    "os",
    "sys",
    "dtime",
    "win32event",
    "win32service",
    "win32serviceutil",
    "servicemanager",
    "Daemonize",
    "__version__",
    "homeDir",
    "appName",
    "sout",
    "PLATFORM",
)

# Windows запускает модули exe из папки пользователя
# Папка должна определяться только исполняемым файлом
keys = os.path.split(os.path.abspath(os.path.join(os.curdir, __file__)))
appName: str = keys[1][: keys[1].find(".")].lower()
homeDir: str = sys.argv[0][: sys.argv[0].replace("\\", "/").rfind("/") + 1]

win32event = None
win32service = None
win32serviceutil = None
servicemanager = None
Daemonize = None


def sout(msg: any, clr: str = "white"):
    """
    :param msg: message
    :param clr: colors available: white|green|sun|violet|breeze|red
    """
    colors = {
        "white": "\x1b[37m",
        "green": "\x1b[0;30;32m",
        "sun": "\033[93m",
        "violet": "\x1b[0;30;35m",
        "breeze": "\x1b[0;30;36m",
        "red": "\x1b[0;30;31m",
    }

    print(f"{colors[clr]}{msg}\x1b[0m")


if os.name == "nt":
    import win32event
    import win32service
    import win32serviceutil
    import servicemanager

    PLATFORM = "nt"
else:
    # TODO supporting
    # from deamonizer import Daemonize  # custom wrapper
    PLATFORM = "posix"
