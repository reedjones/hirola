from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from .models import ServiceOffer, ServiceBookmark
from django.contrib.auth.decorators import login_required
from .utils import user_owns, not_user_owns


@login_required()
def my_services(request):
    services = ServiceOffer.objects \
        .made_by(request.user) \
        .order_by('-created_at') \
        .values_list('name', 'created_at', 'status', 'pk')

    print(services)
    return render(request, 'services/my-index.html', {
        'services': services
    })


@login_required()
def my_bookmarked_services(request):
    services = ServiceOffer.objects \
        .filter(bookmarks__saved_by=request.user) \
        .order_by('-created_at') \
        .values_list('name', 'created_at', 'status', 'pk')

    print(services)
    return render(request, 'services/my-index.html', {
        'services': services
    })


@login_required()
@user_owns
def my_single(request, target_id):
    service = get_object_or_404(ServiceOffer, id=target_id)

    return render(request, 'services/my-single.html', {
        'service': service
    })
