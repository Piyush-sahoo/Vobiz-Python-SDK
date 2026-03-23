from vobiz.utils.validators import *
from vobiz.xml import VobizXMLElement, map_type


class SubElement(VobizXMLElement):
    _name = 'sub'
    _nestable = []

    @property
    def alias(self):
        return self.__alias

    @alias.setter
    def alias(self, value):
        self.__alias = str(
            value) if value is not None else None

    @validate_args(
        value=[of_type(str)],
    )
    def set_alias(self, value):
        self.alias = value
        return self

    def __init__(
        self,
        content=None,
        alias=None,
    ):
        super(SubElement, self).__init__()

        self.content = content
        self.alias = alias

    def to_dict(self):
        d = {
            'alias': self.alias,
        }

        return {
            k: str(map_type(v))
            for k, v in d.items() if v is not None
        }
