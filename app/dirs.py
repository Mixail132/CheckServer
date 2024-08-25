""" Making the relative paths to the project files."""

from pathlib import Path

DIR_ROOT = Path(__file__).parent.parent.resolve()
DIR_APP = DIR_ROOT / "app"
DIR_LINTERS = DIR_ROOT / ".github" / "settings"
DIR_TEMP = DIR_ROOT / ".temp"
DIR_STATIC = DIR_ROOT / "static"
DIR_TESTS = DIR_ROOT / "tests"
