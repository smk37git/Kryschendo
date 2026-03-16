from django import forms
from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-md border border-gray-300 focus:border-[#C4A265] focus:ring-1 focus:ring-[#C4A265] outline-none transition",
                "placeholder": "Your Name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full px-4 py-3 rounded-md border border-gray-300 focus:border-[#C4A265] focus:ring-1 focus:ring-[#C4A265] outline-none transition",
                "placeholder": "Your Email",
            }),
            "message": forms.Textarea(attrs={
                "class": "w-full px-4 py-3 rounded-md border border-gray-300 focus:border-[#C4A265] focus:ring-1 focus:ring-[#C4A265] outline-none transition",
                "placeholder": "Your Message",
                "rows": 5,
            }),
        }
