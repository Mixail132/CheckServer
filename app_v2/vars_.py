import configparser


class IniSection(configparser.ConfigParser):
    @property
    def section(self):
        return self._sections


class Vars:
    def __init__(self):
        configs = IniSection()
        configs.read("vars_.ini", "utf-8")
        parser = configs["VARS"].parser
        headers = parser.sections()

        sources = []
        for net_type in ["WIFI", "DLAN", "INET"]:
            sources += [source for source in headers if net_type in source]
        self.hosts = {source: parser.section[f"{source}"] for source in sources}

        self.telegram_users = {user: tid for user, tid in parser.section["TELEGRAM_USERS"].items()}
        self.viber_users = {user: vid for user, vid in parser.section["VIBER_USERS"].items()}

        self.viber_configs = {par.upper(): value for par, value in parser.section["VIBER_CONFIGS"].items()}
        self.telegram_configs = {par.upper(): value for par, value in parser.section["TELEGRAM_CONFIGS"].items()}

        self.messages = {source: parser.section["MESSAGES"][f"{source.lower()}"] for source in self.hosts}
        self.sendings = {source: False for source in self.hosts}


allvars = Vars()
