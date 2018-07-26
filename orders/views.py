from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from wallets.models import Invoice
from wallets.BitPayUtils import client
from services.models import ServiceOrder


# Create your views here.
@login_required()
def outgoing_order(request, order_id):
    order = ServiceOrder.objects.get(id=order_id)

    return render(request, 'orders/order_status.html', {
        'order': order
    })


@login_required()
def incoming_order_index(request):
    orders = ServiceOrder.objects.filter(service__offered_by=request.user)

    return render(request, 'orders/incoming-index.html', {
        'orders': orders
    })
