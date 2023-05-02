import asyncio
import logging
from typing import Callable, Optional

from .connection_details import VncConnectionDetails
from .display_activity_monitor import start_activity_monitor, stop_activity_monitor
from .screenshot_monitor import (
    ScreenshotMonitor,
    start_screenshot_monitor,
    stop_screenshot_monitor,
)
from .utils import run_command

logger = logging.getLogger(__name__)


class PtWebVncCommands:
    @staticmethod
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
    ) -> str:
        cmd = f"pt-web-vnc start --display-id {display_id} "

        if window_title:
            cmd += f"--window-title '{window_title}' "
        if ssl_certificate:
            cmd += f"--ssl-certificate '{ssl_certificate}' "
        if height:
            cmd += f"--height {height} "
        if width:
            cmd += f"--width {width} "
        if depth:
            cmd += f"--depth {depth} "
        if run:
            cmd += f"--run '{run}' "
        if background_colour:
            cmd += f"--background-colour '{background_colour}' "
        if with_window_manager:
            cmd += "--with-window-manager "
        return cmd

    @staticmethod
    def stop(display_id) -> str:
        return f"pt-web-vnc stop --display-id {display_id}"

    @staticmethod
    def url(display_id) -> str:
        return f"pt-web-vnc url --display-id {display_id}"

    @staticmethod
    def clients(display_id) -> str:
        return f"pt-web-vnc clients --display-id {display_id}"


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
    cmd = PtWebVncCommands.start(
        display_id=display_id,
        window_title=window_title,
        ssl_certificate=ssl_certificate,
        height=height,
        width=width,
        depth=depth,
        run=run,
        background_colour=background_colour,
        with_window_manager=with_window_manager,
    )

    logging.info(f"Starting pt-web-vnc: {cmd}")

    if callable(on_display_activity):
        raise NotImplementedError(
            "To run the 'on activity' feature, use the 'async_start' function"
        )
    run_command(cmd, timeout=10)


def stop(display_id: int) -> None:
    cmd = PtWebVncCommands.stop(display_id)
    logging.info(f"Stopping pt-web-vnc: {cmd}")
    run_command(cmd, timeout=10)


def connection_details(display_id: int) -> VncConnectionDetails:
    cmd = PtWebVncCommands.url(display_id)
    logging.info(f"Getting pt-web-vnc connection details: {cmd}")
    url = run_command(cmd, timeout=10)
    return VncConnectionDetails(url=url.strip())


def clients(display_id: int) -> int:
    cmd = PtWebVncCommands.clients(display_id)
    logging.info(f"Getting pt-web-vnc clients on display {display_id}: {cmd}")
    try:
        return int(run_command(cmd, timeout=10))
    except Exception:
        return 0


async def async_start(
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
    screenshot_timeout: int = 0,
) -> Optional[ScreenshotMonitor]:
    cmd = PtWebVncCommands.start(
        display_id=display_id,
        window_title=window_title,
        ssl_certificate=ssl_certificate,
        height=height,
        width=width,
        depth=depth,
        run=run,
        background_colour=background_colour,
        with_window_manager=True
        if callable(on_display_activity)
        else with_window_manager,
    )

    logging.info(f"Starting pt-web-vnc: {cmd}")
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await proc.wait()
    if callable(on_display_activity):
        start_activity_monitor(
            display_id, on_display_activity, connection_details(display_id)
        )

    screenshot_monitor = None
    if screenshot_timeout > 0:
        screenshot_monitor = start_screenshot_monitor(display_id, screenshot_timeout)
    return screenshot_monitor


async def async_stop(display_id: int) -> None:
    cmd = PtWebVncCommands.stop(display_id)
    logging.info(f"Stopping pt-web-vnc: {cmd}")
    await stop_activity_monitor(display_id)
    await stop_screenshot_monitor(display_id)
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await proc.wait()


async def async_connection_details(display_id: int) -> VncConnectionDetails:
    cmd = PtWebVncCommands.url(display_id)
    logging.info(f"Getting pt-web-vnc connection details: {cmd}")

    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    novnc_url, _ = await proc.communicate()
    return VncConnectionDetails(url=novnc_url.decode().strip())


async def async_clients(display_id: int) -> int:
    cmd = PtWebVncCommands.clients(display_id)
    logging.info(f"Getting pt-web-vnc clients on display {display_id}: {cmd}")

    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    clients, _ = await proc.communicate()
    try:
        return int(clients.strip())
    except Exception:
        return 0
