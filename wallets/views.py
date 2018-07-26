from django.shortcuts import render
from bitpay.client import Client
from . import forms
from django.http import HttpResponse, JsonResponse
from .BitPayUtils import client
from .models import Wallet


# Create your views here.


def my_wallet(request):
    pass


def add_funds(request):
    form = forms.ChargeForm(request.POST)
    if form.is_valid():
        wallet = Wallet.objects.get(user=request.user)
        wallet.deposit(form.cleaned_data['price'])
        return JsonResponse({
            'balance': wallet.current_balance
        })

    wallet = Wallet.objects.get(user=request.user)
    return render(request, "wallets/add_funds.html", {
        'wallet': wallet

    })


def create_invoice(request):
    print(request.POST)
    form = forms.ChargeForm(request.POST)
    if form.is_valid():
        print("is valid")
        data = form.cleaned_data
        invoice = client.grab_invoice(data['price'])

        print(invoice)
        print(invoice['id'])

        return JsonResponse({"id": invoice['id']})
    else:
        print("not valid")
