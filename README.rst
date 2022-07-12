pt-web-vnc
==========

Serve displays and particular applications via VNC & http using `x11vnc` & `novnc`.

Usage
=====

.. code-block:: bash

	pt-web-vnc <COMMAND> --display-id <DISPLAY_ID> --HEIGHT <SCREEN_HEIGHT> --WIDTH <SCREEN_WIDTH> --ssl_certificate <SSL_CERTIFICATE> --window-title <WINDOW_TITLE> --run <RUN_COMMAND> --background-colour <COLOUR>
	where:
		COMMAND: start, stop, url.
		DISPLAY_ID: integer, id for the display to use/create.
		SCREEN_HEIGHT: integer, height in pixels for the virtual display to create. Defaults to 1080.
		SCREEN_WIDTH: integer, width in pixels for the virtual display to create. Defaults to 1920.
		SSL_CERTIFICATE: path to combined SSL certificate & key file. Optional.
		WINDOW_TITLE: Title of a window in a display to share over VNC. Optional.
		RUN_COMMAND: Command to run before starting VNC server.
		COLOUR: string with a colour name to use as background for the virtual display.

Examples
========

Start a virtual display with custom dimensions and background
-------------------------------------------------------------

.. code-block:: bash

	$ pt-web-vnc start --display-id 100 --height 500 --width 1000 --background-colour red
	# Get the URL to connect
	$ pt-web-vnc start --display-id 100
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
