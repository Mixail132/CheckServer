import subprocess
import telegram
import time
import vars


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

def ping_servers(ip: vars.PlantNet):
    for plant_source, hosts in ip.hosts.items():
        are_servers_up = []
        for host in hosts*3:
            server_up = is_server_up(f'{ip.net}{host}')
            are_servers_up.append(server_up)
        if all(are_servers_up) is False:
            telegram.send_alarm_message(
                f"Авария! {vars.alarm_prefix} {vars.messages[plant_source.lower()]}"
                )
            continue


if __name__ == "__main__":
    while True:
        ping_servers(vars.dispatcher_net)
        ping_servers(vars.local_net)
        time.sleep(10)
