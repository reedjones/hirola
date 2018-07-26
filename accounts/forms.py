from django import forms
from profiles.models import Profile


class RegistrationForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(label="password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="password again", widget=forms.PasswordInput())

    nick = forms.CharField(max_length=40, min_length=3)

    def clean(self):

        cleaned_data = super(RegistrationForm, self).clean()

        nicks = [profile.nick for profile in Profile.objects.all()]

        n = cleaned_data.get("nick", None)

        if n in nicks:
            raise forms.ValidationError("The nick {0} is already taken".format(n))

        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError("Passwords don't match")


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


class ImageForm(forms.Form):
    image = forms.ImageField(label="upload image file")
