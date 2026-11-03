from importlib.metadata import version

__version__ = "N/A"
try:
    __version__ = version("pt_web_vnc")
except Exception:
    pass
