from vobiz.utils.validators import *
from vobiz.xml import VobizXMLElement, map_type


class PhonemeElement(VobizXMLElement):
    _name = 'phoneme'
    _nestable = []

    @property
    def alphabet(self):
        return self.__alphabet

    @alphabet.setter
    def alphabet(self, value):
        self.__alphabet = str(
            value) if value is not None else None

    @validate_args(
        value=[of_type(str)],
    )
    def set_alphabet(self, value):
        self.alphabet = value
        return self

    @property
    def ph(self):
        return self.__ph

    @ph.setter
    def ph(self, value):
        self.__ph = str(
            value) if value is not None else None

    @validate_args(
        value=[of_type(str)],
    )
    def set_ph(self, value):
        self.ph = value
        return self

    def __init__(
        self,
        content=None,
        alphabet=None,
        ph=None,
    ):

        super(PhonemeElement, self).__init__()
        self.content = content
        self.alphabet = alphabet
        self.ph = ph

    def to_dict(self):
        d = {
            'alphabet': self.alphabet,
            'ph': self.ph,
        }

        return {
            k: str(map_type(v))
            for k, v in d.items() if v is not None
        }
