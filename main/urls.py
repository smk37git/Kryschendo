from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("unsubscribe/<uuid:token>/", views.unsubscribe, name="unsubscribe"),
    path("books-media/", views.books_media, name="books_media"),
    path("qr/", views.qr_code, name="qr_code"),
]
