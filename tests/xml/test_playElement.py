from unittest import TestCase

from vobiz import vobizxml
from tests import VobizXmlTestCase


class PlayElementTest(TestCase, VobizXmlTestCase):
    def test_set_methods(self):
        expected_response = '<Response><Play loop="1">This is test</Play></Response>'

        loop = 1
        content = 'This is test'
        element = vobizxml.ResponseElement()

        response = element.add(
            vobizxml.PlayElement(content).set_loop(loop)
        ).to_string(False)
        self.assertXmlEqual(response, expected_response)
