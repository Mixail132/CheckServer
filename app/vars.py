import configparser


config = configparser.ConfigParser()
config.read("piconf.ini")

ip_prefix = config["IP"]["IPPRF"]

plants = {
    "RPV06": (config["IP"]["RPV06"].split(",")),
    "RPV07": (config["IP"]["RPV07"].split(",")),
    "RPV09": (config["IP"]["RPV09"].split(",")),
    "RPV12": (config["IP"]["RPV13"].split(",")),
    "RPV13": (config["IP"]["RPV13"].split(",")),
}

messages = {
    "RPV06": config["IP"]["RPV06"],
    "RPV07": config["IP"]["RPV07"],
    "RPV09": config["IP"]["RPV09"],
    "RPV12": config["IP"]["RPV13"],
    "RPV13": config["IP"]["RPV13"],
}
