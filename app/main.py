"""Starting and running the app."""

from app.audit import AuditShields
from app.dirs import FILE_VARS
from app.vars import Vars

all_vars = Vars(FILE_VARS)
auditor = AuditShields(all_vars)


while True:

    for net_ in all_vars.nets:
        if not auditor.is_network_out(net_):
            auditor.check_shields(net_)

    alert = auditor.form_alarm_message()
    cancel = auditor.form_cancel_message()

    auditor.delay_sending()
    auditor.send_messages(alert)
    auditor.set_alarm_sending_status()

    auditor.delay_sending()
    auditor.send_messages(cancel)
    auditor.set_cancel_sending_status()
