from vobiz.utils.validators import *
from vobiz.xml import VobizXMLElement, map_type


class PlayElement(VobizXMLElement):
    _name = 'Play'
    _nestable = []

    @property
    def loop(self):
        return self.__loop

    @loop.setter
    def loop(self, value):
        self.__loop = int(value) if value is not None else None

    @validate_args(
        value=[of_type(int)],
    )
    def set_loop(self, value):
        self.loop = value
        return self

    def __init__(
            self,
            content,
            loop=None,
    ):
        super(PlayElement, self).__init__()

        self.content = content
        self.loop = loop

    def to_dict(self):
        d = {
            'loop': self.loop,
        }
        return {
            k: str(map_type(v))
            for k, v in d.items() if v is not None
        }
