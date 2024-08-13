""" Sending the message to the Telegram users. """

import telebot
from requests.exceptions import ConnectTimeout

from app.vars import allvars

telegramtoken = allvars.telegram_configs["TELEGRAMTOKEN"]
bot = telebot.TeleBot(telegramtoken)


def send_telegram_message(message_text: str) -> None:
    """Sends a message to an existing Telegram bot."""
    for user in allvars.telegram_users.values():
        try:
            bot.send_message(user, message_text)
        except ConnectTimeout:
            continue


if __name__ == "__main__":
    admin = allvars.telegram_users["admin"]
    bot.send_message(admin, "The bot checking!")
