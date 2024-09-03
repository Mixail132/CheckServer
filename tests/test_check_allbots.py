"""Telegram and Viber bots checking."""

from app.audit import AuditShields
from app.telegram import MyTelegramBot
from app.vars import Vars
from app.viber import MyViberBot


def test_one_of_bots_in_use():
    """Checks whether at least one of two bots set as in use."""

    test_telebot = MyTelegramBot()
    test_viberbot = MyViberBot()

    telebot_in_use = test_telebot.check_telegram_bot_set()
    viberbot_in_use = test_viberbot.check_viber_bot_set()

    err_msg = """
    At least one of the bots should be set to 'True'
    in the configuration file.
    """

    assert any([telebot_in_use, viberbot_in_use]), err_msg


def test_alarm_messages_right_and_sent(never_reached_hosts: Vars) -> None:
    """
    Checks all the test hosts are unreached.
    Checks the result message contains all the information needed.
    Checks the ping command number is equal the hosts number.
    """
    all_vars = never_reached_hosts
    auditor = AuditShields(all_vars)

    for net in ["WIFI", "DLAN", "INET"]:
        if not auditor.is_network_out("INET"):
            power_off_shields = auditor.check_shields(net)

            assert True in power_off_shields.values()

    result_message = auditor.form_alarm_message()

    for shield in all_vars.hosts.keys():
        if "SOURCE" in shield:
            continue
        assert all_vars.messages[shield] in result_message

    all_hosts_list = [
        hosts
        for hosts in all_vars.hosts.values()
        if "IN_TOUCH" not in hosts.keys()
    ]

    all_hosts_number = sum(len(x) for x in all_hosts_list)

    assert auditor.pinged_hosts == all_hosts_number
