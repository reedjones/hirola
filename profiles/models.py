from django.db import models
from django.conf import settings


# Create your models here.


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.name, filename)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                primary_key=True,
                                on_delete=models.CASCADE)  # name and email

    photo = models.ImageField(
        'Profile picture',
        upload_to=user_directory_path,
        null=True,
        blank=True,
        default=None
    )

    nick = models.SlugField(
        unique=True,
        allow_unicode=True,
        max_length=60,

    )

    description = models.TextField(
        blank=True,
        null=True,
        default=None
    )

    joined_on = models.DateField(auto_now=True)
    last_login = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nick

    def get_photo(self):
        return self.photo.url

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('public-profile', args=[self.id])
