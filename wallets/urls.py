from django.urls import path, include
from . import views

urlpatterns = [
    path('deposit/', views.add_funds, name='wallet-add-funds'),
    path('get-bitpay-invoice/', views.create_invoice, name='get-bitpay-invoice'),
]
