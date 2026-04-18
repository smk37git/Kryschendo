from django import forms
from .models import ConsentSubmission, BookingRequest, Review, Service

INPUT_CSS = (
    "w-full px-4 py-3 rounded-md border border-gray-300 "
    "focus:border-[#C4A265] focus:ring-1 focus:ring-[#C4A265] outline-none transition"
)
SELECT_CSS = INPUT_CSS
CHECKBOX_CSS = "w-5 h-5 text-teal border-gray-300 rounded focus:ring-[#C4A265]"


class ConsentForm(forms.ModelForm):
    class Meta:
        model = ConsentSubmission
        fields = [
            "client_name",
            "session_date",
            "location_or_platform",
            "agrees_to_terms",
            "typed_signature",
            "date_signed",
            "guardian_name",
            "guardian_signature",
            "guardian_date_signed",
        ]
        widgets = {
            "client_name": forms.TextInput(
                attrs={"class": INPUT_CSS, "placeholder": "Full Legal Name"}
            ),
            "session_date": forms.DateInput(
                attrs={"class": INPUT_CSS, "type": "date"}
            ),
            "location_or_platform": forms.TextInput(
                attrs={"class": INPUT_CSS, "placeholder": "e.g., Zoom, In-Person Seattle"}
            ),
            "agrees_to_terms": forms.CheckboxInput(
                attrs={"class": CHECKBOX_CSS}
            ),
            "typed_signature": forms.TextInput(
                attrs={"class": INPUT_CSS, "placeholder": "Type your full name as signature"}
            ),
            "date_signed": forms.DateInput(
                attrs={"class": INPUT_CSS, "type": "date"}
            ),
            "guardian_name": forms.TextInput(
                attrs={"class": INPUT_CSS, "placeholder": "Parent/Guardian Full Name"}
            ),
            "guardian_signature": forms.TextInput(
                attrs={"class": INPUT_CSS, "placeholder": "Parent/Guardian Signature"}
            ),
            "guardian_date_signed": forms.DateInput(
                attrs={"class": INPUT_CSS, "type": "date"}
            ),
        }
        labels = {
            "client_name": "Client Name",
            "session_date": "Date of Session",
            "location_or_platform": "Location (or Remote Platform)",
            "agrees_to_terms": "I have read, understood, and voluntarily agree to the terms above",
            "typed_signature": "Client Signature (typed full name)",
            "date_signed": "Date",
            "guardian_name": "Parent/Legal Guardian Name",
            "guardian_signature": "Parent/Legal Guardian Signature",
            "guardian_date_signed": "Date",
        }

    def clean_agrees_to_terms(self) -> bool:
        agreed = self.cleaned_data.get("agrees_to_terms")
        if not agreed:
            raise forms.ValidationError(
                "You must agree to the terms to submit this form."
            )
        return agreed


class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = [
            "name",
            "email",
            "phone",
            "service_type",
            "preferred_format",
            "preferred_datetime",
            "message",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": INPUT_CSS, "placeholder": "Your Full Name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": INPUT_CSS, "placeholder": "Your Email"}
            ),
            "phone": forms.TextInput(
                attrs={"class": INPUT_CSS, "placeholder": "Phone Number (optional)"}
            ),
            "service_type": forms.Select(attrs={"class": SELECT_CSS}),
            "preferred_format": forms.Select(attrs={"class": SELECT_CSS}),
            "preferred_datetime": forms.DateTimeInput(
                attrs={"class": INPUT_CSS, "type": "datetime-local"}
            ),
            "message": forms.Textarea(
                attrs={
                    "class": INPUT_CSS,
                    "placeholder": "Any additional details or questions",
                    "rows": 4,
                }
            ),
        }
        labels = {
            "name": "Full Name",
            "email": "Email Address",
            "phone": "Phone Number",
            "service_type": "Service",
            "preferred_format": "Session Format",
            "preferred_datetime": "Preferred Date & Time",
            "message": "Message",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service_type"].queryset = Service.objects.filter(is_active=True)
        self.fields["service_type"].empty_label = "Select a service..."


class ReviewSubmissionForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["author_name", "category", "rating", "body"]
        widgets = {
            "author_name": forms.TextInput(
                attrs={"class": INPUT_CSS, "placeholder": "Your Name"}
            ),
            "category": forms.Select(attrs={"class": SELECT_CSS}),
            "rating": forms.HiddenInput(),
            "body": forms.Textarea(
                attrs={
                    "class": INPUT_CSS,
                    "placeholder": "Share your experience...",
                    "rows": 6,
                }
            ),
        }
        labels = {
            "author_name": "Your Name",
            "category": "Service Category",
            "rating": "Rating",
            "body": "Your Review",
        }
