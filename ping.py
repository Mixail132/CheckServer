import subprocess
import time
import datetime
from vars import *

def is_server_up(host):
    command = ["ping", "-n", "1", host,]
    time.sleep(3)
    subprocess.run(
        ["chcp", "437"],
        shell=True,
        stdout=subprocess.DEVNULL,
    )
    try:
        output = subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            encoding='cp866'
        )
        if "TTL" in output:
            return True
        elif "unreachable" in output:
            return False
    except subprocess.CalledProcessError as e:
        return False


if __name__ =="__main__":
    while True:
        for plant_box, plant_ips in plants.items():
            is_up = []
            for plant_ip in plant_ips:
                is_up.append(is_server_up(f'{ip_prefix}{plant_ip}'))
            if all(is_up) is False:
                print(datetime.datetime.now(), messages[plant_box])
                continue
        time.sleep(10)
