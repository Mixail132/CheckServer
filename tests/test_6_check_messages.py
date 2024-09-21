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
