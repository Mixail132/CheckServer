import subprocess


def glue_scripts(
        script_1,
        script_2,
        script_3,
        output_script
):

    with (open(script_1, "r") as s1,
          open(script_2, "r") as s2,
          open(script_3, "r") as s3,
          open(output_script, "w") as out):

        for line in s1:
            if "app." in line:
                continue
            out.write(line)
        out.write("\n\n")

        for line in s2:
            if "app." in line:
                continue
            out.write(line)
        out.write("\n\n")

        for line in s3:
            if "app." in line:
                continue
            out.write(line)


if __name__ == "__main__":
    file_1 = "vars.py"
    file_2 = "telegram.py"
    file_3 = "main.py"
    output_file = "common.py"

    glue_scripts(
        file_1,
        file_2,
        file_3,
        output_file
    )

    subprocess.run(
        [
         "autopep8",
         "--in-place",
         "--aggressive",
         output_file
        ]
    )
    subprocess.run(["isort", output_file])
