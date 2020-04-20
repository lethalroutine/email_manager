from unittest import TestCase

from emailcoredomain.apps import Email


TEST_EMAIL_DATA = {
    'status': 'P',
    'recipients': ['test@test.com'],
    'subject': 'test subject',
    'message_body': 'test message',
    'sender': 'sender@test.com',
    'id': 1,
}
EMAIL_FIELDS = list(TEST_EMAIL_DATA.keys())


def create_sample_email():
    return Email(**TEST_EMAIL_DATA)


class EmailTestCase(TestCase):
    def test_can_create_empty_email_with_basic_fields(self):
        email = Email()
        self.assertTrue(all(field in email.__dict__ for field in EMAIL_FIELDS))

    def test_validation_of_status_field_set_to_none_is_error(self):
        TEST_EMAIL_DATA.pop('status')
        email = Email(**TEST_EMAIL_DATA)
        self.assertTrue(email.validate())
