from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from config.settings.base import EMAIL_HOST_USER

from .models import CustomerOrder


@receiver(post_save, sender=CustomerOrder)
def notify_by_email(sender, instance, created, **kwargs):
    if created:
        full_name = (
            f"{instance.customer.first_name} {instance.customer.last_name}"
            if instance.customer
            else "No Detail"
        )
        email = instance.customer.email if instance.customer else "No Details"
        phone_number = (
            instance.customer.phone_number
            if instance.customer
            else "No Details"
        )
        address = (
            instance.address.address_text()
            if instance.address
            else "No Details"
        )
        link = f"https://kipaprints.com/profile/customer-order/{instance.id}"

        context = {
            "id": instance.id,
            "full_name": full_name,
            "phone_number": phone_number,
            "email": email,
            "address": address,
            "link": link,
        }

        html_message = render_to_string(
            "email/customer_order_detail.html", context=context
        )

        text_message = (
            f"Order by {full_name}\n "
            f"Email: {email}\n "
            f"Phone Number{phone_number}\n\n"
            f"Total Price: {instance.total_price}\n"
            f"Address: {address}\n\n"
            f"{link}"
        )

        send_mail(
            f"Customer Order #{instance.id}",
            text_message,
            EMAIL_HOST_USER,
            [
                "kipaprints@gmail.com",
            ],  # kipaprints@gmail.com
            fail_silently=True,
            html_message=html_message,
        )
