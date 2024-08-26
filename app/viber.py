""" Sending the message to the Viberbot users. """

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage

from app.vars import all_vars

VIBERBOT_NAME = all_vars.viber_configs["VIBERBOT_NAME"]
VIBERBOT_AVATAR = all_vars.viber_configs["VIBERBOT_AVATAR"]
VIBERBOT_TOKEN = all_vars.viber_configs["VIBERBOT_TOKEN"]

bot_config = BotConfiguration(
    name=VIBERBOT_NAME,
    avatar=VIBERBOT_AVATAR,
    auth_token=VIBERBOT_TOKEN,
)

viber = Api(bot_config)


def send_viber_message(alarm_message: str) -> None:
    """Sends a message to an existing Viber bot."""

    alarm_msg = TextMessage(text=alarm_message)
    for user_id in all_vars.viber_users.values():
        try:
            viber.send_messages(user_id, [alarm_msg])
        # pylint: disable=W0718
        except Exception as ex:
            if "notSubscribed" in ex.args[0]:
                recipients = {
                    name: _id for _id, name in all_vars.viber_users.items()
                }
                bot_admin = all_vars.viber_users["Admin"]
                byby_message = f"{recipients[user_id]} has left this chat."
                byby_msg = TextMessage(text=byby_message)
                viber.send_messages(bot_admin, [byby_msg])
                del recipients, bot_admin
                continue


if __name__ == "__main__":
    viberbot_admin = all_vars.viber_users["Admin"]
    check_message = TextMessage(text="Check the bot!")
    viber.send_messages(viberbot_admin, check_message)
