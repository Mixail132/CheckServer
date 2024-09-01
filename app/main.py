"""Starting the app."""

from app.audit import AuditShields
from app.dirs import FILE_VARS
from app.vars import Vars

all_vars = Vars(FILE_VARS)
auditor = AuditShields(all_vars)
nets_ = ["WIFI", "DLAN", "INET"]


while True:

    for net_ in nets_:
        if not auditor.is_network_out(net_):
            auditor.check_shields(net_)

    alert_message = auditor.form_alarm_message()

    if alert_message:
        auditor.send_alarm_messages(alert_message)
        auditor.set_sending_status()
