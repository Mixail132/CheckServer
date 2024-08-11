from dirs import DIR_ROOT, DIR_APP, DIR_TEMP
import subprocess


def glue_scripts(script_1, script_2, script_3, script_4,  output_script):

    with (open(script_1, "r") as s1,
          open(script_2, "r") as s2,
          open(script_3, "r") as s3,
          open(script_4, "r") as s4,
          open(output_script, "w") as out):

        for script in [s1, s2, s3, s4]:
            for line in script:
                if "app." in line:
                    continue
                elif "__name__" in line:
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
            DIR_ROOT / "static" / "ico.ico",
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
