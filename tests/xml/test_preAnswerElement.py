from unittest import TestCase

from vobiz import vobizxml
from tests import VobizXmlTestCase


class PreAnswerElementTest(TestCase, VobizXmlTestCase):
    def test_set_methods(self):
        expected_response = '<Response><PreAnswer><Speak language="en-US" loop="2" voice="WOMAN">This is test' \
                            '</Speak><Play loop="2">This is test</Play><Wait beep="true" length="1" ' \
                            'minSilence="1" silence="true"/></PreAnswer></Response>'

        content_speak = 'This is test'
        voice_speak = 'WOMAN'
        language_speak = 'en-US'
        loop_speak = 2
        loop_play = 2
        content_play = 'This is test'
        length_wait=1
        silence_wait=True
        min_silence_wait=1
        beep_wait=True

        element = vobizxml.ResponseElement()
        response = element.add(
            vobizxml.PreAnswerElement().add_speak(
                content=content_speak,
                voice=voice_speak,
                language=language_speak,
                loop=loop_speak
            ).add_play(
                content=content_play,
                loop=loop_play
            ).add_wait(
                length=length_wait,
                silence=silence_wait,
                min_silence=min_silence_wait,
                beep=beep_wait,
            )
        ).to_string(False)

        self.assertXmlEqual(response, expected_response)
