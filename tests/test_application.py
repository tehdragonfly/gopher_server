import pytest

from typing import Union
from zope.interface import implementer

from gopher_server.application import Application
from gopher_server.handlers import IHandler


@implementer(IHandler)
class TestHandler:
    async def handle(self, selector: str) -> Union[str, bytes]:
        assert selector in ("string", "bytes", "exception")

        if selector == "string":
            return "test"

        if selector == "bytes":
            return b"test"

        if selector == "exception":
            raise Exception


@pytest.fixture
def application() -> Application:
    return Application(TestHandler())


@pytest.mark.asyncio
async def test_string(application: Application):
    """String responses should finish with a blank line with a dot."""
    response = await application.dispatch(b"string\r\n")
    assert response == b"test\r\n.\r\n"


@pytest.mark.asyncio
async def test_binary(application: Application):
    """Binary responses should not finish with a dot."""
    response = await application.dispatch(b"bytes\r\n")
    assert response == b"test"


@pytest.mark.asyncio
async def test_disallowed_characters(application: Application):
    """The CR, LF and tab characters aren't allowed in selectors."""
    response = await application.dispatch(b"foo\rbar\r\n")
    assert response == b"3Bad selector.\t\terror.host\t0\r\n.\r\n"

    response = await application.dispatch(b"foo\nbar\r\n")
    assert response == b"3Bad selector.\t\terror.host\t0\r\n.\r\n"

    response = await application.dispatch(b"foo\tbar\r\n")
    assert response == b"3Bad selector.\t\terror.host\t0\r\n.\r\n"


@pytest.mark.asyncio
async def test_not_utf8(application: Application):
    """Selectors should be valid UTF-8."""
    response = await application.dispatch(b"\xff")
    assert response == b"3Bad selector.\t\terror.host\t0\r\n.\r\n"


@pytest.mark.asyncio
async def test_exception(application: Application):
    """Exceptions from the handler should be eaten."""
    response = await application.dispatch(b"exception\r\n")
    assert response == b"3Internal server error.\t\terror.host\t0\r\n.\r\n"
