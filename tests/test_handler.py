import os.path
import pytest

from gopher_server.handlers import DirectoryHandler


@pytest.fixture
def directory_handler():
    root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "examples/data/")
    return DirectoryHandler(root)


@pytest.mark.asyncio
async def test_directory_handler_file(directory_handler: DirectoryHandler):
    """File path returns file from the directory."""
    response = await directory_handler.handle("example")
    assert response == "hello world example document\n"


@pytest.mark.asyncio
async def test_directory_handler_directory(directory_handler: DirectoryHandler):
    """Directory name returns index file from the directory."""
    response = await directory_handler.handle("")
    assert response == "iHello world!\t\terror.host\t0\n0example document\t/example\tlocalhost\t7000\n"
