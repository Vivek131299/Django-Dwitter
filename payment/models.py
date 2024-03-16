from django.db import models
from django.contrib.auth.models import User


class PaymentStatus:
    SUCCESS = "Success"
    FAILURE = "Failure"
    PENDING = "Pending"


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, related_name='payments', on_delete=models.DO_NOTHING, blank=False, null=False)
    amount = models.FloatField(blank=False, null=False)
    status = models.CharField(default=PaymentStatus.PENDING, max_length=254, blank=False, null=False)
    provider_order_id = models.CharField(max_length=100, blank=False, null=False)
    payment_id = models.CharField(max_length=100, blank=False, null=False)
    signature_id = models.CharField(max_length=200, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}-{self.user}-{self.status}"
