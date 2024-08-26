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
    config_file: str,
) -> list:
    """Matches variables read from the config file for the project."""
    config_vars = Vars(config_file)
    all_vars = config_vars
    allvars_attrs = dir(all_vars)
    project_vars = []

    for attr in allvars_attrs:
        if attr.startswith("__"):
            continue
        if attr in ("sendings", "read_configs"):
            continue

        project_vars.append(getattr(all_vars, attr))

    _vars = str(project_vars)
    vars_values = re.sub(r"'[^']*':", "", _vars, flags=re.DOTALL)
    vars_values = re.sub(r"[\[\]]|\{|}", "", vars_values)
    vars_values = re.sub(r"'", "", vars_values)
    vars_values = re.sub(r"^\s+", "", vars_values)
    vars_values = re.sub(r",\s+", ",", vars_values)
    work_vars_values = vars_values.split(",")

    return work_vars_values


@pytest.fixture
def config_file_path(config_file: str) -> Path:
    """Defines a system path to the config file."""
    config_path = DIR_APP / config_file

    return config_path


@pytest.fixture
def config_file() -> str:
    """Defines a config file for the test."""
    config_file = "vars.ini"

    return config_file
