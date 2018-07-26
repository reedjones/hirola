from django.db import models
from django.conf import settings
from topics.models import Category
import os
import uuid
from services.models import ServiceOffer
from django.utils import timezone

USER_MODEL = settings.AUTH_USER_MODEL


def uuid_filename(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("document", filename)


class ServiceRequest(models.Model):
    requested_by = models.ForeignKey(
        USER_MODEL, on_delete=models.PROTECT,
        related_name='service_requests'
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    posted_at = models.DateTimeField(
        blank=True, default=None, null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name


class ServiceFulfillment(models.Model):
    service_request = models.ForeignKey(
        ServiceRequest, related_name="fulfillment_offers",
        on_delete=models.PROTECT
    )

    service_offer = models.ForeignKey(
        ServiceOffer, related_name="completions",
        on_delete=models.PROTECT
    )

    offer_completion = "oc"
    request_completion = "rc"
    type_choices = (
        ("offer completion", offer_completion),
        ("request completion", request_completion),
    )
    kind = models.CharField(choices=type_choices, max_length=3)


class SupportingDocument(models.Model):
    submission = models.ForeignKey(ServiceFulfillment, related_name="supporting_documents",
                                   verbose_name="Submission",
                                   on_delete=models.CASCADE)

    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Uploaded by", on_delete=models.CASCADE,
                                    related_name='uploaded_documents')

    created_at = models.DateTimeField(auto_now=True, verbose_name="Created at")
    document = models.FileField(upload_to=uuid_filename, verbose_name="Document")
    description = models.CharField(max_length=140, verbose_name="Description")


class SubmissionMessage(models.Model):
    submission = models.ForeignKey(ServiceFulfillment, related_name="messages", verbose_name="Submission",
                                   on_delete=models.CASCADE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="User", on_delete=models.CASCADE)
    message = models.TextField(verbose_name="Message")

    submitted_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Submitted at")

    class Meta:
        ordering = ["submitted_at"]
        verbose_name = "submission message"
        verbose_name_plural = "submission messages"


class SubmissionResult(models.Model):
    status_undecided = "u"
    status_rejected = "r"
    status_accepted = "a"
    status_choices = (
        ("Undecided", status_undecided),
        ("Rejected", status_rejected),
        ("Accepted", status_accepted),
    )
    submission = models.OneToOneField(ServiceFulfillment, related_name="result", verbose_name="Submission",
                                      on_delete=models.CASCADE)

    status = models.CharField(max_length=2, choices=status_choices, default=status_undecided)
