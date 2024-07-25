import configparser


config = configparser.ConfigParser()
config.read("piconf.ini", "utf-8")


class PlantsIPs:
    ip_prefix: str
    ip_addresses: dict


local_net = PlantsIPs()
dispatcher_net = PlantsIPs()

local_net.net = config["LOC_IPS"]["IP_PREFIX"]
local_net.hosts = {
    "RPV_06": (config["LOC_IPS"]["RPV_06"].split(",")),
    "RPV_07": (config["LOC_IPS"]["RPV_07"].split(",")),
    "RPV_09": (config["LOC_IPS"]["RPV_09"].split(",")),
    "RPV_12": (config["LOC_IPS"]["RPV_12"].split(",")),
    "RPV_13": (config["LOC_IPS"]["RPV_13"].split(",")),
}

dispatcher_net.net = config["DIS_IPS"]["IP_PREFIX"]
dispatcher_net.hosts = {
    "VRU_01": (config["DIS_IPS"]["VRU_01"].split(",")),
    "RPV_04": (config["DIS_IPS"]["RPV_04"].split(",")),
    "RPV_10": (config["DIS_IPS"]["RPV_10"].split(",")),
}

alarm_prefix = config["MESSAGES"]["PREFIX"]
telegramtoken = config["TOKENS"]["TELEGRAMTOKEN"]


class IniSection(configparser.ConfigParser):
    @property
    def section(self):
        return self._sections


config_sections = IniSection()
config_sections.read("piconf.ini", "utf-8")

parser = config_sections["USERS"].parser
users = parser.section["USERS"]
messages = parser.section["MESSAGES"]
