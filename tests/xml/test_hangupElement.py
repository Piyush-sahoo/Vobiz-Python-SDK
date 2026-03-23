from unittest import TestCase

from vobiz import vobizxml
from tests import VobizXmlTestCase


class HangupElementTest(TestCase, VobizXmlTestCase):
    def test_set_methods(self):
        schedule = 60
        reason = "rejected"
        expected_response = '<Response><Hangup reason="rejected" schedule="60"/></Response>'

        element = vobizxml.ResponseElement()
        response = element.add(
            vobizxml.HangupElement().set_reason(reason).set_schedule(schedule)
        ).to_string(False)
        self.assertXmlEqual(response, expected_response)
