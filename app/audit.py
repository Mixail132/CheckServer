"""Performing the main logic of the app. """

import datetime
import subprocess
import sys
import time

from app.telegram import MyTelegramBot
from app.vars import Vars
from app.viber import MyViberBot

CREATE_NO_WINDOW: int = 134217728


class AuditShields:
    """
    Processes and keeps a state
    of the checked power shields.
    """

    def __init__(self, config_vars: Vars) -> None:
        self.vars: Vars = config_vars
        self.pinged_hosts: int = 0
        self.power_off_shields: dict = {
            source: False
            for source in self.vars.hosts.keys()
            if "SOURCE" not in source
        }
        self.power_on_shields: dict = {
            source: False
            for source in self.vars.hosts.keys()
            if "SOURCE" not in source
        }
        self.messages_sent: dict = {}
        self.telegram_sender = MyTelegramBot(self.vars)
        self.viber_sender = MyViberBot(self.vars)
        self.stop_delaying = False

    @staticmethod
    def ping_host(ip_address: str) -> bool:
        """
        Pings a single host if it's up
        or out depending on a platform.
        """

        command = [
            "ping",
            "-n" if sys.platform == "win32" else "-c",
            "2",
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
        """
        Checks an always working host
        to make sure its network works.
        """

        checking_host_ip = self.vars.hosts[f"{network} SOURCE"]["IN_TOUCH"]
        is_host_out = self.ping_host(checking_host_ip)
        return is_host_out

    def check_shields(self, network: str) -> dict:
        """
        Checks if a power shield is on.
        Defines whether a power is off or turned on.
        """
        for shield, plant_ips in self.vars.hosts.items():
            if "SOURCE" in shield:
                continue

            if network in shield:
                ping_results = [
                    self.ping_host(host) for host in plant_ips.values()
                ]
                self.pinged_hosts += len(ping_results)
                ping_result: bool = all(ping_results)

                previous_state = self.power_off_shields[shield]
                self.power_off_shields.update({shield: ping_result})
                current_state = self.power_off_shields[shield]

                states = [previous_state, current_state]

                if states == [True, False]:
                    self.power_on_shields.update({shield: True})

                elif states == [False, True]:
                    self.power_on_shields.update({shield: False})

        return self.power_off_shields

    def form_alarm_message(self) -> str:
        """
        Composes an alarm message
        regarding the certain equipment alarm.
        """

        message_text = ""
        for shield, status in self.power_off_shields.items():
            if not status:
                continue
            if not self.vars.alarm_sendings[shield]:
                message_text += f"{self.vars.alarm_messages[shield]} \n"
        return message_text

    def form_cancel_message(self) -> str:
        """
        Composes a cancel message regarding
        the certain equipment alarm restoring.
        """

        message_text = ""
        for shield, status in self.power_on_shields.items():
            if not status:
                continue
            if not self.vars.cancel_sendings[shield]:
                message_text += f"{self.vars.cancel_messages[shield]} \n"
        return message_text

    def send_messages(self, text: str) -> bool:
        """
        Sends the alarm message
        to proper Telegram and Viber users.
        """

        if_any_bot = any([self.telegram_sender.set, self.viber_sender.set])
        messages_are_sent = []

        if text and if_any_bot:

            viberbot_is_used = self.viber_sender.check_viber_bot_set()
            if viberbot_is_used:
                sent = self.viber_sender.send_series_viber_messages(text)
                messages_are_sent.append(sent)

            telebot_is_used = self.telegram_sender.check_telegram_bot_set()
            if telebot_is_used:
                sent = self.telegram_sender.send_series_telegram_messages(text)
                messages_are_sent.append(sent)

            any_message_is_sent = any(messages_are_sent)
            if any_message_is_sent:
                return True

        return False

    def delay_sending(self):
        """
        Delays a message sendings
        if the reason to send occurs from 23:00 to 06:00.
        """
        send_after = datetime.time(6, 00)
        send_before = datetime.time(23, 00)
        while True:
            time_now = datetime.datetime.now().time()
            if send_after < time_now < send_before:
                return True
            if self.stop_delaying:
                return False
            time.sleep(60)

    def set_alarm_sending_status(self) -> bool:
        """
        Sets a sending status
        if an alarm message is sent.
        """

        statuses_have_been_changed = False
        for shield, status in self.power_off_shields.items():
            if not status:
                continue
            if not self.vars.alarm_sendings[shield]:
                self.vars.alarm_sendings[shield] = True
                self.vars.cancel_sendings[shield] = False
                statuses_have_been_changed = True

        return statuses_have_been_changed

    def set_cancel_sending_status(self) -> bool:
        """
        Sets a sending status
        if a cancel message is sent.
        """

        statuses_have_been_changed = False
        for shield, status in self.power_on_shields.items():
            if not status:
                continue
            if not self.vars.cancel_sendings[shield]:
                self.vars.cancel_sendings[shield] = True
                self.vars.alarm_sendings[shield] = False
                statuses_have_been_changed = True

        return statuses_have_been_changed
