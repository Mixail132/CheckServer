import subprocess
import time
from app.telegram import send_telegram_message
from app.viber import send_viber_message
from app.vars import plants


def ping_server(ip_addr):
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
    elif "100%" in output:
        return True


def is_server_out(vent_units):
    for shield, hosts in vent_units.hosts.items():

        servers_out = [ping_server(host) for host in hosts.values()]
        servers_out += [ping_server(host) for host in hosts.values()]

        if None in servers_out:
            continue

        elif all(servers_out) and not vent_units.sendings[shield]:
            alarm_message_text = vent_units.messages[shield]
            send_telegram_message(alarm_message_text)
            send_viber_message(alarm_message_text)
            vent_units.sendings[shield] = True

        elif not all(servers_out):
            vent_units.sendings[shield] = False


while True:
    is_server_out(plants)
    time.sleep(30)
