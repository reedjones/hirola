from django.db import models
from topics.models import Tag
from django.conf import settings

USER_MODEL = settings.AUTH_USER_MODEL


# Create your models here.


def get_canvas_thumb_path(instance, filename):
    return "canvas/{0}/thumb/{1}".format(instance.id, filename)


def get_canvas__path(instance, filename):
    return "canvas/{0}/{1}".format(instance.id, filename)


class Media(models.Model):
    media_image = 'i'
    media_code = 'c'
    media_pdf = 'p'
    media_gif = 'g'
    media_video = 'v'
    media_audio = 'a'
    media_svg = 's'

    media_choices = (
        (media_audio, 'Audio'),
        (media_code, 'Code (HTML/CSS/JS)'),
        (media_gif, 'Animated GIF'),
        (media_pdf, 'PDF Document'),
        (media_video, 'Video'),
        (media_image, 'Image'),
        (media_svg, 'Animated SVG'),
    )

    content_type = models.CharField(max_length=2, choices=media_choices)


class Canvas(models.Model):
    thumbnail = models.ImageField(default=None, blank=True, null=True, upload_to=get_canvas_thumb_path)
    title = models.CharField(max_length=50)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, default=None, blank=True)
    created_by = models.ForeignKey(USER_MODEL, related_name='canvases', on_delete=models.PROTECT)
