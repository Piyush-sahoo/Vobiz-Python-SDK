from unittest import TestCase

from vobiz import vobizxml
from tests import VobizXmlTestCase


class GatherElementTest(TestCase, VobizXmlTestCase):
    def test_set_methods(self):
        expected_response = '<Response><Gather action="https://foo.example.com/gather" ' \
                            'digitEndTimeout="auto" executionTimeout="15" finishOnKey="#" ' \
                            'hints="sales,support" inputType="dtmf speech" ' \
                            'interimSpeechResultsCallback="https://foo.example.com/interim" ' \
                            'interimSpeechResultsCallbackMethod="POST" language="en-US" log="true" ' \
                            'method="POST" numDigits="4" profanityFilter="false" redirect="true" ' \
                            'speechEndTimeout="3" speechModel="default"><Speak language="en-US" ' \
                            'loop="1" voice="WOMAN">Say or press your choice.</Speak>' \
                            '<Play loop="1">https://example.com/prompt.mp3</Play></Gather></Response>'

        element = vobizxml.ResponseElement()
        response = element.add(
            vobizxml.GatherElement(
                action='https://foo.example.com/gather',
                method='POST',
                input_type='dtmf speech',
                execution_timeout=15,
                digit_end_timeout='auto',
                speech_end_timeout=3,
                finish_on_key='#',
                num_digits=4,
                speech_model='default',
                hints='sales,support',
                language='en-US',
                interim_speech_results_callback='https://foo.example.com/interim',
                interim_speech_results_callback_method='POST',
                log=True,
                redirect=True,
                profanity_filter=False,
            ).add_speak(
                content='Say or press your choice.',
                voice='WOMAN',
                language='en-US',
                loop=1,
            ).add_play(
                content='https://example.com/prompt.mp3',
                loop=1,
            )
        ).to_string(False)

        self.assertXmlEqual(response, expected_response)