import subprocess
import time
from app.telegram import send_alarm_message
from app.vars import plants


def is_server_out(ip_addr):
    command = ["ping", "-n", "2", ip_addr,]
    subprocess.run(
        ["chcp", "437"],
        shell=True,
        stdout=subprocess.DEVNULL,
    )
    try:
        output = subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            encoding='cp866',
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except subprocess.CalledProcessError:
        return True

    if "TTL" in output:
        return False
    elif "unreachable" in output:
        return True


def ping_servers(vent_units):
    for shield, hosts in vent_units.hosts.items():

        servers_out = [is_server_out(host) for host in hosts.values()]
        servers_out += [is_server_out(host) for host in hosts.values()]

        if all(servers_out) and not vent_units.sendings[shield]:
            send_alarm_message(f"{vent_units.messages[shield]}")
            vent_units.sendings[shield] = True

        elif not all(servers_out):
            vent_units.sendings[shield] = False


while True:
    ping_servers(plants)
    time.sleep(30)
