from django.urls import path
from . import views
from . import my_services
from . import public_services

"""
# path('<str:topic>/', views.service_index, name='service-index-topic'),
# path('<str:topic>/<str:category/', views.service_index, name='service-index-topic'),
# path('<str:topic>/<str:category/<str:tag>/', views.service_index, name='service-index-topic'),
#
# path('', views.service_index, name='service-index'),
# path('<int:target_id>/', views.single, name='service-single'),

"""

urlpatterns = [
    # creation
    path('create/', views.create_service_step1, name='create-service-step-1'),
    path('edit/step-2/<int:target_id>/', views.create_service_step2, name='create-service-step-2'),
    path('edit/step-3/<int:target_id>/', views.create_service_step3, name='create-service-step-3'),
    path('edit/step-4/<int:target_id>/', views.create_service_step4, name='create-service-step-4'),

    # editing
    path('edit/details/<int:target_id>/', views.update_details, name='service-update-details'),
    path('edit/description/<int:target_id>/', views.update_description, name='service-update-description'),
    path('edit/<int:target_id>', views.edit_service, name='service-edit'),
    path('edit/status/request-approval/<int:target_id>/', views.request_approval, name='service-request-approval'),
    path('edit/status/publish/<int:target_id>/', views.publish, name='service-publish'),
    path('edit/status/deactivate/<int:target_id>/', views.deactivate, name='service-deactivate'),

    # my stuff
    path('my-services/', my_services.my_services, name='my-services'),
    path('my-services/<int:target_id>/', my_services.my_single, name='my-single'),
    path('my-services/bookmarked/', my_services.my_bookmarked_services, name='my-bookmarked'),

    # public stuff
    path('', public_services.service_index, name="public-service-index"),
    path('<int:target_id>/', public_services.single, name="public-service"),
    path('<int:target_id>/order/', public_services.order, name="public-service-order"),
    path('<int:target_id>/checkout/', public_services.checkout, name="public-service-checkout"),


    # "API" (these will only be accessed by ajax
    path('is-bookmarked/<int:target_id>/', public_services.check_bookmarked, name='check-bookmark'),

]
