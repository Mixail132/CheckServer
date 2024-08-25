""" Picking the variables from 'ini' configure file."""

import configparser
from dataclasses import dataclass
from typing import Any

from app.dirs import DIR_APP


@dataclass
class Vars:
    """Keeps all the config variables."""

    messages: dict[Any, Any]
    hosts: dict[Any, Any]
    sendings: dict[Any, Any]
    viber_configs: dict[Any, Any]
    viber_users: dict[Any, Any]
    telegram_configs: dict[Any, Any]
    telegram_users: dict[Any, Any]


class IniSection(configparser.ConfigParser):
    """Redefine built in methods."""

    def optionxform(self, optionstr):
        """Returns the config keys in the case they are."""
        return optionstr


configs = IniSection()
inifile = DIR_APP / "vars.ini"
obj = configs.read(inifile, "utf-8")

headers = configs.sections()
nets = ["WIFI", "DLAN", "INET"]
sources = []

for net in nets:
    sources += [source for source in headers if net in source]

hosts = {source: dict(configs[f"{source}"].items()) for source in sources}
telegram_users = dict(configs["TELEGRAM_USERS"].items())
viber_users = dict(configs["VIBER_USERS"].items())
telegram_configs = dict(configs["TELEGRAM_CONFIGS"].items())
viber_configs = dict(configs["VIBER_CONFIGS"].items())
sendings = {source: False for source in hosts}
messages = {source: configs["MESSAGES"][f"{source}"] for source in hosts}

allvars = Vars(
    hosts=hosts,
    telegram_users=telegram_users,
    viber_users=viber_users,
    telegram_configs=telegram_configs,
    viber_configs=viber_configs,
    messages=messages,
    sendings=sendings,
)


if __name__ == "__main__":
    print(
        allvars.viber_users,
        allvars.viber_configs,
        allvars.telegram_users,
        allvars.telegram_configs,
        allvars.hosts,
        allvars.sendings,
        allvars.messages,
        sep="\n",
    )
