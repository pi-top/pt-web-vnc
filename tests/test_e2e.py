import asyncio
import re
from os import environ
from tkinter import Tk

import pytest
from mock import AsyncMock

from pt_web_vnc.vnc import (
    async_connection_details,
    async_start,
    async_stop,
    connection_details,
    start,
    stop,
)


@pytest.mark.asyncio
async def test_async_e2e():
    callback = AsyncMock()
    await async_start(display_id=100, on_display_activity=callback)

    await asyncio.sleep(1)

    details = await async_connection_details(display_id=100)
    print(details.url)

    regex = (
        r"http\:\/\/[\-\.a-zA-Z0-9]+:61100\/vnc\.html\?autoconnect=true&resize=scale"
    )
    assert re.match(regex, details.url)

    assert callback.call_count == 0

    # force display activity
    environ["DISPLAY"] = ":100"
    Tk()

    await asyncio.sleep(2)
    assert callback.call_count == 1

    await async_stop(display_id=100)

    await asyncio.sleep(0.1)


def test_e2e():
    start(display_id=50)

    details = connection_details(display_id=50)

    regex = (
        r"http\:\/\/[\-\.a-zA-Z0-9]+:61050\/vnc\.html\?autoconnect=true&resize=scale"
    )
    assert re.match(regex, details.url)

    stop(display_id=50)
