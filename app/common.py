import configparser
import subprocess
import time

import telebot


class IniSection(configparser.ConfigParser):
    @property
    def section(self):
        return self._sections


class Plant:
    def __init__(self):
        config_sections = IniSection()
        config_sections.read("vars.ini", "utf-8")
        parser = config_sections["VARS"].parser
        self.sources = [source for source in parser.section.keys(
        ) if "RPV" in source or "VRU" in source]
        self.users = {
            user: tg_id for user,
            tg_id in parser.section["USERS"].items()}
        self.tokens = {
            social_media: token for social_media,
            token in parser.section["TOKENS"].items()}
        self.hosts = {
            source: parser.section[f"{source}"] for source in self.sources}
        self.messages = {
            source: parser.section["MESSAGES"][f"{source.lower()}"] for source in self.sources}
        self.sendings = {source: False for source in self.sources}


plants = Plant()


telegramtoken = plants.tokens["telegramtoken"]
bot = telebot.TeleBot(telegramtoken)


def send_alarm_message(message_text):
    for user in plants.users.values():
        bot.send_message(user, message_text)


def is_server_out(ip_addr):
    command = ["ping", "-n", "2", ip_addr,]
    subprocess.run(
        ["chcp", "437"],
        shell=True,
        stdout=subprocess.DEVNULL,
    )
    try:
        output = subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            encoding='cp866',
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except subprocess.CalledProcessError:
        return None

    if "TTL" in output:
        return False
    elif "unreachable" in output:
        return True


def ping_servers(vent_units):
    for shield, hosts in vent_units.hosts.items():

        servers_out = [is_server_out(host) for host in hosts.values()]
        servers_out += [is_server_out(host) for host in hosts.values()]

        if None in servers_out:
            continue

        elif all(servers_out) and not vent_units.sendings[shield]:
            send_alarm_message(f"{vent_units.messages[shield]}")
            vent_units.sendings[shield] = True

        elif not all(servers_out):
            vent_units.sendings[shield] = False


while True:
    ping_servers(plants)
    time.sleep(30)
