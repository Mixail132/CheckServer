""" Picking the variables from 'ini' configure file."""

import configparser
from pathlib import Path

from app.dirs import FILE_VARS


class IniSection(configparser.ConfigParser):
    """Redefine built in methods."""

    def optionxform(self, optionstr):
        """Returns the config keys in the case they are."""
        return optionstr


class Vars:
    """Keeps all the config variables."""

    def __init__(self, config_file: Path) -> None:
        """Reads the variables from a config file."""
        configs = IniSection()
        configs.read(config_file, "utf-8")

        headers = configs.sections()
        nets = ["WIFI", "DLAN", "INET"]
        sources = []

        for net in nets:
            sources += [source for source in headers if net in source]

        self.hosts = {
            source: dict(configs[f"{source}"].items()) for source in sources
        }
        self.telegram_users = dict(configs["TELEGRAM_USERS"].items())
        self.viber_users = dict(configs["VIBER_USERS"].items())
        self.telegram_configs = dict(configs["TELEGRAM_CONFIGS"].items())
        self.viber_configs = dict(configs["VIBER_CONFIGS"].items())
        self.sendings = {source: False for source in self.hosts}
        self.messages = {
            source: configs["MESSAGES"][f"{source}"] for source in self.hosts
        }


if __name__ == "__main__":
    file_vars = FILE_VARS
    all_vars = Vars(file_vars)
    print(
        all_vars.viber_users,
        all_vars.viber_configs,
        all_vars.telegram_users,
        all_vars.telegram_configs,
        all_vars.hosts,
        all_vars.sendings,
        all_vars.messages,
        sep="\n",
    )
