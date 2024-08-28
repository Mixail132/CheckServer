"""Using system ping command hosts checking."""

from app.audit import AuditShields
from app.vars import Vars


def test_base_ping_settings_work_fine(config_vars: Vars) -> None:
    """Checks the project's ping job using always in touch server."""

    inet_hosts = config_vars.hosts["INET SOURCE"]
    in_touch_host = inet_hosts["IN_TOUCH"]

    audit_shields = AuditShields(config_vars)
    is_host_out = audit_shields.ping_host(in_touch_host)

    assert is_host_out is False
