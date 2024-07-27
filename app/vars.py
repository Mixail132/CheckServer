import configparser


class IniSection(configparser.ConfigParser):
    @property
    def section(self):
        return self._sections


config_sections = IniSection()
config_sections.read("vars.ini", "utf-8")
parser = config_sections["VARS"].parser


class Plant:
    hosts: dict
    messages: dict
    sources: list
    alarms: dict
    sendings: dict
    users: dict
    tokens: dict


plants = Plant()

plants.sources = [source for source in parser.section.keys() if "RPV" in source or "VRU" in source]
plants.users = {user: tg_id for user, tg_id in parser.section["USERS"].items()}
plants.tokens = {social_media: token for (social_media, token) in parser.section["TOKENS"].items()}

plants.hosts = {}
for source in plants.sources:
    plants.hosts[source] = parser.section[f"{source}"]

plants.messages = {}
for source in plants.sources:
    plants.messages[source] = parser.section["MESSAGES"][f"{source.lower()}"]

