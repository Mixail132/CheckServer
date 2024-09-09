"""Starting the app."""

from app.audit import AuditShields
from app.dirs import FILE_VARS
from app.vars import Vars

all_vars = Vars(FILE_VARS)
auditor = AuditShields(all_vars)


m = iter(range(1, 100))
while True:

    for net_ in all_vars.nets:
        if not auditor.is_network_out(net_):
            auditor.check_shields(net_)

    alert = auditor.form_alarm_message()
    cancel = auditor.form_cancel_message()

    auditor.send_messages(alert)
    auditor.set_alarm_sending_status()

    auditor.send_messages(cancel)
    auditor.set_cancel_sending_status()

    n = next(m)
    print(n)
    if n == 3:
        for shield, hosts in all_vars.hosts.items():
            if "INET" in shield:
                for host in hosts.keys():
                    hosts[host] = "www.google.com"
