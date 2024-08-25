"""Data for testing."""

import pytest

from app.dirs import DIR_APP
from app.vars import allvars


@pytest.fixture
def test_read_vars():
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
def proj_read_vars():
    """The variables read from the config file for the project."""
    allvars_attrs = dir(allvars)
    project_vars = []

    for attr in allvars_attrs:
        if attr.startswith("__") or attr == "sendings":
            continue
        project_vars.append(getattr(allvars, attr))

    project_vars_values = []
    for values in project_vars:
        for value in values.values():
            project_vars_values.append(value)

    _project_vars_values = []
    for item in project_vars_values:
        if isinstance(item, dict):
            for _vl in item.values():
                _project_vars_values.append(_vl)
        else:
            _project_vars_values.append(item)

    return _project_vars_values
