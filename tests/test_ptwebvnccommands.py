from pt_web_vnc.vnc import PtWebVncCommands


def test_start_command():
    assert (
        PtWebVncCommands.start(display_id=100) == "pt-web-vnc start --display-id 100 "
    )
    assert (
        PtWebVncCommands.start(display_id=100, window_title="wpagui")
        == "pt-web-vnc start --display-id 100 --window-title 'wpagui' "
    )
    assert PtWebVncCommands.start(
        display_id=100,
        window_title="wpagui",
        ssl_certificate="/tmp/file.cert",
        height=1080,
        width=1920,
        depth=8,
        run="ls -la",
        background_colour="blue",
        with_window_manager=True,
    ) == (
        "pt-web-vnc start --display-id 100 "
        "--window-title 'wpagui' --ssl-certificate '/tmp/file.cert' "
        "--height 1080 --width 1920 --depth 8 --run 'ls -la' "
        "--background-colour 'blue' --with-window-manager "
    )


def test_stop_command():
    assert PtWebVncCommands.stop(display_id=100) == "pt-web-vnc stop --display-id 100"


def test_url_command():
    assert PtWebVncCommands.url(display_id=100) == "pt-web-vnc url --display-id 100"


def test_clients_command():
    assert (
        PtWebVncCommands.clients(display_id=100)
        == "pt-web-vnc clients --display-id 100"
    )
