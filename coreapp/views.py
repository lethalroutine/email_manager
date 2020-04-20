from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from coreapp.serializers import EmailRestApiSerializer, EmailStatusSerializer
from emailcoredomain.repository import DjangoRepository
from emailcoredomain.apps import FakeEmailService, EmailDispatcher


class EmailRestApiView(APIView):

    def get(self, request, format=None):
        repo = DjangoRepository()
        emails = repo.get_all_emails()
        serializer = EmailRestApiSerializer(emails, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EmailRestApiSerializer(data=request.data)
        if serializer.is_valid():
            email_id = serializer.save()
            response_data = dict(serializer.data)
            response_data['id'] = email_id

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailDetailView(APIView):
    def get(self, request, pk, format=None):
        repo = DjangoRepository()
        email = repo.get_email(pk)
        serializer = EmailRestApiSerializer(email)

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        repo = DjangoRepository()
        serializer = EmailStatusSerializer(data=request.data)
        if serializer.is_valid():
            is_set_to_send = serializer.data.get('status') == 'S'
            if is_set_to_send:
                email = repo.get_email(pk)
                email_service = FakeEmailService()
                email_dispatcher = EmailDispatcher(email_service=email_service)
                email_dispatcher.send_email(email)

                repo.mark_as_sent(pk)

                return Response({'message': f'email with id: {pk} successfully sent'})

        return Response({'error': 'set status to "S" to send email'}, status=status.HTTP_400_BAD_REQUEST)
