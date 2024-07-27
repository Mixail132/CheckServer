import subprocess
import telegram
import time
from vars import plants


def is_server_up(ip_addr):
    command = ["ping", "-n", "1", ip_addr,]
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
    except subprocess.CalledProcessError:
        return False

    if "TTL" in output:
        return True
    elif "unreachable" in output:
        return False


def ping_servers(vent_units):
    for shield, hosts in vent_units.hosts.items():
        servers_up = []
        for host in hosts:
            server_up = is_server_up(host)
            servers_up.append(server_up)
        if all(servers_up) is False:
            telegram.send_alarm_message(f"{vent_units.messages[shield]}")
            continue


if __name__ == "__main__":
    while True:
        ping_servers(plants)
        time.sleep(10)
