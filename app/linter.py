"""Run the linters locally."""

import subprocess

from app.dirs import DIR_APP, DIR_LINTERS, DIR_TESTS


def run_linters():
    """Launches the linters with their settings."""

    commands = (
        [
            "pylint",
            f"--rcfile={DIR_LINTERS / '.pylintrc'}",
            DIR_APP,
            DIR_TESTS,
        ],
        ["isort", "-c", DIR_APP, DIR_TESTS],
        [
            "flake8",
            "--config",
            f"{DIR_LINTERS / '.flake8'}",
            DIR_APP,
            DIR_TESTS,
        ],
        [
            "black",
            "--diff",
            "--config",
            f"{DIR_LINTERS / '.black'}",
            DIR_APP,
            DIR_TESTS,
        ],
        [
            "mypy",
            "--config-file",
            f"{DIR_LINTERS / 'mypy.ini'}",
            DIR_APP,
            DIR_TESTS,
        ],
    )
    for command in commands:
        print(
            "\n",
            "🔥 ",
            command[0],
        )
        subprocess.run(command, check=False)


if __name__ == "__main__":
    run_linters()
