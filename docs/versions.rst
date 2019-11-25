Version history
===============

0.4.0
-----

*25th November 2019*

* Updated main script to accept a specific path to serve files from.

0.3.0
-----

*8th November 2019*

* Replaced the `selector` argument given to handlers with a
  :class:`Request <gopher_server.handlers.Request>` object. This allows the
  handler to know the hostname and port number to use for local links in menus.
* `DirectoryHandler`: Added functionality to automatically generate menus for
  subdirectories.
* `PatternHandler`: Added support for both synchronous and async view
  functions.

0.2.0
-----

*23rd October 2019*

* Added a main script so the server can be run with `python -m gopher_server`.
* Moved `quic_listener`'s dependencies to an extra.

0.1.0
-----

*14th October 2019*

* Original release.
