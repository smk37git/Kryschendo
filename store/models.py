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


class ConsentSubmission(models.Model):
    FORM_TYPE_CHOICES = [
        ("kundalini", "Remote Healings: Kundalini Energy Transmission"),
        ("spirit_rescue", "Mediumship: Spirit Rescue"),
        ("intuitive", "Intuitive Session"),
    ]

    form_type = models.CharField(max_length=20, choices=FORM_TYPE_CHOICES)
    client_name = models.CharField(max_length=200)
    session_date = models.DateField()
    location_or_platform = models.CharField(max_length=200)
    agrees_to_terms = models.BooleanField(default=False)
    typed_signature = models.CharField(max_length=200)
    date_signed = models.DateField()

    guardian_name = models.CharField(max_length=200, blank=True)
    guardian_signature = models.CharField(max_length=200, blank=True)
    guardian_date_signed = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "consent submission"
        verbose_name_plural = "consent submissions"

    def __str__(self) -> str:
        return f"{self.get_form_type_display()} — {self.client_name} ({self.date_signed})"


class BookingRequest(models.Model):
    FORMAT_CHOICES = [
        ("zoom", "Zoom (Remote)"),
        ("in_person", "In-Person (Seattle)"),
        ("phone", "Phone / FaceTime"),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    service_type = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="booking_requests",
    )
    preferred_format = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    preferred_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Preferred date and time for the session",
    )
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "booking request"
        verbose_name_plural = "booking requests"

    def __str__(self) -> str:
        return f"{self.name} — {self.service_type or 'General'} ({self.created_at:%Y-%m-%d})"
