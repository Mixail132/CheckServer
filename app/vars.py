import configparser


class IniSection(configparser.ConfigParser):
    @property
    def section(self):
        return self._sections


class Vars:
    def __init__(self):
        config_sections = IniSection()
        config_sections.read("vars.ini", "utf-8")
        parser = config_sections["VARS"].parser
        self.sources = [
            source for source in parser.section.keys() if "RPV" in source or "VRU" in source
        ]
        self.hosts = {source: parser.section[f"{source}"] for source in self.sources}
        self.telegram_users = {
            user: tg_id for user, tg_id in parser.section["TELEGRAM_USERS"].items()
        }
        self.viber_users = {
            user: tg_id for user, tg_id in parser.section["VIBER_USERS"].items()
        }
        self.viber_configs = {
            par_name.upper(): par_value for par_name, par_value in parser.section["VIBER_CONFIGS"].items()
        }
        self.tokens = {
            token_name.upper(): token_value for token_name, token_value in parser.section["TOKENS"].items()
        }
        self.messages = {
            source: parser.section["MESSAGES"][f"{source.lower()}"] for source in self.sources
        }
        self.sendings = {
            source: False for source in self.sources
        }


plants = Vars()
for k in plants.checkers:
    print(k)
