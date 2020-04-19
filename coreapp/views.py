from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from coreapp.models import Email
from coreapp.serializers import EmailSerializer, EmailRestApiSerializer, EmailStatusSerializer


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


class EmailDetailView(APIView):
    def get(self, request, pk, format=None):
        email = Email.objects.get(pk=pk)
        serializer = EmailSerializer(email)

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        email = Email.objects.get(pk=pk)
        serializer = EmailStatusSerializer(data=request.data)
        if serializer.is_valid():
            is_set_to_send = serializer.data.get('status') == 'S'
            if is_set_to_send:
                email.status = 'S'
                email.save()

                return Response(EmailSerializer(email).data)

        return Response({'error': 'set status to "S" to send email'}, status=status.HTTP_400_BAD_REQUEST)
