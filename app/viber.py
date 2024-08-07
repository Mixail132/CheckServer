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


def send_viber_message(alarm_message):
    alarm_msg = TextMessage(text=alarm_message)
    for user_id in plants.viber_users.values():
        try:
            viber.send_messages(user_id, [alarm_msg])
        except Exception as ex:
            if "notSubscribed" in ex.args[0]:
                recipients = {name: chat_id for chat_id, name in plants.viber_users.items()}
                bot_admin = plants.viber_users["admin"]
                byby_message = f"{recipients[user_id]} has left this chat."
                byby_msg = TextMessage(text=byby_message)
                viber.send_messages(bot_admin, [byby_msg])
                del recipients, bot_admin
                continue
