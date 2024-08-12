""" Picking the variables from 'ini' configure file. """
import configparser
from pathlib import Path
from dataclasses import dataclass
from typing import Any

DIR_ROOT = Path(__file__).parent.parent.resolve()
DIR_APP = DIR_ROOT / "app"
DIR_TEMP = DIR_ROOT / "temp"
DIR_STATIC = DIR_ROOT / "static"


class IniSection(configparser.ConfigParser):
    """ Makes the builtin method to be returned. """
    @property
    def section(self):
        """ Returns the builtin method. """
        return self._sections


@dataclass
class Vars:
    """ Keeps all the configuration variables. """
    viber_configs: dict[Any, Any]
    viber_users: dict[Any, Any]
    viber_configs: dict[Any, Any]
    telegram_users: dict[Any, Any]
    telegram_configs: dict[Any, Any]
    hosts: dict[Any, Any]
    sendings: dict[Any, Any]
    messages: dict[Any, Any]


configs = IniSection()
configs.read("vars.ini", "utf-8")
parser = configs["VARS"].parser
headers = parser.sections()
sources = []
for net_type in ["WIFI", "DLAN", "INET"]:
    sources += [source for source in headers if net_type in source]


hosts = {source: parser.section[f"{source}"] for source in sources}
telegram_users = dict(parser.section["TELEGRAM_USERS"].items())
viber_users = dict(parser.section["VIBER_USERS"].items())
telegram_configs = {par.upper(): value for par, value in parser.section["TELEGRAM_CONFIGS"].items()}
viber_configs = {par.upper(): value for par, value in parser.section["VIBER_CONFIGS"].items()}
messages = {source: parser.section["MESSAGES"][f"{source.lower()}"] for source in hosts}
sendings = {source: False for source in hosts}


allvars = Vars(
    hosts=hosts,
    telegram_users=telegram_users,
    viber_users=viber_users,
    telegram_configs=telegram_configs,
    viber_configs=viber_configs,
    messages=messages,
    sendings=sendings
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
