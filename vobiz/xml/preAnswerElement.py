
from vobiz.xml import (
    PlayElement,
    VobizXMLElement,
    SpeakElement,
    WaitElement,
    map_type,
    DTMFElement,
    RedirectElement,
    MessageElement,
)


class PreAnswerElement(VobizXMLElement):
    _name = 'PreAnswer'
    _nestable = [
        'Speak',
        'Play',
        'Wait'
    ]

    def __init__(self):
        super(PreAnswerElement, self).__init__()

    def to_dict(self):
        d = {}
        return {
            k: str(map_type(v))
            for k, v in d.items() if v is not None
        }

    def add_speak(
            self,
            content,
            voice=None,
            language=None,
            loop=None, ):
        self.add(
            SpeakElement(
                content=content,
                voice=voice,
                language=language,
                loop=loop, ))
        return self

    def add_play(
            self,
            content,
            loop=None, ):
        self.add(PlayElement(
            content=content,
            loop=loop, ))
        return self

    def add_wait(
            self,
            length=None,
            silence=None,
            min_silence=None,
            beep=None, ):
        self.add(
            WaitElement(
                length=length,
                silence=silence,
                min_silence=min_silence,
                beep=beep, ))
        return self

