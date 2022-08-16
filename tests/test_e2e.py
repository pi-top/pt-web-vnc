import asyncio
import re
from os import environ
from tkinter import Tk

import pytest
import requests
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

    # URL has the correct format
    regex = (
        r"http\:\/\/[\-\.a-zA-Z0-9]+:61100\/vnc\.html\?autoconnect=true&resize=scale"
    )
    assert re.match(regex, details.url)

    # Server is running
    url = f"{details.scheme}://localhost:{details.port}{details.path}"
    r = requests.get(url)
    assert r.status_code == 200

    assert callback.call_count == 0

    # force display activity
    environ["DISPLAY"] = ":100"
    Tk()

    await asyncio.sleep(2)

    # Callback was called after display activity
    assert callback.call_count == 1

    await async_stop(display_id=100)

    await asyncio.sleep(10)

    # Server isn't running
    with pytest.raises(requests.exceptions.ConnectionError):
        r = requests.get(url)


def test_e2e():
    start(display_id=50)

    details = connection_details(display_id=50)
    # Server is running
    url = f"{details.scheme}://localhost:{details.port}{details.path}"
    r = requests.get(url)
    assert r.status_code == 200

    regex = (
        r"http\:\/\/[\-\.a-zA-Z0-9]+:61050\/vnc\.html\?autoconnect=true&resize=scale"
    )
    assert re.match(regex, details.url)

    stop(display_id=50)

    # Server isn't running
    with pytest.raises(requests.exceptions.ConnectionError):
        r = requests.get(url)
