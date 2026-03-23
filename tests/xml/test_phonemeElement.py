from unittest import TestCase

from vobiz import vobizxml
from tests import VobizXmlTestCase


class ElementTest(TestCase, VobizXmlTestCase):
    def test_set_methods(self):
        alphabet = "ipa"
        ph = "t&#x259;mei&#x325;&#x27E;ou&#x325;"
        expected_response = '<Response><Speak><phoneme alphabet="ipa" ph="t&amp;#x259;mei&amp;' \
                            '#x325;&amp;#x27E;ou&amp;#x325;">Well</phoneme></Speak></Response>'

        element = vobizxml.ResponseElement()
        response = element.add(
            vobizxml.SpeakElement("").add(
                vobizxml.PhonemeElement("Well").set_alphabet(alphabet).set_ph(ph)
            )
        ).to_string(False)
        self.assertXmlEqual(response, expected_response)
