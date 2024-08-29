"""Telegram got checking."""

import pytest
from telebot.types import User

from app.dirs import DIR_ROOT, GITHUB_ROOTDIR
from app.telegram import MyTelegramBot
from app.vars import Vars


# @pytest.mark.skipif(
#     GITHUB_ROOTDIR in f"{DIR_ROOT}",
#     reason="Denied to send requests from GitHub.",
# )
def test_telegram_bot_exists(config_vars_set: Vars):
    """Checks weather the Telegrab bot exists."""
    test_bot = MyTelegramBot()
    bot_exists = test_bot.check_telegram_bot_exists()
    err_msg = "Telegram bot does not exist."

    vars_ = config_vars_set
    bot_name = vars_.telegram_configs["TELEGRAMBOT_NAME"]
    bot_url = vars_.telegram_configs["TELEGRAMBOT_URL"]

    assert bot_exists is not None, err_msg
    assert isinstance(bot_exists, User), err_msg
    assert bot_exists.is_bot is True, err_msg

    assert bot_exists.first_name == bot_name, "Incorrect bot name in configs."

    bot_username = bot_url.replace("@", "").replace(".bot", "")
    assert bot_username in bot_exists.username, "Wrong bot url in configs."
