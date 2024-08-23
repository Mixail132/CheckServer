"""Run the linters locally."""

import subprocess

from app.vars import DIR_APP, DIR_LINTERS


def run_linters():
    """Launches the linters with their settings."""

    commands = (
        ["pylint", f"--rcfile={DIR_LINTERS / '.pylintrc'}", "app"],
        ["isort", "-c", DIR_APP],
        ["flake8", "--config", f"{DIR_LINTERS / '.flake8'}", DIR_APP],
        ["black", "--diff", "--config", f"{DIR_LINTERS / '.black'}", "."],
        ["mypy", "--config-file", f"{DIR_LINTERS / 'mypy.ini'}", DIR_APP],
    )
    for command in commands:
        print(command[0])
        subprocess.run(command, check=False)


if __name__ == "__main__":
    run_linters()
