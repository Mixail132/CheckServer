"""Data for testing."""

import re
from pathlib import Path

import pytest

from app.dirs import DIR_APP
from app.vars import Vars


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

    config_path = total_config_file_path

    config_vars = Vars(config_path)
    allvars_attrs = dir(config_vars)
    project_vars = []

    for attr in allvars_attrs:
        if attr.startswith("__"):
            continue
        if attr in ("sendings", "read_configs"):
            continue

        project_vars.append(getattr(config_vars, attr))

    _vars = str(project_vars)
    vars_values = re.sub(r"'[^']*':", "", _vars, flags=re.DOTALL)
    vars_values = re.sub(r"[\[\]]|\{|}", "", vars_values)
    vars_values = re.sub(r"'", "", vars_values)
    vars_values = re.sub(r"^\s+", "", vars_values)
    vars_values = re.sub(r",\s+", ",", vars_values)
    work_vars_values = vars_values.split(",")

    return work_vars_values


@pytest.fixture(params=["original_vars_number", "extended_vars_number"])
def total_config_file_path(
    request,
    example_config_file_path: Path,
    working_config_file_path: Path,
    extended_config_file_path: Path,
) -> Path:
    """Defines a system path to the config file to be tested."""
    if request.param == "extended_vars_number":
        return extended_config_file_path

    if working_config_file_path.is_file():
        return working_config_file_path

    return example_config_file_path


@pytest.fixture
def example_config_file_path() -> Path:
    """Defines a system path to the example config file."""
    test_config_file = DIR_APP / "example_vars.ini"

    return test_config_file


@pytest.fixture
def working_config_file_path() -> Path:
    """Defines a system path to the working config file."""
    test_config_file = DIR_APP / "vars.ini"

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
    """Extends the example config file with a few parameters."""
    with open(path, "r", encoding="utf-8") as file:
        old_file = file.readlines()

        for number, line in enumerate(old_file):
            if "192." in line:
                added_var = "TEST_999 = 192.168.122.254\n"
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
