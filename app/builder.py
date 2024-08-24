""" Actions for building the output 'exe' file. """

import subprocess
from pathlib import Path

from app.dirs import DIR_APP, DIR_STATIC, DIR_TEMP


def glue_scripts(
    output_script: Path,
    input_scripts: list[Path],
) -> None:
    """Combines all the scripts to a single one."""
    with open(output_script, "w", encoding="utf-8") as out:
        for script in input_scripts:
            with open(script, "r", encoding="utf-8") as lines:
                for line in lines:
                    if "app." in line or '"""' in line:
                        continue
                    if "__name__" in line:
                        break
                    out.write(line)
                out.write("\n\n")


if __name__ == "__main__":

    files = [
        DIR_APP / "dirs.py",
        DIR_APP / "vars.py",
        DIR_APP / "telegram.py",
        DIR_APP / "viber.py",
        DIR_APP / "main.py",
    ]

    output_file = DIR_APP / "commons.py"

    glue_scripts(output_file, files)

    subprocess.run(
        [
            "autopep8",
            "--in-place",
            "--aggressive",
            output_file,
        ],
        check=True,
    )

    subprocess.run(["isort", output_file], check=True)

    subprocess.run(
        [
            "pyinstaller",
            "--noconfirm",
            "--onefile",
            "--windowed",
            "--icon",
            DIR_STATIC / "ico.ico",
            "--name",
            "CheckServer",
            DIR_APP / "commons.py",
            "--distpath",
            DIR_APP,
            "--workpath",
            DIR_TEMP / "build",
            "--specpath",
            DIR_TEMP,
        ],
        check=True,
    )
