from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.dispatch import Signal
from allauth.account.signals import email_confirmed

# Create your views here.

def activate_email(request, user, to_email):
    mail_subject = "Activate your user account"
    message = render_to_string("users/template_activate_account.html",
                               {
                                    'user': user.username,
                                    'domain': get_current_site(request).domain,
                                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                    'token': account_activation_token.make_token(user),
                                     'protocol': 'https' if request.is_secure() else 'http'
                               })

    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, mark_safe(f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on \
                    received activation link to confirm and complete the registration. \n<b>Note:</b> Check your spam folder.'))
    else:
        messages.error(request, mark_safe(f"Problem sending email to {to_email}, check if you have typed it correctly."))


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = form.save(commit=False)  # commit=false means user will not be saved on database
            user.is_active = False  # user will not be able to login until he verifies his email and is_active=True
            user.save()  # saving user to database
            username = form.cleaned_data.get('username')
            activate_email(request, user, email)
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login to your account.")
        Signal.send(email_confirmed, sender=User, instance=user, created=True)
        return redirect('login')

    else:
        messages.error(request, "Activation link is invalid")

    return redirect('login')