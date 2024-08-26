""" Sending the message to the Telegram users. """

import telebot
from requests.exceptions import ConnectTimeout

from app.vars import Vars

telegram_vars = Vars("vars.ini")
TELEGRAMBOT_TOKEN = telegram_vars.telegram_configs["TELEGRAMBOT_TOKEN"]
bot = telebot.TeleBot(TELEGRAMBOT_TOKEN)


def send_telegram_message(message_text: str) -> None:
    """Sends a message to an existing Telegram bot."""
    for user in telegram_vars.telegram_users.values():
        try:
            bot.send_message(user, message_text)
        except ConnectTimeout:
            continue


if __name__ == "__main__":
    admin = telegram_vars.telegram_users["Admin"]
    bot.send_message(admin, "The bot checking!")
