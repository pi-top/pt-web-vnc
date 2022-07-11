import asyncio
import logging
from typing import Callable, List, Optional, Union

from .connection_details import VncConnectionDetails


class DisplayActivityMonitor:
    display_number: int
    callbacks: List
    current_activity: Union[None, str]
    on_display_activity: Optional[Callable]
    _stop: bool
    _monitor_task: Optional[asyncio.Task]
    SLEEP_TIME = 1

    def __init__(self, display_number: int) -> None:
        self.display_number = display_number
        self.callbacks = []
        self.current_activity = None
        self.on_display_activity = None
        self._stop = False
        self._monitor_task = None

    def start(self) -> None:
        self._monitor_task = asyncio.create_task(self._monitor())

    async def _monitor(self) -> None:
        logging.debug(
            f"Starting to monitor for activity on display '{self.display_number}'"
        )
        self._stop = False
        self.current_activity = await self._get_number_of_windows()

        while not self._stop:
            current_windows = await self._get_number_of_windows()
            if current_windows and current_windows != self.current_activity:
                logging.debug(f"Activity detected on display '{self.display_number}'")
                self.current_activity = current_windows
                if callable(self.on_display_activity):
                    await self.on_display_activity()
            await asyncio.sleep(self.SLEEP_TIME)

    async def _get_number_of_windows(self):
        proc = await asyncio.create_subprocess_shell(
            f"xwininfo -d :{self.display_number} -root -tree",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await proc.communicate()
        return stdout

    async def stop(self) -> None:
        logging.debug(
            f"Stopping checks for activity on display '{self.display_number}'"
        )
        self._stop = True
        if self._monitor_task:
            self._monitor_task.cancel()
            await asyncio.wait(self._monitor_task)


display_activity_monitors = {}


def start_activity_monitor(
    display_id: int,
    on_display_activity: Callable,
    connection_details: VncConnectionDetails,
):
    activity_monitor = DisplayActivityMonitor(display_id)

    # Callback to run when there's activity in a display
    async def on_monitor_activity():
        if connection_details:
            await on_display_activity(connection_details)

    display_activity_monitors[display_id] = activity_monitor
    activity_monitor.on_display_activity = on_monitor_activity
    activity_monitor.start()


async def stop_activity_monitor(display_id: int):
    activity_monitor = display_activity_monitors.get(display_id)
    if activity_monitor:
        await activity_monitor.stop()
        display_activity_monitors.pop(display_id)
