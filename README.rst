pt-web-vnc
==========

Serve a display or the window of a particular application via VNC & http using `x11vnc` & `novnc`.
The script can share an existing display or create a new one, depending on the provided display id. New displays are created using `Xvfb` and it's dimensions and color depth can be specified via command line arguments.
It's also possible to share particular windows from a display by using the 'window-title' argument. This will look for a window with the provided name in a given display and will only share that particular section of the display. If this argument is not provided, the whole display is shared.

A python module `pt_web_vnc` is also included which provides synchronous and asynchronous wrappers around the `pt-web-vnc` script.


Usage
=====

.. code-block:: bash

  pt-web-vnc <COMMAND> --display-id <DISPLAY_ID> --HEIGHT <SCREEN_HEIGHT> --WIDTH <SCREEN_WIDTH> --ssl-certificate <SSL_CERTIFICATE> --window-title <WINDOW_TITLE> --run <RUN_COMMAND> --background-colour <COLOUR> --with-window-manager

  where:
    COMMAND: {start, stop, url, clients}
      start: start sharing a display or app based on the given arguments.
      stop: stop sharing the given display.
      url: print the novnc URL where the provided display is being served.
      clients: print the number of clients connected to a particular display.
    --display-id DISPLAY_ID: integer, id for the display to use/create. If the provided display ID doesn\'t exist, a new one will be created.
    --height SCREEN_HEIGHT: integer, height in pixels for the virtual display to create. Defaults to 1080.
    --width SCREEN_WIDTH: integer, width in pixels for the virtual display to create. Defaults to 1920.
    --depth SCREEN_DEPTH: integer, pixel depth for the virtual display to create. Defaults to 24.
    --ssl-certificate SSL_CERTIFICATE: path to combined SSL certificate & key file. Optional.
    --window-title WINDOW_TITLE: Title of a window in a display to share over VNC. Optional.
    --run RUN_COMMAND: Command to run before starting VNC server.
    --background-colour COLOUR: string with a colour name to use as background for the virtual display.
    --with-window-manager: start a window manager in the specified DISPLAY_ID. For now, the window manager used is 'bspwm'.


Examples
========

Start a virtual display with custom dimensions and background
-------------------------------------------------------------

.. code-block:: bash

	$ pt-web-vnc start --display-id 100 --height 500 --width 1000 --background-colour red
	# Get the URL to connect
	$ pt-web-vnc url --display-id 100
	http://pi-top.local:61100/vnc.html?autoconnect=true
	$ pt-web-vnc stop --display-id 100

Run an application in a virtual display and share its window
------------------------------------------------------------

By using the `--run` argument to start an application and providing its window title via `--window-title` it's possible to share a particular window.

.. code-block:: bash

	# Start chromium and look for its window title
	$ pt-web-vnc start --display-id 50 --run 'chromium-browser' --window-title 'New Tab - Chromium'
	# Get the URL to connect
	$ pt-web-vnc url --display-id 50
	http://pi-top.local:61050/vnc.html?autoconnect=true
	$ pt-web-vnc stop --display-id 50

Share an existing display
-------------------------

It's possible to share your main display instead of creating a new one by providing its display id. In most cases, the id for your main display will be `0`.

.. code-block:: bash

	$ pt-web-vnc start --display-id 0
	# Get the URL to connect
	$ pt-web-vnc url --display-id 0
	http://pi-top.local:61000/vnc.html?autoconnect=true
	$ pt-web-vnc stop --display-id 000


Python module examples
======================

Create and share a display with custom dimensions and background colour
-----------------------------------------------------------------------

.. code-block:: python

  >>> from pt_web_vnc import start, connection_details, stop
  >>> start(
  	display_id=50,
  	height=500,
  	width=1000,
  	background_colour="blue",
  )
  >>> # Get connection details
  >>> details = connection_details(display_id=50)
  >>> details.url
  'http://pi-top.local:61050/vnc.html?autoconnect=true&resize=scale'

  >>> # Stop sharing
  >>> stop(display_id=50)


Asynchronously start sharing display 0
--------------------------------------

.. code-block:: python

  >>> import asyncio
  >>> from pt_web_vnc import async_start, async_connection_details, async_stop
  >>> # Start sharing display 0
  >>> asyncio.run(async_start(display_id=0)
  ...
  >>> # Get connection details
  >>> details = asyncio.run(async_connection_details(display_id=0))
  >>> details.url
  'http://pi-top.local:61000/vnc.html?autoconnect=true&resize=scale'
  >>> # Returned object also containes parsed elements of the URL
  >>> details.scheme
  'http'
  >>> details.hostname
  'pi-top.local'
  >>> details.port
  61000
  >>> details.path
  '/vnc.html?autoconnect=true&resize=scale'
  >>> # Stop sharing display 0
  >>> asyncio.run(async_stop(display_id=0)
