from django.db import models

from emailcoredomain.apps import Email as DomainEmail


class Recipient(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email_address = models.EmailField(max_length=50)
    parent_email = models.ForeignKey('Email', on_delete=models.CASCADE, related_name='recipients')


class Email(models.Model):
    sender = models.EmailField(max_length=50)
    subject = models.CharField(max_length=50)
    body = models.TextField()
    status = models.CharField(choices=[('P', 'pending'), ('S', 'sent')], max_length=1)

    @classmethod
    def save_from_core_domain(cls, email):
        model_email = cls.objects.create(
            sender=email.sender,
            subject=email.subject,
            body=email.message_body,
            status=email.status
        )

        for recipient in email.recipients:
            Recipient.objects.create(
                first_name='',
                last_name='',
                email_address=recipient,
                parent_email=model_email
            )

        return model_email.id

    @staticmethod
    def to_core_domain(email_model):
        email_domain = DomainEmail(
            **{
                'id': email_model.id,
                'status': email_model.status,
                'sender': email_model.sender,
                'subject': email_model.subject,
                'message_body': email_model.body
            }
        )

        recipients = [recipient.email_address for recipient in email_model.recipients.all()]

        email_domain.recipients = recipients

        return email_domain

    @classmethod
    def to_core_domain_list(cls, emails_collection):
        return [cls.to_core_domain(email_model) for email_model in emails_collection]

