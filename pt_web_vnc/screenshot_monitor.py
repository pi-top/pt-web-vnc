import atexit
import logging
from threading import Thread
from time import sleep

from PIL import ImageGrab

from pt_web_vnc.utils import run_command


class ScreenshotMonitor:
    def __init__(self, display_id, screenshot_timeout) -> None:
        self.display_id = display_id
        self.screenshot_timeout = screenshot_timeout
        self.image = None
        self.take_screenshots = True
        self.thread = Thread(target=self.screenshot_loop, daemon=True)
        self.thread.start()
        atexit.register(self.stop)

    def screenshot_loop(self):
        while self.display_is_alive() and self.take_screenshots:
            try:
                self.image = self.grab_screenshot()
                sleep(self.screenshot_timeout)
            except Exception as e:
                logging.error(f"Error taking screenshot: {e}")
        self.stop()

    def grab_screenshot(self):
        return ImageGrab.grab(xdisplay=f":{self.display_id}")

    def display_is_alive(self) -> bool:
        try:
            run_command(
                f"xwininfo -d ':{self.display_id}' -all -root",
                timeout=3,
                check=True,
            )
            return True
        except Exception:
            return False

    def stop(self):
        self.take_screenshots = False
        if self.thread and self.thread.is_alive():
            self.thread.join()
