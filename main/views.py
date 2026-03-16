from django.shortcuts import render
from store.models import Service, Review


def index(request):
    context = {
        "services": Service.objects.filter(is_active=True)[:6],
        "reviews": Review.objects.filter(is_approved=True, is_featured=True)[:8],
    }
    return render(request, "main/index.html", context)


def about(request):
    return render(request, "main/about.html")


def contact(request):
    return render(request, "main/contact.html")
