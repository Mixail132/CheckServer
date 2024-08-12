from app.vars import allvars
from vars import DIR_STATIC
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage

vibertoken = allvars.viber_configs["VIBERTOKEN"]
vibername = allvars.viber_configs["BOT_NAME"]
viberavatar = DIR_STATIC / "logo.jpg"

bot_config = BotConfiguration(
    name=vibername,
    avatar=viberavatar,
    auth_token=vibertoken
)

viber = Api(bot_config)


def send_viber_message(alarm_message: str) -> None:
    alarm_msg = TextMessage(text=alarm_message)
    for user_id in allvars.viber_users.values():
        try:
            viber.send_messages(user_id, [alarm_msg])
        except Exception as ex:
            if "notSubscribed" in ex.args[0]:
                recipients = {name: chat_id for chat_id, name in allvars.viber_users.items()}
                bot_admin = allvars.viber_users["admin"]
                byby_message = f"{recipients[user_id]} has left this chat."
                byby_msg = TextMessage(text=byby_message)
                viber.send_messages(bot_admin, [byby_msg])
                del recipients, bot_admin
                continue


if __name__ == "__main__":
    admin = allvars.viber_users["admin"]
    check_message = TextMessage(text="Check the bot!")
    viber.send_messages(admin, check_message)
