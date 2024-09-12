"""Telegram and Viber bots checking."""

from app.audit import AuditShields
from app.vars import Vars


def test_alarm_message_is_full(config_vars_set: Vars) -> None:
    """
    Sets the sources' power statuses as if they're off.
    Forms an alarm message.
    Ensures all the powered-off items are included in the message.
    """
    auditor = AuditShields(config_vars_set)

    auditor.power_off_shields = {
        source: True for source in config_vars_set.hosts.keys()
    }

    result_message = auditor.form_alarm_message()
    assert result_message

    for shield in config_vars_set.hosts.keys():
        assert config_vars_set.alarm_messages[shield] in result_message


def test_cancel_message_is_full(config_vars_set: Vars) -> None:
    """
    Sets the sources' power statuses as if they're on.
    Forms a cancel message.
    Ensures all the powered-on items are included in the message.
    """
    auditor = AuditShields(config_vars_set)

    auditor.power_on_shields = {
        source: True for source in config_vars_set.hosts.keys()
    }

    result_message = auditor.form_cancel_message()
    assert result_message

    for shield in config_vars_set.hosts.keys():
        assert config_vars_set.cancel_messages[shield] in result_message
