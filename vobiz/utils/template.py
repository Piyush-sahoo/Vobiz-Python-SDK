from vobiz.utils.location import Location


class Parameter:
    def __init__(
        self,
        type,
        text=None,
        media=None,
        payload=None,
        currency=None,
        date_time=None,
        location=None,
        parameter_name=None,
    ):
        self.type = type
        self.text = text
        self.media = media
        self.payload = payload
        self.currency = Currency(**currency) if currency else None
        self.date_time = DateTime(**date_time) if date_time else None
        self.location = location
        self.parameter_name = parameter_name


class Component:
    def __init__(self, type, sub_type=None, index=None, parameters=None):
        self.type = type
        self.sub_type = sub_type
        self.index = index
        self.parameters = parameters if parameters is not None else []


class Template:
    def __init__(self, name, language, components=None):
        self.name = name
        self.language = language
        self.components = components if components is not None else []


class Currency:
    def __init__(self, fallback_value, currency_code, amount_1000):
        self.fallback_value = fallback_value
        self.currency_code = currency_code
        self.amount_1000 = amount_1000


class DateTime:
    def __init__(self, fallback_value):
        self.fallback_value = fallback_value
