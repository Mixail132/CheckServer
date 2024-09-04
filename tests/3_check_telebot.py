"""Telegram bot checking."""

import ast

import pytest
from telebot.types import User

from app.dirs import DIR_ROOT, GITHUB_ROOTDIR
from app.telegram import MyTelegramBot
from app.vars import Vars


def skip_condition():
    """Skips the test if the bot is not used."""
    test_telebot = MyTelegramBot()
    bot_in_use_var = test_telebot.set
    bot_in_use = ast.literal_eval(bot_in_use_var)
    return not bot_in_use


@pytest.mark.skipif(skip_condition(), reason="The bot is not used")
def test_telegram_bot_configs_exist(config_vars_set: Vars):
    """Checks whether all the Telegram bot config variables exist."""

    vars_ = config_vars_set

    assert vars_.telegram_configs["TELEGRAMBOT_NAME"]
    assert vars_.telegram_configs["TELEGRAMBOT_TOKEN"]
    assert vars_.telegram_configs["TELEGRAMBOT_URL"]
    assert vars_.telegram_configs["TELEGRAMBOT_SET"]
    assert vars_.telegram_users["Admin"]


@pytest.mark.skipif(
    GITHUB_ROOTDIR in f"{DIR_ROOT}", reason="Denied to ping from GitHub."
)
@pytest.mark.skipif(skip_condition(), reason="The bot is not used")
def test_telegram_bot_exists(config_vars_set: Vars):
    """Checks whether the Telegram bot exists."""

    vars_ = config_vars_set
    bot_in_use = vars_.telegram_configs["TELEGRAMBOT_SET"]
    if not ast.literal_eval(bot_in_use):
        pytest.skip()

    test_bot = MyTelegramBot()

    bot_exists = test_bot.check_telegram_bot_exists()
    err_msg = "Telegram bot does not exist."

    vars_ = config_vars_set
    bot_status = vars_.telegram_configs["TELEGRAMBOT_SET"]

    assert isinstance(ast.literal_eval(bot_status), bool)

    bot_name = vars_.telegram_configs["TELEGRAMBOT_NAME"]
    bot_url = vars_.telegram_configs["TELEGRAMBOT_URL"]

    assert bot_exists is not None, err_msg
    assert isinstance(bot_exists, User), err_msg
    assert bot_exists.is_bot is True, err_msg

    assert bot_exists.first_name == bot_name, "Incorrect bot name in configs."

    bot_username = bot_url.replace("@", "")
    assert bot_username in bot_exists.username, "Wrong bot url in configs."
