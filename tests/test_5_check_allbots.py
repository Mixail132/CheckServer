"""Telegram and Viber bots checking."""

import pytest

from app.audit import AuditShields
from app.dirs import DIR_ROOT, GITHUB_ROOTDIR
from app.telegram import MyTelegramBot
from app.vars import Vars
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


@pytest.mark.skipif(
    GITHUB_ROOTDIR in f"{DIR_ROOT}", reason="Denied to ping from GitHub"
)
def test_alarm_messages_right_and_sent(bad_hosts_vars: Vars) -> None:
    """
    Checks all the test hosts are unreached.
    Checks the result message contains all the information needed.
    Checks the ping command number is equal the hosts number.
    Checks the result message has been sent.
    Checks the sent message doesn't send twice.
    """
    auditor = AuditShields(bad_hosts_vars)

    assert all(auditor.power_off_shields.values()) is False

    for net in bad_hosts_vars.nets:
        if not auditor.is_network_out(net):
            auditor.check_shields(net)

    assert all(auditor.power_off_shields.values()) is True

    result_message = auditor.form_alarm_message()
    assert result_message

    all_hosts_list = [
        hosts
        for hosts in bad_hosts_vars.hosts.values()
        if "IN_TOUCH" not in hosts.keys()
    ]

    all_hosts_number = sum(len(host) for host in all_hosts_list)
    assert auditor.pinged_hosts == all_hosts_number

    once_sent_message = auditor.send_messages(result_message)
    assert once_sent_message is True

    auditor.set_alarm_sending_status()

    for shield in bad_hosts_vars.alarm_sendings.keys():
        if "SOURCE" in shield:
            continue
        assert bad_hosts_vars.alarm_sendings[shield] is True

    rematched_message = auditor.form_alarm_message()
    assert not rematched_message

    twice_sent_message = auditor.send_messages(rematched_message)
    assert twice_sent_message is False


@pytest.mark.skipif(
    GITHUB_ROOTDIR in f"{DIR_ROOT}", reason="No credentials on GitHub"
)
def test_cancel_messages_right_and_sent(bad_hosts_vars: Vars) -> None:
    """
    Sets all the test hosts as unreached and available again.
    Just sets without pinging.
    Checks the result message has been sent.
    Checks the sent message doesn't send twice.
    """
    auditor = AuditShields(bad_hosts_vars)

    for shield in bad_hosts_vars.hosts.keys():
        auditor.power_off_shields.update({shield: True})

    assert all(auditor.power_off_shields.values()) is True

    alarm_message = auditor.form_alarm_message()
    assert alarm_message

    first_alarm_message = auditor.send_messages(alarm_message)
    assert first_alarm_message is True

    auditor.set_alarm_sending_status()

    for shield in bad_hosts_vars.alarm_sendings.keys():
        if "SOURCE" in shield:
            continue
        assert bad_hosts_vars.alarm_sendings[shield] is True

    rematched_message = auditor.form_alarm_message()
    assert not rematched_message

    second_alarm_message = auditor.send_messages(rematched_message)
    assert second_alarm_message is False

    for shield in bad_hosts_vars.hosts.keys():
        auditor.power_on_shields.update({shield: True})

    assert all(auditor.power_on_shields.values()) is True

    cancel_message = auditor.form_cancel_message()
    assert cancel_message

    first_cancel_message = auditor.send_messages(cancel_message)
    assert first_cancel_message is True

    auditor.set_cancel_sending_status()

    for shield in bad_hosts_vars.cancel_sendings.keys():
        if "SOURCE" in shield:
            continue
        assert bad_hosts_vars.cancel_sendings[shield] is True

    rematched_message = auditor.form_cancel_message()
    assert not rematched_message

    second_cancel_message = auditor.send_messages(rematched_message)
    assert second_cancel_message is False
