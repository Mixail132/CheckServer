"""Checking the completeness of messages and their sending."""

import pytest

from app.audit import AuditShields
from app.dirs import DIR_ROOT, GITHUB_ROOTDIR
from app.vars import Vars


def test_alarm_message_is_full(config_vars_set: Vars) -> None:
    """
    Sets the sources' power statuses as if they're off.
    Forms an alarm message.
    Ensures all the powered-off items are included in the message.
    """
    auditor = AuditShields(config_vars_set)

    alarm_message = auditor.form_alarm_message()
    assert not alarm_message

    auditor.power_off_shields = {
        source: True for source in config_vars_set.hosts.keys()
    }

    alarm_message = auditor.form_alarm_message()
    assert alarm_message

    for shield in config_vars_set.hosts.keys():
        assert config_vars_set.alarm_messages[shield] in alarm_message


def test_cancel_message_is_full(config_vars_set: Vars) -> None:
    """
    Sets the sources' power statuses as if they're on.
    Forms a cancel message.
    Ensures all the powered-on items are included in the message.
    """
    auditor = AuditShields(config_vars_set)

    cancel_message = auditor.form_cancel_message()
    assert not cancel_message

    auditor.power_on_shields = {
        source: True for source in config_vars_set.hosts.keys()
    }

    cancel_message = auditor.form_cancel_message()
    assert cancel_message

    for shield in config_vars_set.hosts.keys():
        assert config_vars_set.cancel_messages[shield] in cancel_message


@pytest.mark.skipif(
    GITHUB_ROOTDIR in f"{DIR_ROOT}", reason="Denied pinging from GitHub"
)
def test_emergency_message_sent(bad_hosts_vars: Vars) -> None:
    """
    Checks all the test hosts are unreached.
    Checks the ping command number is equal the hosts number.
    Checks the result message has been sent.
    Checks that the message once sent, doesn't send twice.
    """
    auditor = AuditShields(bad_hosts_vars)
    assert all(auditor.power_off_shields.values()) is False

    for net in bad_hosts_vars.nets:
        if not auditor.is_network_out(net):
            auditor.check_shields(net)

    assert all(auditor.power_off_shields.values()) is True

    alarm_message = auditor.form_alarm_message()
    assert alarm_message

    all_hosts_list = [
        hosts
        for hosts in bad_hosts_vars.hosts.values()
        if "IN_TOUCH" not in hosts.keys()
    ]

    all_hosts_number = sum(len(host) for host in all_hosts_list)
    assert auditor.pinged_hosts == all_hosts_number

    first_alarm_message = auditor.send_messages(alarm_message)
    assert first_alarm_message is True

    status = auditor.set_alarm_sending_status()
    assert status is True

    for shield in bad_hosts_vars.alarm_sendings.keys():
        if "SOURCE" in shield:
            continue
        assert bad_hosts_vars.alarm_sendings[shield] is True

    rematched_message = auditor.form_alarm_message()
    assert not rematched_message

    second_alarm_message = auditor.send_messages(rematched_message)
    assert second_alarm_message is False


@pytest.mark.skipif(
    GITHUB_ROOTDIR in f"{DIR_ROOT}", reason="No credentials on GitHub"
)
def test_cancel_message_sent(bad_hosts_vars: Vars) -> None:
    """
    Sets all the test hosts status as if they are available again.
    Just setting without pinging.
    Checks the result message has been sent.
    Checks that the message, once sent doesn't send twice.
    """
    auditor = AuditShields(bad_hosts_vars)

    for shield in bad_hosts_vars.hosts.keys():
        auditor.power_on_shields.update({shield: True})

    assert all(auditor.power_on_shields.values()) is True

    cancel_message = auditor.form_cancel_message()
    assert cancel_message

    first_cancel_message = auditor.send_messages(cancel_message)
    assert first_cancel_message is True

    status = auditor.set_cancel_sending_status()
    assert status is True

    for shield in bad_hosts_vars.cancel_sendings.keys():
        if "SOURCE" in shield:
            continue
        assert bad_hosts_vars.cancel_sendings[shield] is True

    rematched_message = auditor.form_cancel_message()
    assert not rematched_message

    second_cancel_message = auditor.send_messages(rematched_message)
    assert second_cancel_message is False
