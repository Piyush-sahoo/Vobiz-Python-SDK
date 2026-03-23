
from vobiz.utils.validators import *
from vobiz.xml import VobizXMLElement, map_type


class RedirectElement(VobizXMLElement):
    _name = 'Redirect'
    _nestable = []

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, value):
        self.__method = str(value) if value is not None else None

    @validate_args(
        value=[of_type(str)],
    )
    def set_method(self, value):
        self.method = value
        return self

    def __init__(
            self,
            content,
            method=None,
    ):
        super(RedirectElement, self).__init__()

        self.content = content
        self.method = method

    def to_dict(self):
        d = {
            'method': self.method,
        }
        return {
            k: str(map_type(v))
            for k, v in d.items() if v is not None
        }
