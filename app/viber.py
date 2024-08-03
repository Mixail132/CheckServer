from viberbot import Api
from app.vars import plants
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage

vibertoken = plants.tokens["VIBERTOKEN"]
viberavatar = plants.viber_configs["BOT_AVATAR"]
vibername = plants.viber_configs["BOT_NAME"]

bot_config = BotConfiguration(
    name=vibername,
    avatar=viberavatar,
    auth_token=vibertoken
)

viber = Api(bot_config)


def send_viber_message(message_text):
    message = TextMessage(text=message_text)
    for user_id in plants.viber_users.values():
        viber.send_messages(user_id, [message])


