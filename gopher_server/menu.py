from dataclasses import dataclass


class Menu(list):
    def serialize(self):
        return "\r\n".join(_.serialize() for _ in self)


@dataclass
class MenuItem:
    type: str # TODO enum
    name: str
    selector: str
    host: str
    port: int

    def serialize(self):
        return "%s%s\t%s\t%s\t%s" % (
            self.type, self.name, self.selector, self.host, self.port,
        )
