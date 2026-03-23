from vobiz.utils.validators import *
from vobiz.xml import VobizXMLElement, map_type


class BreakElement(VobizXMLElement):
    _name = 'break'
    _nestable = []

    @property
    def strength(self):
        return self.__strength

    @strength.setter
    def strength(self, value):
        self.__strength = str(
            value) if value is not None else None

    @validate_args(
        value=[of_type(str)],
    )
    def set_strength(self, value):
        self.strength = value
        return self

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, value):
        self.__time = str(
            value) if value is not None else None

    @validate_args(
        value=[of_type(str)],
    )
    def set_time(self, value):
        self.time = value
        return self

    def __init__(
        self,
        content=None,
        strength=None,
        time=None,
    ):

        super(BreakElement, self).__init__()
        self.content = content
        self.strength = strength
        self.time = time

    def to_dict(self):
        d = {
            'strength': self.strength,
            'time': self.time,
        }

        return {
            k: str(map_type(v))
            for k, v in d.items() if v is not None
        }
