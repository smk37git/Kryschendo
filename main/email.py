from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_form_email(
    subject: str,
    template_name: str,
    context: dict,
    reply_to: str | None = None,
) -> None:
    """Send a form submission email to the site owner."""
    body = render_to_string(template_name, context)
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_EMAIL],
        reply_to=[reply_to] if reply_to else None,
    )
    email.send(fail_silently=False)
