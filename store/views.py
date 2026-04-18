from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, Review
from .forms import ConsentForm, BookingRequestForm, ReviewSubmissionForm
from main.email import send_form_email


# Map service slugs to dedicated templates with literal copy
SLUG_TEMPLATE_MAP = {
    "kundalini-energy-transmission": "store/services/kundalini_detail.html",
    "mediumship-spirit-rescue": "store/services/spirit_rescue_detail.html",
    "clairvoyant-guidance": "store/services/clairvoyant_detail.html",
}

CONSENT_TEMPLATES = {
    "kundalini": "store/consent/kundalini_consent.html",
    "spirit_rescue": "store/consent/spirit_rescue_consent.html",
    "intuitive": "store/consent/intuitive_consent.html",
}


def service_list(request):
    context = {
        "services": Service.objects.filter(is_active=True),
    }
    return render(request, "store/service_list.html", context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    template = SLUG_TEMPLATE_MAP.get(slug, "store/service_detail.html")
    context = {
        "service": service,
        "reviews": service.reviews.filter(is_approved=True),
    }
    return render(request, template, context)


def review_list(request):
    context = {
        "healing_reviews": Review.objects.filter(is_approved=True, category="healing"),
        "intuitive_reviews": Review.objects.filter(is_approved=True, category="intuitive"),
    }
    return render(request, "store/review_list.html", context)


def consent_form(request, form_type: str):
    template = CONSENT_TEMPLATES.get(form_type)
    if not template:
        raise Http404("Consent form not found.")

    if request.method == "POST":
        form = ConsentForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.form_type = form_type
            submission.ip_address = request.META.get("REMOTE_ADDR")
            submission.save()
            send_form_email(
                subject=f"Consent Form: {submission.get_form_type_display()} — {submission.client_name}",
                template_name="store/emails/consent_submission.txt",
                context={"submission": submission},
            )
            messages.success(request, "Your consent form has been submitted successfully.")
            return redirect("store:consent_success")
    else:
        form = ConsentForm()

    return render(request, template, {"form": form, "form_type": form_type})


def consent_success(request):
    return render(request, "store/consent/consent_success.html")


def booking_request(request):
    if request.method == "POST":
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            booking = form.save()
            send_form_email(
                subject=f"Booking Request: {booking.name} — {booking.service_type or 'General'}",
                template_name="store/emails/booking_request.txt",
                context={"booking": booking},
                reply_to=booking.email,
            )
            messages.success(
                request,
                "Your booking request has been submitted! Krystene will be in touch soon.",
            )
            return redirect("store:booking_success")
    else:
        form = BookingRequestForm()
    return render(request, "store/booking_request.html", {"form": form})


def booking_success(request):
    return render(request, "store/booking_success.html")


def submit_review(request):
    if request.method == "POST":
        form = ReviewSubmissionForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.is_approved = False
            review.is_featured = False
            review.save()
            messages.success(
                request,
                "Thank you for your review! It will appear on the site after approval.",
            )
            return redirect("store:review_list")
    else:
        form = ReviewSubmissionForm()
    return render(request, "store/submit_review.html", {"form": form})
