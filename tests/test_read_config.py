"""
Check weather the configuration variables
have been completely read from 'ini' file.
"""


def test_config_file_has_completely_read(
    vars_read_for_test: list,
    vars_read_for_work: list,
) -> None:
    """Checks the vars number and weather they've been completely read."""

    for var in vars_read_for_test:
        assert var in vars_read_for_work

    for _ in range(len(vars_read_for_test)):
        print(vars_read_for_work[_])

    assert len(vars_read_for_work) == len(vars_read_for_test)
