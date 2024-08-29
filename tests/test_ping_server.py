"""Using system ping command hosts checking."""

from app.audit import AuditShields

# from app.vars import Vars


def test_base_ping_settings_work_fine(config_vars_set) -> None:
    """Checks the project's ping job using always in touch server."""

    vars_ = config_vars_set
    inet_hosts = vars_.hosts["INET SOURCE"]
    audit_shields = AuditShields(vars_)
    in_touch_host = inet_hosts["IN_TOUCH"]
    is_host_out = audit_shields.ping_host(in_touch_host)

    assert is_host_out is False
