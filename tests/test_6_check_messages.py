"""Checking the completeness of messages."""

from app.audit import AuditShields
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


def test_messages_can_be_formed_in_a_cycle(bad_hosts_vars: Vars) -> None:
    """
    Checks the ability to send an alarm message
    if the crash occurs again after recovery.
    """

    auditor = AuditShields(bad_hosts_vars)

    true_statuses = {
        shield: True for shield in auditor.power_off_shields.keys()
    }

    false_statuses = {
        shield: False for shield in auditor.power_off_shields.keys()
    }

    for _ in range(3):

        auditor.power_off_shields = false_statuses
        assert not auditor.form_alarm_message()
        auditor.power_off_shields = true_statuses
        assert auditor.form_alarm_message()

        status = auditor.set_alarm_sending_status()
        assert status is True

        auditor.power_on_shields = false_statuses
        assert not auditor.form_cancel_message()
        auditor.power_on_shields = true_statuses
        assert auditor.form_cancel_message()

        status = auditor.set_cancel_sending_status()
        assert status is True
