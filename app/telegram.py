""" Sending the message to the Telegram users. """

import telebot
from requests.exceptions import ConnectTimeout

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
            self.send_one_telegram_message(user, alarm_message)


if __name__ == "__main__":
    check_bot = telebot.TeleBot(TELEGRAMBOT_TOKEN)
    admin = telegram_vars.telegram_users["Admin"]
    check_bot.send_message(admin, "The bot checking!")
