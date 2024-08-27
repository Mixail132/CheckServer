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
def config_file_path() -> Path:
    """Defines a system path to the config file."""
    test_config_file = DIR_APP / "example_vars.ini"
    work_config_file = DIR_APP / "vars.ini"
    if work_config_file.is_file():
        return work_config_file
    else:
        return test_config_file
