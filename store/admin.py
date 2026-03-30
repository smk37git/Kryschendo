from django.contrib import admin
from .models import ServiceCategory, Service, Review


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
