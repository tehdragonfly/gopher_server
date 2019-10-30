import os.path
import pytest

from gopher_server.handlers import DirectoryHandler, NotFound, PatternHandler, Request


BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "examples/data/")


@pytest.fixture
def directory_handler() -> DirectoryHandler:
    return DirectoryHandler(BASE_PATH)


@pytest.mark.asyncio
async def test_directory_handler_file(directory_handler: DirectoryHandler):
    """File path returns file from the directory."""
    response = await directory_handler.handle(Request("localhost", 7000, "example"))
    with open(os.path.join(BASE_PATH + "example")) as f:
        assert response == f.read()


@pytest.mark.asyncio
async def test_directory_handler_binary(directory_handler: DirectoryHandler):
    """Binary files are returned as bytes."""
    response = await directory_handler.handle(Request("localhost", 7000, "image.png"))
    with open(os.path.join(BASE_PATH + "image.png"), "rb") as f:
        assert response == f.read()


@pytest.mark.asyncio
async def test_directory_handler_directory(directory_handler: DirectoryHandler):
    """Directory name returns index file from the directory."""
    response = await directory_handler.handle(Request("localhost", 7000, ""))
    with open(os.path.join(BASE_PATH + "index")) as f:
        assert response == f.read()


@pytest.mark.asyncio
async def test_directory_handler_not_found(directory_handler: DirectoryHandler):
    """Non-existient file raises NotFound."""
    with pytest.raises(NotFound):
        await directory_handler.handle(Request("localhost", 7000, "qwertyuiop"))


@pytest.fixture
def pattern_handler() -> PatternHandler:
    handler = PatternHandler()

    @handler.register("static_pattern")
    def static_pattern(request):
        """Static pattern function just receives the selector."""
        assert request.selector == "static_pattern"
        return "static pattern response"

    @handler.register("dynamic_pattern/(?P<arg>.+)")
    def dynamic_pattern(request, not_arg=None, arg=None):
        """Dynamic pattern function receives named capturing groups as keyword arguments."""
        assert request.selector == "dynamic_pattern/" + arg
        assert not_arg is None
        return "dynamic response for " + arg

    return handler


@pytest.mark.asyncio
async def test_pattern_handler_static(pattern_handler: PatternHandler):
    response = await pattern_handler.handle(Request("localhost", 7000, "static_pattern"))
    assert response == "static pattern response"


@pytest.mark.asyncio
async def test_pattern_handler_dynamic(pattern_handler: PatternHandler):
    response = await pattern_handler.handle(Request("localhost", 7000, "dynamic_pattern/foo"))
    assert response == "dynamic response for foo"


@pytest.mark.asyncio
async def test_pattern_handler_not_found(pattern_handler: PatternHandler):
    """Unrecognised pattern raises NotFound."""
    with pytest.raises(NotFound):
        await pattern_handler.handle(Request("localhost", 7000, "qwertyuiop"))
