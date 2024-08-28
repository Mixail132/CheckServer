"""Data for testing."""

import re
from pathlib import Path

import pytest

from app.dirs import DIR_APP
from app.vars import Vars


@pytest.fixture
def vars_read_for_test(
    config_file_path: Path,
) -> list:
    """Matches variables read from the config file for the test."""
    with open(config_file_path, "r", encoding="utf-8") as file:
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
    config_file_path: Path,
) -> list:
    """Matches variables read from the config file for the project."""
    config_vars = Vars(config_file_path)
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


@pytest.fixture
def config_file_path(
        test_config_file_path: Path,
        work_config_file_path: Path
) -> Path:
    """Checks both files and defines an existing config file."""
    if work_config_file_path.is_file():
        return work_config_file_path

    return test_config_file_path


@pytest.fixture
def test_config_file_path() -> Path:
    """Defines a system path to the config file for tests."""
    test_config_file = DIR_APP / "example_vars.ini"

    return test_config_file


@pytest.fixture
def work_config_file_path() -> Path:
    """Defines a system path to the config file for work."""
    work_config_file_path = DIR_APP / "vars.ini"
    return work_config_file_path


@pytest.fixture
def added_vars_read_for_test(
    test_config_file_path: Path,
) -> list:
    """Add some variables and matches them for the test."""
    with open(test_config_file_path, "w", encoding="utf-8") as file:
        test_vars_values = []
        lines = file.split("\n")
        for line in file:
            if "192." in line:
                added_line = "TEST_999 = 192.168.125.100"
                test_vars_values.append(added_line)
            test_vars_values.append(line.replace("\n", ""))
    with open(test_config_file_path, "r", encoding="utf-8") as file:
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
def added_vars_read_for_work(
    config_file_path: Path,
) -> list:
    """Add some variables and matches them for the project."""
    config_vars = Vars(config_file_path)
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
