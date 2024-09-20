"""Checking the messages' sending."""

import concurrent.futures
import datetime

import pytest

from app.audit import AuditShields
from app.dirs import DIR_ROOT, GITHUB_ROOTDIR
from app.vars import Vars


@pytest.mark.skipif(
    GITHUB_ROOTDIR in f"{DIR_ROOT}", reason="Denied pinging from GitHub."
)
def test_emergency_message_is_sent(bad_hosts_vars: Vars) -> None:
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
    GITHUB_ROOTDIR in f"{DIR_ROOT}", reason="No secrets on GitHub."
)
def test_cancel_message_is_sent(bad_hosts_vars: Vars) -> None:
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


def test_message_is_sent_only_during_the_day(bad_hosts_vars) -> None:
    """
    Checks that a message is sent
    only between 06:00 and 23:00.
    """

    msg_text = "Testing. It's not a night now,"
    auditor = AuditShields(bad_hosts_vars)

    time_now = datetime.datetime.now().time()
    send_after = datetime.time(6, 0)
    send_before = datetime.time(23, 0)

    if send_after < time_now < send_before:

        message_is_not_delayed = auditor.delay_sending()
        message_is_sent = auditor.send_messages(msg_text)

        assert message_is_not_delayed
        assert message_is_sent


def test_sending_delay_works_fine_at_night(bad_hosts_vars) -> None:
    """
    Checks that a message is sent
    only between 06:00 and 23:00
    because of the delay is working.
    """

    auditor = AuditShields(bad_hosts_vars)

    time_now = datetime.datetime.now().time()
    send_after = datetime.time(6, 00)
    send_before = datetime.time(23, 00)

    if send_after > time_now or send_before < time_now:

        with pytest.raises(concurrent.futures.TimeoutError) as err:
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            future = executor.submit(auditor.delay_sending)
            future.result(timeout=4)

        assert isinstance(err, pytest.ExceptionInfo)

        auditor.stop_delaying = True

        message_is_delayed = auditor.delay_sending()
        assert not message_is_delayed


def test_messages_can_be_sent_in_a_cycle(bad_hosts_vars: Vars) -> None:
    """
    Checks the ability to send an alarm message
    if the crash occurs again after recovery.
    """

    auditor = AuditShields(bad_hosts_vars)

    assert not auditor.form_alarm_message()

    true_statuses = {shield: True for shield in auditor.power_off_shields.keys()}
    auditor.power_off_shields = true_statuses

    assert auditor.form_alarm_message()

    status = auditor.set_alarm_sending_status()
    assert status is True
    status = auditor.set_cancel_sending_status()
    assert status is False

    true_statuses = {status: True for status in auditor.power_on_shields.keys()}
    auditor.power_on_shields = true_statuses

    assert auditor.form_cancel_message()

    status = auditor.set_cancel_sending_status()
    assert status is True
