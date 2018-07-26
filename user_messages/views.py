from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from .models import Thread, Message, UserThread
from . import forms
from django.core.paginator import Paginator
from django.template import Context
from django.template import Template
from django.template.loader import render_to_string
from django.conf import settings

USER_MODEL = settings.AUTH_USER_MODEL


@login_required()
def inbox(request):
    threads = Thread.ordered(Thread.inbox(request.user))

    return render(request, 'user_messages/inbox.html', {
        'threads': threads
    })


def thread(request, target_id):
    thread_ = Thread.objects.get(id=target_id)

    return render(request, 'user_messages/thread.html', {
        'thread': thread_
    })


def get_messages(request, target_id):
    """
    This will be used to actually fetch the messages from a thread, lazy loading as the user scrolls up
    :param request:
    :param target_id:
    :return:
    """
    target_thread = Thread.objects.get(id=target_id)
    messages = target_thread.messages.ordered()
    paginator = Paginator(messages, 6)
    page = request.GET.get('page', None)
    if page:
        messages = paginator.get_page(page)
        data = {'messages': []}
        for message in messages:
            html = render_to_string('user_messages/message.html', {'message': message, 'user': request.user})
            data['messages'].append(html)
            return JsonResponse(data)


@login_required()
def new_message(request):
    form = forms.NewMessageForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        user = USER_MODEL.objects.get(id=data['to_user_id'])
        msg = Message.new_message(from_user=request.user, content=data['content'],
                                  to_users=[user])  # <- we need the to user


@login_required()
def new_reply(request, target_id):
    target_thread = Thread.objects.get(id=target_id)
    form = forms.MessageReplyForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        msg = Message.new_reply(thread=target_thread, user=request.user, content=data['content'])
