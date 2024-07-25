import subprocess
import time
import vars
import telegram


def is_server_up(host):
    command = ["ping", "-n", "1", host,]
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
    except subprocess.CalledProcessError:
        return False


def ping_servers(plant_addresses):
    for plant_source, plant_ips in plant_addresses.ip_addresses.items():
        are_servers_up = []
        for plant_ip in plant_ips*3:
            server_up = is_server_up(f'{plant_addresses.ip_prefix}{plant_ip}')
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
