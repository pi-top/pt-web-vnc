import logging
from typing import Callable, Optional
from urllib.parse import urlparse

from .display_activity_monitor import start_activity_monitor, stop_activity_monitor
from .utils import run_command

logger = logging.getLogger(__name__)


def start(
    display_id: int,
    window_title: Optional[str] = None,
    ssl_certificate: Optional[str] = None,
    height: Optional[int] = None,
    width: Optional[int] = None,
    depth: Optional[int] = None,
    run: Optional[str] = None,
    background_colour: Optional[str] = None,
    with_window_manager: Optional[bool] = None,
    on_display_activity: Optional[Callable] = None,
) -> None:
    cmd = f"pt-web-vnc start --display-id {display_id}"

    if window_title:
        cmd += f"--window-title {window_title} "
    if ssl_certificate:
        cmd += f"--ssl-certificate {ssl_certificate} "
    if height:
        cmd += f"--height {height} "
    if width:
        cmd += f"--width {width} "
    if depth:
        cmd += f"--depth {depth} "
    if run:
        cmd += f"--run-command {run} "
    if background_colour:
        cmd += f"--background-colour {background_colour} "
    if with_window_manager:
        cmd += "--with-window-manager "

    logging.info(f"Starting pt-web-vnc: {cmd}")
    run_command(cmd, timeout=10)

    if callable(on_display_activity):
        start_activity_monitor(
            display_id, on_display_activity, connection_details(display_id)
        )


def stop(display_id: int) -> None:
    cmd = f"pt-web-vnc stop --display-id {display_id}"
    logging.info(f"Stopping pt-web-vnc: {cmd}")
    run_command(cmd, timeout=10)
    stop_activity_monitor(display_id)


class VncConnectionDetails:
    def __init__(self, url) -> None:
        self._parsed_url = urlparse(url)

    @property
    def url(self):
        return self._parsed_url.geturl()

    @property
    def hostname(self):
        return self._parsed_url.hostname

    @property
    def port(self):
        return self._parsed_url.port

    @property
    def path(self):
        return f"{self._parsed_url.path}?{self._parsed_url.query}"


def connection_details(display_id: int) -> VncConnectionDetails:
    cmd = f"pt-web-vnc url --display-id {display_id}"
    logging.info(f"Getting pt-web-vnc connection details: {cmd}")
    url = run_command(cmd, timeout=10)
    return VncConnectionDetails(url=url.strip())


async def async_start(*args, **kwargs):
    pass


async def async_stop(*args, **kwargs):
    pass


async def async_connection_details(*args, **kwargs):
    pass
