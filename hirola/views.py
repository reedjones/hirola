from django.shortcuts import render
from services.models import ServiceOffer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from topics.models import Category


def home(request):
    offers = ServiceOffer.objects.active().order_by('-created_at')[:10]
    topics = Category.objects.top_level().order_by('name')
    print(topics)
    topic_tree = []
    for t in topics:
        topic_tree.append({
            'name': t.name,
            'id': t.pk,
            'children': [{'name': n.name, 'id': n.pk} for n in Category.objects.children_of(t)]
        })
    return render(request, 'home-copy.html', {
        'offers': offers,
        'topics':topic_tree
    })
