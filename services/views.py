from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ServiceOffer, ServiceReview, ServiceBookmark, ServiceOrder, Image, Gallery
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.shortcuts import render, get_object_or_404
# Create your views here.
from .forms import ServiceReviewForm, ServiceForm1, ServiceForm2, TextForm, ServiceFull, OrderForm, CharForm, \
    ServiceForm3
from .utils import user_owns, not_user_owns
from django.contrib import messages
from django.urls import reverse
from topics.models import Category
import json


@login_required()
def create_service_step1(request):
    form = ServiceForm1(request.POST)
    if form.is_valid():
        service = ServiceOffer.objects.from_form(
            form.cleaned_data,
            request.user)

        return HttpResponseRedirect(reverse('create-service-step-2', args=[service.id]))

    topics = Category.objects.top_level()
    topic_tree = []
    for t in topics:
        topic_tree.append({
            'name': t.name,
            'id': t.pk,
            'children': [{'name': n.name, 'id': n.pk} for n in Category.objects.children_of(t)]
        })

    return render(request,
                  'services/create-step-1.html',
                  {'form': form, 'topics': json.dumps(topic_tree), 'ptopics': topic_tree})


@login_required()
@user_owns
def create_service_step2(request, target_id):
    service = ServiceOffer.objects.get(id=target_id)
    form = ServiceForm2(request.POST)
    # print(form.groups)
    if form.is_valid():
        data = form.cleaned_data

        details = data['details']
        delivery_time = data['delivery_time']
        delivery_period = data['delivery_period']
        price = data['price']

        service.step_2_update(details, delivery_time, delivery_period, price)

        return HttpResponseRedirect(reverse('create-service-step-3', args=[service.id]))

    euro = {
        'sort': 'text',
        'value': '€',
        "give_id": None
    }

    amount = {
        "sort": "text",
        "give_id": "id_current_price",
        "value": "5.00"
    }

    for_price = {'id': 'id_price', 'items': [euro, amount]}  # field.auto_id
    # print("creating")
    groups = [
        for_price
    ]

    return render(request, 'services/create-step-2.html', {
        'form': form,
        'service': service,
        'target_id': target_id,
        'form_group': ['id_price'],
        'groups': groups
    })


@login_required()
@user_owns
def create_service_step3(request, target_id):
    service = ServiceOffer.objects.get(id=target_id)
    form = ServiceForm3(request.POST, request.FILES)
    if request.method == 'POST':
        print("posted")
    if form.is_valid():
        print("valid")
        gallery = Gallery(service=service)
        gallery.save()

        gallery_files = request.FILES.getlist('gallery')
        for f in gallery_files:
            i = Image(img=f, gallery=gallery)
            i.save()

        service.main_image = request.FILES['main_image']
        service.save()
        return HttpResponseRedirect(reverse('create-service-step-4', args=[service.id]))
    else:
        print(form.errors)

    return render(request, 'services/create-step-3.html', {
        'service': service,
        'form': form
    })


@login_required()
@user_owns
def create_service_step4(request, target_id):
    service = ServiceOffer.objects.get(id=target_id)

    if request.method == 'POST':
        # here will confirm something but for now
        service.request_approval()
        return HttpResponse("posted")

    return render(request, 'services/create-step-4.html', {
        'service': service
    })


@login_required()
@user_owns
def update_description(request, target_id):
    service = ServiceOffer.objects.get(id=target_id)
    form = TextForm(request.POST)
    if form.is_valid():
        service.update_description(form.cleaned_data)
        messages.success(request, 'Entry was successfully edited!')


@login_required()
@user_owns
def update_details(request, target_id):
    service = ServiceOffer.objects.get(id=target_id)
    form = TextForm(request.POST)
    if form.is_valid():
        service.update_details(form.cleaned_data)
        messages.success(request, 'Entry was successfully edited!')


@login_required()
@user_owns
def update_service(request, target_id):
    service = ServiceOffer.objects.get(id=target_id)
    form = ServiceFull(request.POST)
    if form.is_valid():
        pass


