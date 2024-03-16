import json

from django.shortcuts import render
import razorpay
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Order, PaymentStatus


razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


@login_required
def donate(request):
    user_donations = list(Order.objects.filter(user=request.user).filter(status=PaymentStatus.SUCCESS).order_by("-timestamp"))
    total_donation = sum(list(donation.amount for donation in user_donations))
    return render(request, 'donate.html', {'user_donations': user_donations, 'total_donation': total_donation})


@login_required
def payment(request):
    if request.method == 'POST':
        amount = int(request.POST['amount']) * 100
        currency = 'INR'

        razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='1'))

        razorpay_order_id = razorpay_order['id']

        order = Order.objects.create(user=request.user, amount=amount, provider_order_id=razorpay_order_id)
        order.save()

        callback_url = 'http://localhost:8000/donate/payment_handler/'

        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['username'] = request.user.username + " | Dwitter"

        return render(request, 'payment.html', context=context)

    else:
        return HttpResponseBadRequest()


@csrf_exempt
# @login_required
def payment_handler(request):
    if request.method == 'POST':

        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            order = Order.objects.get(provider_order_id=razorpay_order_id)
            order.payment_id = payment_id
            order.signature_id = signature
            order.save()

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            result = razorpay_client.utility.verify_payment_signature(params_dict)

            if result is not None:
                # amount = 20000

                # try:
                #     # razorpay_client.payment.capture(payment_id, amount)
                #     return render(request, 'payment_success.html')
                #
                # except:
                #     return render(request, 'payment_fail.html')

                order.status = PaymentStatus.SUCCESS
                order.save()
                return render(request, 'payment_success.html')

            else:
                order.status = PaymentStatus.FAILURE
                order.save()
                return render(request, 'payment_fail.html')

        except:
            payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
            provider_order_id = json.loads(request.POST.get("error[metadata]")).get("order_id")
            order = Order.objects.get(provider_order_id=provider_order_id)
            order.payment_id = payment_id
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, 'payment_fail.html')

    else:
        return HttpResponseBadRequest()
