from django.shortcuts import render
from services.models import ServiceInspector, ServiceOffer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import InspectorForm
from django.http import HttpResponse


# Create your views here.


def waiting_offers(request):
    service_list = ServiceOffer.objects.awaiting_approval().order_by('created_at')

    paginator = Paginator(service_list, 12)
    page = request.GET.get('page')
    services = paginator.get_page(page)

    return render(request, 'super_admin/services-awaiting-approval.html',
                  {'services': services})


def service_approve(request, target_id):
    service = ServiceOffer.objects.get(id=target_id)
    print(request.POST)
    if 'approve' in request.POST:
        service.publish()
        print(service.status)
    elif 'deny' in request.POST:
        deny_form = InspectorForm(request.POST)
        if deny_form.is_valid():
            data = deny_form.cleaned_data
            s = ServiceInspector(service=service, note=data['note'], reason=data['reason'])
            s.save()
            return HttpResponse("created")

    deny_form = InspectorForm()
    return render(request, 'super_admin/service-approve.html', {
        'service': service,
        'deny_form': deny_form
    })
