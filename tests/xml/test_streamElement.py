from unittest import TestCase

from vobiz import vobizxml
from vobiz.exceptions import ValidationError
from tests import VobizXmlTestCase


class StreamElementTest(TestCase, VobizXmlTestCase):
    def test_set_methods(self):
        expected_response = """<Response>
                                    <Stream bidirectional="true" extraHeaders="a=1,b=2" keepCallAlive="true">wss://test.url</Stream>
                                </Response>"""

        content = 'wss://test.url'
        bidirectional = True
        extraHeaders = "a=1,b=2"
        keepCallAlive = True

        element = vobizxml.ResponseElement()
        response = element.add(
            vobizxml.StreamElement(content, bidirectional=bidirectional, extraHeaders=extraHeaders, keepCallAlive=keepCallAlive)
        ).to_string(False)
        self.assertXmlEqual(response, expected_response)

    def test_validations_on_elements(self):
        expected_error = 'bidirectional must be a boolean value.'

        actual_error = ''
        content = 'wss://test.url'
        bidirectional = "hello"
        try:
            vobizxml.StreamElement(content=content, bidirectional=bidirectional)
        except ValidationError as e:
            print("Error: ", str(e))
            actual_error = str(e)
        self.assertXmlEqual(expected_error, actual_error)
