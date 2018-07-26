from django import template

from user_messages.models import Thread

register = template.Library()


@register.filter
def unread(thread, user):
    """
    Check whether there are any unread messages for a particular thread for a user.
    """
    return bool(thread.userthread_set.filter(user=user, unread=True))


@register.filter
def unread_thread_count(user):
    """
    Return the number of Threads with unread messages for this user, useful for highlighting on an account bar for example.
    """
    return Thread.unread(user).count()


@register.filter
def get_thumbnail_for(thread, user):
    other_user = thread.users.exclude(id=user.id).first()

    return other_user.profile.photo.url


@register.filter
def get_other_user_nick(thread, user):
    return thread.users.exclude(id=user.id).first().profile.nick
