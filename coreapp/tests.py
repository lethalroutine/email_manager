from django.test import TestCase

from coreapp import models
from emailcoredomain.repository import DjangoRepository
from emailcoredomain.apps import Email


TEST_EMAIL_DATA = {
    'sender': 'test@test.com',
    'subject': 'test subject',
    'body': 'test body',
    'status': 'P',
}

TEST_DOMAIN_EMAIL_DATA = {
    'status': 'P',
    'recipients': ['test@test.com'],
    'subject': 'test subject',
    'message_body': 'test message',
    'sender': 'sender@test.com',
    'id': 1,
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


class RepositoryBasicTestCase(TestCase):
    def setUp(self):
        self.repo = DjangoRepository()

    def test_repo_can_save_email_from_domain(self):
        email_domain = Email(**TEST_DOMAIN_EMAIL_DATA)

        self.repo.save_email(email_domain)

        [email_model] = models.Email.objects.all()

        self.assertEqual(email_model.sender, email_domain.sender)

    def test_repo_can_get_domain_email_from_db(self):
        email_model = models.Email.objects.create(**TEST_EMAIL_DATA)

        email_domain = self.repo.get_email(email_model.id)

        self.assertEqual(email_model.sender, email_domain.sender)

    def test_repo_can_get_all_domain_email_from_db(self):
        email_model1 = models.Email.objects.create(**TEST_EMAIL_DATA)
        email_model2 = models.Email.objects.create(**TEST_EMAIL_DATA)

        domain_emails = self.repo.get_all_emails()

        self.assertEqual([email.id for email in domain_emails], [email_model1.id, email_model2.id])

    def test_repo_mark_email_as_sent(self):
        email = create_test_email()
        self.repo.mark_as_sent(email.id)
        email.refresh_from_db()
        self.assertEqual(email.status, 'S')
