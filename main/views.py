from django.contrib import messages
from django.shortcuts import render, redirect
from store.models import Service, Review
from .forms import ContactForm, SubscriberForm
from .models import Subscriber
from .email import send_form_email


def index(request):
    context = {
        "services": Service.objects.filter(is_active=True)[:6],
        "reviews": Review.objects.filter(is_approved=True, is_featured=True)[:8],
    }
    return render(request, "main/index.html", context)


def about(request):
    return render(request, "main/about.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            submission = form.save()
            send_form_email(
                subject=f"New Contact: {submission.name}",
                template_name="main/emails/contact_submission.txt",
                context={"submission": submission},
                reply_to=submission.email,
            )
            messages.success(request, "Your message has been sent. Krystene will be in touch soon!")
            return redirect("main:contact")
    else:
        form = ContactForm()
    return render(request, "main/contact.html", {"form": form})


def subscribe(request):
    if request.method == "POST":
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            subscriber, created = Subscriber.objects.get_or_create(
                email=email,
                defaults={"name": form.cleaned_data.get("name", "")},
            )
            if not created and not subscriber.is_active:
                subscriber.is_active = True
                subscriber.save()
            messages.success(request, "You've been subscribed to the mailing list!")
        else:
            messages.error(request, "Please provide a valid email address.")
        return redirect(request.POST.get("next", "main:index"))
    return redirect("main:index")


def unsubscribe(request, token):
    try:
        subscriber = Subscriber.objects.get(unsubscribe_token=token)
        subscriber.is_active = False
        subscriber.save()
        return render(request, "main/unsubscribed.html")
    except Subscriber.DoesNotExist:
        return render(request, "main/unsubscribed.html", {"error": True})


def books_media(request):
    return render(request, "main/books_media.html")


def qr_code(request):
    return render(request, "main/qr_code.html")
