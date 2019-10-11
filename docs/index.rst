gopher_server
=============

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Contents:

   api

`gopher_server` is a library for building `Gopher protocol <https://en.wikipedia.org/wiki/Gopher_(protocol)>`_
servers.

For maximum flexibility it takes a layered approach, separating the code for
I/O, Gopher protocol semantics and generating a response.

To get started, take a look at the examples below, or dive right into the
:doc:`API documentation <api>`.

A simple Gopher server
----------------------

Here's an example of a server which serves static files:

.. code-block::
   :linenos:

   from asyncio import get_event_loop

   from gopher_server.application import Application
   from gopher_server.handlers import DirectoryHandler
   from gopher_server.listeners import tcp_listener


   handler = DirectoryHandler("data/")
   application = Application(handler)


   if __name__ == "__main__":
       loop = get_event_loop()
       loop.create_task(tcp_listener(application, "0.0.0.0", 7000))
       loop.run_forever()

The :class:`Application <gopher_server.application.Application>` is initialised
on line 9. Its sole argument is a *handler* (any object implementing the
:class:`IHandler <gopher_server.handlers.IHandler>` interface). In this case we
use a :class:`DirectoryHandler <gopher_server.handlers.DirectoryHandler>`,
which serves static files from a given directory.

The application and handler layers are self-contained and do no I/O. Instead,
the job of listening for connections is done by a *listener* function. On line
14 we use the :func:`tcp_listener <gopher_server.listeners.tcp_listener>`,
which listens for connections using an unencrypted TCP socket (as specified by
the Gopher standard).

Less simple Gopher servers
--------------------------

Alternative listeners
~~~~~~~~~~~~~~~~~~~~~

Whilst Gopher-over-TCP was a reasonable choice in 1993, the modern internet
should be encrypted by default. As such this library provides a couple of
non-standard listeners which have encryption:

* :func:`tcp_tls_listener <gopher_server.listeners.tcp_tls_listener>` serves
  Gopher-over-TLS. Though non-standard, there are many clients which support
  using TLS for encryption.
* :func:`quic_listener <gopher_server.listeners.quic_listener>` serves
  Gopher-over-QUIC. As `the QUIC protocol
  <https://en.wikipedia.org/wiki/QUIC>`_ is still new, client support for this
  is currently almost non-existent.

For hybrid servers it's easy to run multiple listeners with a single
application:

.. code-block::

   if __name__ == "__main__":
       loop = get_event_loop()
       loop.create_task(tcp_listener(application, "0.0.0.0", 7000))
       loop.create_task(tcp_tls_listener(
           application, "0.0.0.0", 7001,
           "server.crt", "key.pem",
       ))
       loop.create_task(quic_listener(
           application, "0.0.0.0", 7000,
           "server.crt", "key.pem",
       ))
       loop.run_forever()

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
