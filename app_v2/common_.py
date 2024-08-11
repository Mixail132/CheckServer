import configparser
import subprocess

import telebot
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage


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
        self.hosts = {
            source: parser.section[f"{source}"] for source in sources}

        self.telegram_users = {user: tid for user,
                               tid in parser.section["TELEGRAM_USERS"].items()}
        self.viber_users = {user: vid for user,
                            vid in parser.section["VIBER_USERS"].items()}

        self.viber_configs = {par.upper(): value for par,
                              value in parser.section["VIBER_CONFIGS"].items()}
        self.telegram_configs = {
            par.upper(): value for par,
            value in parser.section["TELEGRAM_CONFIGS"].items()}

        self.messages = {
            source: parser.section["MESSAGES"][f"{source.lower()}"] for source in self.hosts}
        self.sendings = {source: False for source in self.hosts}


allvars = Vars()


telegramtoken = allvars.telegram_configs["TELEGRAMTOKEN"]
bot = telebot.TeleBot(telegramtoken)


def send_telegram_message(message_text):
    for user in allvars.telegram_users.values():
        bot.send_message(user, message_text)


vibertoken = allvars.viber_configs["VIBERTOKEN"]
viberavatar = allvars.viber_configs["BOT_AVATAR"]
vibername = allvars.viber_configs["BOT_NAME"]

bot_config = BotConfiguration(
    name=vibername,
    avatar=viberavatar,
    auth_token=vibertoken
)

viber = Api(bot_config)


def send_viber_message(alarm_message):
    alarm_msg = TextMessage(text=alarm_message)
    for user_id in allvars.viber_users.values():
        try:
            viber.send_messages(user_id, [alarm_msg])
        except Exception as ex:
            if "notSubscribed" in ex.args[0]:
                recipients = {
                    name: chat_id for chat_id,
                    name in allvars.viber_users.items()}
                bot_admin = allvars.viber_users["admin"]
                byby_message = f"{recipients[user_id]} has left this chat."
                byby_msg = TextMessage(text=byby_message)
                viber.send_messages(bot_admin, [byby_msg])
                del recipients, bot_admin
                continue


class AuditShields:

    def __init__(self, config_vars: Vars) -> None:
        self.vars = config_vars
        self.shields_out = {}
        self.messages_sent = {}

    @staticmethod
    def ping_host(ip_address: str) -> bool:
        """ Checks a single host if it's up or out """
        command = ["ping", "-n", "1", ip_address, ]
        subprocess.run(["chcp", "437"], shell=True,
                       stdout=subprocess.DEVNULL, )
        try:
            output = subprocess.check_output(
                command,
                stderr=subprocess.STDOUT,
                encoding='cp866',
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except subprocess.CalledProcessError as err:
            output = err.output

        if "TTL" in output:
            return False
        elif "100%" in output:
            return True

    def is_network_out(self, network: str) -> bool:
        """ Checks an always working host to make sure its network works """
        checking_host_ip = self.vars.hosts[f"{network} SOURCE"]["in_touch"]
        is_out = self.ping_host(checking_host_ip)
        return is_out

    def check_shields(self, network: str) -> dict:
        for shield, hosts in self.vars.hosts.items():
            if network in shield and "SOURCE" not in shield:
                hosts_out = [self.ping_host(host) for host in hosts.values()]
                self.shields_out.update({shield: all(hosts_out)})
        return self.shields_out

    def form_alarm_message(self) -> str:
        """ Composes an alarm message text regarding the certain equipment alarm """
        message_text = ""
        for shield, status in self.shields_out.items():
            if not status:
                continue
            if not self.vars.sendings[shield]:
                self.vars.sendings[shield] = True
                message_text += f"{self.vars.messages[shield]} \n"
        return message_text

    @staticmethod
    def send_alarm_message(text: str) -> None:
        """ Sends the alarm message to proper Telegram and Viber users """
        if text:
            text = f"Alarm!\n{text}"
            send_telegram_message(text)
            send_viber_message(text)


auditor = AuditShields(allvars)

while True:
    for net in ["WIFI", "DLAN", "INET"]:
        if auditor.is_network_out(net):
            auditor.check_shields(net)
    message = auditor.form_alarm_message()
    auditor.send_alarm_message(message)
