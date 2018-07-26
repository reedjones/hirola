from django import template
from services.models import ServiceOffer

register = template.Library()


@register.filter(name='get_status')
def get_status(value):
    choices = ServiceOffer.status_choices
    for item in choices:
        if item[0] == value:
            return item[1]
    return value


@register.filter(name="get_my_url")
def get_my_url(value):
    return "/services/my-services/{0}/".format(value)