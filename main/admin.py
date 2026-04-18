from django.contrib import admin
from .models import ContactSubmission, Subscriber


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created_at", "is_read"]
    list_filter = ["is_read", "created_at"]
    list_editable = ["is_read"]
    search_fields = ["name", "email", "message"]
    readonly_fields = ["created_at"]


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "is_active", "subscribed_at"]
    list_editable = ["is_active"]
    list_filter = ["is_active", "subscribed_at"]
    search_fields = ["email", "name"]
    readonly_fields = ["subscribed_at", "unsubscribe_token"]
    date_hierarchy = "subscribed_at"
