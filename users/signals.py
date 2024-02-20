from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from allauth.account.signals import email_confirmed
from django.core.mail import send_mail
from api.models import Profile


@receiver(email_confirmed)
@receiver(post_save, sender=User)
def create_profile_and_send_welcome_email(sender, instance, created, **kwargs):

    if created and instance.is_active:

        user_profile = Profile(user=instance)
        user_profile.save()
        # user_profile.follows.set([])  # to clear the follows list because by default user follows itself when profile is created.
        # user_profile.save()


        print(f"\nSending welcome email to {instance.email}\n")
        send_mail(
            "Welcome | Dwitter",
            f"Welcome {instance.first_name},\nYour account has been created on Dwitter.\nThanks.",
            None,
            [instance.email],
            fail_silently=False
        )
