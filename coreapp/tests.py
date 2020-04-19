from django.test import TestCase

from coreapp import models

TEST_EMAIL_DATA = {
    'sender': 'test@test.com',
    'subject': 'test subject',
    'body': 'test body',
    'status': 'pending',
}


def create_test_recipient(parent_email, email_address='test@test.com'):
    return models.Recipient.objects.create(
        first_name='',
        last_name='',
        parent_email=parent_email,
        email_address=email_address
    )


def create_test_email():
    return models.Email.objects.create(
        sender='test@test.com',
        subject='test subject',
        body='test body',
        status='pending'
    )


class BasicModelsTestCase(TestCase):
    def setUp(self):
        self.test_email_data = TEST_EMAIL_DATA

    def test_email_model_can_be_created(self):
        email = models.Email.objects.create(**self.test_email_data)

        self.assertEqual(email.subject, self.test_email_data['subject'])

    def test_recipient_is_assigned_to_email(self):
        email = models.Email.objects.create(**self.test_email_data)
        create_test_recipient(email)

        self.assertEqual(email.recipients.first().email_address, 'test@test.com')

    def test_email_can_have_multiple_recipients(self):
        email = models.Email.objects.create(
            **self.test_email_data
        )
        create_test_recipient(email)
        create_test_recipient(email)

        self.assertEqual(len(email.recipients.all()), 2)
