from abc import ABCMeta, abstractmethod


class Email:
    MANDATORY_FIELDS_LIST = ['id', 'status', 'sender', 'recipients', 'subject', 'message_body']

    def __init__(self, **kwargs):
        [setattr(self, field_name, None) for field_name in self.MANDATORY_FIELDS_LIST]
        self.__dict__.update(**kwargs)

    def validate(self):
        return all(hasattr(self, field_name) for field_name in self.MANDATORY_FIELDS_LIST)

    def __str__(self):
        return f'Email values id: {self.id}, subject: {self.subject}, sender: {self.sender}'


class IEmailDispatcher(metaclass=ABCMeta):
    @abstractmethod
    def send_email(self, email):
        raise NotImplemented


class EmailDispatcher(IEmailDispatcher):
    def __init__(self, email_service):
        self.email_service = email_service

    def send_email(self, email):
        self.email_service.send(email)


class FakeEmailService:
    def send(self, email):
        print(email, ' sent')

        return True
