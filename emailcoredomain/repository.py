from abc import ABCMeta, abstractmethod

from coreapp import models


class AbstractRepository(metaclass=ABCMeta):
    @abstractmethod
    def save_email(self, email):
        raise NotImplementedError

    @abstractmethod
    def get_email(self, email_id):
        raise NotImplementedError

    @abstractmethod
    def get_all_emails(self):
        raise NotImplementedError

    @abstractmethod
    def mark_as_sent(self, email_id):
        raise NotImplementedError


class DjangoRepository(AbstractRepository):
    def save_email(self, email):
        models.Email.save_from_core_domain(email)

    def get_email(self, email_id):
        email_model = models.Email.objects.get(pk=email_id)
        return models.Email.to_core_domain(email_model)

    def get_all_emails(self):
        emails_collection = models.Email.objects.all()
        return models.Email.to_core_domain_list(emails_collection)

    def mark_as_sent(self, email_id):
        email = models.Email.objects.get(pk=email_id)
        email.status = 'S'
        email.save()
