from rest_framework import serializers

from coreapp import models


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Recipient


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Email
