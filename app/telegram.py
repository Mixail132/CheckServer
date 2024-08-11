import telebot
from app.vars import allvars

telegramtoken = allvars.telegram_configs["TELEGRAMTOKEN"]
bot = telebot.TeleBot(telegramtoken)

def send_telegram_message(message_text):
    for user in allvars.telegram_users.values():
        bot.send_message(user, message_text)


if __name__ == "__main__":
    admin = allvars.telegram_users["admin"]
    bot.send_message(admin, "The bot checking!")
