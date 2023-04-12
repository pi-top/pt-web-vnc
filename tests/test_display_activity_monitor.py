import asyncio

import pytest
from mock import AsyncMock
from testpath import MockCommand

from pt_web_vnc.connection_details import VncConnectionDetails
from pt_web_vnc.display_activity_monitor import (
    display_activity_monitors,
    start_activity_monitor,
    stop_activity_monitor,
)


@pytest.mark.asyncio
async def test_callback_called_on_activity():
    detail = VncConnectionDetails(
        "http://pi-top.local:61000/vnc.html?autoconnect=true&resize=scale"
    )
    callback = AsyncMock()

    start_activity_monitor(100, callback, detail)

    with MockCommand.fixed_output("xwininfo", "0") as xwinfinfo_mock:
        await asyncio.sleep(0.2)  # wait for display monitor to find this

    xwinfinfo_mock.assert_called()
    assert callback.call_count == 0

    with MockCommand.fixed_output("xwininfo", "1") as xwinfinfo_mock:
        await asyncio.sleep(2)  # wait for display monitor to find this

    assert callback.call_count == 1

    await stop_activity_monitor(100)


@pytest.mark.asyncio
async def test_callback_not_called_if_no_activity():
    detail = VncConnectionDetails(
        "http://pi-top.local:61000/vnc.html?autoconnect=true&resize=scale"
    )
    callback = AsyncMock()

    start_activity_monitor(100, callback, detail)

    with MockCommand.fixed_output("xwininfo", "0") as xwinfinfo_mock:
        await asyncio.sleep(0.2)  # wait for display monitor to find this

    xwinfinfo_mock.assert_called()
    assert callback.call_count == 0

    with MockCommand.fixed_output("xwininfo", "0") as xwinfinfo_mock:
        await asyncio.sleep(2)  # wait for display monitor to find this

    assert callback.call_count == 0

    await stop_activity_monitor(100)


@pytest.mark.asyncio
async def test_keep_track_of_displays_to_track_on_start_and_stop():
    detail = VncConnectionDetails(
        "http://pi-top.local:61000/vnc.html?autoconnect=true&resize=scale"
    )
    callback = AsyncMock()

    assert len(display_activity_monitors) == 0
    start_activity_monitor(100, callback, detail)

    assert len(display_activity_monitors) == 1
    assert 100 in display_activity_monitors

    await stop_activity_monitor(100)

    assert len(display_activity_monitors) == 0
    assert 100 not in display_activity_monitors
