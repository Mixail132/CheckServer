from app.vars import read_config
from app.vars import DIR_APP


def test_config_file_has_completely_read():
    path = "../app/vars.ini"
    with open(path, "r", encoding="utf-8") as file:
        params = []
        for line in file:
            if line.startswith(";"):
                continue
            elif line.startswith("["):
                continue
            elif line == "\n":
                continue
            else:
                params.append(line)
    for param in params:
        print(param)



if __name__ == "__main__":
    test_config_file_has_completely_read()