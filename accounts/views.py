from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from . import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import is_safe_url
from wallets.models import Wallet

User = get_user_model()


# Create your views here.

def register(request):
    """
    kinda trick because you don't want to call is_valid() on this one
    :param request:
    :return:
    """

    if request.POST:
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            print("valid")
            data = form.cleaned_data
            if User.objects.filter(email=data['email']).count > 1:
                print("already used")
            user = User.objects.create_user(
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            profile = Profile(
                user=user,
                nick=data['nick'])
            profile.save()
            authenticated = authenticate(email=data['email'],
                                         password=data['password1'])

            
            login(request, authenticated)
            wallet = Wallet(user=request.user)
            wallet.save()
            return HttpResponseRedirect(reverse('add-photo'))

    form = forms.RegistrationForm()
    return render(request, 'accounts/register.html', {
        'form': form
    })


def login_(request):
    """
        the underscore is to not conflict with the django login function
        :param request:
        :return:
    """
    if request.user.is_authenticated:
        return HttpResponse("you're already logged in")

    form = forms.LoginForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            # messages.ERROR("You Don't have an account dude")
            return HttpResponseRedirect('/?login-does-not-exist')

        authenticated = authenticate(email=email,
                                     password=form.cleaned_data['password'])

        if authenticated and user.is_active:
            login(request, authenticated)
            redirect_to = request.GET.get(next, '')
            if is_safe_url(redirect_to):
                HttpResponseRedirect(redirect_to)
        else:
            return HttpResponse("account inactive")

    return render(request, 'accounts/login.html', {
        'form': form
    })


@login_required()
def add_photo(request):
    profile = Profile.objects.get(user=request.user)
    form = forms.ImageForm(request.POST, request.FILES)
    if form.is_valid():
        profile.photo = request.FILES['image']
        profile.save()
        return HttpResponseRedirect('/')
    else:
        print(form.errors)

    return render(request, 'accounts/add-photo.html', {'form': form,
                                                       'profile': profile})


def logout_(request):
    """
    the underscore is to not conflict with the django logout function
    :param request:
    :return:
    """
    if request.user.is_anonymous:
        return HttpResponseRedirect('/')
    logout(request)
    return HttpResponseRedirect('/')


def forgot_password(request):
    pass
