from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from coreapp.models import Email
from coreapp.serializers import EmailSerializer, EmailRestApiSerializer


class EmailRestApiView(APIView):
    def get(self, request, format=None):
        emails = Email.objects.all()
        serializer = EmailSerializer(emails, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EmailRestApiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

