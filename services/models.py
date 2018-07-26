import decimal
from django.db import models
from topics.models import Category, Tag
from django.conf import settings
from profiles.models import Profile
from django.utils.functional import cached_property
from .managers import ServiceOfferManager

USER_MODEL = settings.AUTH_USER_MODEL


def get_image_path(instance, filename):
    return "service_{0}/{1}".format(instance.id, filename)


def get_service_image_path(instance, filename):
    return "service_{0}/main_image/{1}".format(instance.id, filename)


class ServiceOffer(models.Model):
    status_waiting = 'w'
    status_requested = 'r'
    status_approved = 'a'
    status_published = 'p'
    status_inactive = 'i'
    status_denied = 'd'

    status_choices = (
        (status_waiting, 'draft'),
        (status_requested, 'requested'),
        (status_approved, 'approved'),
        (status_published, 'published'),
        (status_inactive, 'inactive'),
        (status_denied, 'denied'),
    )

    time_hour = "h"
    time_day = "d"  # max time = 24 days

    time_choices = (
        (time_hour, "hours"),
        (time_day, "days"),
    )

    name = models.CharField(max_length=200)
    description = models.TextField()
    offered_by = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name='services_offered'
    )
    created_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=50,
        choices=status_choices
    )

    delivery_time = models.IntegerField(null=True, blank=True, default=None)
    delivery_period = models.CharField(choices=time_choices, null=True, blank=True, default=None, max_length=6)

    price = models.DecimalField(max_digits=4, decimal_places=2, default=40.00)

    details = models.TextField(
        null=True, blank=True, default=None
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT
    )

    tags = models.ManyToManyField(
        Tag, default=None, blank=True

    )

    objects = ServiceOfferManager()

    edit_locked = models.BooleanField(default=False)

    main_image = models.ImageField(upload_to=get_service_image_path,
                                   null=True, default=None, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        # return reverse('services.views.single', args=[self.id])
        return reverse('service-single', args=[self.id])

    def get_fee(self):
        fee = decimal.Decimal(0.045)
        val = fee * self.price
        return round(val + decimal.Decimal(0.25), 2)  # fee = 4.5 %ofCharge + 0.25

    def get_total(self):
        return round(self.price + self.get_fee(), 2)

    @cached_property
    def get_profile_url(self):
        print("here")
        p = Profile.objects.get(user=self.offered_by)
        return p.get_absolute_url()

    def step_2_update(self, details, dtime, dperiod, price):
        print("saving")
        self.details = details
        self.delivery_time = dtime
        self.delivery_period = dperiod
        self.price = price
        self.save(update_fields=['details', 'delivery_time', 'delivery_period', 'price'])

    def publish(self):
        self.status = self.status_published
        self.update_status()

    def approve(self):
        self.status = self.status_approved
        self.update_status()

    def deactivate(self):
        self.status = self.status_inactive
        self.update_status()

    def request_approval(self):
        self.status = self.status_requested
        self.update_status()
        self.prevent_editing()

    def deny(self):
        self.status = self.status_denied
        self.update_status()

    def update_status(self):
        self.save(update_fields=['status'])

    def prevent_editing(self):
        self.edit_locked = True
        self.save(update_fields=['edit_locked'])

    def allow_editing(self):
        self.edit_locked = False
        if self.status == self.status_published or self.status == self.status_inactive:
            self.status = self.status_waiting
            self.save(update_fields=['edit_locked', 'status'])
        else:
            self.save(update_fields=['edit_locked'])

    def can_review(self):
        return self.status == self.status_published

    def update_description(self, value):
        self.description = value
        self.save(update_fields=['description'])

    def update_details(self, value):
        self.details = value
        self.save(update_fields=['details'])

    def add_tags(self, tags):
        for tag in tags:
            tag, created = Tag.objects.get_or_create(name=tag)
            self.tags.add(tag)
        self.save()

    def add_admin_note(self, note):
        inspector = ServiceInspector(service=self, note=note)
        inspector.save()

    def get_notes(self):
        return self.admin_notes.all().order_by('created_by')

    def get_my_url(self):
        return "/services/my-services/{0}/".format(self.id)

    def get_public_url(self):
        return "/services/{0}/".format(self.id)


class ServiceReviewManager(models.Manager):
    def from_form(self, data, user, service):
        review = self.create(
            by=user, target=service, text=data['text'])
        return review


class ServiceReview(models.Model):
    by = models.ForeignKey(
        USER_MODEL, on_delete=models.PROTECT
    )
    target = models.ForeignKey(ServiceOffer, related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField()

    objects = ServiceReviewManager()


class ServiceInspectorManager(models.Manager):
    pass


class ServiceInspectorQueryManager(models.QuerySet):
    pass


class ServiceInspector(models.Model):
    """
    manages the status of services,
    used for sending notes to user about why service was not approved
    """
    BadContent = 'B'
    NotEnoughInfo = 'I'
    ForbiddenMedia = 'M'
    Spelling = 'S'
    Duplicate = 'D'
    Other = 'O'
    ForbiddenTopic = 'T'
    reason_choices = (
        (BadContent, 'Content does not meet quality standards'),
        (NotEnoughInfo, 'There are not enough details in your positing'),
        (ForbiddenMedia, 'Change one or more of the media files in your posting'),
        (Spelling, 'Your posting contains too many spelling or grammatical errors'),
        (Duplicate, 'This posting is duplicate content'),
        (ForbiddenTopic, 'This kind of content is not allowed on ZaStovku'),
        (Other, 'See admin notes'),
    )

    objects = ServiceInspectorManager()
    service = models.ForeignKey(ServiceOffer, related_name='admin_notes', on_delete=models.CASCADE)
    note = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    reason = models.CharField(choices=reason_choices, default=Other, max_length=2)

    def __str__(self):
        return "Request  Denied on {0}. Reason: {1}".format(self.created_on, self.reason)

    def get_reason(self):
        for choice in self.reason_choices:
            if choice[0] == self.reason:
                return choice[1]

    def deny_service(self):
        service = self.service
        service.status = service.status_denied
        service.edit_locked = False
        service.save()


class ServiceBookmark(models.Model):
    saved_by = models.ForeignKey(USER_MODEL, related_name="saved_services", on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceOffer, related_name="bookmarks", on_delete=models.CASCADE)
    saved_on = models.DateField(auto_now=True)

    def __str__(self):
        return "Bookmark: " + self.service.name


class ServiceOrderManager(models.Manager):
    pass


class ServiceOrder(models.Model):
    status_awaiting_delivery = 'ad'
    status_delivered = 'd'
    status_timeout = 'to'
    status_awaiting_payment = 'ap'

    status_options = (
        (status_awaiting_delivery, "Awaiting Delivery"),
        (status_delivered, "Delivered"),
        (status_timeout, "Not Delivered In Time"),
        (status_awaiting_payment, "Awaiting Payment")
    )

    status = models.CharField(choices=status_options, max_length=3, default=status_awaiting_payment)

    ordered_by = models.ForeignKey(USER_MODEL, related_name="outgoing_orders", on_delete=models.PROTECT)
    service = models.ForeignKey(ServiceOffer, related_name="order_requests", on_delete=models.PROTECT)
    ordered_at = models.DateTimeField(auto_now=True)
    objects = ServiceOrderManager()


class ServiceDelivery(models.Model):
    service = models.ForeignKey(ServiceOffer, related_name="deliveries", on_delete=models.PROTECT)
    order = models.ForeignKey(ServiceOrder, on_delete=models.PROTECT)


class Gallery(models.Model):
    service = models.OneToOneField(ServiceOffer, related_name="gallery", on_delete=models.CASCADE)


class Image(models.Model):
    img = models.ImageField(upload_to=get_image_path)
    gallery = models.ForeignKey(Gallery, related_name="images", on_delete=models.CASCADE)
