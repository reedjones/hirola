from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='messages-inbox'),
    path('thread/<int:target_id>/', views.thread, name='messages-single-thread'),
    path('send/', views.new_message, name="messages-send-message"),
    path('reply/', views.new_reply, name="messages-reply"),
]
