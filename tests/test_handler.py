import os.path
import pytest

from gopher_server.handlers import DirectoryHandler


BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "examples/data/")


@pytest.fixture
def directory_handler():
    return DirectoryHandler(BASE_PATH)


@pytest.mark.asyncio
async def test_directory_handler_file(directory_handler: DirectoryHandler):
    """File path returns file from the directory."""
    response = await directory_handler.handle("example")
    with open(os.path.join(BASE_PATH + "example")) as f:
        assert response == f.read()


@pytest.mark.asyncio
async def test_directory_handler_directory(directory_handler: DirectoryHandler):
    """Directory name returns index file from the directory."""
    response = await directory_handler.handle("")
    with open(os.path.join(BASE_PATH + "index")) as f:
        assert response == f.read()
