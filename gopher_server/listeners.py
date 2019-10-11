import asyncio
import ssl

from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from gopher_server.application import Application


async def tcp_listener(application: Application, host: str, port: int):
    """Basic unencrypted TCP listener."""
    async def handle_connection(reader, writer):
        data = await reader.readline()
        writer.write(await application.dispatch(data))
        writer.write_eof()
    await asyncio.start_server(handle_connection, host, port)


async def tcp_tls_listener(application: Application, host: str, port: int,
                           certificate_path: str, private_key_path: str, password: str=None):
    """Gopher-over-TLS listener."""
    ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(certificate_path, private_key_path, password)
    async def handle_connection(reader, writer):
        data = await reader.readline()
        writer.write(await application.dispatch(data))
        writer.write_eof()
    await asyncio.start_server(handle_connection, host, port, ssl=ssl_context)


async def quic_listener(application: Application, host: str, port: int,
                        certificate_path: str, private_key_path: str, password: str=None,
                        quic_configuration_args=None):
    """
    Gopher-over-QUIC listener.

    This uses the `aioquic <https://aioquic.readthedocs.io/>`_ library to
    provide a QUIC connection.

    The life-cycle of a QUIC connection is slightly different to a traditional
    TCP connection due to the use of QUIC streams. Gopher-over-TCP only supports
    one request per connection, however `quic_listener` supports one request
    per *stream*, allowing clients to re-use the connection by creating a new
    stream for each request.
    """

    with open(certificate_path, "rb") as f:
        certificate = x509.load_pem_x509_certificate(
            f.read(), backend=default_backend(),
        )
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(), password=password, backend=default_backend(),
        )

    configuration = QuicConfiguration(
        is_client=False,
        certificate=certificate,
        private_key=private_key,
        **quic_configuration_args or {},
    )

    def stream_handler(reader, writer):
        async def handle_stream():
            data = await reader.read()
            writer.write(await application.dispatch(data))
            writer.write_eof()
        asyncio.ensure_future(handle_stream())

    await serve(host, port, configuration=configuration, stream_handler=stream_handler)
