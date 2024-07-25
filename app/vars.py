import configparser


config = configparser.ConfigParser()
config.read("piconf.ini", "utf-8")

ip_prefix = config["IP"]["IPPRF"]
al_prefix = config["MESSAGES"]["PREFIX"]

plants = {
    "RPV06": (config["IP"]["RPV06"].split(",")),
    "RPV07": (config["IP"]["RPV07"].split(",")),
    "RPV09": (config["IP"]["RPV09"].split(",")),
    "RPV12": (config["IP"]["RPV12"].split(",")),
    "RPV13": (config["IP"]["RPV13"].split(",")),
}

messages = {
    "RPV06": config["MESSAGES"]["RPV06"],
    "RPV07": config["MESSAGES"]["RPV07"],
    "RPV09": config["MESSAGES"]["RPV09"],
    "RPV12": config["MESSAGES"]["RPV13"],
    "RPV13": config["MESSAGES"]["RPV13"],
}
