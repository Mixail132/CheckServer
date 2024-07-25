import telebot
import vars

bot = telebot.TeleBot(vars.telegramtoken)

def send_alarm_message(message_text):
    for user in vars.users.values():
        bot.send_message(user, message_text)
