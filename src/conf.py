import configparser
import os
import re
import time
from typing import Tuple, Dict
from signal import CTRL_C_EVENT, SIGTERM

from anyWinService import homeDir

from loguru import logger


__all__ = ("cfg", "task", "log")


class FakeMatch:
    def __init__(self, match):
        self.match = match

    def group(self, name):
        return self.match.group(name).lower()


class FakeRe:
    def __init__(self, regex):
        self.regex = regex

    def match(self, text):
        m = self.regex.match(text)
        if m:
            return FakeMatch(m)
        return None


class Task:
    def __init__(self, exe: str, exeKey: str, exePath: str, stopSignal: str):
        self._stopSignalMap: Dict[str, int] = {"ctr+c": CTRL_C_EVENT, "kill": SIGTERM}

        try:
            self.stopSignal = self._stopSignalMap[stopSignal]
        except KeyError:
            k = ", ".join(self._stopSignalMap.keys())
            raise KeyError(f"wrong key for stopSignal. Available: {k}")

        self.exe = exe
        self.exeKey = exeKey
        self.exePath = exePath


def lowcase_sections(
    parser: configparser.RawConfigParser,
) -> configparser.RawConfigParser:
    parser.SECTCRE = FakeRe(re.compile(r"\[ *(?P<header>[^]]+?) *]"))
    return parser


def write_section(section: str, params: dict) -> bool:
    try:
        with open(f"{homeDir}{cfgFileName}", "a") as configFile:
            configFile.write(f"\n[{section}]\n")
            for k, v in params.items():
                configFile.write(f"{k} = {v}\n")

        return True
    except Exception as e:
        print(f"Can't write to {cfgFileName}: {e}")
        return False


def open_config() -> configparser.RawConfigParser:
    if not os.path.exists(f"{homeDir}{cfgFileName}"):
        with open(f"{homeDir}{cfgFileName}", "tw", encoding="utf-8") as _:
            pass

    config = configparser.RawConfigParser(
        comment_prefixes=(["//", "#", ";"]), allow_no_value=True
    )
    config = lowcase_sections(config)

    try:
        config.read(f"{homeDir}{cfgFileName}")
    except Exception as e:
        print(f"Fail to read configuration file: {e}")
        time.sleep(3)
        raise SystemExit(1)
    return config


def get_svc_params() -> Tuple[str, str, str]:
    try:
        return (
            cfg.get("service", "Name"),
            cfg.get("service", "DisplayName"),
            cfg.get("service", "Description"),
        )
    except Exception as e:
        e = f"incorrect parameters in [Service]: {e}"
        print(e)
        time.sleep(3)
        raise SystemExit(1)


def get_task(config: configparser) -> Task:
    return Task(
        config.get("app", "exe"),
        config.get("app", "exeKey"),
        config.get("app", "exePath"),
        config.get("app", "stopSignal"),
    )


def create_logger(config: configparser) -> logger:
    logMaxSizeMb = config.getint("logger", "logMaxSizeMb")
    logMaxSizeMb = f"{logMaxSizeMb} MB"
    logMaxFiles = config.getint("logger", "logMaxFiles")
    assert logMaxFiles > 0, ValueError("logMaxFiles mast be > 0")

    if config.getboolean("logger", "enable"):
        level = "INFO"
    else:
        level = "WARNING"

    logger.add(
        f"{homeDir}app.log",
        rotation=logMaxSizeMb,
        retention=logMaxFiles,
        compression="zip",
        level=level,
        format="<green>{time}</green> <level>{message}</level>",
    )
    return logger


if __name__ != "__main__":
    cfgFileName = "settings.cfg"
    cfg = open_config()
    log = create_logger(cfg)
    task = get_task(cfg)
    print("starting...")
