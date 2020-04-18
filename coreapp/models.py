from django.db import models


class Recipient(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email_address = models.EmailField()


class Email(models.Model):
    recipients = models.ForeignKey('Recipient')
    sender = models.EmailField()
    subject = models.CharField(max_length=50)
    body = models.TextField()
    status = models.CharField(choices=[('P', 'pending'), ('S', 'sent')])
