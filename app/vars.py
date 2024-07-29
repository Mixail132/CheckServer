import configparser


class IniSection(configparser.ConfigParser):
    @property
    def section(self):
        return self._sections


class Plant:
    def __init__(self):
        config_sections = IniSection()
        config_sections.read("vars.ini", "utf-8")
        parser = config_sections["VARS"].parser
        self.sources = [source for source in parser.section.keys() if "RPV" in source or "VRU" in source]
        self.telegram_users = {user: tg_id for user, tg_id in parser.section["TELEGRAM_USERS"].items()}
        self.tokens = {social_media: token for social_media, token in parser.section["TOKENS"].items()}
        self.hosts = {source: parser.section[f"{source}"] for source in self.sources}
        self.messages = {source: parser.section["MESSAGES"][f"{source.lower()}"] for source in self.sources}
        self.sendings = {source: False for source in self.sources}


plants = Plant()
