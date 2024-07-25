import subprocess
import time
import vars
import telegram


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
    except subprocess.CalledProcessError:
        return False


def ping_servers():
    for plant_source, plant_ips in vars.plants.items():
        are_servers_up = []
        for plant_ip in plant_ips*3:
            server_up = is_server_up(f'{vars.ip_prefix}{plant_ip}')
            are_servers_up.append(server_up)
        if all(are_servers_up) is False:
            telegram.send_alarm(
                f"Авария! {vars.al_prefix} {vars.messages[plant_source.lower()]}"
                )
            continue


if __name__ == "__main__":
    while True:
        ping_servers()
        time.sleep(10)
