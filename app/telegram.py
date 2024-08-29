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

    def send_telegram_message(self, message_text: str) -> None:
        """Sends a message to the bot."""
        for user in telegram_vars.telegram_users.values():
            try:
                self.bot.send_message(user, message_text)
            except ConnectTimeout:
                continue


if __name__ == "__main__":
    check_bot = telebot.TeleBot(TELEGRAMBOT_TOKEN)
    admin = telegram_vars.telegram_users["Admin"]
    check_bot.send_message(admin, "The bot checking!")
