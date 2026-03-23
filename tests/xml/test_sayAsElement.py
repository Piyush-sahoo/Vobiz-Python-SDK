from unittest import TestCase

from vobiz import vobizxml
from tests import VobizXmlTestCase


class SayAsElementTest(TestCase, VobizXmlTestCase):
    def test_set_methods(self):
        expected_response = '<Response><Speak><say-as format="application/ssml+xml" interpret-as="spell-out">' \
                            'This is Test</say-as></Speak></Response>'
        interpret_as = "spell-out"
        format = "application/ssml+xml"
        content = 'This is Test'

        element = vobizxml.ResponseElement()

        response = element.add(
            vobizxml.SpeakElement("").add(
                vobizxml.SayAsElement(content).set_interpret_as(interpret_as).set_format(format)
            )
        ).to_string(False)

        self.assertXmlEqual(response, expected_response)
