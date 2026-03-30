from django.db import models


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "service categories"

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="services",
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to="services/", blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="SVG icon name or CSS class")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class Review(models.Model):
    CATEGORY_CHOICES = [
        ("healing", "Kundalini Transmissions, Soul Clearings & Intuitive Sessions"),
        ("intuitive", "Intuitive Session Reviews"),
    ]

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="reviews",
        null=True,
        blank=True,
    )
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="healing", blank=True
    )
    author_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(
        default=5, choices=[(i, i) for i in range(1, 6)]
    )
    body = models.TextField()
    is_approved = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.author_name} — {self.rating}/5"
