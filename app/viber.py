""" Sending the message to the Viberbot users. """

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage

from app.vars import allvars

vibertoken = allvars.viber_configs["VIBERTOKEN"]
vibername = allvars.viber_configs["BOT_NAME"]
viberavatar = allvars.viber_configs["VIBER_AVATAR"]

bot_config = BotConfiguration(name=vibername, avatar=viberavatar, auth_token=vibertoken)

viber = Api(bot_config)


def send_viber_message(alarm_message: str) -> None:
    """Sends a message to an existing Viber bot."""

    alarm_msg = TextMessage(text=alarm_message)
    for user_id in allvars.viber_users.values():
        try:
            viber.send_messages(user_id, [alarm_msg])
        # pylint: disable=W0718
        except Exception as ex:
            if "notSubscribed" in ex.args[0]:
                recipients = {
                    name: chat_id for chat_id, name in allvars.viber_users.items()
                }
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
