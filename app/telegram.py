import telebot
from vars import Plant

plants = Plant()
telegramtoken = plants.tokens["telegramtoken"]
bot = telebot.TeleBot(telegramtoken)

def send_alarm_message(message_text):
    for user in plants.users.values():
        bot.send_message(user, message_text)
