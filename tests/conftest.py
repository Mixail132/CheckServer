"""Data for testing."""

import re

import pytest

from app.dirs import DIR_APP
from app.vars import allvars


@pytest.fixture
def test_read_vars() -> list:
    """The variables read from the config file for the test."""
    path = DIR_APP / "vars.ini"
    with open(path, "r", encoding="utf-8") as file:
        test_vars = []
        for line in file:
            if line.startswith(";") or line.startswith("["):
                continue
            if line == "\n":
                continue
            line = line.split(" = ")[1]
            test_vars.append(line.replace("\n", ""))

    return test_vars


@pytest.fixture
def proj_read_vars() -> list:
    """The variables read from the config file for the project."""
    allvars_attrs = dir(allvars)
    project_vars = []

    for attr in allvars_attrs:
        if attr.startswith("__") or attr == "sendings":
            continue
        project_vars.append(getattr(allvars, attr))

    _vars = str(project_vars)
    vars_values = re.sub(r"'[^']*':", "", _vars, flags=re.DOTALL)
    vars_values = re.sub(r"[\[\]]|\{|}", "", vars_values)
    vars_values = re.sub(r"'", "", vars_values)
    vars_values = re.sub(r"^\s+", "", vars_values)
    vars_values = re.sub(r",\s+", ",", vars_values)
    project_vars_values = vars_values.split(",")

    return project_vars_values
