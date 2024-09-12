"""Telegram and Viber bots checking."""

from app.telegram import MyTelegramBot
from app.viber import MyViberBot


def test_one_of_bots_in_use(
    test_telebot: MyTelegramBot, test_viberbot: MyViberBot
) -> None:
    """Checks whether at least one of two bots set as in use."""

    telebot_in_use = test_telebot.check_telegram_bot_set()
    viberbot_in_use = test_viberbot.check_viber_bot_set()

    err_msg = """
    At least one of the bots should be set to 'True'
    in the configuration file.
    """

    assert any([telebot_in_use, viberbot_in_use]), err_msg
