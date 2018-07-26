from django import forms
from .models import Message
from django.contrib.auth import get_user_model


class UserModelChoiceField(forms.ModelChoiceField):
    pass


class NewMessageForm(forms.ModelForm):
    subject = forms.CharField()
    to_user = forms.IntegerField(widget=forms.HiddenInput)
    content = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")

        super(NewMessageForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        data = self.cleaned_data
        to_user = get_user_model().objects.get(id=data['to_user'])
        return Message.new_message(
            self.user, [to_user], data["subject"], data["content"]
        )

    class Meta:
        model = Message
        fields = ["to_user", "subject", "content"]


class MessageReplyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.thread = kwargs.pop("thread")
        self.user = kwargs.pop("user")
        super(MessageReplyForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        return Message.new_reply(
            self.thread, self.user, self.cleaned_data["content"]
        )

    class Meta:
        model = Message
        fields = ["content"]
