from django import forms
from .models import ContactSubmission, Subscriber

INPUT_CSS = (
    "w-full px-4 py-3 rounded-md border border-gray-300 "
    "focus:border-[#C4A265] focus:ring-1 focus:ring-[#C4A265] outline-none transition"
)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": INPUT_CSS,
                "placeholder": "Your Name",
            }),
            "email": forms.EmailInput(attrs={
                "class": INPUT_CSS,
                "placeholder": "Your Email",
            }),
            "message": forms.Textarea(attrs={
                "class": INPUT_CSS,
                "placeholder": "Your Message",
                "rows": 5,
            }),
        }


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email", "name"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "w-full px-3 py-2 rounded-md border border-white/20 bg-white/10 text-white placeholder-white/50 focus:border-gold focus:ring-1 focus:ring-gold outline-none transition text-sm",
                "placeholder": "Your email address",
            }),
            "name": forms.TextInput(attrs={
                "class": "w-full px-3 py-2 rounded-md border border-white/20 bg-white/10 text-white placeholder-white/50 focus:border-gold focus:ring-1 focus:ring-gold outline-none transition text-sm",
                "placeholder": "Your name (optional)",
            }),
        }
