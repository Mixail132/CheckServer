"""Viber bot checking."""

import ast

import pytest

from app.dirs import DIR_APP, DIR_ROOT, FILE_VARS, GITHUB_ROOTDIR
from app.vars import Vars
from app.viber import MyViberBot


def skip_condition() -> bool:
    """Skips the test if the bot is not used."""
    config_vars = Vars(FILE_VARS)
    test_viberbot = MyViberBot(config_vars)
    bot_in_use_var = test_viberbot.set
    bot_in_use = ast.literal_eval(bot_in_use_var)
    return not bot_in_use


@pytest.mark.skipif(skip_condition(), reason="The bot is not used")
def test_bot_viber_configs_exist(config_vars_set: Vars):
    """Checks whether all the Viber bot config variables exist."""

    vars_ = config_vars_set

    assert vars_.viber_configs["VIBERBOT_TOKEN"]
    assert vars_.viber_configs["VIBERBOT_NAME"]
    assert vars_.viber_configs["VIBERBOT_AVATAR"]
    assert vars_.viber_configs["VIBERBOT_SET"]
    assert vars_.viber_users["Admin"]

    bot_status = vars_.viber_configs["VIBERBOT_SET"]
    assert isinstance(ast.literal_eval(bot_status), bool)

    if GITHUB_ROOTDIR in f"{DIR_ROOT}":
        pytest.skip()

    bot_avatar = vars_.viber_configs["VIBERBOT_AVATAR"]
    assert (DIR_APP / bot_avatar).is_file()
