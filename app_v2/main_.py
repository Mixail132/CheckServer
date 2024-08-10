import subprocess
from app_v2.telegram_ import send_telegram_message
from app_v2.viber_ import send_viber_message
from app_v2.vars_ import Vars, allvars


class AuditShields:

    def __init__(self, config_vars: Vars) -> None:
        self.vars = config_vars
        self.shields_out = {}
        self.messages_sent = {}

    @staticmethod
    def ping_host(ip_address: str) -> bool:
        """ Checks a single host if it's up or out """
        command = ["ping", "-n", "1", ip_address, ]
        subprocess.run(["chcp", "437"], shell=True, stdout=subprocess.DEVNULL, )
        try:
            output = subprocess.check_output(
                command,
                stderr=subprocess.STDOUT,
                encoding='cp866',
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except subprocess.CalledProcessError as err:
            output = err.output

        if "TTL" in output:
            return False
        elif "100%" in output:
            return True

    def is_network_out(self, network: str) -> bool:
        """ Checks an always working host to make sure its network works """
        checking_host_ip = self.vars.hosts[f"{network} SOURCE"]["in_touch"]
        is_out = self.ping_host(checking_host_ip)
        return is_out

    def check_shields(self, network: str) -> dict:
        for shield, hosts in self.vars.hosts.items():
            if network in shield and "SOURCE" not in shield:
                hosts_out = [self.ping_host(host) for host in hosts.values()]
                self.shields_out.update({shield: all(hosts_out)})
        return self.shields_out

    def form_alarm_message(self) -> str:
        """ Composes an alarm message text regarding the certain equipment alarm """
        message_text = ""
        for shield, status in self.shields_out.items():
            if not status:
                continue
            if not self.vars.sendings[shield]:
                self.vars.sendings[shield] = True
                message_text += f"{self.vars.messages[shield]} \n"
        return message_text

    @staticmethod
    def send_alarm_message(text: str) -> None:
        """ Sends the alarm message to proper Telegram and Viber users """
        if text:
            text = f"Alarm!\n{text}"
            send_telegram_message(text)
            send_viber_message(text)


auditor = AuditShields(allvars)

while True:
    for net in ["WIFI", "DLAN"]:
        if auditor.is_network_out(net):
            auditor.check_shields(net)
    message = auditor.form_alarm_message()
    auditor.send_alarm_message(message)
