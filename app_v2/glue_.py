import subprocess


def glue_scripts(script_1, script_2, script_3, script_4,  output_script):

    with (open(script_1, "r") as s1,
          open(script_2, "r") as s2,
          open(script_3, "r") as s3,
          open(script_4, "r") as s4,
          open(output_script, "w") as out):

        for line in s1:
            if "app_v2." in line:
                continue
            elif "if __name__" in line:
                break
            out.write(line)
        out.write("\n\n")

        for line in s2:
            if "app_v2." in line:
                continue
            elif "if __name__" in line:
                break
            out.write(line)
        out.write("\n\n")

        for line in s3:
            if "app_v2." in line:
                continue
            elif "if __name__" in line:
                break
            out.write(line)

        for line in s4:
            if "app_v2." in line:
                continue
            elif "if __name__" in line:
                break
            out.write(line)


if __name__ == "__main__":
    file_1 = "vars_.py"
    file_2 = "telegram_.py"
    file_3 = "viber_.py"
    file_4 = "main_.py"
    output_file = "common_.py"

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
    subprocess.run(["isort", output_file])