@login_required()
@user_owns
def edit_service(request, target_id):
    service = ServiceOffer.objects.get(
        id=target_id
    )
    form = ServiceFull(request.POST)
    if form.is_valid():
        pass

    return render(request,
                  'services/edit.html',
                  {'service': service, 'form': form})


@require_POST
@login_required()
@user_owns
def request_approval(request, target_id):
    service = ServiceOffer.objects.get(id=target_id)
    service.request_approval()
    messages.success(request, 'Request Received')
    return HttpResponseRedirect(reverse('service-edit', args=[target_id]))


@login_required()
@user_owns
def publish(request, target_id):
    service = ServiceOffer.objects.get(id=target_id)
    if service.status == service.status_requested:
        # they already request and it has not been approved yet
        messages.warning(request, 'Your service is already awaiting approval.')
    if service.status == service.status_denied:
        # they already request and it was denied
        notes = service.admin_notes.all()
        messages.error(request, 'You need to make changes, or re-submit your service for approval!')
    if service.status == service.status_approved:
        # they requested and it was approved and ready to publish
        service.publish()
        messages.success(request, 'Service Published!')

        return HttpResponseRedirect(reverse('service-single'), args=[target_id])

    return HttpResponseRedirect(reverse('service-edit', args=[target_id]))


@require_POST
@login_required()
@user_owns
def deactivate(request, target_id):
    service = ServiceOffer.objects.get(id=target_id)
    if service.status == service.status_published:
        service.deactivate()
        # messages.info(request, 'Service has been deactivated')

    else:
        # you cant deactivate a service that isn't published
        pass
    return HttpResponseRedirect(reverse('service-edit', args=[target_id]))


@login_required()
@not_user_owns
def create_review(request, target_id):
    service = get_object_or_404(ServiceOffer, id=target_id)
    form = ServiceReviewForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        review = ServiceReview.objects.from_form(data, request.user, service)

    return render(request,
                  'services/review.html',
                  {'service': service, 'form': form})





@login_required()
def my_services(request, topic=None, category=None, tag=None):
    """
    Services created by the current user,
    :param request:
    :param topic:
    :param category:
    :param tag:
    :return:
    """
    if topic:
        if category:
            if tag:
                service_list = ServiceOffer.objects.made_by(request.user).posted_under(topic, category).tagged(tag)
            else:
                service_list = ServiceOffer.objects.made_by(request.user).posted_under(topic, category)
        else:
            service_list = ServiceOffer.objects.made_by(request.user).posted_under(topic)
    else:
        service_list = ServiceOffer.objects.made_by(request.user)

    service_list.order_by('created_at')
    paginator = Paginator(service_list, 20)
    page = request.GET.get('page')
    services = paginator.get_page(page)

    return render(request, 'services/my-index.html', {
        'services': services
    })


@login_required()
@user_owns
def my_single(request, target_id):
    service = get_object_or_404(ServiceOffer, id=target_id)

    return render(request, 'services/my-single.html', {'service': service})


def single(request, target_id):
    """
    view a single offer,
    options: save for later, order
    :param request:
    :param target_id:
    :return:
    """
    logged_in = request.user.is_authenticated
    save_form = OrderForm(request.POST)
    order_form = OrderForm(request.POST)

    if save_form.is_valid() and "bookmark" in request.POST:
        if not logged_in:
            return HttpResponseRedirect("/accounts/login/")  # here will add ?next={this_offer_url}&action=bookmark
        data = save_form.cleaned_data
        target = ServiceOffer.objects.get(id=data['target_id'])
        bookmark = ServiceBookmark(saved_by=request.user,
                                   service=target)
        bookmark.save()

    if order_form.is_valid() and "order" in request.POST:
        if not logged_in:
            return HttpResponseRedirect("/accounts/login/")
        data = order_form.cleaned_data
        target = ServiceOffer.objects.get(id=data['target_id'])
        order = ServiceOrder(ordered_by=request.user, service=target)
        order.save()
        # here will direct to order step 1

    service = get_object_or_404(ServiceOffer, id=target_id)

    return render(request, 'services/public-single.html', {'service': service})
