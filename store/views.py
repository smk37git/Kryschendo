from django.shortcuts import render, get_object_or_404
from .models import Service, Review


def service_list(request):
    context = {
        "services": Service.objects.filter(is_active=True),
    }
    return render(request, "store/service_list.html", context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    context = {
        "service": service,
        "reviews": service.reviews.filter(is_approved=True),
    }
    return render(request, "store/service_detail.html", context)


def review_list(request):
    context = {
        "healing_reviews": Review.objects.filter(is_approved=True, category="healing"),
        "intuitive_reviews": Review.objects.filter(is_approved=True, category="intuitive"),
    }
    return render(request, "store/review_list.html", context)
