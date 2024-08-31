""" Sending the message to the Telegram users. """

import telebot
from requests.exceptions import ConnectTimeout
from telebot.apihelper import ApiTelegramException
from telebot.types import User

from app.dirs import FILE_VARS
from app.vars import Vars

telegram_vars = Vars(FILE_VARS)
TELEGRAMBOT_TOKEN = telegram_vars.telegram_configs["TELEGRAMBOT_TOKEN"]


class MyTelegramBot:
    """Telegram bot class."""

    def __init__(self):
        """Initializes the bot."""
        self.token = TELEGRAMBOT_TOKEN
        self.bot = telebot.TeleBot(self.token)
        self.admin = telegram_vars.telegram_users["Admin"]

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

    def send_series_telegram_messages(self, alarm_message: str) -> None:
        """Sends a message to a series of Telegram bot users."""
        for user in telegram_vars.telegram_users.values():
            try:
                self.send_one_telegram_message(user, alarm_message)

            except ApiTelegramException as err:
                if "bot was blocked by the user" in err.args[0]:
                    telegram_users = telegram_vars.telegram_users.items()
                    user_who_blocked_bot = [
                        key for key, val in telegram_users if val == user
                    ][0]
                    message = f"{user_who_blocked_bot} has blocked this bot!"
                    self.send_one_telegram_message(self.admin, message)
                continue


if __name__ == "__main__":
    telegram_bot_admin = telegram_vars.telegram_users["Admin"]
    telegram_sender = MyTelegramBot()
    telegram_sender.send_one_telegram_message(
        telegram_bot_admin, "Check the bot!"
    )
