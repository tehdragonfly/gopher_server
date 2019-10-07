from gopher_server.menu import InfoMenuItem, Menu, MenuItem


def test_menu_item():
    menu_item = MenuItem("0", "foo", "hello/foo", "localhost", 7000)
    assert menu_item.serialize() == "0foo\thello/foo\tlocalhost\t7000"


def test_info_menu_item():
    menu_item = InfoMenuItem("hello world example menu")
    assert menu_item.serialize() == "ihello world example menu\t\terror.host\t0"


def test_menu():
    menu = Menu([
        InfoMenuItem("hello world example menu"),
        "this is a string",
        MenuItem("0", "foo", "hello/foo", "localhost", 7000),
    ])
    assert menu.serialize() == "ihello world example menu\t\terror.host\t0\r\nthis is a string\r\n0foo\thello/foo\tlocalhost\t7000"
