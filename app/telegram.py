""" Sending the message to the Telegram users. """

import ast

import telebot
from requests.exceptions import ConnectTimeout
from telebot.apihelper import ApiTelegramException
from telebot.types import User

from app.dirs import FILE_VARS
from app.vars import Vars


class MyTelegramBot:
    """Telegram bot class."""

    def __init__(self, config_vars):
        """Initializes the bot."""

        self.admin = config_vars.telegram_users["Admin"]
        self.set = config_vars.telegram_configs["TELEGRAMBOT_SET"]
        self.token = config_vars.telegram_configs["TELEGRAMBOT_TOKEN"]
        self.users = config_vars.telegram_users

        self.bot = telebot.TeleBot(self.token)

    def check_telegram_bot_set(self) -> bool:
        """Checks if the bot is in use."""
        bot_in_use = ast.literal_eval(self.set)
        if bot_in_use and self.admin:
            return True

        return False

    def check_telegram_bot_exists(self) -> User | None:
        """Checks if the bot exists."""
        try:
            get_bot = self.bot.get_me()
        except ApiTelegramException:
            get_bot = None

        return get_bot

    def send_one_telegram_message(self, user_id_, alarm_msg_: str) -> bool:
        """Sends a message to a single Viber bot user."""
        try:
            self.bot.send_message(user_id_, alarm_msg_)
        except ConnectTimeout:
            return False

        return True

    def send_series_telegram_messages(self, alarm_message: str) -> bool:
        """Sends a message to a series of Telegram bot users."""
        sending_statuses: list = [bool, bool]
        for user in self.users.values():
            try:
                sending_status = self.send_one_telegram_message(
                    user, alarm_message
                )
            except ApiTelegramException as err:
                if "bot was blocked by the user" in err.args[0]:
                    telegram_users = self.users.items()
                    user_who_blocked_bot = [
                        key for key, val in telegram_users if val == user
                    ][0]
                    tm_msg = f"{user_who_blocked_bot} has blocked this bot!"
                    self.send_one_telegram_message(self.admin, tm_msg)
                continue
            sending_statuses.append(sending_status)

        return any(sending_statuses)


if __name__ == "__main__":
    all_vars_t = Vars(FILE_VARS)
    telegram_sender = MyTelegramBot(all_vars_t)
    telegram_bot_admin = telegram_sender.admin
    if telegram_sender.check_telegram_bot_set() is not None:
        telegram_sender.send_one_telegram_message(
            telegram_bot_admin, "Check the bot!"
        )
