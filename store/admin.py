from django.contrib import admin
from .models import ServiceCategory, Service, Review, ConsentSubmission, BookingRequest


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
    list_editable = ["order"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "price", "is_active", "order"]
    list_editable = ["is_active", "order"]
    list_filter = ["is_active", "category"]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title", "description"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["author_name", "category", "rating", "service", "is_approved", "is_featured", "order"]
    list_editable = ["is_approved", "is_featured", "order"]
    list_filter = ["is_approved", "is_featured", "rating", "category"]
    search_fields = ["author_name", "body"]


@admin.register(ConsentSubmission)
class ConsentSubmissionAdmin(admin.ModelAdmin):
    list_display = ["client_name", "form_type", "session_date", "date_signed", "created_at"]
    list_filter = ["form_type", "created_at"]
    search_fields = ["client_name", "typed_signature"]
    readonly_fields = ["created_at", "ip_address"]
    date_hierarchy = "created_at"


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "service_type", "preferred_format", "preferred_datetime", "is_confirmed", "created_at"]
    list_editable = ["is_confirmed"]
    list_filter = ["is_confirmed", "preferred_format", "service_type", "created_at"]
    search_fields = ["name", "email", "message"]
    readonly_fields = ["created_at"]
    date_hierarchy = "created_at"
