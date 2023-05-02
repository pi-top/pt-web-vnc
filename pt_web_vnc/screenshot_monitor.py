import asyncio
import logging

from PIL import ImageGrab

from pt_web_vnc.utils import run_command


class ScreenshotMonitor:
    def __init__(self, display_id, screenshot_timeout) -> None:
        self.display_id = display_id
        self.screenshot_timeout = screenshot_timeout
        self.image = None
        self._stop = False

    def start(self) -> None:
        self._monitor_task = asyncio.create_task(self._screenshot_loop())

    async def _screenshot_loop(self):
        while self._display_is_alive() and not self._stop:
            try:
                self.image = ImageGrab.grab(xdisplay=f":{self.display_id}")
            except Exception as e:
                logging.error(f"Error taking screenshot: {e}")
            await asyncio.sleep(self.screenshot_timeout)
        self.stop()

    def _display_is_alive(self) -> bool:
        try:
            run_command(
                f"xwininfo -d ':{self.display_id}' -all -root",
                timeout=3,
                check=True,
            )
            return True
        except Exception:
            return False

    async def stop(self):
        self._stop = True
        if self._monitor_task and not self._monitor_task.done():
            self._monitor_task.cancel()
            await asyncio.wait([self._monitor_task])
            self._monitor_task = None


screenshot_monitors = {}


def start_activity_monitor(
    display_id: int,
    screenshot_timeout,
):
    screenshot_monitor = ScreenshotMonitor(display_id, screenshot_timeout)

    screenshot_monitors[display_id] = screenshot_monitor
    screenshot_monitor.start()


async def stop_screenshot_monitor(display_id: int):
    screenshot_monitor = screenshot_monitors.get(display_id)
    if screenshot_monitor:
        await screenshot_monitor.stop()
        screenshot_monitors.pop(display_id)
