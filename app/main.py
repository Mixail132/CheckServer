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
    message = auditor.form_alarm_message()
    auditor.send_alarm_messages(message)
