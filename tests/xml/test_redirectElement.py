from unittest import TestCase

from vobiz import vobizxml
from tests import VobizXmlTestCase


class RedirectElementTest(TestCase, VobizXmlTestCase):
    def test_set_methods(self):
        expected_response = '<Response><Redirect method="POST">This is Test</Redirect></Response>'

        method = "POST"
        content = 'This is Test'

        element = vobizxml.ResponseElement()
        response = element.add(
            vobizxml.RedirectElement(content).set_method(method)
        ).to_string(False)

        self.assertXmlEqual(response, expected_response)
