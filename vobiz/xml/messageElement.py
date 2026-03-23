from vobiz.xml import VobizXMLElement, map_type
from vobiz.utils.validators import *


class MessageElement(VobizXMLElement):
    _name = 'Message'
    _nestable = []

    @property
    def src(self):
        return self.__src

    @src.setter
    def src(self, value):
        self.__src = str(value) if value is not None else None

    @validate_args(
        value=[of_type(str)],
    )
    def set_src(self, value):
        self.src = value
        return self

    @property
    def dst(self):
        return self.__dst

    @dst.setter
    def dst(self, value):
        self.__dst = str(value) if value is not None else None

    @validate_args(
        value=[of_type(str)],
    )
    def set_dst(self, value):
        self.dst = value
        return self

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = str(value) if value is not None else None

    @validate_args(
        value=[of_type(str)],
    )
    def set_type(self, value):
        self.type = value
        return self

    @property
    def callback_url(self):
        return self.__callback_url

    @callback_url.setter
    def callback_url(self, value):
        self.__callback_url = str(
            value) if value is not None else None

    @validate_args(
        value=[of_type(str)],
    )
    def set_callback_url(self, value):
        self.callback_url = value
        return self

    @property
    def callback_method(self):
        return self.__callback_method

    @callback_method.setter
    def callback_method(self, value):
        self.__callback_method = str(
            value) if value is not None else None

    @validate_args(
        value=[of_type(str)],
    )
    def set_callback_method(self, value):
        self.callback_method = value
        return self

    def __init__(
            self,
            content,
            src=None,
            dst=None,
            type=None,
            callback_url=None,
            callback_method=None,
    ):
        super(MessageElement, self).__init__()

        self.content = content
        self.src = src
        self.dst = dst
        self.type = type
        self.callback_url = callback_url
        self.callback_method = callback_method

    def to_dict(self):
        d = {
            'src': self.src,
            'dst': self.dst,
            'type': self.type,
            'callbackUrl': self.callback_url,
            'callbackMethod': self.callback_method,
        }
        return {
            k: str(map_type(v))
            for k, v in d.items() if v is not None
        }
