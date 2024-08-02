import telebot
from app.vars import plants

telegramtoken = plants.tokens["telegramtoken"]
bot = telebot.TeleBot(telegramtoken)

def send_telegram_message(message_text):
    for user in plants.telegram_users.values():
        bot.send_message(user, message_text)
