from rest_framework import serializers

from emailcoredomain.apps import Email
from emailcoredomain.repository import DjangoRepository


class RecipientListSerializer(serializers.ListField):
    recipient = serializers.CharField(max_length=50)


class EmailRestApiSerializer(serializers.Serializer):
    recipients = RecipientListSerializer()
    sender = serializers.CharField(max_length=50)
    subject = serializers.CharField(max_length=50)
    message_body = serializers.CharField()
    status = serializers.ChoiceField([('P', 'pending'), ('S', 'sent')])

    def save(self):
        email_data = self.get_email_data()
        repo = DjangoRepository()
        email = Email(**email_data)
        if not email.validate():
            return None
        email_id = repo.save_email(email)

        return email_id

    def get_email_data(self):
        email_fields = self.get_email_fields()
        email_data = {key: value for key, value in self.validated_data.items() if key in email_fields}
        return email_data

    @staticmethod
    def get_email_fields():
        email_fields = Email.MANDATORY_FIELDS_LIST
        return email_fields

    def update(self, instance, validated_data):
        pass

    def create(self):
        pass


class EmailStatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=1)
