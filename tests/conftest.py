"""Data for testing."""

import ast
import re
from pathlib import Path

import pytest
from pytest import FixtureRequest

from app.dirs import DIR_APP, FILE_VARS
from app.telegram import MyTelegramBot
from app.vars import Vars
from app.viber import MyViberBot


@pytest.fixture
def vars_read_for_test(
    total_config_file_path: Path,
) -> list:
    """Matches variables read from the config file for the test."""

    config_path = total_config_file_path

    with open(config_path, "r", encoding="utf-8") as file:
        test_vars_values = []
        for line in file:
            if line.startswith(";") or line.startswith("["):
                continue
            if line == "\n":
                continue
            line = line.split(" = ")[1]
            test_vars_values.append(line.replace("\n", ""))

    return test_vars_values


@pytest.fixture
def vars_read_for_work(
    total_config_file_path: Path,
) -> list:
    """Matches variables read from the config file for the project."""

    config_vars = Vars(total_config_file_path)

    telegram_ids = config_vars.telegram_users.values()
    viber_ids = config_vars.viber_users.values()
    telegram_settings = config_vars.telegram_configs.values()
    viber_settings = config_vars.viber_configs.values()
    alarm_messages = config_vars.alarm_messages.values()
    cancel_messages = config_vars.cancel_messages.values()
    hosts = [
        hosts for host in config_vars.hosts.values() for hosts in host.values()
    ]
    vars_values = [
        telegram_ids,
        viber_ids,
        telegram_settings,
        viber_settings,
        alarm_messages,
        cancel_messages,
        hosts,
    ]

    work_vars_values = [
        list_items for lists in vars_values for list_items in lists
    ]

    return work_vars_values


@pytest.fixture(params=["original_vars_number", "extended_vars_number"])
def total_config_file_path(
    request: FixtureRequest,
    extended_config_file_path: Path,
) -> Path:
    """Defines a system path to the config file to be tested."""
    if request.param == "extended_vars_number":
        return extended_config_file_path

    return FILE_VARS


@pytest.fixture
def example_config_file_path() -> Path:
    """Defines a system path to the example config file."""
    test_config_file = DIR_APP / "example_vars.ini"

    return test_config_file


@pytest.fixture
def extended_config_file_path(example_config_file_path: Path):
    """
    Extends the example config file with a few parameters.
    Returns the system path to the file.
    Removes the added parameters after the test to be done.
    """

    config_file_path = add_test_vars_to_config_file(example_config_file_path)

    yield config_file_path

    del_added_vars_from_config_file(config_file_path)


def add_test_vars_to_config_file(path: Path) -> Path:
    """
    Extends the example config file with a few parameters.
    Puts an invalid IP address to detect it in a test.
    """
    with open(path, "r", encoding="utf-8") as file:
        old_file = file.readlines()

        for number, line in enumerate(old_file):
            ip_mask = re.search(r"(\d{1,3}\.){3}", line)
            if ip_mask:
                added_var = "TEST_BAD_IP = o99.999.9I.\n"
                old_file.insert(number + 1, added_var)
                break

        for number, line in enumerate(old_file):
            if "TELEGRAM_USERS" in line:
                added_var = "TEST_User = 1234567890\n"
                old_file.insert(number + 1, added_var)
                break

    with open(path, "w", encoding="utf-8") as file:
        new_file = "".join(old_file)
        file.write(new_file)

    return path


def del_added_vars_from_config_file(path: Path) -> None:
    """Removes the added parameters after the test to be done."""

    with open(path, "r", encoding="utf-8") as lines:
        old_file = []
        for line in lines:
            if "TEST" in line:
                continue
            old_file.append(line)

    with open(path, "w", encoding="utf-8") as file:
        original_file = "".join(old_file)
        file.write(original_file)


@pytest.fixture
def config_vars_set() -> Vars:
    """Returns the object full of config variables."""

    return Vars(FILE_VARS)


@pytest.fixture
def bad_hosts_vars(config_vars_set: Vars) -> Vars:
    """
    Returns the config variables object
    where all the IP addresses will never be reached,
    and all 'in-touch' hosts will always be reached.
    Reduces a number of hosts to minimize testing time.
    """

    all_vars = config_vars_set
    all_hosts = str(all_vars.hosts)

    any_host = r"(\d{1,3}\.){3}\d{1,3}"
    never_reached_host = "192.0.2.1"
    bad_hosts = re.sub(any_host, never_reached_host, all_hosts)

    all_vars.hosts = ast.literal_eval(bad_hosts)

    always_available_host = "www.google.com"
    for hosts in all_vars.hosts.values():
        for name in hosts.keys():
            if "IN_TOUCH" in name:
                hosts[name] = always_available_host

    reduced_hosts = {}
    for source, hosts in all_vars.hosts.items():
        hosts_number = 0
        for name, host in hosts.items():
            if hosts_number >= 1:
                continue
            reduced_hosts.update({source: {name: host}})
            hosts_number += 1

    all_vars.hosts = reduced_hosts

    viber_admin = {
        vb_user: vb_id
        for vb_user, vb_id in all_vars.viber_users.items()
        if vb_user == "Admin"
    }

    telegram_admin = {
        tg_user: tg_id
        for tg_user, tg_id in all_vars.telegram_users.items()
        if tg_user == "Admin"
    }

    all_vars.viber_users = viber_admin
    all_vars.telegram_users = telegram_admin

    return all_vars


@pytest.fixture
def test_telebot(config_vars_set: Vars) -> MyTelegramBot:
    """Return the test bot object."""

    return MyTelegramBot(config_vars_set)


@pytest.fixture
def test_viberbot(config_vars_set: Vars) -> MyViberBot:
    """Return the test bot object."""

    return MyViberBot(config_vars_set)


@pytest.fixture
def config_file_as_a_text() -> str:
    """Reads a config file, returns it as a string."""

    with open(FILE_VARS, "r", encoding="utf-8") as file:
        config_file_list = []
        for line in file:
            if line.startswith(";"):
                continue
            if line == "\n":
                continue
            config_file_list.append(line)
        config_file_text = "".join(config_file_list)

    return config_file_text


@pytest.fixture
def bad_hosts_vars_reduced(bad_hosts_vars: Vars) -> Vars:
    """Reduces a number of hosts to minimize testing time."""
    reduced_hosts = {}
    for source, hosts in bad_hosts_vars.hosts.items():
        hosts_number = 0
        for name, host in hosts.items():
            if hosts_number >= 1:
                continue
            reduced_hosts.update({source: {name: host}})
            hosts_number += 1

    bad_hosts_vars.hosts = reduced_hosts

    return bad_hosts_vars
