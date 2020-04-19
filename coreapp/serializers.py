from rest_framework import serializers

from coreapp import models


class EmailSerializer(serializers.ModelSerializer):
    recipients = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='email_address'
    )

    class Meta:
        fields = ['id', 'recipients', 'sender', 'subject', 'body', 'status']
        model = models.Email


class RecipientListSerializer(serializers.ListField):
    recipient = serializers.CharField(max_length=50)


class EmailRestApiSerializer(serializers.Serializer):
    recipients = RecipientListSerializer()
    sender = serializers.CharField(max_length=50)
    subject = serializers.CharField(max_length=50)
    body = serializers.CharField()
    status = serializers.ChoiceField([('P', 'pending'), ('S', 'sent')])

    def save(self):
        email_data = self.get_email_data()
        email = models.Email.objects.create(**email_data)

        self.save_recipients(email)

    def save_recipients(self, email):
        for recipient in self.validated_data['recipients']:
            models.Recipient.objects.create(
                first_name='',
                last_name='',
                email_address=recipient,
                parent_email=email
            )

    def get_email_data(self):
        email_fields = self.get_email_fields()
        email_data = {key: value for key, value in self.validated_data.items() if key in email_fields}
        return email_data

    def get_email_fields(self):
        return [name.name for name in models.Email._meta.get_fields()[2:]]

    def update(self, instance, validated_data):
        pass

    def create(self):
        pass


class EmailStatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=1)
