from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.service_list, name="service_list"),
    path("reviews/", views.review_list, name="review_list"),
    path("reviews/submit/", views.submit_review, name="submit_review"),
    path("book/", views.booking_request, name="booking_request"),
    path("book/success/", views.booking_success, name="booking_success"),
    path("consent/success/", views.consent_success, name="consent_success"),
    path("consent/<str:form_type>/", views.consent_form, name="consent_form"),
    path("<slug:slug>/", views.service_detail, name="service_detail"),
]
