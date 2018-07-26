from django.db import models

class ServiceOfferManager(models.Manager):
    """
    Manager for ServiceOfferObjects,

    """

    def get_queryset(self):
        return ServiceQuerySet(self.model, using=self._db)

    def from_form(self, data, user):
        from topics.models import Category
        c = Category.objects.get(pk=data['category'])

        service = self.create(name=data['name'],
                              description=data['description'],
                              offered_by=user,
                              category=c,
                              status=self.model.status_waiting)

        print("[Message: Service {0} Created, Category: {1}]".format(service, c))
        return service

    def active(self):
        return self.get_queryset().active()

    def posted_under(self, topic, category=None):
        return self.get_queryset().posted_under(topic, category)

    def tagged(self, value):
        return self.get_queryset().tagged(value)

    def made_by(self, user):
        return self.get_queryset().made_by(user)

    def awaiting_approval(self):
        return self.get_queryset().awaiting_approval()


class ServiceQuerySet(models.QuerySet):

    def active(self):
        return self.filter(status=self.model.status_published)

    def drafts(self):
        return self.filter(status=self.model.status_waiting)

    def inactive(self):
        return self.filter(status=self.model.status_inactive)

    def approved(self):
        return self.filter(status=self.model.status_approved)

    def awaiting_approval(self):
        return self.filter(status=self.model.status_requested)

    def tagged(self, value):
        return self.filter(tags__name=value)

    def posted_under(self, topic, category=None):
        if category:
            return self.filter(category__name=topic).filter(category__parent__name=category)
        return self.filter(category__name=topic)

    def made_by(self, user):
        return self.filter(offered_by=user)
