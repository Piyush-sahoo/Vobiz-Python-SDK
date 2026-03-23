class Header:
    def __init__(self, type=None, text=None, media=None):
        self.type = type
        self.text = text
        self.media = media


class Body:
    def __init__(self, text=None):
        self.text = text


class Footer:
    def __init__(self, text=None):
        self.text = text


class Row:
    def __init__(self, id=None, title=None, description=None):
        self.id = id
        self.title = title
        self.description = description


class Section:
    def __init__(self, title=None, rows=None):
        self.title = title
        self.rows = rows if rows is not None else []


class Btn:
    def __init__(self, id=None, title=None, cta_url=None):
        self.id = id
        self.title = title
        self.cta_url = cta_url


class Action:
    def __init__(self, buttons=None, sections=None):
        self.buttons = buttons if buttons is not None else []
        self.sections = sections if sections is not None else []


class Interactive:
    def __init__(self, type=None, header=None, body=None, footer=None, action=None):
        self.type = type
        self.header = header
        self.body = body
        self.footer = footer
        self.action = action
