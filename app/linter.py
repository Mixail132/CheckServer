import subprocess
from app.vars import DIR_LINTERS_SETTINGS, DIR_APP

def run_linters():
    files = f"{DIR_APP / '*.py'}"
    commands = (
        ["pylint", "app"],
        ["isort", "-c", DIR_APP],
        ["flake8", "--config", f"{DIR_LINTERS_SETTINGS / '.flake8'}", files],
        ["black", "--check", "--line-length", "79", files],
        ["mypy", "--config-file", f"{DIR_LINTERS_SETTINGS / 'mypy.ini'}", DIR_APP]
    )
    for command in commands:
        print(command[0])
        subprocess.run(command)


if __name__ == "__main__":
    run_linters()
