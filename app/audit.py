"""Performing the main logic of the app. """

import subprocess
import sys

from app.telegram import MyTelegramBot
from app.vars import Vars
from app.viber import MyViberBot

CREATE_NO_WINDOW: int = 134217728


class AuditShields:
    """Processes and keeps a state of the checked power shields."""

    def __init__(self, config_vars: Vars) -> None:
        self.vars: Vars = config_vars
        self.shields_out: dict = {}
        self.messages_sent: dict = {}
        self.telegram_sender: MyTelegramBot = MyTelegramBot()
        self.viber_sender: MyViberBot = MyViberBot()

    @staticmethod
    def ping_host(ip_address: str) -> bool:
        """Pings a single host if it's up or out depending on a platform."""
        command = [
            "ping",
            "-n" if sys.platform == "win32" else "-c",
            "3",
            ip_address,
        ]

        if sys.platform == "win32":
            subprocess.run(
                ["chcp", "437"],
                check=True,
                shell=True,
                stdout=subprocess.DEVNULL,
            )

        try:
            if sys.platform == "win32":
                output = subprocess.check_output(
                    command,
                    stderr=subprocess.STDOUT,
                    encoding="cp866",
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
            else:
                output = subprocess.check_output(
                    command, stderr=subprocess.STDOUT, encoding="utf-8"
                )

        except subprocess.CalledProcessError as err:
            output = err.output

        if "TTL" in output or "ttl" in output:
            return False

        return True

    def is_network_out(self, network: str) -> bool:
        """Checks an always working host to make sure its network works."""
        checking_host_ip = self.vars.hosts[f"{network} SOURCE"]["IN_TOUCH"]
        is_out = self.ping_host(checking_host_ip)
        return is_out

    def check_shields(self, network: str) -> dict:
        """Checks if a power shield is on."""
        for shield, plant_ips in self.vars.hosts.items():
            if network in shield and "SOURCE" not in shield:
                hosts_out = [
                    self.ping_host(host) for host in plant_ips.values()
                ]
                self.shields_out.update({shield: all(hosts_out)})
        return self.shields_out

    def form_alarm_message(self) -> str:
        """Composes an alarm message regarding the certain equipment alarm."""
        message_text = ""
        for shield, status in self.shields_out.items():
            if not status:
                continue
            if not self.vars.sendings[shield]:
                message_text += f"{self.vars.messages[shield]} \n"
        return message_text

    def send_alarm_messages(self, text: str) -> bool:
        """Sends the alarm message to proper Telegram and Viber users."""

        if_any_bot = any([self.telegram_sender.set, self.viber_sender.set])
        messages_is_sent = []

        if text and if_any_bot:

            text = f"Alarm!\n{text}"

            viberbot_is_used = self.viber_sender.check_viber_bot_set()
            if viberbot_is_used:
                sent = self.viber_sender.send_series_viber_messages(text)
                messages_is_sent.append(sent)

            telebot_is_used = self.telegram_sender.check_telegram_bot_set()
            if telebot_is_used:
                sent = self.telegram_sender.send_series_telegram_messages(text)
                messages_is_sent.append(sent)

            any_messages_is_sent = any(messages_is_sent)
            if any_messages_is_sent:
                return True

        return False

    def set_sending_status(self) -> None:
        """Sets a sending status if an alarm message is sent."""
        for shield, status in self.shields_out.items():
            if not status:
                continue
            if not self.vars.sendings[shield]:
                self.vars.sendings[shield] = True
