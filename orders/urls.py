from django.urls import path, include
from . import views

urlpatterns = [
    path('outgoing/<int:order_id>/status/', views.outgoing_order, name="outgoing-order-status"),
    path('incoming/', views.incoming_order_index, name="incoming-order-index"),
]
