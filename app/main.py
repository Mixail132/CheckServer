import subprocess
import time
from app.telegram import send_alarm_message
from app.vars import Plant


def is_server_up(ip_addr):
    command = ["ping", "-n", "3", ip_addr,]
    subprocess.run(
        ["chcp", "437"],
        shell=False,
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
        for _ in range(3):
            servers_up += [is_server_up(host) for host in hosts.values()]

        if all(servers_up) is False and not vent_units.sendings[shield]:
            send_alarm_message(f"{vent_units.messages[shield]}")
            vent_units.sendings[shield] = True

        elif all(servers_up) is True:
            vent_units.sendings[shield] = False


plants = Plant()
while True:
    ping_servers(plants)
    time.sleep(30)
