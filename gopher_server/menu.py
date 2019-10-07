from dataclasses import dataclass


class Menu(list):
    """
    Convenience class for building menus.

    This is a list wrapper which serialises and concatenates any
    :class:`MenuItem`\ s and :class:`InfoMenuItem`\ s contained within.
    """

    def serialize(self) -> str:
        """Serialise and concatenate the contained items."""
        return "\r\n".join(
            (_ if isinstance(_, str) else _.serialize())
            for _ in self
        )


@dataclass
class MenuItem:
    """A menu item of any kind."""

    type: str # TODO enum
    name: str
    selector: str
    host: str
    port: int

    def serialize(self) -> str:
        """Serialise the menu item to a string."""
        return "%s%s\t%s\t%s\t%s" % (
            self.type, self.name, self.selector, self.host, self.port,
        )


class InfoMenuItem:
    """
    An information (`i`) menu item.

    This automatically fills the selector, hostname and port columns with dummy
    values.
    """

    def __init__(self, name: str):
        self.name = name

    def serialize(self) -> str:
        """Serialise the menu item to a string."""
        return "i%s\t\terror.host\t0" % self.name
