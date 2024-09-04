""" Sending the message to the Viberbot users. """

import ast

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage

from app.dirs import FILE_VARS
from app.vars import Vars


class MyViberBot:
    """Viber bot class."""

    def __init__(self, config_vars: Vars) -> None:
        """Initializes the bot."""

        self.admin = config_vars.viber_users["Admin"]
        self.avatar = config_vars.viber_configs["VIBERBOT_AVATAR"]
        self.name = config_vars.viber_configs["VIBERBOT_NAME"]
        self.set = config_vars.viber_configs["VIBERBOT_SET"]
        self.token = config_vars.viber_configs["VIBERBOT_TOKEN"]
        self.users = config_vars.viber_users

        bot_config = BotConfiguration(
            name=self.name,
            avatar=self.avatar,
            auth_token=self.token,
        )
        self.viber = Api(bot_config)

    def check_viber_bot_set(self) -> bool:
        """Checks if the bot is in use."""
        bot_in_use = ast.literal_eval(self.set)
        if bot_in_use and self.admin:
            return True

        return False

    def send_one_viber_message(self, user_id_: str, alarm_msg_: str) -> bool:
        """Sends a message to a single Viber bot user."""
        the_alarm_message = TextMessage(text=alarm_msg_)
        try:
            self.viber.send_messages(user_id_, [the_alarm_message])
        except ConnectionError:
            return False

        return True

    def send_series_viber_messages(self, alarm_message: str) -> bool:
        """Sends a message to a series of Viber bot users."""
        sending_statuses: list = [bool, bool]
        for user_id in self.users.values():
            sending_status: bool = False
            try:
                sending_status = self.send_one_viber_message(
                    user_id, alarm_message
                )
            # pylint: disable=W0718
            except Exception as ex:
                if "notSubscribed" in ex.args[0]:
                    recipients = {
                        name: _id for _id, name in self.users.items()
                    }
                    vb_message = f"{recipients[user_id]} has left this chat."
                    byby_msg = TextMessage(text=vb_message)
                    self.viber.send_messages(self.admin, [byby_msg])
                    del recipients, self.admin
                    continue
            sending_statuses.append(sending_status)

        return any(sending_statuses)


if __name__ == "__main__":
    all_vars_v = Vars(FILE_VARS)
    viber_sender = MyViberBot(all_vars_v)
    viberbot_admin = viber_sender.admin
    if viber_sender.check_viber_bot_set() is not None:
        viber_sender.send_one_viber_message(viberbot_admin, "Check the bot!")
