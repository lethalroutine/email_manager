from django.db import models


class Recipient(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email_address = models.EmailField(max_length=50)
    parent_email = models.ForeignKey('Email', on_delete=models.CASCADE)


class Email(models.Model):
    sender = models.EmailField(max_length=50)
    subject = models.CharField(max_length=50)
    body = models.TextField()
    status = models.CharField(choices=[('P', 'pending'), ('S', 'sent')], max_length=1)
