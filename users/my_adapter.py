from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model


# This adapter is used to connect the social account to the already existing user account.
class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Connects the social account to the existing user if the user already exists.
        """
        user = get_user_model()
        social_email = sociallogin.account.extra_data['email']

        # Find the user with the same email address.
        user = user.objects.filter(email=social_email).first()

        # If the user is found, link the social account to the user.
        if user:
            sociallogin.connect(request, user)
