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

    for var in vars_read_for_work:
        assert var in vars_read_for_test

    assert len(vars_read_for_work) == len(vars_read_for_test)


def test_there_are_no_unpair_brackets(config_file_as_a_text: str) -> None:
    """Compares open and close square brackets quantity."""

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
