""" Actions for building the output 'exe' file. """

import subprocess
from pathlib import Path

from app.vars import DIR_APP, DIR_STATIC, DIR_TEMP


def glue_scripts(
        script_1: Path,
        script_2: Path,
        script_3: Path,
        script_4: Path,
        output_script: Path,
) -> None:
    """ Combines all the scripts to a single one. """

    with (open(script_1, "r", encoding="utf-8") as s1,
          open(script_2, "r", encoding="utf-8") as s2,
          open(script_3, "r", encoding="utf-8") as s3,
          open(script_4, "r", encoding="utf-8") as s4,
          open(output_script, "w") as out):

        for script in [s1, s2, s3, s4]:
            for line in script:
                if 'app.' in line:
                    continue
                if '"""' in line:
                    continue
                elif '__name__' in line:
                    break
                out.write(line)
            out.write("\n\n")


if __name__ == "__main__":
    file_1 = DIR_APP / "vars.py"
    file_2 = DIR_APP / "telegram.py"
    file_3 = DIR_APP / "viber.py"
    file_4 = DIR_APP / "main.py"
    output_file = DIR_APP / "commons.py"

    glue_scripts(
        file_1,
        file_2,
        file_3,
        file_4,
        output_file,
    )

    subprocess.run(
        [
         "autopep8",
         "--in-place",
         "--aggressive",
         output_file
        ]
    )

    subprocess.run(
        [
         "isort",
         output_file
        ]
    )

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
            DIR_TEMP
        ]
    )
