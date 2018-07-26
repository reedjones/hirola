from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logout_, name='logout'),
    path('register/', views.register, name="register"),
    path('login/', views.login_, name="login"),
    path('photo/', views.add_photo, name="add-photo"),
    path('forgot-password/', views.forgot_password, name="forgot-password"),
]