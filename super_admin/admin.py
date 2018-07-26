from django.contrib.admin import AdminSite
from django.http import HttpResponse

from services.models import ServiceInspector
from .views import waiting_offers, service_approve
from django.urls import path



class MyAdminSite(AdminSite):
    site_header = 'Super Admin Site'

    def custom_view(self, request):
        return HttpResponse("Test")

    def get_urls(self):
        from django.conf.urls import url
        urls = super(MyAdminSite, self).get_urls()
        urls += [
            url(r'^custom_view/$', self.admin_view(self.custom_view)),
            path('services-waiting/', self.admin_view(waiting_offers)),
            path('service-approve/<int:target_id>/', self.admin_view(service_approve)),
        ]
        return urls


admin_site = MyAdminSite(name='myadmin')
admin_site.register(ServiceInspector)
