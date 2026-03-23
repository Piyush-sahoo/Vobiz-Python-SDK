from unittest import TestCase

from vobiz import vobizxml
from tests import VobizXmlTestCase


class WaitElementTest(TestCase, VobizXmlTestCase):
    def test_set_methods(self):
        expected_response = '<Response><Wait beep="true" length="1" minSilence="1" silence="true"/></Response>'

        length = 1
        silence = True
        min_silence = 1
        beep = True

        element = vobizxml.ResponseElement()
        response = element.add(
            vobizxml.WaitElement().set_length(length).set_silence(
                silence
            ).set_min_silence(min_silence).set_beep(beep)
        ).to_string(False)

        self.assertXmlEqual(response, expected_response)
