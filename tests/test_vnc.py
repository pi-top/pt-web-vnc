from unittest.mock import Mock, patch

import pytest
from testpath import MockCommand

from pt_web_vnc.vnc import (
    async_clients,
    async_connection_details,
    async_start,
    async_stop,
    clients,
    connection_details,
    start,
    stop,
)


def test_start():
    with MockCommand("pt-web-vnc") as ptwebvnc:
        start(display_id=100)

    ptwebvnc.assert_called(["start", "--display-id", "100"])


def test_start_on_display_activity():
    callback = Mock()
    with MockCommand("pt-web-vnc") as ptwebvnc:
        with pytest.raises(NotImplementedError):
            start(display_id=100, on_display_activity=callback)

    ptwebvnc.assert_called(["start", "--display-id", "100"])


def test_stop():
    with MockCommand("pt-web-vnc") as ptwebvnc:
        stop(display_id=100)

    ptwebvnc.assert_called(["stop", "--display-id", "100"])


def test_connection_details():
    with MockCommand("pt-web-vnc") as ptwebvnc:
        connection_details(display_id=100)

    ptwebvnc.assert_called(["url", "--display-id", "100"])


def test_clients():
    with MockCommand("pt-web-vnc") as ptwebvnc:
        clients(display_id=100)

    ptwebvnc.assert_called(["clients", "--display-id", "100"])


@pytest.mark.parametrize(
    "command_output,expected_result",
    (
        ("1", 1),
        ("2", 2),
        ("Error", 0),
    ),
)
def test_clients_output(command_output, expected_result):

    with MockCommand.fixed_output("pt-web-vnc", command_output) as ptwebvnc:
        connected_clients = clients(display_id=100)

    assert connected_clients == expected_result
    ptwebvnc.assert_called(["clients", "--display-id", "100"])


@pytest.mark.asyncio
async def test_async_start():

    with MockCommand("pt-web-vnc") as ptwebvnc:
        await async_start(display_id=100)

    ptwebvnc.assert_called(["start", "--display-id", "100"])
    await async_stop(display_id=100)


@patch("pt_web_vnc.vnc.connection_details")
@patch("pt_web_vnc.vnc.start_activity_monitor")
@pytest.mark.asyncio
async def test_async_start_on_display_activity(
    start_activity_monitor_mock, connection_details_mock
):
    callback = Mock()
    with MockCommand("pt-web-vnc") as ptwebvnc:
        await async_start(display_id=100, on_display_activity=callback)

    ptwebvnc.assert_called(["start", "--display-id", "100", "--with-window-manager"])
    start_activity_monitor_mock.assert_called_once_with(
        100, callback, connection_details_mock()
    )
    await async_stop(display_id=100)


@pytest.mark.asyncio
async def test_async_stop():
    with MockCommand("pt-web-vnc") as ptwebvnc:
        await async_stop(display_id=100)

    ptwebvnc.assert_called(["stop", "--display-id", "100"])


@pytest.mark.asyncio
async def test_async_connection_details():
    with MockCommand("pt-web-vnc") as ptwebvnc:
        await async_connection_details(display_id=100)

    ptwebvnc.assert_called(["url", "--display-id", "100"])


@pytest.mark.asyncio
async def test_async_clients():
    with MockCommand("pt-web-vnc") as ptwebvnc:
        await async_clients(display_id=100)

    ptwebvnc.assert_called(["clients", "--display-id", "100"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_output,expected_result",
    (
        ("1", 1),
        ("2", 2),
        ("Error", 0),
    ),
)
async def test_async_clients_output(command_output, expected_result):

    with MockCommand.fixed_output("pt-web-vnc", command_output) as ptwebvnc:
        clients = await async_clients(display_id=100)

    assert clients == expected_result
    ptwebvnc.assert_called(["clients", "--display-id", "100"])
