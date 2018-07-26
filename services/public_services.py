from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import ServiceOffer, ServiceBookmark
from profiles.models import Profile
from .utils import not_user_owns
from .forms import CharForm, IntForm, CheckoutForm
from django.contrib.auth.decorators import login_required
from wallets.BitPayUtils import client
from wallets.models import Invoice, Wallet, EscrowWallet
from .models import ServiceOrder
from django.urls import reverse


def service_index(request, topic=None, category=None, tag=None):
    if topic and category and tag:
        service_list = ServiceOffer.objects.active().posted_under(topic, category).tagged(tag)
    elif topic and category:
        service_list = ServiceOffer.objects.active().posted_under(topic, category)

    elif topic:
        service_list = ServiceOffer.objects.active().posted_under(topic)

    else:
        service_list = ServiceOffer.objects.active()

    service_list.order_by('-created_at')

    paginator = Paginator(service_list, 12)
    page = request.GET.get('page')
    services = paginator.get_page(page)

    return render(request, 'services/index.html', {
        'services': services

    })


def single(request, target_id):
    service = ServiceOffer.objects.get(id=target_id)
    if request.method == 'POST':
        # When checking values like this always remember to include the csrf!
        f = IntForm(request.POST)  # use request.POST not request.POST['specific_value'], to insure csrf present
        if f.is_valid() and request.user.is_authenticated:
            # ^ check authenticated just in case
            data = f.cleaned_data
            if not data['value'] == service.id:
                # this would mean someone attempted to post from another page
                print("{0} is not equal to {1}".format(data['value'], service.id))
            if request.user == service.offered_by:
                return JsonResponse({
                    'saved': 0,
                    'message': 'you cant save your own offer'
                })

            b, created = ServiceBookmark.objects.get_or_create(saved_by=request.user, service=service)
            b.save()
            return JsonResponse({
                'saved': data['value'],
                'message': 'saved'
            })

    profile = Profile.objects.get(user=service.offered_by)
    return render(request, 'services/public-single.html', {
        'service': service,
        'profile': profile
    })


@login_required()
@not_user_owns
def order(request, target_id):
    service = ServiceOffer.objects.get(id=target_id)

    return render(request, 'services/order.html', {
        'service': service
    })


@login_required()
@not_user_owns
def checkout(request, target_id):
    service = ServiceOffer.objects.get(id=target_id)
    wallet = Wallet.objects.get(user=request.user)

    form = CheckoutForm(request.POST)
    if form.is_valid():
        print("valid")
        data = form.cleaned_data
        ordered = ServiceOrder(service=service, ordered_by=request.user, status=ServiceOrder.status_awaiting_delivery)
        ordered.save()
        print(data['platform'])

        if data['platform'] == 'bitpay':
            pass

        elif data['platform'] == 'wallet':
            to_account = Wallet.objects.get(user=service.offered_by)
            escrow = EscrowWallet(from_account=wallet, target_account=to_account)
            escrow.hold_funds(service.get_total())

        return HttpResponseRedirect(reverse('outgoing-order-status', args=[ordered.id]))
    else:
        print(form.errors)

    return render(request, 'services/checkout.html', {
        'service': service,
        'wallet': wallet

    })


def check_bookmarked(request, target_id):
    if not request.user.is_authenticated:
        return JsonResponse({'msg': 0})
    s = ServiceOffer.objects.get(id=target_id)
    try:
        b = ServiceBookmark.objects.get(saved_by=request.user, service=s)
        return JsonResponse({'msg': 1})
    except ServiceBookmark.DoesNotExist:
        return JsonResponse({'msg': 0})
