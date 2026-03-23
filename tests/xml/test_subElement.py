from unittest import TestCase

from vobiz import vobizxml
from tests import VobizXmlTestCase


class SubElementTest(TestCase, VobizXmlTestCase):
    def test_set_methods(self):
        expected_response = '<Response><Speak>substitution example <sub alias="World Wide Web Consortium">W3C</sub></Speak></Response>'
        alias="World Wide Web Consortium"

        element = vobizxml.ResponseElement()
        response = element.add(
            vobizxml.SpeakElement("substitution example ").add(
                vobizxml.SubElement("W3C").set_alias(alias)
            )
        ).to_string(False)
        self.assertXmlEqual(response, expected_response)
