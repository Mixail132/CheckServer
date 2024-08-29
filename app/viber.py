""" Sending the message to the Viberbot users. """

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage

from app.dirs import FILE_VARS
from app.vars import Vars

viber_vars = Vars(FILE_VARS)

VIBERBOT_NAME = viber_vars.viber_configs["VIBERBOT_NAME"]
VIBERBOT_AVATAR = viber_vars.viber_configs["VIBERBOT_AVATAR"]
VIBERBOT_TOKEN = viber_vars.viber_configs["VIBERBOT_TOKEN"]


class MyViberBot:
    """Viber bot class."""

    def __init__(self):
        """Initializes the bot."""

        bot_config = BotConfiguration(
            name=VIBERBOT_NAME,
            avatar=VIBERBOT_AVATAR,
            auth_token=VIBERBOT_TOKEN,
        )
        self.viber = Api(bot_config)

    def send_one_viber_message(self, user_id_: str, alarm_msg_: str) -> bool:
        """Sends a message to a single Viber bot user."""
        the_alarm_message = TextMessage(text=alarm_msg_)
        try:
            self.viber.send_messages(user_id_, [the_alarm_message])
        except ConnectionError:
            return False

        return True

    def send_series_viber_messages(self, alarm_message: str) -> None:
        """Sends a message to a series of Viber bot users."""

        for user_id in viber_vars.viber_users.values():
            try:
                self.send_one_viber_message(user_id, alarm_message)
            # pylint: disable=W0718
            except Exception as ex:
                if "notSubscribed" in ex.args[0]:
                    recipients = {
                        name: _id
                        for _id, name in viber_vars.viber_users.items()
                    }
                    bot_admin = viber_vars.viber_users["Admin"]
                    byby_message = f"{recipients[user_id]} has left this chat."
                    byby_msg = TextMessage(text=byby_message)
                    self.viber.send_messages(bot_admin, [byby_msg])
                    del recipients, bot_admin
                    continue


if __name__ == "__main__":
    viberbot_admin = viber_vars.viber_users["Admin"]
    viber_sender = MyViberBot()
    viber_sender.send_one_viber_message(viberbot_admin, "Check the bot!")
