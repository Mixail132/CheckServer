"""
Check weather the configuration variables
have been completely read from 'ini' file.
If there are no errors in them.
"""

import ipaddress
import re
from pathlib import Path

import pytest
import validators

from app.dirs import DIR_ROOT, FILE_VARS, GITHUB_ROOTDIR
from app.vars import Vars


def test_config_file_has_completely_read(
    vars_read_for_test: list,
    vars_read_for_work: list,
) -> None:
    """Checks the vars number and weather they've been completely read."""
    for var in vars_read_for_test:
        assert var in vars_read_for_work

    for var in vars_read_for_work:
        assert var in vars_read_for_test

    assert len(vars_read_for_work) == len(vars_read_for_test)


def test_square_brackets_arranged_right(config_file_as_a_text: str) -> None:
    """Checks whether the brackets are properly arranged."""

    open_brackets = config_file_as_a_text.count("[")
    close_brackets = config_file_as_a_text.count("]")

    assert open_brackets == close_brackets

    config_file_list = config_file_as_a_text.splitlines()
    pair_brackets = 0

    for line in config_file_list:

        if line.startswith("["):
            assert line.endswith("]")
        else:
            continue

        assert line.index("]") - line.index("[") > 1
        assert line.count("[") == 1
        assert line.count("]") == 1

        pair_brackets += 1

    assert pair_brackets == open_brackets


def test_ip_addresses_are_valid(config_vars_set: Vars) -> None:
    """
    Checks for a valid format of all the IP addresses and urls.
    """

    err_msg = "The configuration file contains invalid host"

    hosts = [
        host
        for hosts in config_vars_set.hosts.values()
        for host in hosts.values()
    ]
    for host in hosts:
        ip_mask = re.search(r"(.{1,3}\.){3}", host)
        if ip_mask:
            try:
                ip_is_valid = ipaddress.ip_address(host)
            except ValueError:
                ip_is_valid = None

            assert bool(ip_is_valid), err_msg

        elif host[0].isalpha():

            assert validators.url(f"http://{host}"), err_msg


def test_invalid_ip_is_detected(extended_config_file_path: Path) -> None:
    """
    Puts an invalid IP to the config file.
    Checks whether this IP is found.
    """
    config_vars_set = Vars(extended_config_file_path)

    hosts = [
        host
        for hosts in config_vars_set.hosts.values()
        for host in hosts.values()
    ]
    with pytest.raises(ValueError):

        for host in hosts:
            ip_mask = re.search(r"(.{1,3}\.){3}", host)
            if ip_mask:
                assert ipaddress.ip_address(host)


def test_right_config_file_chosen() -> None:
    """Checks whether the right configuration file is used."""

    if GITHUB_ROOTDIR in str(DIR_ROOT):
        assert "example_vars.ini" in str(FILE_VARS)

    else:
        assert "vars.ini" in str(FILE_VARS)


def test_shields_have_corresponding_messages(config_vars_set: Vars) -> None:
    """Finds a message text that corresponds a certain shield."""

    shields = list(config_vars_set.hosts.keys())
    pointers = list(config_vars_set.messages.keys())

    assert shields == pointers


def test_neded_vars_exist(config_vars_set: Vars) -> None:
    """Checks if all the necessary variables are collected."""

    assert config_vars_set.nets


def test_all_network_variables_are_completely_removed(
    config_file_as_a_text: str, config_vars_set: Vars
) -> None:
    """Checks whether all the network components are complete."""

    project_nets = ["WIFI", "DLAN", "INET"]
    user_nets: list = config_vars_set.nets
    err_msg = """
    The network components are not completely
    removed from the configuration file.
    """
    for net in project_nets:
        if net not in user_nets:
            assert net not in config_file_as_a_text, f"{err_msg} {net}"
