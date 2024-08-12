""" Picking the variables from 'ini' configure file. """
import configparser
from pathlib import Path

DIR_ROOT = Path(__file__).parent.parent.resolve()
DIR_APP = DIR_ROOT / "app"
DIR_TEMP = DIR_ROOT / "temp"
DIR_STATIC = DIR_ROOT / "static"


class IniSection(configparser.ConfigParser):
    @property
    def section(self):
        return self._sections


class Vars:
    def __init__(self) -> None:
        """ Reads the config file and matches its variables. """

        configs = IniSection()
        configs.read("vars.ini", "utf-8")
        parser = configs["VARS"].parser
        headers = parser.sections()

        sources = []
        for net_type in ["WIFI", "DLAN", "INET"]:
            sources += [source for source in headers if net_type in source]

        self.hosts = {
            source: parser.section[f"{source}"] for source in sources
        }
        self.telegram_users = {
            user: tid for user, tid in parser.section["TELEGRAM_USERS"].items()
        }
        self.viber_users = {
            user: vid for user, vid in parser.section["VIBER_USERS"].items()
        }
        self.viber_configs = {
            par.upper(): value for par, value in parser.section["VIBER_CONFIGS"].items()
        }
        self.telegram_configs = {
            par.upper(): value for par, value in parser.section["TELEGRAM_CONFIGS"].items()
        }
        self.messages = {
            source: parser.section["MESSAGES"][f"{source.lower()}"] for source in self.hosts
        }
        self.sendings = {
            source: False for source in self.hosts
        }


allvars = Vars()
