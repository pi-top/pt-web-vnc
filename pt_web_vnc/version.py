from pkg_resources import get_distribution

__version__ = "N/A"
try:
    __version__ = get_distribution("pt_web_vnc").version
except Exception:
    pass
