from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotAllowed

from .models import ServiceOffer


def user_owns(function):
    def wrap(request, *args, **kwargs):
        service = get_object_or_404(ServiceOffer, pk=kwargs['target_id'])
        if service.offered_by == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def not_user_owns(function):
    def wrap(request, *args, **kwargs):
        service = get_object_or_404(ServiceOffer, pk=kwargs['target_id'])
        if service.offered_by != request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def remove_punctuation(value=""):
    s = "! @ # $ % ^ & * ( ) ' \" . , / \ > < ; : { } [ ] | \ ~ `"
    puntuation = s.split(' ')
    for i in puntuation:
        value.replace(i, '')
    value.replace("/", "")
    value.replace("\\", "")
    return value


def remove_script(value=""):
    value = value.replace("<script>", "").replace("<form>", "").replace("var", "").replace("(){", "").replace("{", "")
    return value



