from django.test import TestCase

from coreapp import models


def create_test_recipient(parent_email, email_address='test@test.com'):
    return models.Recipient.objects.create(
        first_name='',
        last_name='',
        parent_email=parent_email,
        email_address=email_address
    )


class BasicModelsTestCase(TestCase):
    def setUp(self):
        self.test_email_data = {
            'sender': 'test@test.com',
            'subject': 'test subject',
            'body': 'test body',
            'status': 'pending',
        }

    def test_email_model_can_be_created(self):
        email = models.Email.objects.create(**self.test_email_data)

        self.assertEqual(email.subject, self.test_email_data['subject'])

    def test_recipient_is_assigned_to_email(self):
        email = models.Email.objects.create(**self.test_email_data)
        create_test_recipient(email)

        self.assertEqual(email.recipient_set.first().email_address, 'test@test.com')

    def test_email_can_have_multiple_recipients(self):
        email = models.Email.objects.create(
            **self.test_email_data
        )
        create_test_recipient(email)
        create_test_recipient(email)

        self.assertEqual(len(email.recipient_set.all()), 2)
