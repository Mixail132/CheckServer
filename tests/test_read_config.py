"""
Check weather the configuration variables
have been completely read from 'ini' file.
"""


def test_config_file_has_completely_read(
    test_read_vars: list,
    proj_read_vars: list,
) -> None:
    """Checks the vars number and weather they've been completely read."""

    for var in test_read_vars:
        assert var in proj_read_vars

    assert len(proj_read_vars) == len(test_read_vars)
