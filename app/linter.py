"""Run the linters locally."""

import subprocess

from app.dirs import DIR_APP, DIR_LINTERS, DIR_TESTS


def run_linters() -> None:
    """
    Executes a series of commands to run linters
    with certain parameters.
    """
    commands = (
        [
            "pylint",
            f"--rcfile={DIR_LINTERS / '.pylintrc'}",
            f"{DIR_APP}",
            f"{DIR_TESTS}",
        ],
        ["isort", "-c", f"{DIR_APP}", f"{DIR_TESTS}"],
        [
            "flake8",
            "--config",
            f"{DIR_LINTERS / '.flake8'}",
            f"{DIR_APP}",
            f"{DIR_TESTS}",
        ],
        [
            "black",
            "--diff",
            "--config",
            f"{DIR_LINTERS / '.black'}",
            f"{DIR_APP}",
            f"{DIR_TESTS}",
        ],
        [
            "mypy",
            "--config-file",
            f"{DIR_LINTERS / 'mypy.ini'}",
            f"{DIR_APP}",
            f"{DIR_TESTS}",
        ],
    )
    for command in commands:
        print(
            "\n",
            "🔥 ",
            command[0],
        )
        command_ = " ".join(command)
        subprocess.run(command_, check=False)


if __name__ == "__main__":
    run_linters()
