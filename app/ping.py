import subprocess
import telegram
import time
from vars import Plant


def is_server_up(ip_addr):
    command = ["ping", "-n", "3", ip_addr,]
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
        servers_up = [is_server_up(host) for host in hosts]
        servers_up += [is_server_up(host) for host in hosts]
        servers_up += [is_server_up(host) for host in hosts]
        if all(servers_up) is False and not vent_units.sendings[shield]:
            telegram.send_alarm_message(f"{vent_units.messages[shield]}")
            vent_units.sendings[shield] = True
        elif all(servers_up) is True:
            vent_units.sendings[shield] = False




if __name__ == "__main__":
    plants = Plant()
    while True:
        ping_servers(plants)
        time.sleep(10)
