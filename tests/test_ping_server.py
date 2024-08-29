"""Using system ping command hosts checking."""

import subprocess

from app.audit import AuditShields
from app.vars import Vars


def test_base_ping_settings_work_fine(config_vars_set: Vars) -> None:
    """Checks the project's ping job using always in touch server."""

    # vars_ = config_vars_set
    # inet_hosts = vars_.hosts["INET SOURCE"]
    # audit_shields = AuditShields(vars_)
    # in_touch_host = inet_hosts["IN_TOUCH"]
    # is_host_out = audit_shields.ping_host("www.google.com")
    host = subprocess.run(["ping", "-c", "3", "www.google.com"])
    print(host)
    assert "TTL" in host or "ttl" in host
    # assert is_host_out is False
