from vars import allvars


class Host:
    def __init__(self, source):
        self.source = source


for shield_name in allvars.sorces:
    host = Host(shield_name)



# host.shield_name = "RPV_09"
# host.plant_name = "PV_212"
# host.ip_address = "192.168.104.231"
# host.shield_status = True
# host.alarm_status = True
# host.message_sent = False
# host.net_type = "Lan"
# host.net_checker = "192.168.250.50"


