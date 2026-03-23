from vobiz import exceptions
from vobiz.xml.streamElement import StreamElement


class AudioStreamElement(StreamElement):
    """
    AudioStream element.

    Minimal spec-compatible implementation. Mirrors Stream attribute behavior
    while rendering with the AudioStream tag.
    """
    _name = 'AudioStream'

    def __init__(
            self,
            content,
            bidirectional=None,
            audioTrack=None,
            streamTimeout=None,
            statusCallbackUrl=None,
            statusCallbackMethod=None,
            contentType=None,
            extraHeaders=None,
            keepCallAlive=None
    ):
        if content is None or str(content).strip() == '':
            raise exceptions.ValidationError('AudioStream content (WebSocket URL) is required.')
        super(AudioStreamElement, self).__init__(
            content=content,
            bidirectional=bidirectional,
            audioTrack=audioTrack,
            streamTimeout=streamTimeout,
            statusCallbackUrl=statusCallbackUrl,
            statusCallbackMethod=statusCallbackMethod,
            contentType=contentType,
            extraHeaders=extraHeaders,
            keepCallAlive=keepCallAlive,
        )