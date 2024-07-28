import telebot
from app.vars import plants

telegramtoken = plants.tokens["telegramtoken"]
bot = telebot.TeleBot(telegramtoken)

def send_alarm_message(message_text):
    for user in plants.users.values():
        bot.send_message(user, message_text)
