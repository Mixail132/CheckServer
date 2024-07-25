import configparser


config = configparser.ConfigParser()
config.read("piconf.ini", "utf-8")

ip_prefix = config["IPS"]["IPPRF"]
al_prefix = config["MESSAGES"]["PREFIX"]
telegramtoken = config["TOKENS"]["TELEGRAMTOKEN"]

plants = {
    "RPV_06": (config["IPS"]["RPV_06"].split(",")),
    "RPV_07": (config["IPS"]["RPV_07"].split(",")),
    "RPV_09": (config["IPS"]["RPV_09"].split(",")),
    "RPV_12": (config["IPS"]["RPV_12"].split(",")),
    "RPV_13": (config["IPS"]["RPV_13"].split(",")),
}


class IniSection(configparser.ConfigParser):
    @property
    def sections(self):
        return self._sections


config_users = IniSection()
config_users.read("piconf.ini", "utf-8")

parser = config_users["USERS"].parser
users = parser.sections["USERS"]
messages = parser.sections["MESSAGES"]

